from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime
from app.db import db
import logging

router = APIRouter()
@router.get("/top_categories", response_description="Offline sources")
async def top_categories(request: Request):
    doc = await db["ml"].find_one({"name": 'existing_ips'})
    existing_ips = doc['data'].values() if doc else []
    taps = await db["collections"].find().to_list(length=1000)
    ips = []
    total = 0
    for tap in taps:
        for node in tap['nodes']:
            ips.append(node['ip_address'])
    data = []
    for tap in taps:
        for source in tap['nodes']:
            nets = {}
            for ip in existing_ips:
                if (ip['source'] == source['name']):
                    if ip['tgt_addr'] not in ips:
                        unknown_ip = ip['tgt_addr']
                    else:
                        continue
                    ip_split = unknown_ip.split('.')
                    if len(ip_split) != 4:
                        continue
                    total += 1
                    net = ip_split[0]
                    if net not in nets:
                        nets[net] = [unknown_ip]
                    else:
                        net_map[net]['source'] = f"{net}.0.0.0"
                        nets[net]['count'] += 1
            for net, net_ips in nets.items():
                logging.error(net)
                logging.error(net_ips)
                unknown_node = {
                    "title": f"{tap['name']} - {source['name']}",
                    'count': net_ips,
                    'percent': len(net_ips) / 20 * 100,
                    }
                data.append(unknown_node)
    doc = await db["ml"].find_one({"name": 'existing_ips'})
    existing_ips = doc['data'].values() if doc else []
    doc = await db["ml"].find_one({"name": 'unknown_ips'})
    if not doc:
        return False
    net_map = {}
    for tap, unknown_ips in doc['data'].items():
        for src in unknown_ips:
            net = src.split('.')[0]
            if net not in net_map:
                net_map[net] = {
                    'tap': tap,
                    'color': 'error',
                    'count': 1,
                    'source': src,
                }
            else:
                net_map[net]['count'] += 1
                net_map[net]['source'] = f"{net}.0.0.0"
    count = sum([x['count'] for x in net_map.values()])
    for net in net_map.values():
        data.append({
            'title': net['tap'],
            'percent': net['count'] / 20 * 100,
            'count': net['source']
        })
    return data

@router.get("/sum_chart", response_description="Summary chart")
async def sum_chart(request: Request):
  existing_ips = await db["ml"].find_one({"name": 'existing_ips'})
  existing_ips = existing_ips['data'].values()
  now = datetime.datetime.utcnow()
  label = 0
  labels = []
  data = []
  for i in range(59,0,-1):
    start_date = now - datetime.timedelta(minutes=i*24)
    end_date = now - datetime.timedelta(minutes=i*24 - 24)
    count = 0
    for ip in existing_ips:
        if ip['time'] > start_date and ip['time'] < end_date:
            count += 1
    data.append(count)
    label += count
    minute = (now - datetime.timedelta(minutes=i*24)).minute
    hour = (now - datetime.timedelta(minutes=i*24)).hour
    dt = f"{hour:02d}:{minute:02d}"
    labels.append(dt)  
  response_data = {
    'labels': labels,
    'label': label,
    'data': data,
  }
  return response_data

@router.get("/map_data", response_description="Map data")
async def map_data(request: Request):
    doc = await db["ml"].find_one({"name": 'existing_ips'})
    existing_ips = doc['data'].values() if doc else []
    doc = await db["ml"].find_one({"name": 'unknown_ips'})
    unknown_ips = doc['data'] if doc else []
    taps = await db["collections"].find().to_list(length=1000)
    ips = []
    for tap in taps:
        for node in tap['nodes']:
            ips.append(node['ip_address'])
    data = {
        'nodes': [],
        'links': []
    }
    for tap in taps:
        tap_node = {
            "id": tap['name'], 
            "status": "unknown", 
            'name': [tap['name']],
            'type': 'tap',
            'radius': 12
        }
        for source in tap['nodes']:
            nets = {}
            node = {
                "id": tap['name'] + '-' + source['name'], 
                "status": "offline", 
                'name': [source['name']],
                'type': 'node',
                'radius': 8
                }
            link = {
                "source": tap['name'], 
                "target": tap['name'] + '-' + source['name']
            }
            for ip in existing_ips:
                if ip['tap'] == tap['name']:
                    tap_node['status'] = 'online'
                if (ip['source'] == source['name']):
                    node['status'] = 'online'
                    if ip['tgt_addr'] not in ips:
                        unknown_ip = ip['tgt_addr']
                    else:
                        continue
                    ip_split = unknown_ip.split('.')
                    if len(ip_split) != 4:
                        continue
                    net = ip_split[0]
                    if net not in nets:
                        nets[net] = [unknown_ip]
                    else:
                        nets[net].append("\n" + "unknown_ip")
            for net, net_ips in nets.items():
                unknown_node = {
                    "id": f"{tap['name']}-{source['name']}-{net}",
                    "status": "unknown", 
                    'name': net_ips,
                    'type': 'node',
                    'radius': 8 + len(ips) if len(ips) < 16 else 16
                    }
                unknown_link = {
                    "source": f"{tap['name']}-{source['name']}", 
                    "target": f"{tap['name']}-{source['name']}-{net}"
                }
                data['nodes'].append(unknown_node)
                data['links'].append(unknown_link)
            data['nodes'].append(node)
            data['links'].append(link)
        data['nodes'].append(tap_node)
    nets = {}
    for tap, unknown_ip in unknown_ips.items():
        nets[tap] = {}
        for ip in unknown_ip:
            ip_split = ip.split('.')
            if len(ip_split) != 4:
                continue
            net = ip_split[0]
            if net not in nets[tap]:
                nets[tap][net] = [ip]
            else:
                nets[tap][net].append("\n" + ip)
    for tap, nets in nets.items():
        for net, ips in nets.items():
            unknown_node = {
                "id": f"{tap}-{net}",
                "status": "unknown", 
                'name': ips,
                'type': 'node',
                'radius': 8 + len(ips) if len(ips) < 16 else 16
                }
            unknown_link = {
                "source": f"{tap}", 
                "target": f"{tap}-{net}", 
            }
            data['nodes'].append(unknown_node)
            data['links'].append(unknown_link)
    return data    