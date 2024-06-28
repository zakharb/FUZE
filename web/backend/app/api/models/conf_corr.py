from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, List

class RuleModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    tactic: str = Field(...)
    events: List = Field(...)
    severity: str = Field(...)
    timer: str = Field(...)

class OutNodeModel(RuleModel):
    id: str = Field(...)
    time: str = Field(...)

class UpdateRuleModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    tactic: str = Field(...)
    events: List = Field(...)
    severity: str = Field(...)
    timer: str = Field(...)
