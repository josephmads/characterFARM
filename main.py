from config import CFG

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
import motor.motor_asyncio

from models import *

app = FastAPI()

# Connecting to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(CFG["MONGODB_URL"])
db = client.character_farm

# CRUD Routes
@app.post(
        "/basic/",
        response_description="Add new basic character",
        response_model=BasicCharacterModel
        )
async def create_basic_character(character: BasicCharacterModel = Body(...)):
    character = jsonable_encoder(character)
    new_character = await db["basic"].insert_one(character)
    created_character = await db["basic"].find_one(
        {"_id": new_character.inserted_id}
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_character)

@app.get(
        "/basic/", 
        response_description="List all basic characters", 
        response_model=List[BasicCharacterModel]
        )
async def list_basic_characters():
    basic_characters = await db["basic"].find().to_list(1000)
    return basic_characters

@app.get(
    "/basic/{id}",
    response_description="Get a single basic character",
    response_model=BasicCharacterModel
    )
async def show_basic_character(id: str):
    if (character := await db["basic"].find_one({"_id": id})) is not None:
        return character
    
    raise HTTPException(status_code=404, detail=f"Character {id} not found")


# Search Route: requires MongoDB Atlas and creation of an DB Index.
@app.get(
    "/basic/search/",
    response_description="Get basic characters that match query",
    response_model=List[BasicCharacterModel]
    )
async def find_basic_character(query):
    if (character := await db["basic"].aggregate([
        {
        "$search": {
            "index": "cf_basic",
            "text": {
                "query": query,
                "path": {
                    "wildcard": "*"
                    }
                }
            }
        }]).to_list(1000)):

        return character
    
    raise HTTPException(status_code=404, detail=f"Character {query} not found")