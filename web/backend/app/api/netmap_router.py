from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime
import random
import json

router = APIRouter()
@router.get("/top_categories", response_description="Offline sources")
async def top_categories(request: Request):
    rules = await request.app.mongodb["rules"].find().to_list(length=10000)
    data = []
    services = {}
    for rule in rules:
        src = rule['src']
        if src not in services:
            services[src] = 0
        else:
            services[src] += 1
    sorted_services = dict(sorted(services.items(), key=lambda item: item[1], reverse=True))
    for service in sorted_services:
        unknown_node = {
            'id': service,
            'title': service,
            'count': services[service],
            'norm_count': 1,
            'subtitle': 'service',
            'delta': services[service],
            }
        data.append(unknown_node)
    return data[:10]

@router.get("/sum_chart", response_description="Summary chart")
async def sum_chart(request: Request):
  existing_ips = await request.app.mongodb["ml"].find_one({"name": 'existing_ips'})
#   existing_ips = existing_ips['data'].values()
  now = datetime.datetime.utcnow()
  label = 0
  labels = []
  data = []
  response_data = {
    'labels': labels,
    'label': label,
    'data': data,
  }
  return response_data

@router.get("/polar", response_description="Polar chart max Errors")
async def polar_max(request: Request):
    services = await request.app.mongodb["services"].find().to_list(length=1000)
    data = {}
    severity = {
        'high': 0,
        'medium': 0,
        'low': 0,
    }
    for service in services:
        if service['severity'] in severity:
            severity[service['severity']] += 1
    labels = [ x for x in severity ]
    data = [ x for x in severity.values() ]
    response_data = {
        'labels': labels,
        'data': data,
    }
    return response_data

@router.get("/map_data", response_description="Map data")
async def map_data(request: Request):
    rules = await request.app.mongodb["rules"].find().to_list(length=1000)
    services = await request.app.mongodb["services"].find().to_list(length=1000)
    nodes = await request.app.mongodb["nodes"].find().to_list(length=1000)
    services_map = { x['name']:x['severity'] for x in services }
    zones_map = {}
    for node in nodes:
        name = node['name']
        if node['zone'] == 'external':
            zones_map[name] = 'error'
        elif node['zone'] == 'dmz':
            zones_map[name] = 'warning'
        else:
            zones_map[name] = 'success'
    nodes = []
    links = []
    for rule in rules:
        src = rule['src']
        dst = rule['dst']
        service = rule['service']
        node_src = {
            "id": src, 
            "status": 'sucess',
            'name': src,
            'type': 'node',
            }
        if src not in zones_map:
            node_src['status'] = 'error'
        else:
            node_src['status'] = zones_map[src]
        if node_src not in nodes:
            nodes.append(node_src)
        if service not in services_map:
            severity = 'low'
        else:
            severity = services_map[service]
        node_dest = {
            "id": dst, 
            "status": "sucess",
            'name': dst,
            'type': 'node'
            }
        if dst not in zones_map:
            node_dest['status'] = 'error'
        else:
            node_dest['status'] = zones_map[dst]
        if node_dest not in nodes:
            nodes.append(node_dest)
        link = {
            "source": src, 
            "target": dst,
            "severity": severity
        }
        links.append(link)
    map_data = {"nodes": nodes, "links": links}
    # print(json.dumps(nodes, indent=4))
    return map_data

@router.get("/tree_sources", response_description="Map tree source data")
async def tree_sources(request: Request):
    rules = await request.app.mongodb["rules"].find().to_list(length=10000)
    rules = [ x for x in rules if x['action'] == 'Accept' ]
    connections = {}
    more_connections = {}
    for rule in rules:
        src = rule['src']
        if src in more_connections:
            more_connections[src] += 1
        else:
            more_connections[src] = 0
    for rule in rules:
        src = rule['src']
        dst = rule['dst']
        service = rule['service']
        if dst in more_connections:
            dest_data = [{
                'name': dst,
                'children': [{'name': more_connections[dst], 'size':1}]
            }]
        else:
            dest_data = [{
                'name': dst,
                'children': [{'name': '', 'size':1}]
            }]
        if src not in connections:
            connections[src] = [{
                'name': service,
                'children': dest_data
            }]
        else:
            connections[src].append({
                'name': service,
                'children': dest_data
            })
    data = {
        'name': '',
        'children': []
    } 
    for name, children in connections.items():
        child = {
            'name': name,
            'children': children
        }
        data['children'].append(child) 
    return data

@router.get("/tree_destinations", response_description="Map tree destination data")
async def tree_destinations(request: Request):
    rules = await request.app.mongodb["rules"].find().to_list(length=10000)
    rules = [ x for x in rules if x['action'] == 'Accept' ]
    connections = {}
    more_connections = {}
    for rule in rules:
        src = rule['dst']
        if src in more_connections:
            more_connections[src] += 1
        else:
            more_connections[src] = 0
    for rule in rules:
        src = rule['dst']
        dst = rule['src']
        service = rule['service']
        if dst in more_connections:
            dest_data = [{
                'name': dst,
                'children': [{'name': more_connections[dst], 'size':1}]
            }]
        else:
            dest_data = [{
                'name': dst,
                'children': [{'name': '', 'size':1}]
            }]
        if src not in connections:
            connections[src] = [{
                'name': service,
                'children': dest_data
            }]
        else:
            connections[src].append({
                'name': service,
                'children': dest_data
            })
    data = {
        'name': '',
        'children': []
    } 
    for name, children in connections.items():
        child = {
            'name': name,
            'children': children
        }
        data['children'].append(child) 
    print(json.dumps(data, indent=4))
    return data