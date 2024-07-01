from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import UploadFile, File
from bson.objectid import ObjectId
from fastapi import Query
from app.api.models.conf_corr import RuleModel, UpdateRuleModel
from app.db import db

import json

router = APIRouter()

@router.post("/", response_description="Add new rule")
async def create_rule(request: Request, rule: RuleModel = Body(...)):
    rule = jsonable_encoder(rule)
    rule['time'] = datetime.utcnow().replace(microsecond=0)
    result = await db["correlation"].insert_one(rule)
    rule['id'] = str(result.inserted_id)
    rule['time'] = str(rule['time'])
    del rule['_id']
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=rule)

@router.get("/", response_description="List all rules")
async def list_rules(request: Request,
                     severity: str = Query(None, description="Severity"),
                     name: str = Query(None, description="Name of the Rule"),
                     tactic: str = Query(None, description="Tactic of the attack"),
                     startDate: str = Query(None, description="Start date"),
                     endDate: str = Query(None, description="End date")):
    list_rules = []
    query = {}
    color = {
      'high': 'error',
      'med': 'warning',
      'low': 'secondary' 
    }
    if startDate and endDate:
        start_datetime = datetime.fromisoformat(startDate)
        end_datetime = datetime.fromisoformat(endDate)
        query['time'] = {"$gte": start_datetime, "$lte": end_datetime}
    if severity:
        query["severity"] = severity
    if name:
        query["name"] = name
    if tactic:
        query["tactic"] = tactic
    for doc in await db["correlation"].find(query).sort("_id", -1).to_list(length=10000):
        doc['_id'] = str(doc['_id'])
        if doc['severity'] in color:
            doc['color'] = color[doc['severity']]
        else:
            doc['color'] = 'secondary'
        list_rules.append(doc)
    return list_rules

@router.get("/{id}", response_description="Get a single rule")
async def get_rule(id: str, request: Request):
    color = {
      'high': 'error',
      'med': 'warning',
      'low': 'secondary' 
    }
    if (rule := await db["correlation"].find_one({"_id": ObjectId(id) })) is not None:
        rule['_id'] = str(rule['_id'])
        severity = rule['severity']
        if severity in color:
            rule['color'] = color[rule['severity']]
        return rule
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")

@router.put("/{id}", response_description="Update Rule")
async def update_rule(id: str, request: Request, rule: UpdateRuleModel = Body(...)):
    col = db["correlation"]
    if await col.find_one({"_id": ObjectId(id)}):
        rule = jsonable_encoder(rule)
        rule['time'] = datetime.utcnow().replace(microsecond=0)
        await col.update_one({"_id": ObjectId(id)}, {"$set": rule})
        doc = await col.find_one({"_id": ObjectId(id)})
        doc['_id'] = str(doc['_id'])
        return doc
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")

@router.delete("/{id}", response_description="Delete Rule")
async def delete_rule(id: str, request: Request):
    delete_result = await db["correlation"].delete_one(
        {"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Rule deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")

@router.post("/copy/{id}", response_description="Copy Rule")
async def copy_rule(id: str, request: Request):
    rule = await db["correlation"].find_one({"_id": ObjectId(id)})
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule {id} not found")
    copy = dict(rule)
    del copy["_id"]
    copy["name"] += '_copy'
    copy['time'] = datetime.utcnow().replace(microsecond=0)
    result = await db["correlation"].insert_one(copy)
    copy["_id"] = str(result.inserted_id)
    copy["time"] = str(copy["time"])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=copy)

@router.get("/export/", response_description="Export rules")
async def export_rules(request: Request):
    list_rules = []
    for doc in await db["correlation"].find().to_list(length=10000):
       del doc['_id']
       list_rules.append(doc)
    return list_rules

@router.put("/import/", response_description="Import rules")
async def import_rules(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    list_rules = []
    for doc in await db["correlation"].find().to_list(length=1000):
       doc['id'] = str(doc['_id'])
       del doc['_id']
       list_rules.append(doc)
    return list_rules

@router.get("/install/", response_description="Install rules")
async def install_rules(request: Request):
    collection = await db["collections"].find().to_list(length=1000)
    normalization = await db["normalizations"].find().to_list(length=1000)
    correlation = await db["correlation"].find().to_list(length=1000)
    config = {
        'collection': collection,
        'normalization': normalization,
        'correlation': correlation,
    }
    with open('/app/config/config.json', 'w') as f:
        f.write(json.dumps(config, indent=4, sort_keys=True, default=str))
    return {"message": "Config installed successfully and Core service restarted"}
