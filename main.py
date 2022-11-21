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

@app.get("/disease/{disease_code}", response_model=schemas.Disease)
def get_disease_by_id (disease_code: str):
    disease =  db.query(models.Disease).filter(models.Disease.disease_code == disease_code).first()
    if disease is None:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@app.post("/disease", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_disease(disease: schemas.Disease):
    db_disease = models.Disease(**disease.dict())
    db_item = db.query(models.Disease).filter(models.Disease.disease_code == db_disease.disease_code).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Disease already exists")

    db.add(db_disease)
    db.commit()
    db.refresh(db_disease)
    return PostResponse(message="Disease created successfully", success=True)

@app.put("/disease/{disease_code}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_disease(disease_code: str, disease: schemas.Disease):
    db_disease = db.query(models.Disease).filter(models.Disease.disease_code == disease_code).first()
    if db_disease is None:
        raise HTTPException(status_code=404, detail="Disease not found")

    db_disease.disease_code = disease.disease_code
    db_disease.pathogen = disease.pathogen
    db_disease.disease_name = disease.disease_name
    db_disease.disease_type_id = disease.disease_type_id
    db.commit()
    return PostResponse(message="Disease updated successfully", success=True)

@app.delete("/disease/{disease_code}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def delete_disease(disease_code: int):
    db_disease = db.query(models.Disease).filter(models.Disease.id == id).first()
    if db_disease is None:
        raise HTTPException(status_code=404, detail="Disease not found")

    db.delete(db_disease)
    db.commit()
    return PostResponse(message="Disease deleted successfully", success=True)



###################################################################################
@app.get("/discover")
def get_all_discover():
    return db.query(models.Discover).all()

@app.post("/discover", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_discover(discover: schemas.Discover):
    db_discover = models.Discover(**discover.dict())
    db.add(db_discover)
    db.commit()
    db.refresh(db_discover)
    return PostResponse(message="Discover created successfully", success=True)

@app.get("/countrynamelist")
def get_countrynamelist():
    return db.query(models.Country.cname).all()

@app.get("/diseasecodelist")
def get_diseasecodelist():
    return db.query(models.Disease.disease_code).all()


@app.get('/users', response_model=List[schemas.Users])
def get_all_users():
    return db.query(models.Users).all()

@app.post('/users', response_model=PostResponse)
def create_user(user: schemas.Users):
    db_user = models.Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return PostResponse(message="User created successfully", success=True)

@app.delete('/users/{email}', response_model=PostResponse)
def delete_user(email: str):
    db_user = db.query(models.Users).filter(models.Users.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return PostResponse(message="User deleted successfully", success=True)

@app.put('/users/{email}', response_model=PostResponse)
def update_user(email: str, user: schemas.Users):
    db_user = db.query(models.Users).filter(models.Users.email == email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.email = user.email
    db_user.name = user.name
    db_user.surname = user.surname
    db_user.salary = user.salary
    db_user.phone = user.phone
    db_user.cname = user.cname
    db.commit()
    return PostResponse(message="User updated successfully", success=True)


