from sqlalchemy.sql.expression import null
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from database import Base


class DiseaseType(Base):
    __tablename__ = "diseasetype"
    id = Column(Integer, primary_key=True)
    description = Column(String(140), nullable=False)


class Country(Base):
    __tablename__ = "country"
    cname = Column(String(50), primary_key=True)
    population = Column(BigInteger, nullable=False)


class Disease(Base):
    __tablename__ = "disease"
    disease_code = Column(String(50), primary_key=True)
    pathogen = Column(String(20), nullable=False)
    description = Column(String(140), nullable=False)
    id = Column(Integer, ForeignKey("diseasetype.id", ondelete='CASCADE'), nullable=True, unique=True)


class Discover(Base):
    __tablename__ = "discover"
    cname = Column(String(50), ForeignKey("country.cname"), primary_key=True)
    disease_code = Column(String(50), ForeignKey("disease.disease_code"), primary_key=True)
    first_enc_date = Column(DateTime, nullable=False)


class Users(Base):
    __tablename__ = "users"
    email = Column(String(60), primary_key=True, unique=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(40), nullable=False)
    salary = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    cname = Column(String(50), ForeignKey("country.cname"), nullable=False)


class PublicServant(Base):
    __tablename__ = "publicservant"
    email = Column(String(60), ForeignKey("users.email"), primary_key=True)
    department = Column(String(50), nullable=False)


class Doctor(Base):
    __tablename__ = "doctor"
    email = Column(String(60), ForeignKey("users.email"), primary_key=True)
    degree = Column(String(20), nullable=False)


class Specialize(Base):
    __tablename__ = "specialize"
    id = Column(Integer, ForeignKey("diseasetype.id"), primary_key=True)
    email = Column(String(60), ForeignKey("doctor.email"), primary_key=True)


class Record(Base):
    __tablename__ = "record"
    email = Column(String(60), ForeignKey("publicservant.email"), primary_key=True)
    cname = Column(String(50), ForeignKey("country.cname"), primary_key=True)
    disease_code = Column(String(50), ForeignKey("disease.disease_code"), primary_key=True)
    total_deaths = Column(Integer, nullable=False)
    total_patients = Column(Integer, nullable=False)
