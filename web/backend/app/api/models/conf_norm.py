from typing import Optional
from pydantic import BaseModel, Field
from typing import Dict, List

class NormalizationModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    tax_main: str = Field(...)
    events: List = Field(...)
    profile: str = Field(...)

class OutNodeModel(NormalizationModel):
    id: str = Field(...)
    time: str = Field(...)

class UpdateNormalizationModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    tax_main: str = Field(...)
    events: List = Field(...)
    profile: str = Field(...)
