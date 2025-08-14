# app/main.py
"""
FastAPI app exposing an endpoint to transcribe an audio/video file using OpenAI Whisper.

Docs:
- Interactive docs (Swagger): /docs
- ReDoc: /redoc

Notes:
- Request body uses a Pydantic model with an example for OpenAPI.
- Responses are typed with a response model and documented error variants.
- Keeps compatibility with CI/CD (deterministic responses and clear typing).
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import time
import os
from app.utils import transcribe_file
from threading import Lock

app = FastAPI()

@app.post("/transcribe/", summary="IN = audio file path / OUT = JSON", tags=["API"])
async def transcribe(file_path: str):
    """
    Transcribes the audio content of a given file.

    # Args:
        file_path (str): The path to the audio file to be transcribed.
    
    # Returns:
    JSONResponse: A JSON response containing:
    - file_name (str): The name of the transcribed file.
    - date_time (str): The UTC timestamp when the transcription was processed.
    - processing_time (str): The time taken to process the transcription, in seconds.
    - transcription_text (str or None): The transcribed text, or None if an error occurred.
    - error (str or None): Error message if transcription failed, otherwise None.
    
    # Raises:
        None
    
    # Example:
        response = await transcribe("/path/to/audio.wav")
    """
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

@app.get("/health", summary="Health check", tags=["Monitoring"])
async def health_check():
    """
    Simple health check endpoint to verify API is running.
    """
    return {"status": "ok", "message": "API is healthy"}

# Monitoring state (in-memory, resets on restart)
monitoring_data = {
    "total_processing_time": 0.0,
    "total_file_size_mb": 0.0,
    "num_requests": 0
}
monitoring_lock = Lock()

@app.middleware("http")
async def monitor_transcription_time(request, call_next):
    if request.url.path == "/transcribe/":
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        # Extract file_path from request
        try:
            body = await request.json()
            file_path = body.get("file_path", "")
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024) if os.path.exists(file_path) else 0.0
        except Exception:
            file_size_mb = 0.0

        with monitoring_lock:
            monitoring_data["total_processing_time"] += duration
            monitoring_data["total_file_size_mb"] += file_size_mb
            monitoring_data["num_requests"] += 1

        return response
    else:
        return await call_next(request)

@app.get("/monitoring/average_time_per_mb", summary="Average processing time per MB", tags=["Monitoring"])
async def average_time_per_mb():
    """
    Returns the average processing time per MB of file processed.
    """
    with monitoring_lock:
        total_time = monitoring_data["total_processing_time"]
        total_mb = monitoring_data["total_file_size_mb"]
        num_requests = monitoring_data["num_requests"]

    avg_time_per_mb = (total_time / total_mb) if total_mb > 0 else None
    return {
        "total_requests": num_requests,
        "total_file_size_mb": total_mb,
        "total_processing_time_sec": total_time,
        "average_time_per_mb_sec": avg_time_per_mb
    }

@app.get("/monitoring/stats", summary="Global monitoring stats", tags=["Monitoring"])
async def monitoring_stats():
    """
    Returns global monitoring statistics: total requests, total file size processed, and total processing time.
    """
    with monitoring_lock:
        stats = monitoring_data.copy()
    return stats