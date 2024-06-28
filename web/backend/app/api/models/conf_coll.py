from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, List

class RuleModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    nodes: List = Field(...)

class OutRuleModel(RuleModel):
    id: str = Field(...)
    time: str = Field(...)

class UpdateRuleModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    nodes: List = Field(...)
