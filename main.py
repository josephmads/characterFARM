from config import CFG

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import motor.motor_asyncio
import random

from models import *

app = FastAPI()

# Connecting to MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(CFG["MONGODB_URL"])
db = client.character_farm

# CRUD Routes
@app.post(
        "/basic/create/",
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
        "/basic/all/", 
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

# Search Route: requires MongoDB Atlas and creation of a DB Index.
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
    
    raise HTTPException(status_code=404, detail=f'"{query}" not found')

@app.get(
        "/basic/random/",
        response_description="Get a random basic character",
        response_model=BasicCharacterModel
        )
async def random_basic_character():
    total_characters = await db["basic"].count_documents({})
    random_index = random.randint(0, total_characters -1)
    random_character = await db["basic"].find().skip(random_index).limit(1).to_list(1)

    return random_character[0]

@app.put(
        "/basic/update/{id}", 
        response_description="Update a basic character", 
        response_model=UpdateBasicCharacterModel)
async def update_basic_character(id: str, character: UpdateBasicCharacterModel = Body(...)):
    character = {k: v for k, v in character.dict().items() if v is not None}

    if len(character) >= 1:
        update_result = await db["basic"].update_one({"_id": id}, {"$set": character})

        if update_result.modified_count == 1:
            if (
                updated_character := await db["basic"].find_one({"_id": id})
            ) is not None:
                return updated_character

    if (existing_character := await db["basic"].find_one({"_id": id})) is not None:
        return existing_character

    raise HTTPException(status_code=404, detail=f"Character {id} not found")

@app.delete(
        "/basic/delete/{id}", 
        response_description="Delete a basic character")
async def delete_basic_character(id: str):
    delete_result = await db["basic"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Character {id} not found")
