from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


# JSON to BSON Conversion
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Basic Character Model
class BasicCharacterModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    backstory: str = Field(...)
    tags: list = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "description": "A non-descript person.",
                "backstory": "Jane has always been average.",
                "tags": ["average", "reliable"]
            }
        } 

# Update Basic Character Model
class UpdateBasicCharacterModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    backstory: Optional[str]
    tags: Optional[list]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "description": "A non-descript person.",
                "backstory": "Jane has always been average.",
                "tags": ["average", "reliable"]
            }
        } 
        