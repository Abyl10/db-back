from pydantic import BaseModel
from typing import List, Optional

class DiseaseType(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True

class Country(BaseModel):
    cname: str
    population: int

    class Config:
        orm_mode = True


class Disease(BaseModel):
    disease_code: str
    pathogen: str
    description: str
    id: int

    class Config:
        orm_mode = True


class Discover(BaseModel):
    cname: str
    disease_code: str
    first_enc_date: str

    class Config:
        orm_mode = True


class Users(BaseModel):
    email: str
    name: str
    surname: str
    salary: int
    phone: str
    cname: str

    class Config:
        orm_mode = True


class PublicServant(BaseModel):
    email: str
    department: str

    class Config:
        orm_mode = True


class Doctor(BaseModel):
    email: str
    degree: str

    class Config:
        orm_mode = True


class Specialize(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class Record(BaseModel):
    email: str
    cname: str
    disease_code: str
    total_deaths: int
    total_patients: int

    class Config:
        orm_mode = True
        
