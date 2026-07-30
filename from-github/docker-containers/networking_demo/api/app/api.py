import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from typing import List

from enum import Enum


class FileType(Enum):
    music: str = 'MUSIC'
    image: str = 'IMAGE'
    default: str = 'DEFAULT'

BASE_PATH = '/mnt/data/storage'
IMAGE_PATH = os.path.join(BASE_PATH, FileType.image.value)
MUSIC_PATH = os.path.join(BASE_PATH, FileType.music.value)
DEFAULT_PATH = os.path.join(BASE_PATH, FileType.default.value)
os.makedirs(IMAGE_PATH, exist_ok=True)
os.makedirs(MUSIC_PATH, exist_ok=True)
os.makedirs(DEFAULT_PATH, exist_ok=True)

app = FastAPI(title="API demonstration")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message":"Hello from the API."}

@app.get("/images", response_model=List[str])
def getAllImages():
    return os.listdir(IMAGE_PATH)

@app.get("/image/{filename}")
def getImageById(filename: str):
    try:
        file = os.path.join(IMAGE_PATH, filename)
        return FileResponse(file)
    except Exception as e:
        return HTTPException(500, f'Something went wrong while trying to return file {filename}')
    

@app.get("/music", response_model=List[str])
def getAllMusic():
    return os.listdir(MUSIC_PATH)

@app.get("/music/{filename}", response_class=FileResponse)
def getMusicById(filename: str):
    try:
        file = os.path.join(MUSIC_PATH, filename)
        return FileResponse(file)
    except Exception as e:
        return HTTPException(500, f'Something went wrong while trying to return file {filename}')

@app.post("/upload")
def uploadFile(file: UploadFile = File(...), type: FileType = FileType.default):
    print(f"Upload type: {type}")
    print(f"Upload type: {type.value}")
    fileLocation = os.path.join(BASE_PATH, type.value, file.filename)
    try:
        open(fileLocation, 'wb').write(file.file.read())
    except Exception as e:
        print(e)
        return HTTPException(500, f'Something went wrong while trying to upload file {file.filename}')

    return Response(f'Uploaded file to {fileLocation}', 200)