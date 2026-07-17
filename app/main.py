
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from arq import create_pool
from arq.connections import RedisSettings

class ImageAnalysisRequest(BaseModel):
    file_path: str
    thread_id: str

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.arq_pool = await create_pool(RedisSettings(host="localhost", port=6379))
    yield
    await app.state.arq_pool.close()

app = FastAPI(
    title="Multimodal Medical AI Gateway", 
    version="1.0.0",
    lifespan=lifespan
)

async def get_queue(app: FastAPI = Depends()) -> Any:
    from fastapi import Request
    return app.state.arq_pool

@app.post("/api/v1/vision/analyze", status_code=202)
async def queue_vision_analysis(
    payload: ImageAnalysisRequest, 
    queue=Depends(get_queue)
):
    try:
        job = await queue.enqueue_job(
            "process_medical_image_task", 
            file_path=payload.file_path, 
            thread_id=payload.thread_id
        )
        
        return {
            "status": "Accepted",
            "message": "Medical scan queued successfully for async processing pipeline.",
            "job_id": job.job_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to register task inside broker queue: {str(e)}"
        )

@app.get("/api/v1/vision/status/{job_id}")
async def get_task_status(job_id: str, queue=Depends(get_queue)):
    from arq.jobs import Job
    job = Job(job_id, queue)
    status = await job.status()
    
    response = {"job_id": job_id, "status": status.value}
    
    if status.value == "complete":
        response["result"] = await job.result()
        
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)