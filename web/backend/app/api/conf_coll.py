from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from app.api.models.conf_coll import RuleModel, UpdateRuleModel
from bson.objectid import ObjectId
from app.db import db
from typing import List

router = APIRouter()

@router.post("/rule", response_description="Add new rule")
async def create_rule(request: Request, 
                      rule: RuleModel = Body(...)):
    rule = jsonable_encoder(rule)
    rule['time'] = datetime.utcnow().replace(microsecond=0)
    result = await db["collections"].insert_one(rule)
    rule['id'] = str(result.inserted_id)
    rule['time'] = str(rule['time'])
    rule['_id'] = str(rule['_id'])
    return JSONResponse(status_code=status.HTTP_201_CREATED, 
                        content=rule)

@router.get("/rule", response_description="List all rules")
async def list_rules(request: Request):
    list_rules = []
    for doc in await db["collections"].find().to_list(length=100):
       doc['_id'] = str(doc['_id'])
       list_rules.append(doc)
    return list_rules

@router.get("/rule/{id}", response_description="Get a single rule")
async def get_rule(id: str, request: Request):
    if (rule := await db["collections"].find_one({"_id": ObjectId(id) })) is not None:
        rule['_id'] = str(rule['_id'])
        return rule
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")

@router.put("/rule/{id}")
async def update_rule(id: str, 
                      request: Request, 
                      rule: UpdateRuleModel = Body(...)):
    col = db["collections"]
    if await col.find_one({"_id": ObjectId(id)}):
        rule = jsonable_encoder(rule)
        rule['time'] = datetime.utcnow().replace(microsecond=0)
        await col.update_one({"_id": ObjectId(id)}, {"$set": rule})
        doc = await col.find_one({"_id": ObjectId(id)})
        doc['_id'] = str(doc['_id'])
        return doc
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")

@router.delete("/rule/{id}", response_description="Delete Rule")
async def delete_rule(id: str, 
                      request: Request):
    delete_result = await db["collections"].delete_one(
        {"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Rule deleted successfully"}
    raise HTTPException(status_code=404, 
                        detail=f"Rule {id} not found")

@router.post("/copy/{id}", response_description="Copy Rule")
async def copy_rule(id: str, request: Request):
    rule = await db["collections"].find_one({"_id": ObjectId(id)})
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule {id} not found")
    copy = dict(rule)
    del copy["_id"]
    copy["name"] += '_copy'
    copy['time'] = datetime.utcnow().replace(microsecond=0)
    result = await db["collections"].insert_one(copy)
    copy["_id"] = str(result.inserted_id)
    copy["time"] = str(copy["time"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, 
                        content=copy)

@router.get("/nodes", response_description="List all nodes")
async def list_nodes(request: Request):
    list_nodes = []
    for doc in await db["collections"].find().to_list(length=100):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        for node in doc['nodes']:
            node = f"{doc['name']}-{node['ip_address']}" 
            list_nodes.append(node)
    return list_nodes

@router.get("/export", response_description="Export rules")
async def export_rules(request: Request):
    list_rules = []
    for doc in await db["collections"].find().to_list(length=10000):
       del doc['_id']
       list_rules.append(doc)
    return list_rules

@router.post("/rule/import", response_description="Import rules")
async def import_rules(request: Request):
    data = await request.json()
    for d in data:
        d['time'] = datetime.utcnow().replace(microsecond=0)
    list_rules = []
    for doc in await db["collections"].find().to_list(length=1000):
        doc['_id'] = str(doc['_id'])
        list_rules.append(doc)
    return list_rules
