from fastapi import APIRouter, Request
from app.db import db

router = APIRouter()
@router.get("/assets", response_description="Unknown sources")
async def list_assets(request: Request):
    doc = await db["ml"].find_one({"name": 'unknown_ips'})
    if not doc:
        return False
    data = []
    for tap, unknown_ips in doc['data'].items():
        for src in unknown_ips:
            uniq = tap + "~" + src
            data.append({
                'tap': tap,
                '_id': uniq,
                'color': 'error',
                'count': len(unknown_ips[src].values()),
                'source': src
            })
    return data


@router.get("/assets/{asset_uniq}", response_description="Asset data")
async def get_asset(asset_uniq: str, request: Request):
    doc = await db["ml"].find_one({"name": 'unknown_ips'})
    if not doc:
        return False
    tap, ip = asset_uniq.split('~')
    if tap not in doc['data']:
        return False
    if ip not in doc['data'][tap]:
        return False
    connections = {}
    for conn in doc['data'][tap][ip].values():
        if conn['tgt_addr'] in connections:
            connections[conn['tgt_addr']].append(conn['proto'])
        else:
            connections[conn['tgt_addr']] = [conn['proto']]
    asset = {
        'tap': tap,
        'source': ip,
        'connections': [connections],
        'color': 'error'
    }
    return asset