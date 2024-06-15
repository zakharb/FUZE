from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, List

class RuleModel(BaseModel):
    name: str = Field(...)
    desc: str = Field(...)

class OutRuleModel(RuleModel):
    id: str = Field(...)

class UpdateRuleModel(BaseModel):
    name: str = Field(...)
    desc: str = Field(...)
