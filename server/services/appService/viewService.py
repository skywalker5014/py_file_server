from fastapi import Request, APIRouter
from sqlalchemy import and_
from databaseHandler.databaseSetup import User_uploads
from services.authService.authService import auth2
from databaseHandler.databaseSetup import  session
import time
import logging
logging.basicConfig(filename="./server.log", level=logging.INFO)

view_router = APIRouter()

@view_router.get("/check")
def registraion_save(req: Request):
     if auth2(req.headers.get("Authorization"))[0]:
          logging.info(f"{time.ctime()} : /check ran successfully")
          user = auth2(req.headers.get("Authorization"))[1]
          query_result1 = session.query(User_uploads).filter(User_uploads.email == user).all()
          query_result2 = session.query(User_uploads).filter(and_(User_uploads.expiry_status == False, User_uploads.email != user)).all()
          print(query_result1)
          print(query_result2)
          return {"user data" : query_result1, "downloadable data": query_result2}
     else:
          logging.info(f"{time.ctime()} : access token expired at /check")
          return "token expired login again"