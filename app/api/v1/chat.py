

import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import Any
from app.api.dependencies import get_redis, get_langgraph_workflow

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    text: str
    thread_id: str

@router.post("/query")
async def process_text_query(
    payload: ChatRequest,
    redis=Depends(get_redis),
    workflow=Depends(get_langgraph_workflow)
):
    cache_key = f"cache:llm:{payload.text.strip().lower()}"
    cached_response = await redis.get(cache_key)
    
    if cached_response:
        return {"response": cached_response.decode("utf-8"), "cached": True}
        
    config = {"configurable": {"thread_id": payload.thread_id}}
    initial_state = {"messages": [("user", payload.text)]}
    
    try:
        final_state = await workflow.ainvoke(initial_state, config=config)
        assistant_reply = final_state["messages"][-1].content
        
        await redis.setex(cache_key, 3600, assistant_reply)
        
        return {"response": assistant_reply, "cached": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/stream")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    redis=Depends(get_redis),
    workflow=Depends(get_langgraph_workflow)
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            user_text = payload.get("text", "")
            thread_id = payload.get("thread_id", "default_socket_session")
            
            config = {"configurable": {"thread_id": thread_id}}
            initial_state = {"messages": [("user", user_text)]}
            
            async for event in workflow.astream(initial_state, config=config):
                if "final_response_node" in event:
                    node_output = event["final_response_node"]
                    msg = node_output.get("messages", [])[-1][1]
                    await websocket.send_json({"type": "chunk", "content": msg})
                    
    except WebSocketDisconnect:
        pass