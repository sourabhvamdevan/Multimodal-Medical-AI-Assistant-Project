

import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from app.api.dependencies import get_arq_queue

router = APIRouter(prefix="/vision", tags=["Vision"])

UPLOAD_DIR = "/tmp/medical_scans"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", status_code=202)
async def upload_medical_scan(
    file: UploadFile = File(...),
    thread_id: str = Form(...),
    queue=Depends(get_arq_queue)
):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(65536):
                buffer.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write image data to storage disk: {str(e)}")
        
    try:
        job = await queue.enqueue_job(
            "process_medical_image_task",
            file_path=file_path,
            thread_id=thread_id
        )
        return {
            "status": "Accepted",
            "job_id": job.job_id,
            "thread_id": thread_id,
            "message": "Image scheduled for background PyTorch/OpenCV pipeline processing."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to push task to background worker broker: {str(e)}")