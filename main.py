from config import CFG

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

app = FastAPI()

# Connecting to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(CFG["MONGODB_URL"])
db = client.character_farm

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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "description": "A basic stand-in example.",
            }
        } 

# Endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get(
        "/characters/basic/", 
        response_description="List all characters", 
        response_model=List[BasicCharacterModel]
        )
async def list_basic_characters():
    basic_characters = await db["basic"].find().to_list(1000)
    return basic_characters