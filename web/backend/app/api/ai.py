import json
import openai
from fastapi import APIRouter, Body, Request, HTTPException, status
from bson.objectid import ObjectId
from app.config import OPENAI_API_KEY
from fastapi.responses import StreamingResponse
import time

router = APIRouter()
@router.get("/playbook/{id}", response_description="Get a playbook for meta event")
async def get_playbook(id: str, request: Request):
    incident = await request.app.mongodb["incidents"].find_one({"_id": ObjectId(id)})
    if incident:
        text = ('There is incident in OT SIEM. '
                'I need short one page playbook regarding NIST 2 document. '
                'Without contact details, only steps.'
                'This is the incident: \n')
        text += json.dumps(incident, default=str)
        resp = send_data_to_chatgpt(text)
        return StreamingResponse(
            resp, 
            media_type="'text/event-stream")
    raise HTTPException(status_code=404, detail=f"Meta event {id} not found")

async def send_data_to_chatgpt(text=""):
    """
    send text to chatGPT
    :param text: text to send to API
    :return: completition from API
    """
    completion = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {
            "role": "user", 
            "content": text,
            },
        ],
        temperature=0,
        stream=True,
    )
    async for resp in completion:
        delta = resp['choices'][0]['delta']
        if delta:
            content = delta.get('content', '').replace("\n", "<br>")
            yield content

