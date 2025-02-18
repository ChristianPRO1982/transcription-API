from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import time
import os
from app.utils import transcribe_file

app = FastAPI()

@app.post("/transcribe/")
async def transcribe(file_path: str):
    start_time = time.time()
    file_name = os.path.basename(file_path)
    
    text, error = transcribe_file(file_path)

    processing_time = time.time() - start_time
    response = {
        "file_name": file_name,
        "date_time": datetime.utcnow().isoformat(),
        "processing_time": f"{processing_time:.2f} seconds",
        "transcription_text": text,
        "error": error
    }
    
    return JSONResponse(content=response)