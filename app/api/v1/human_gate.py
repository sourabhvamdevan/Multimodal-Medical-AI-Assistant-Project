


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.dependencies import get_langgraph_workflow

router = APIRouter(prefix="/human", tags=["Human-in-the-Loop Gate"])

class ValidationApprovalRequest(BaseModel):
    thread_id: str
    approved: bool
    clinical_override_notes: str | None = None

@router.post("/validate")
async def submit_human_clinical_validation(
    payload: ValidationApprovalRequest,
    workflow=Depends(get_langgraph_workflow)
):
    config = {"configurable": {"thread_id": payload.thread_id}}
    
    try:
        snapshot = await workflow.aget_state(config)
        if not snapshot.next:
            raise HTTPException(
                status_code=400, 
                detail="No execution breakpoint found or thread state context window has already completed."
            )
            
        current_analysis = snapshot.values.get("analysis_output", "")
        updated_findings = payload.clinical_override_notes if payload.clinical_override_notes else current_analysis
        
        state_update = {
            "human_approved": payload.approved,
            "analysis_output": f"[Physician Audited Response]: {updated_findings}" if payload.approved else "[Rejected by Clinician Assessment]"
        }
        
        await workflow.aupdate_state(config, state_update, as_node="image_analysis_node")
        
        if payload.approved:
            finalized_state = await workflow.ainvoke(None, config=config)
            response_msg = finalized_state["messages"][-1].content
            return {"status": "Resumed & Completed", "final_response": response_msg}
            
        return {"status": "Halted", "message": "Verification marked as rejected. Halting graph loop state progression."}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to modify graph runtime validation values: {str(e)}")