from typing import List
from urllib import response

from fastapi import FastAPI, HTTPException
from pydantic.generics import GenericModel
from sqlalchemy import null
from starlette import status
from starlette.middleware.cors import CORSMiddleware

import models
import schemas
from database import engine, SessionLocal

app = FastAPI()

db = SessionLocal()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostResponse(GenericModel):
    message: str
    success: bool

###################################################################################
@app.get("/diseasetypes", response_model=List[schemas.DiseaseType])
def get_all_diseasetypes():
    dtypes = db.query(models.DiseaseType).all()
    if dtypes is None:
        raise HTTPException(status_code=404, detail="DiseaseType is empty")
    return dtypes

@app.get("/diseasetypes/{id}", response_model=schemas.DiseaseType)
def get_diseasetype_id (id: int):
    dtype =  db.query(models.DiseaseType).filter(models.DiseaseType.id == id).first()
    if dtype is None:
        raise HTTPException(status_code=404, detail="DiseaseType not found")
    return dtype

@app.post("/diseasetypes", response_model=PostResponse)
def create_diseasetype(dtype: schemas.DiseaseType):
    new_dtype = models.DiseaseType(id=dtype.id, description=dtype.description)
    db_item = db.query(models.DiseaseType).filter(models.DiseaseType.id == dtype.id).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="DiseaseType already exists")
    db.add(new_dtype)
    db.commit()
    db.refresh(new_dtype)
    return PostResponse(message="DiseaseType created successfully", success=True)

@app.put("/diseasetypes/{id}", response_model=PostResponse)
def update_diseasetype(id: int, dtype: schemas.DiseaseType):
    db_item = db.query(models.DiseaseType).filter(models.DiseaseType.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="DiseaseType not found")
    db_item.description = dtype.description
    db.commit()
    db.refresh(db_item)
    return PostResponse(message="DiseaseType updated successfully", success=True)

@app.delete("/diseasetypes/{id}", response_model=PostResponse)
def delete_diseasetype(id: int):
    db_item = db.query(models.DiseaseType).filter(models.DiseaseType.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="DiseaseType not found")
    db.delete(db_item)
    db.commit()
    return PostResponse(message="DiseaseType deleted successfully", success=True)

###################################################################################
@app.get("/country")
def get_all_country():
    return db.query(models.Country).all()

@app.get("/country/{cname}", response_model=schemas.Country)
def get_country_cname (cname: str):
    country =  db.query(models.Country).filter(models.Country.cname == cname).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@app.post("/country", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_country(country: schemas.Country):
    db_country = models.Country(**country.dict())
    db_item = db.query(models.Country).filter(models.Country.cname == db_country.cname).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Country already exists")

    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return PostResponse(message="Country created successfully", success=True)

@app.put("/country/{cname}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_country(cname: str, country: schemas.Country):
    db_country = db.query(models.Country).filter(models.Country.cname == cname).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db_country.cname = country.cname
    db_country.population = country.population
    db.commit()
    return PostResponse(message="Country updated successfully", success=True)

@app.delete("/country/{cname}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def delete_country(cname: str):
    db_country = db.query(models.Country).filter(models.Country.cname == cname).first()
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db.delete(db_country)
    db.commit()
    return PostResponse(message="Country deleted successfully", success=True)



###################################################################################
@app.get("/disease")
def get_all_disease():
    return db.query(models.Disease).all()
