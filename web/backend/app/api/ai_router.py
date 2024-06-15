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
    # meta_event = await request.app.mongodb["meta_events"].find_one({"_id": ObjectId(id)})
    meta_event = 'just test incident'
    if meta_event:
        text = ('There is incident in OT SIEM. '
                'I need short one page playbook regarding NIST 2 document. '
                'Without contact details, only steps.'
                'This is the incident: \n')
        text += json.dumps(meta_event, default=str)
        resp = send_data_to_chatgpt(text)
        #resp = fake_video_streamer()
        #print('start stream')
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
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user", 
            "content": text,
            },
        ],
        temperature=0,
        stream=True,
    )
    data = ""
    async for resp in completion:
        delta = resp['choices'][0]['delta']
        if delta:
            content = delta.get('content', '').replace("\n", "<br>")
            yield content

def fake_video_streamer():
    print('start stream func')
    for i in range(10):
        print(i)
        yield f"fake {i}, "
        time.sleep(0.5)
