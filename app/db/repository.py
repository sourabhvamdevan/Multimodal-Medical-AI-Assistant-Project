

import json
import uuid
from typing import Optional, List, Dict, Any
import aiosqlite
from app.db.models import ThreadModel, HumanValidationModel, AuditLogModel

class MedicalRepository:
    def __init__(self, db_conn: aiosqlite.Connection):
        self.db = db_conn

    async def create_thread(self, thread_id: str, metadata: Dict[str, Any]) -> ThreadModel:
        metadata_json = json.dumps(metadata)
        await self.db.execute(
            "INSERT INTO threads (thread_id, metadata) VALUES (?, ?)",
            (thread_id, metadata_json)
        )
        await self.db.commit()
        return ThreadModel(thread_id=thread_id, metadata=metadata)

    async def get_thread(self, thread_id: str) -> Optional[ThreadModel]:
        async with self.db.execute(
            "SELECT thread_id, created_at, metadata FROM threads WHERE thread_id = ?",
            (thread_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return ThreadModel(
                    thread_id=row["thread_id"],
                    created_at=row["created_at"],
                    metadata=json.loads(row["metadata"]) if row["metadata"] else {}
                )
        return None

    async def create_validation_entry(self, thread_id: str, findings: str) -> str:
        validation_id = str(uuid.uuid4())
        await self.db.execute(
            "INSERT INTO human_validations (id, thread_id, status, findings, reviewed_by) VALUES (?, ?, ?, ?, ?)",
            (validation_id, thread_id, "PENDING", findings, "SYSTEM")
        )
        await self.db.commit()
        return validation_id

    async def update_validation_status(
        self, validation_id: str, status: str, findings: str, reviewer: str
    ) -> bool:
        cursor = await self.db.execute(
            "UPDATE human_validations SET status = ?, findings = ?, reviewed_by = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, findings, reviewer, validation_id)
        )
        await self.db.commit()
        return cursor.rowcount > 0

    async def get_validation_by_thread(self, thread_id: str) -> Optional[HumanValidationModel]:
        async with self.db.execute(
            "SELECT id, thread_id, status, findings, reviewed_by, updated_at FROM human_validations WHERE thread_id = ? ORDER BY updated_at DESC LIMIT 1",
            (thread_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return HumanValidationModel(
                    id=row["id"],
                    thread_id=row["thread_id"],
                    status=row["status"],
                    findings=row["findings"],
                    reviewed_by=row["reviewed_by"],
                    updated_at=row["updated_at"]
                )
        return None

    async def log_audit_action(self, thread_id: str, action: str, actor: str, payload: Dict[str, Any]) -> None:
        log_id = str(uuid.uuid4())
        payload_json = json.dumps(payload)
        await self.db.execute(
            "INSERT INTO audit_logs (id, thread_id, action, actor, payload) VALUES (?, ?, ?, ?, ?)",
            (log_id, thread_id, action, actor, payload_json)
        )
        await self.db.commit()