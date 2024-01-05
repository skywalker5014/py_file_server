from fastapi import Request, APIRouter
from fastapi.responses import FileResponse
from services.authService.authService import auth2
from databaseHandler.databaseSetup import User_uploads, session
import time
import logging
logging.basicConfig(filename="./server.log", level=logging.INFO)


download_router = APIRouter()

@download_router.post("/download")
def download(filecode: str, req: Request):
     if auth2(req.headers.get("Authorization"))[0]:
         logging.info(f"{time.ctime()} : /download route ran successfully")     
         fileinfo = session.query(User_uploads).filter(User_uploads.uuid_code == filecode).one()
         if not fileinfo.expiry_status: 
             logging.info(f"{time.ctime()} : sent file to requester at /download")     
             sendfile = f"./saved/{fileinfo.filename}"
             return FileResponse(sendfile)
         else:
              logging.info(f"{time.ctime()} : deleted file could not be sent to requester at /download")
              return "file has beed deleted"
     else: 
          logging.info(f"{time.ctime()} : user access token expired at /download")
          return "token expired"

