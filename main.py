from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
# from . import models
from db import get_db, engine
import models
import schemas
from repositories import AddressRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
import geopy.geocoders
from geopy.geocoders import Nominatim
import pandas as pd
from geopy import distance

app = FastAPI(title="Address Book",
    description="Address book created for Assingment",
    version="1.0.0",)

geolocator = Nominatim(user_agent="Address Book")

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post('/add_address', tags=["Address"],response_model=schemas.Address,status_code=201)
async def create_item(address_request: schemas.AddCreate, db: Session = Depends(get_db)):
    """
    Create an Address and store it in the database
    """

    return await AddressRepo.create(db=db, address=address_request)


@app.get('/get-add', tags=["Address"], status_code=201)
async def get_all(db: Session = Depends(get_db)): 
     """
    To get list of all Addresses in database
    """
        
    addList = db.query(models.Address).all()
    return addList

@app.put('/update-add/{add_id}', tags=["Address"],response_model=schemas.Address)
async def update_item(add_id: int,address_request: schemas.Address, db: Session = Depends(get_db)):
    """
    Update an Address stored in the database
    """
    db_item = AddressRepo.fetch_by_id(db, add_id)
    if db_item:
        update_item_encoded = jsonable_encoder(address_request)
        db_item.name = update_item_encoded['name']
        db_item.address = update_item_encoded['address']
        db_item.address_point = geolocator.geocode(update_item_encoded['address']).point

        return await AddressRepo.update(db=db, data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")

@app.get('/get-add-by-distance', tags=["Address"], status_code=201)
async def get_by_distance(address_loc: str, udistance: int, db: Session = Depends(get_db)):
    """
    To Calculate the distance between given point and point in address book. Returns a address that matches both distance and given Point
    """
    
    query = db.query(models.Address).all()
    for row in query:
        print(row.address_point)
        curr_add = geolocator.geocode(address_loc).point
        print(curr_add)
        tdistance = distance.great_circle(curr_add, row.address_point)
        
        if tdistance == udistance:
            return [row.name, row.address ]
    

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
    
