from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
import time

app = FastAPI()

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    start_time = time.time()
    file_name = file.filename
    
    processing_time = time.time() - start_time
    response = {
        "file_name": file_name,
        "date_time": datetime.utcnow().isoformat() + "Z",
        "processing_time": f"{processing_time:.2f} seconds",
        "transcription_text": "TEXT"
    }
    
    return JSONResponse(content=response)