import datetime
import bcrypt
import jwt
from fastapi import APIRouter, Request
from databaseHandler.databaseSetup import  User, session
from requestModels.requestModels import User_login, User_register
import os
from dotenv import load_dotenv
import time
import logging
logging.basicConfig(filename="./server.log", level=logging.INFO)

load_dotenv()
home_router = APIRouter()

@home_router.post("/register")
async def user_registration(info: User_register):
    logging.info(f"{time.ctime()} : /register ran successfully")
    bytes_pass = bytes(info.password, encoding='utf-8')
    hashed_pass = bcrypt.hashpw(bytes_pass, bcrypt.gensalt())
    new_user = User(username=info.username, email=info.email, passhash=hashed_pass.decode())
    session.add(new_user)
    session.commit()
    logging.info(f"{time.ctime()} : new user registration successful, user: {info.email} at /register")
    return "registration success"

@home_router.post("/login")
def user_login(loginInfo : User_login):
    logging.info(f"{time.ctime()} : /login ran successfully")
    user = session.query(User).filter(User.email == loginInfo.email).one()
    bytes_pass = bytes(loginInfo.password, encoding='utf-8')
    bytes_hash = bytes(user.passhash, encoding='utf-8')  
    if bcrypt.checkpw(bytes_pass, bytes_hash):
        logging.info(f"{time.ctime()} : user: {user.email} successfully logged in at /login")
        token = jwt.encode({"useremail" : loginInfo.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.getenv("SECRET_KEY"), algorithm="HS256" )
        return {"accesstoken": token}
    else:
        logging.info(f"{time.ctime()} : user: {user} wrong password input at /login")
        return "password wrong"