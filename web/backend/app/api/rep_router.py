from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime
from bson.objectid import ObjectId

from app.api.rep_model import MessageModel
#, eventModel, MetaeventModel
import random
import json
from fastapi import Query

router = APIRouter()
@router.get("/messages", response_description="List all messages")
async def list_messages(
    request: Request,
    node_tap: str = Query(None, description="Tap name"),
    src: str = Query(None, description="Source"),
    code: str = Query(None, description="Code"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    list_messages = []
    query = {}
    if startDate and endDate:
        start_datetime = datetime.datetime.fromisoformat(startDate)
        end_datetime = datetime.datetime.fromisoformat(endDate)
        query['time'] = {"$gte": start_datetime, "$lte": end_datetime}
    if node_tap:
        query["node_tap"] = node_tap
    if code:
        query["code"] = code
    if src:
        query["node_name"] = src
    for doc in await request.app.mongodb["messages"].find(query).sort("_id", -1).to_list(length=1000):
        message = {
            'id': str(doc['_id']),
            'node_tap': doc['node_tap'],
            'node_name': doc['node_name'],
            'code': doc['code'],
            'raw_data': doc['raw_data'],
            'time': doc['time'],
        }         
        list_messages.append(message)
    return list_messages 

@router.get("/messages/{id}", response_description="Get a single message")
async def show_message(id: str, request: Request):
    if (message := await request.app.mongodb["messages"].find_one({"_id": id })) is not None:
        message['_id'] = str(message['_id'])
        return message
    raise HTTPException(status_code=404, detail=f"Message {id} not found")@router.get("/messages", response_description="List all messages")

@router.get("/packets", response_description="List all packets")
async def list_packets(
    request: Request,
    node_tap: str = Query(None, description="Tap name"),
    proto: str = Query(None, description="Protocol"),
    src_addr: str = Query(None, description="Source IP"),
    tgt_addr: str = Query(None, description="Target IP"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    list_packets = []
    query = {}
    if startDate and endDate:
        start_datetime = datetime.datetime.fromisoformat(startDate)
        end_datetime = datetime.datetime.fromisoformat(endDate)
        query['time'] = {"$gte": start_datetime, "$lte": end_datetime}
    if node_tap:
        query["node_tap"] = node_tap
    if proto:
        query["proto"] = proto
    if src_addr:
        query["src_addr"] = src_addr
    if tgt_addr:
        query["tgt_addr"] = tgt_addr
    for doc in await request.app.mongodb["packets"].find(query).sort("_id", -1).to_list(length=1000):
        packet = {
            'id': str(doc['_id']),
            'proto': doc['proto'],
            'node_tap': doc['node_tap'],
            'src_addr': doc['src_addr'],
            'tgt_addr': doc['tgt_addr'],
            'raw_data': doc['raw_data'],
            'time': doc['time'],
        }        
        list_packets.append(packet)
    return list_packets

@router.get("/packets/{id}", response_description="Get a single packet")
async def show_packets(id: str, request: Request):
    if (packet := await request.app.mongodb["packets"].find_one({"_id": id })) is not None:
        packet['_id'] = str(packet['_id'])
        return packet
    raise HTTPException(status_code=404, detail=f"Packet {id} not found")@router.get("/messages", response_description="List all messages")

@router.get("/events", response_description="List all events")
async def list_events(
    request: Request,
    event_name: str = Query(None, description="Rule name"),
    node_tap: str = Query(None, description="Tap name"),
    node_name: str = Query(None, description="Node name"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    data = []
    query = {}
    if startDate and endDate:
        start_datetime = datetime.datetime.fromisoformat(startDate)
        end_datetime = datetime.datetime.fromisoformat(endDate)
        query['time'] = {"$gte": start_datetime, "$lte": end_datetime}
    if event_name:
        query["name"] = event_name
    if node_tap:
        query["node_tap"] = node_tap
    if node_name:
        query["node_name"] = node_name
    list_events = []
    for doc in await request.app.mongodb["events"].find(query).sort("_id", -1).to_list(length=10000):
        event = {
            'id': str(doc['_id']),
            'node_tap': doc['node_tap'],
            'node_name': doc['node_name'],
            'name': doc['name'],
            'time': doc['time'],
        }
        list_events.append(event)
    return list_events

@router.get("/events/{id}", response_description="Get a single event")
async def show_event(id: str, request: Request):
    if (event := await request.app.mongodb["events"].find_one({"_id": ObjectId(id) })) is not None:
        return event['fields']
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")@router.get("/events", response_description="List all events")


@router.get("/meta_events", response_description="List all meta_events")
async def list_meta_events(
    request: Request,
    tactic: str = Query(None, description="Filter by tactic"),
    severity: str = Query(None, description="Filter by severity"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    list_meta_events = []
    filter_query = {}
    if tactic:
        filter_query['tactic'] = tactic
    if severity:
        filter_query['severity'] = severity
    for doc in await request.app.mongodb["crit_rules"].find(filter_query).sort("_id", -1).to_list(length=100):
        meta_event = {
            'id': str(doc['_id']),
            'name': doc['name'],
            'description': doc['description'],
            'time': doc['time'],
            'severity': doc['severity'],
            'tactic': doc['tactic'],
            'positive': doc['positive'],
            'rules': '123'
        }
        list_meta_events.append(meta_event)
    print(list_meta_events)
    return list_meta_events


@router.get("/meta_events/{id}", response_description="Get a single meta_event")
async def show_meta_event(id: str, request: Request):
    print(id)
    if (meta_event := await request.app.mongodb["crit_rules"].find_one({"_id": ObjectId(id) })) is not None:
        meta_event['_id'] = str(meta_event['_id'])      
        meta_event['description'] = meta_event['rules']
        return meta_event
    raise HTTPException(status_code=404, detail=f"Meta event {id} not found")

@router.get("/meta_events/filter", response_description="Get a filter meta_event")
async def filter_meta_event(id: str, request: Request):
    list_meta_events = []
    return list_meta_events

@router.get("/playbook/{id}", response_description="Get a playbook for meta event")
async def get_playbook(id: str, request: Request):
    return '123123123'
    meta_event = await request.app.mongodb["meta_events"].find_one({"_id": ObjectId(id)})
    if meta_event:
        print(meta_event)
        playbook = []
        return playbook
    raise HTTPException(status_code=404, detail=f"Meta event {id} not found")
