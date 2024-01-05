from pathlib import Path
import shutil
from typing import Annotated
from uuid import uuid4, uuid5
from databaseHandler.databaseSetup import  session
from fastapi import File, Form, Request, UploadFile, APIRouter
from databaseHandler.databaseSetup import User_uploads
from services.authService.authService import auth2
import time
import logging
logging.basicConfig(filename="./server.log", level=logging.INFO)

upload_router = APIRouter()

@upload_router.post("/upload2")
def uploads(file: Annotated[UploadFile, File()], expire: Annotated[str, Form()], req: Request):
     if auth2(req.headers.get("Authorization"))[0]:
          logging.info(f"{time.ctime()} : /upload2 ran successfully")
          user = auth2(req.headers.get("Authorization"))[1]
          destination = Path(f"./saved/{file.filename}")
          code = uuid5(uuid4(), file.filename)
          if file.size != None:
              new_file = User_uploads(email=user, filename=file.filename, uuid_code=code, expiry=expire, expiry_status=False)
              session.add(new_file)
              session.commit()
              logging.info(f"{time.ctime()} : user: {user} uploaded new file {file.filename} with expiration at {expire} at /upload2")
              with destination.open("wb") as f:
                   shutil.copyfileobj(file.file, f)
                   file.file.close()
              return "file saved"
          else:
               logging.info(f"{time.ctime()} : no file received to save at /upload2")
               return "no file sent"
     else:
          logging.info(f'{time.ctime()} : access token expired at /upload2')
          return "token expired"