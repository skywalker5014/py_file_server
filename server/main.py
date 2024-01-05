from fastapi import FastAPI
import uvicorn
from services.appService.homeService import home_router
from services.appService.downloadService import download_router
from services.appService.uploadService import upload_router
from services.appService.viewService import view_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import time
import logging
logging.basicConfig(filename="./server.log", level=logging.INFO)

load_dotenv()



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(download_router)
app.include_router(home_router)
app.include_router(upload_router)
app.include_router(view_router)


if __name__ == "__main__":
         logging.info(f"{time.ctime()} : server started")
         uvicorn.run("main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")), reload=True)