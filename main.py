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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


###################################################################################

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

@app.get("/usersemaillist")
def get_emails():
    return db.query(models.Users.email).all()

###################################################################################
@app.get("/publicservant")
def get_all_publicservant():
    return db.query(models.PublicServant).all()

@app.get("/publicservant/{email}", response_model=schemas.PublicServant)
def get_publicservant_by_email (email: str):
    publicservant =  db.query(models.PublicServant).filter(models.PublicServant.email == email).first()
    if publicservant is None:
        raise HTTPException(status_code=404, detail="Public servant not found")
    return publicservant

@app.post("/publicservant", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_publicservant(publicservant: schemas.PublicServant):
    db_publicservant = models.PublicServant(**publicservant.dict())
    db_item = db.query(models.PublicServant).filter(models.PublicServant.email == db_publicservant.email).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Public servant already exists")

    db.add(db_publicservant)
    db.commit()
    db.refresh(db_publicservant)
    return PostResponse(message="Public servant created successfully", success=True)

@app.put("/publicservant/{email}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_publicservant(email: str, publicservant: schemas.PublicServant):
    db_publicservant = db.query(models.PublicServant).filter(models.PublicServant.email == email).first()
    if db_publicservant is None:
        raise HTTPException(status_code=404, detail="Public servant not found")

    db_publicservant.email = publicservant.email
    db_publicservant.department = publicservant.department
    db.commit()
    return PostResponse(message="Public servant updated successfully", success=True)

@app.delete("/publicservant/{email}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def delete_publicservant(email: str):
    db_publicservant = db.query(models.PublicServant).filter(models.PublicServant.email == email).first()
    if db_publicservant is None:
        raise HTTPException(status_code=404, detail="Public servant not found")

    db.delete(db_publicservant)
    db.commit()
    return PostResponse(message="Public servant deleted successfully", success=True)

###################################################################################
@app.get("/doctor")
def get_all_doctor():
    return db.query(models.Doctor).all()

@app.get("/doctor/{email}", response_model=schemas.Doctor)
def get_doctor_by_email (email: str):
    doctor =  db.query(models.Doctor).filter(models.Doctor.email == email).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/doctor", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_doctor(doctor: schemas.Doctor):
    db_doctor = models.Doctor(**doctor.dict())
    db_item = db.query(models.Doctor).filter(models.Doctor.email == db_doctor.email).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Doctor already exists")

    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return PostResponse(message="Doctor created successfully", success=True)

@app.put("/doctor/{email}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_doctor(email: str, doctor: schemas.Doctor):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.email == email).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db_doctor.email = doctor.email
    db_doctor.degree = doctor.degree
    db.commit()
    return PostResponse(message="Doctor updated successfully", success=True)


@app.delete("/doctor/{email}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def delete_doctor(email: str):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.email == email).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(db_doctor)
    db.commit()
    return PostResponse(message="Doctor deleted successfully", success=True)

###################################################################################

@app.get("/specialize")
def get_all_specialize():
    return db.query(models.Specialize).all()

###################################################################################
@app.get("/record")
def get_all_record():
    return db.query(models.Record).all()

@app.post("/record", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_record(record: schemas.Record):
    db_record = models.Record(**record.dict())
    db_item = db.query(models.Record).filter(models.Record.id == db_record.id).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Record already exists")

    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return PostResponse(message="Record created successfully", success=True)

@app.put("/record/{cname}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_record(cname: str, record: schemas.Record):
    db_record = db.query(models.Record).filter(models.Record.cname == cname).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    db_record.cname = record.cname
    db_record.disease_code = record.disease_code
    db_record.email = record.email
    db_record.total_deaths = record.total_deaths
    db_record.total_patients = record.total_patients
    db.commit()
    return PostResponse(message="Record updated successfully", success=True)

@app.delete("/record/{cname}", status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def delete_record(cname: str):
    db_record = db.query(models.Doctor).filter(models.Record.cname == cname).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(db_record)
    db.commit()
    return PostResponse(message="Record deleted successfully", success=True)