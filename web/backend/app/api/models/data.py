from typing import Optional
import uuid
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class MessageModel(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    normalization: str = Field(...)
    create_time: str = Field(...)
    src_node_addr: str = Field(...)
    tgt_node_addr: str = Field(...)
    proto: str = Field(...)
    flags: str = Field(...)
    frag: str = Field(...)