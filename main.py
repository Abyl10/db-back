from fastapi import FastAPI, HTTPException
from sqlalchemy import null
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

###################################################################################
@app.get("/diseasetypes", response_model=schemas.DiseaseType)
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

# @app.post("/diseasetypes", status_code=201)
# def create_diseasetype(dtype: schemas.DiseaseType):



###################################################################################
@app.get("/country")
def get_all_country():
    return db.query(models.Country).all()


@app.get("/disease")
def get_all_disease():
    return db.query(models.Disease).all()
