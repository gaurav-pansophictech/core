from typing import List

import pydantic.root_model
from pydantic import BaseModel


class FormResponseData(BaseModel):
    id: str
    name: str
    version: float
    organization_id: str

    class Config:
        from_attributes = True


class FormFieldsResponseData(BaseModel):
    id: str
    name: str
    field_type: str
    validation_rules: dict

    class Config:
        from_attributes = True


class FormFieldsResponseList(pydantic.RootModel[str]):
    root: List[FormFieldsResponseData]


class FormResponseListData(BaseModel):
    id: str
    name: str
    version: float
    organization_id: str
    form_fields: List[FormFieldsResponseData]

    class Config:
        from_attributes = True
