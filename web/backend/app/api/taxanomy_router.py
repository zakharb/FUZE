from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import UploadFile, File

from app.api.taxanomy_model import TaxanomyModel, UpdateTaxanomyModel
from bson.objectid import ObjectId
import json


router = APIRouter()

@router.post("/taxanomy", response_description="Add new taxanomy")
async def create_rule(request: Request, rule: TaxanomyModel = Body(...)):
    rule = jsonable_encoder(rule)
    rule['time'] = datetime.now()
    result = await request.app.mongodb["taxanomy"].insert_one(rule)
    rule['id'] = str(result.inserted_id)
    rule['time'] = str(rule['time'])
    del rule['_id']
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=rule)

@router.get("/taxanomy", response_description="List all taxanomy")
async def list_taxanomy(request: Request):
    list_taxanomy = []
    for doc in await request.app.mongodb["taxanomy"].find().to_list(length=100):
       doc['id'] = str(doc['_id'])
       del doc['_id']
       list_taxanomy.append(doc)
    return list_taxanomy

@router.get("/taxanomy/{id}", response_description="Get a single taxanomy")
async def get_taxanomy(id: str, 
                    request: Request):
    if (taxanomy := await request.app.mongodb["taxanomy"].find_one({"_id": ObjectId(id) })) is not None:
        taxanomy['_id'] = str(taxanomy['_id'])
        return taxanomy
    raise HTTPException(status_code=404, detail=f"Taxanomy {id} not found")

@router.put("/taxanomy/{id}")
async def update_taxanomy(id: str, 
                      request: Request, 
                      taxanomy: UpdateTaxanomyModel = Body(...)):
    col = request.app.mongodb["taxanomy"]
    if await col.find_one({"_id": ObjectId(id)}):
        taxanomy = jsonable_encoder(taxanomy)
        await col.update_one({"_id": ObjectId(id)}, {"$set": taxanomy})
        await col.find_one({"_id": ObjectId(id)})
        return {'id': id}
    raise HTTPException(status_code=404, detail=f"Taxanomy {id} not found")

@router.delete("/taxanomy/{id}", response_description="Delete Taxanomy")
async def delete_taxanomy(id: str, 
                      request: Request):
    delete_result = await request.app.mongodb["taxanomy"].delete_one(
        {"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Taxanomy deleted successfully"}
    raise HTTPException(status_code=404, 
                        detail=f"Taxanomy {id} not found")

@router.get("/nodes", response_description="List all nodes")
async def list_nodes(request: Request):
    list_nodes = []
    for doc in await request.app.mongodb["taxanomy"].find().to_list(length=100):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        for node in doc['nodes']:
            node = f"{doc['name']}-{node['ip_address']}" 
            list_nodes.append(node)
    return list_nodes

@router.get("/export", response_description="Export taxanomy")
async def export_taxanomy(request: Request):
    list_taxanomy = []
    for doc in await request.app.mongodb["taxanomy"].find().to_list(length=10000):
       del doc['_id']
       list_taxanomy.append(doc)
    return list_taxanomy
