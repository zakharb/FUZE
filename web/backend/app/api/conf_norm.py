from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import UploadFile, File
from bson.objectid import ObjectId
import json

from app.db import db
from app.api.models.conf_norm import NormalizationModel, UpdateNormalizationModel

router = APIRouter()

@router.post("/rule", response_description="Add new rule")
async def create_rule(request: Request,
                      rule: NormalizationModel = Body(...)):
    rule = jsonable_encoder(rule)
    rule['time'] = datetime.utcnow().replace(microsecond=0)
    result = await db["normalizations"].insert_one(rule)
    rule['_id'] = str(result.inserted_id)
    rule['time'] = str(rule['time'])
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=rule)


@router.get("/rule", response_description="List all rules")
async def list_rules(request: Request):
    list_rules = []
    for doc in await db["normalizations"].find().to_list(length=1000):
        doc['_id'] = str(doc['_id'])
        list_rules.append(doc)
    return list_rules


@router.get("/rule/{id}", response_description="Get a single rule")
async def get_rule(id: str, request: Request):
    if (rule := await db["normalizations"].find_one({"_id": ObjectId(id)})) is not None:
        rule['_id'] = str(rule['_id'])
        return rule
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")


@router.put("/rule/{id}", response_description="Update Rule")
async def update_rule(id: str,
                      request: Request,
                      rule: UpdateNormalizationModel = Body(...)):
    col = db["normalizations"]
    if await col.find_one({"_id": ObjectId(id)}):
        rule = jsonable_encoder(rule)
        rule['time'] = datetime.utcnow().replace(microsecond=0)
        await col.update_one({"_id": ObjectId(id)}, {"$set": rule})
        doc = await col.find_one({"_id": ObjectId(id)})
        doc['_id'] = str(doc['_id'])
        return doc
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")


@router.delete("/rule/{id}", response_description="Delete Rule")
async def delete_rule(id: str, request: Request):
    delete_result = await db["normalizations"].delete_one(
        {"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Rule deleted successfully"}
    raise HTTPException(status_code=404,
                        detail=f"Rule {id} not found")


@router.post("/copy/{id}", response_description="Copy Rule")
async def copy_rule(id: str, request: Request):
    rule = await db["normalizations"].find_one({"_id": ObjectId(id)})
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule {id} not found")
    copy = dict(rule)
    del copy["_id"]
    copy["name"] += '_copy'
    copy['time'] = datetime.utcnow().replace(microsecond=0)
    result = await db["normalizations"].insert_one(copy)
    copy["_id"] = str(result.inserted_id)
    copy["time"] = str(copy["time"])
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=copy)


@router.get("/export", response_description="Export rules")
async def export_rules(request: Request):
    list_rules = []
    for doc in await db["normalizations"].find().to_list(length=10000):
        del doc['_id']
        list_rules.append(doc)
    return list_rules


@router.put("/import", response_description="Import rules")
async def import_rules(request: Request, file: UploadFile = File(...)):
    col = db["normalizations"]
    contents = await file.read()
    rules = json.loads(contents)
    result = col.insert_many(rules)
    list_rules = []
    for doc in await db["normalizations"].find().to_list(length=1000):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        list_rules.append(doc)
    return list_rules


@router.get("/names", response_description="List all nodes")
async def list_names(request: Request):
    list_nodes = []
    for doc in await db["normalizations"].find().to_list(length=1000):
        list_nodes.append(doc['name'])
    return list_nodes
