from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, List

class RuleModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    ip: str = Field(...)
    collector: str = Field(...)
    service: str = Field(...)

class OutRuleModel(RuleModel):
    id: str = Field(...)

class UpdateRuleModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    ip: str = Field(...)
    collector: str = Field(...)
    service: str = Field(...)
