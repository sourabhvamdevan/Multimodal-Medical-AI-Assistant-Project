

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ThreadModel(BaseModel):
    thread_id: str
    created_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class HumanValidationModel(BaseModel):
    id: str
    thread_id: str
    status: str
    findings: str
    reviewed_by: str
    updated_at: Optional[datetime] = None

class AuditLogModel(BaseModel):
    id: str
    thread_id: str
    action: str
    actor: str
    timestamp: Optional[datetime] = None
    payload: Optional[Dict[str, Any]] = Field(default_factory=dict)