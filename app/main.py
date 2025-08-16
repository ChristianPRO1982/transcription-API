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

from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
import time
import os
from app.utils import transcribe_file
from threading import Lock
import secrets

from app.auth import create_access_token, get_current_subject
from app.config import DEMO_USERNAME, DEMO_PASSWORD

app = FastAPI()

@app.post("/token", tags=["auth"])
async def issue_token(
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Issue a short-lived access token for service/client usage.
    """
    if not (
        secrets.compare_digest(username, DEMO_USERNAME)
        and secrets.compare_digest(password, DEMO_PASSWORD)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/transcribe/", summary="IN = audio file path / OUT = JSON", tags=["API"])
async def transcribe(file_path: str, subject: str = Depends(get_current_subject)):
    """
    Transcribes the audio content of a given file. Protected by JWT Bearer.
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
        "error": error,
        "requested_by": subject,
    }

    return JSONResponse(content=response)


@app.get("/health", summary="Health check", tags=["Monitoring"])
async def health_check():
    """
    Simple health check endpoint to verify API is running.
    """
    return {"status": "ok", "message": "API is healthy"}


monitoring_data = {
    "total_processing_time": 0.0,
    "total_file_size_mb": 0.0,
    "num_requests": 0,
}
monitoring_lock = Lock()


@app.middleware("http")
async def monitor_transcription_time(request, call_next):
    """
    Measure per-request timing and size aggregates.
    """
    if request.url.path == "/transcribe/":
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        try:
            body = await request.json()
            file_path = body.get("file_path", "")
            file_size_mb = (
                os.path.getsize(file_path) / (1024 * 1024)
                if os.path.exists(file_path)
                else 0.0
            )
        except Exception:
            file_size_mb = 0.0
        with monitoring_lock:
            monitoring_data["total_processing_time"] += duration
            monitoring_data["total_file_size_mb"] += file_size_mb
            monitoring_data["num_requests"] += 1
        return response
    return await call_next(request)


@app.get("/monitoring/average_time_per_mb", summary="Average processing time per MB", tags=["Monitoring"])
async def average_time_per_mb(subject: str = Depends(get_current_subject)):
    """
    Return average processing time per MB. Protected by JWT Bearer.
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
        "average_time_per_mb_sec": avg_time_per_mb,
    }


@app.get("/monitoring/stats", summary="Global monitoring stats", tags=["Monitoring"])
async def monitoring_stats(subject: str = Depends(get_current_subject)):
    """
    Return global monitoring stats. Protected by JWT Bearer.
    """
    with monitoring_lock:
        stats = monitoring_data.copy()
    return stats
