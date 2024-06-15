from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import UploadFile, File

from app.api.sources_model import RuleModel, UpdateRuleModel
from bson.objectid import ObjectId
import json


import csv
from io import StringIO

router = APIRouter()

@router.post("/rule", response_description="Add new rule")
async def create_rule(request: Request, 
                      rule: RuleModel = Body(...)):
    rule = jsonable_encoder(rule)
    rule['time'] = datetime.now()
    result = await request.app.mongodb["sources"].insert_one(rule)
    rule['id'] = str(result.inserted_id)
    rule['time'] = str(rule['time'])
    del rule['_id']
    return JSONResponse(status_code=status.HTTP_201_CREATED, 
                        content=rule)

@router.get("/rule", response_description="List all rules")
async def list_rules(request: Request):
    list_rules = []
    for doc in await request.app.mongodb["sources"].find().to_list(length=1000):
       doc['id'] = str(doc['_id'])
       del doc['_id']
       list_rules.append(doc)
    return list_rules

@router.get("/rule/{id}", response_description="Get a single rule")
async def get_rule(id: str, request: Request):
    rule = await request.app.mongodb["sources"].find_one({"_id": ObjectId(id) })
    if rule:
        rule['_id'] = str(rule['_id'])
        print(rule)
        return rule
    else:
        raise HTTPException(status_code=404, detail=f"Rule {id} not found")

@router.put("/rule/{id}")
async def update_rule(id: str, 
                      request: Request, 
                      rule: UpdateRuleModel = Body(...)):
    col = request.app.mongodb["sources"]
    if await col.find_one({"_id": ObjectId(id)}):
        rule = jsonable_encoder(rule)
        await col.update_one({"_id": ObjectId(id)}, {"$set": rule})
        await col.find_one({"_id": ObjectId(id)})
        return {'id': id}
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")

@router.delete("/rule/{id}", response_description="Delete Rule")
async def delete_rule(id: str, 
                      request: Request):
    delete_result = await request.app.mongodb["sources"].delete_one(
        {"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Rule deleted successfully"}
    raise HTTPException(status_code=404, 
                        detail=f"Rule {id} not found")

@router.post("/copy/{id}", response_description="Copy Rule")
async def copy_rule(id: str, request: Request):
    # Fetch the rule to copy
    rule = await request.app.mongodb["sources"].find_one({"_id": ObjectId(id)})
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule {id} not found")
    # Create a new copy with a unique id
    copy = dict(rule)
    del copy["_id"]
    copy["name"] += '_copy'
    copy['time'] = datetime.utcnow()
    result = await request.app.mongodb["sources"].insert_one(copy)
    copy["_id"] = str(result.inserted_id)
    copy["time"] = str(copy["time"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, 
                        content=copy)

@router.get("/nodes", response_description="List all nodes")
async def list_nodes(request: Request):
    list_nodes = []
    for doc in await request.app.mongodb["sources"].find().to_list(length=1000):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        for node in doc['nodes']:
            node = f"{doc['name']}-{node['ip_address']}" 
            list_nodes.append(node)
    return list_nodes

@router.get("/export", response_description="Export rules")
async def export_rules(request: Request):
    list_rules = []
    for doc in await request.app.mongodb["sources"].find().to_list(length=10000):
       del doc['_id']
       list_rules.append(doc)
    return list_rules

@router.delete("/delete_all", response_description="Delete All rules")
async def import_rules(request: Request):
    request.app.mongodb["sources"].drop()
    return 'Rules are cleared'

@router.put("/import", response_description="Import rules")
async def import_rules(request: Request, file: UploadFile = File(...)):
    #add raw rules
    col = request.app.mongodb["sources"]
    contents = await file.read()
    sources = json.loads(contents)
    rules = []
    for raw_rule in sources:
        rules.append({
            'name': raw_rule['name'],
            'src': raw_rule['src'],
            'dst': raw_rule['dst'],
            'service': raw_rule['service'],
            'hits': raw_rule['hits'],
            'action': raw_rule['action'],
            'track': raw_rule['track'],
        })
    result = col.insert_many(rules)
    #add nodes
    nodes = []
    col = request.app.mongodb["nodes"]
    for rule in rules:
        for name in rule['src'].split(','):
            node ={
                'name': name,
                'zone': 'internal'
            }
            if node not in nodes:
                nodes.append(node)
        for name in rule['dst'].split(','):
            node ={
                'name': name,
                'zone': 'internal'
            }
            if node not in nodes:
                nodes.append(node)
    result = col.insert_many(nodes)
    #add services
    services = []
    col = request.app.mongodb["services"]
    for rule in rules:
        for name in rule['service'].split(','):
            service ={
                'name': name,
                'severity': 'low'
            }
            if service not in services:
                services.append(service)
    result = col.insert_many(services)
    #add sources
    col = request.app.mongodb["sources"]
    sources = {}
    for rule in rules:
        src_ips = rule['src'].split(',')
        dst_ips = [ x for x in  rule['dst'].split(',')]
        for src_ip in src_ips:
            if src_ip in sources:
                for service in rule['service'].split(','):
                    if service in sources[src_ip]:
                        sources[src_ip][service].extend(dst_ips)
                    else:
                        sources[src_ip][service] = dst_ips
            else:
                sources[src_ip] = {}
                for service in rule['service'].split(','):
                    sources[src_ip][service] = dst_ips
    result = col.insert_many([ {'name': key, 'services': value} for key, value in sources.items() ])
    #add destinations
    col = request.app.mongodb["destinations"]
    sources = {}
    for rule in rules:
        src_ips = rule['dst'].split(',')
        dst_ips = [ x for x in  rule['src'].split(',')]
        for src_ip in src_ips:
            if src_ip in sources:
                for service in rule['service'].split(','):
                    if service in sources[src_ip]:
                        sources[src_ip][service].extend(dst_ips)
                    else:
                        sources[src_ip][service] = dst_ips
            else:
                sources[src_ip] = {}
                for service in rule['service'].split(','):
                    sources[src_ip][service] = dst_ips
    result = col.insert_many([ {'name': key, 'services': value} for key, value in sources.items() ])
    #return raw rules
    list_rules = []
    for doc in await request.app.mongodb["sources"].find().to_list(length=1000):
       doc['id'] = str(doc['_id'])
       del doc['_id']
       list_rules.append(doc)
    return list_rules

@router.put("/import_csv", response_description="Import rules CSV")
async def import_rules(request: Request, file: UploadFile = File(...)):
    #add raw rules
    col = request.app.mongodb["sources"]
    contents = await file.read()
    # Decode contents to a string
    contents_str = contents.decode('utf-8')
    # Use StringIO to treat string as file-like object for csv reader
    file_like = StringIO(contents_str)
    # Use csv reader to parse contents
    csv_reader = csv.DictReader(file_like, delimiter=';')
    
    # Prepare list to store rules
    rules = []
    # Iterate over CSV rows
    for row in csv_reader:
        # Process each row as needed
        # For example, assuming the CSV has columns: rule_id, action, source, destination, protocol
        rule = {
            "rule_id": row['No'],
            "action": row['Action'],
            "name": row['Name'],
            "src": row['Source'],
            "dst": row['Destination'],
            "hits": row['Hits'],
            "action": row['Action'],
            "track": row['Track'],
            "service": row['Service']
        }
        if rule['rule_id']:
            rules.append(rule)
    result = col.insert_many(rules)

    #return raw rules
    list_rules = []
    for doc in await request.app.mongodb["sources"].find().to_list(length=1000):
       doc['id'] = str(doc['_id'])
       del doc['_id']
       list_rules.append(doc)
    return list_rules
