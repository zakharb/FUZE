from pydantic import BaseModel, Field

class TaxanomyModel(BaseModel):
    tax_main: str = Field(...)
    tax_object: str = Field(...)
    tax_action: str = Field(...)

class OutTaxanomyModel(TaxanomyModel):
    id: str = Field(...)

class UpdateTaxanomyModel(BaseModel):
    tax_main: str = Field(...)
    tax_object: str = Field(...)
    tax_action: str = Field(...)
