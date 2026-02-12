from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import shutil
import os

app = FastAPI()

# CORS FIX 🔥
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data.json"

class FormData(BaseModel):
    username: str
    age: int


# POST ENDPOINT FOR THE NORMAL FORM DATA

# @app.post("/api/data")
# def receive_data(data: FormData):
#     new_data = data.dict()  # convert pydantic model to normal dict

#     # Load existing file or create new list
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r") as f:
#             existing = json.load(f)
#     else:
#         existing = []

#     # Append new entry
#     existing.append(new_data)

#     # Save back to file
#     with open(DATA_FILE, "w") as f:
#         json.dump(existing, f, indent=2)

#     return {"message": "Data stored", "stored": new_data}



# FILE UPLOAD ENPOINT STRUCTURE :
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# POST ENDPOINT FOR THE FILE UPLOAD HANDLING AND STORAGE
@app.post('/upload')
def upload_file(
    username: str = Form(...),
    age: int = Form(...),
    file: UploadFile = File(...)
):
    file_location = f"{UPLOAD_DIR}/{file.filename}"


    # SAVING THE FILE TO THE TEMPORARY STORAGE
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    return {
        "message": "file uploaded",
        "username": username,
        "age": age,
        "file_saved_to": file_location
    }