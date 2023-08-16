from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import random

from .models import *

router = APIRouter()

# CRUD Routes
@router.post(
        "/create/",
        response_description="Add new basic character",
        response_model=BasicCharacterModel
        )
async def create_basic_character(request: Request, character: BasicCharacterModel = Body(...)):
    character = jsonable_encoder(character)
    new_character = await request.app.db["basic"].insert_one(character)
    created_character = await request.app.db["basic"].find_one(
        {"_id": new_character.inserted_id}
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_character)

@router.get(
        "/all/", 
        response_description="List all basic characters", 
        response_model=List[BasicCharacterModel]
        )
async def list_basic_characters(request: Request):
    basic_characters = await request.app.db["basic"].find().to_list(1000)
    return basic_characters

@router.get(
    "/{id}",
    response_description="Get a single basic character",
    response_model=BasicCharacterModel
    )
async def show_basic_character(request: Request, id: str):
    if (character := await request.app.db["basic"].find_one({"_id": id})) is not None:
        return character
    
    raise HTTPException(status_code=404, detail=f"Character {id} not found")

# Search route requires MongoDB Atlas and creation of a DB Index.
@router.get(
    "/search/",
    response_description="Get basic characters that match query",
    response_model=List[BasicCharacterModel]
    )
async def find_basic_character(request: Request, query):
    if (character := await request.app.db["basic"].aggregate([
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

@router.get(
        "/random/",
        response_description="Get a random basic character",
        response_model=BasicCharacterModel
        )
async def random_basic_character(request: Request):
    total_characters = await request.app.db["basic"].count_documents({})
    random_index = random.randint(0, total_characters -1)
    random_character = await request.app.db["basic"].find().skip(random_index).limit(1).to_list(1)

    return random_character[0]

@router.put(
        "/update/{id}", 
        response_description="Update a basic character", 
        response_model=UpdateBasicCharacterModel)
async def update_basic_character(request: Request, id: str, character: UpdateBasicCharacterModel = Body(...)):
    character = {k: v for k, v in character.dict().items() if v is not None}

    if len(character) >= 1:
        update_result = await request.app.db["basic"].update_one({"_id": id}, {"$set": character})

        if update_result.modified_count == 1:
            if (
                updated_character := await request.app.db["basic"].find_one({"_id": id})
            ) is not None:
                return updated_character

    if (existing_character := await request.app.db["basic"].find_one({"_id": id})) is not None:
        return existing_character

    raise HTTPException(status_code=404, detail=f"Character {id} not found")

@router.delete(
        "/delete/{id}", 
        response_description="Delete a basic character")
async def delete_basic_character(request: Request, id: str):
    delete_result = await request.app.db["basic"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Character {id} not found")

