from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime
from app.db import db
import json

router = APIRouter()
@router.get("/assets", response_description="Offline sources")
async def list_assets(request: Request):
    doc = await db["ml"].find_one({"name": 'existing_ips'})
    if not doc:
        return False
    existing_ips = [ x for x in doc['data'].values() ]
    taps = await db["collections"].find().to_list(length=1000)
    taps_map = {}
    for tap in taps:
        for source in tap['nodes']:
            uniq = tap['name'] + "~" + source['name']
            taps_map[uniq] = {
                'tap': tap['name'],
                '_id': uniq,
                'color': 'error',
                'time': 'Offline',
                'source': source['name'],
                'connections': {}
            }
    data = {}
    for ip in existing_ips:
        uniq = ip['tap'] + "~" + ip['source']
        if uniq in taps_map:
            uniq_source = taps_map[uniq]
            uniq_source['_id'] = uniq
            uniq_source['color'] = 'success'
            uniq_source['time'] = ip['time'].replace(microsecond=0)
            connections = uniq_source['connections']
            if ip['tgt_addr'] in connections:
                connections[ip['tgt_addr']].append(ip['proto'])
            else:
                connections[ip['tgt_addr']] = [ip['proto']]
    data = [ x for x in taps_map.values() ]
    return data


@router.get("/assets/{asset_uniq}", response_description="Asset data")
async def get_asset(asset_uniq: str, request: Request):
    doc = await db["ml"].find_one({"name": 'existing_ips'})
    if not doc:
        return False
    existing_ips = [ x for x in doc['data'].values() ]
    tap, source = asset_uniq.split('~')
    connections = {}
    asset = {
        'tap': tap,
        'source': source,
        'status': 'Offline',
        'color': 'error'
    }
    for ip in existing_ips:
        if ip['tap'] == tap and ip['source'] == source:
            if ip['tgt_addr'] in connections:
                connections[ip['tgt_addr']].append(ip['proto'])
            else:
                connections[ip['tgt_addr']] = [ip['proto']]
            asset['status'] = 'Online'
            asset['color'] = 'success'
    asset['protocols'] = [x for x in connections.values()]
    asset['connections'] = [connections]
    return asset