from fastapi import APIRouter, Request
import json
from app.db import db

router = APIRouter()
@router.get("/install_config", response_description="Install config to Core")
async def install_config(request: Request):
   config = {}
   data = {}
   for doc in await db["collections"].find().to_list(length=100):
      if not 'name' in doc:
         continue
      tap = {}
      for node in doc['nodes']:
         if ('ip_address' in node
            and 'name' in node
            ):
            tap[node['ip_address']] = {
               'name': node['name'],
            }
      data[doc['name']] = tap
   config['collection'] = data
   data = {}
   config['normalization'] = await db["normalizations"].find().to_list(length=1000)
   data = {}
   config['correlation'] = await db["correlation"].find().to_list(length=1000)
   with open('/app/config/config.json', 'w') as f:
      f.write(json.dumps(config, indent=4, sort_keys=True, default=str))
   return {"message": "Config installed successfully and Core service restarted"}


@router.get("/drop_db", response_description="Drob Database")
async def drop_db(request: Request):
   await db.drop_collection('messages')
   await db.create_collection(
      'messages',
      timeseries={
            'timeField': 'time',
            'metaField': 'source',
            'granularity': 'seconds',
      },
      expireAfterSeconds=31536000)
   await db.drop_collection('events')
   await db.create_collection(
      'events',
      timeseries={
            'timeField': 'time',
            'metaField': 'source',
            'granularity': 'seconds',
      },
      expireAfterSeconds=31536000)
   await db.drop_collection('incidents')
   await db.create_collection(
      'incidents',
      timeseries={
            'timeField': 'time',
            'metaField': 'tactic',
            'granularity': 'seconds',
      },
      expireAfterSeconds=31536000)
   await db.drop_collection('packets')
   await db.create_collection(
      'packets',
      timeseries={
            'timeField': 'time',
            'metaField': 'tap',
            'granularity': 'seconds',
      },
      expireAfterSeconds=2592000)
   await db.drop_collection('ml')
   await db.drop_collection('ai')
   await db.drop_collection('existing_ips')
   await db.drop_collection('existing_protocol')
   await db.drop_collection('existing_tcp_port')
   await db.drop_collection('existing_udp_port')
   await db.drop_collection('existing_pkt_count')
   await db.drop_collection('existing_pkt_len')
   return 'ok'