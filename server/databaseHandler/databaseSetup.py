from sqlalchemy import Boolean, ForeignKey, and_, create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_LINK")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


class User(Base):
     __tablename__ = "users"
     id = Column(Integer, Sequence("user_id_seq"))
     username = Column(String(50), unique=True)
     email = Column(String(50), unique=True, primary_key=True)
     passhash = Column(String)

class User_uploads(Base):
     __tablename__ = "user_uploads"
     email = Column(String, ForeignKey("users.email"))
     filename = Column(String)
     uuid_code = Column(String, unique=True, primary_key=True)
     expiry = Column(String)
     expiry_status = Column(Boolean)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
