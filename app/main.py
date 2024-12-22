from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import shutil
import os
import zipfile
from datetime import datetime
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "/app/uploads"

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_files(files: list[UploadFile]):
    transfer_id = str(uuid.uuid4())
    transfer_dir = os.path.join(UPLOAD_DIR, transfer_id)
    os.makedirs(transfer_dir)

    for file in files:
        file_path = os.path.join(transfer_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Create ZIP file
    zip_path = f"{transfer_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(transfer_dir):
            for file in files:
                zipf.write(os.path.join(root, file), file)

    return {"transfer_id": transfer_id}

@app.get("/download/{transfer_id}")
async def download_files(transfer_id: str):
    zip_path = os.path.join(UPLOAD_DIR, f"{transfer_id}.zip")
    return FileResponse(zip_path)
