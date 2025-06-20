from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os, shutil
from uuid import uuid4
from app.agent_workflow import run_pitch_deck_workflow

app = FastAPI()

# The server will run at http://localhost:8000 by default when started with uvicorn
# Upload endpoint: http://localhost:8000/upload

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

UPLOAD_DIR = "./app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    # Health check endpoint to confirm server is running
    return {
        "message": "Backend is running.",
        "upload_endpoint": "http://localhost:8000/upload"
    }

@app.post("/upload")
async def upload_pitch_deck(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".pptx"]:
        return {"error": "Only .pdf and .pptx formats are allowed."}

    file_id = f"{uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_id)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = run_pitch_deck_workflow(file_path)
        return result
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
