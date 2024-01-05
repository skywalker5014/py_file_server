import schedule
import time
from sqlalchemy import Boolean, ForeignKey, and_, create_engine, Column, Integer, String, Sequence, update
# from sqlalchemy.ext.declarative import declarative_bas
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(filename="./server.log", level=logging.INFO)

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_LINK")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

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

def checker(expiry):
     hour = int(expiry.split(":")[0])
     minute = int(expiry.split(":")[1])
     current_hour = 24 if int(time.ctime()[11:19].split(':')[0]) == 00 else int(time.ctime()[11:19].split(':')[0])
     current_minute = int(time.ctime()[11:19].split(':')[1])
     if current_hour >= hour and current_minute >= minute:
          print(f"checker true: {hour} {minute} pytime: {current_hour} {current_minute}")
          return True
     else:
          print(f"checker false: {hour} {minute} pytime: {current_hour} {current_minute}")
          return False

def exterminator():
    result = session.query(User_uploads).all()
    logging.info(f"{time.ctime()} : data expire handler schedular ran a session")
    if len(result) != 0:
         for item in result:
              if item.expiry_status == False and checker(item.expiry):
                   print(f"inside loop: {item.filename} {item.expiry} {item.expiry_status}")
                   updated_record = update(User_uploads).where(User_uploads.uuid_code == item.uuid_code).values(expiry_status=True)
                   session.execute(updated_record)
                   session.commit()
                   if os.path.exists(f"./saved/{item.filename}"):
                        os.remove(f"./saved/{item.filename}")



schedule.every(30).seconds.do(exterminator)


while True:
     schedule.run_pending()
     time.sleep(1)