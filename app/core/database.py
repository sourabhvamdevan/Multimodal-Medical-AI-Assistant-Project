

import os
import aiosqlite
from typing import AsyncGenerator
from app.core.config import settings

class DatabaseSession:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = None

    async def __aenter__(self):
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row
        return self._conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            await self._conn.close()

class DatabaseManager:
    def __init__(self, db_path: str = settings.SQLITE_DB_FILE):
        self.db_path = db_path

    def session(self) -> DatabaseSession:
        return DatabaseSession(self.db_path)

    async def init_database(self) -> None:
        async with self.session() as db:
            await db.execute("PRAGMA journal_mode = WAL;")
            await db.execute("PRAGMA synchronous = NORMAL;")
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS threads (
                    thread_id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                );
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS human_validations (
                    id TEXT PRIMARY KEY,
                    thread_id TEXT,
                    status TEXT,
                    findings TEXT,
                    reviewed_by TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(thread_id) REFERENCES threads(thread_id)
                );
            """)
            await db.commit()

db_manager = DatabaseManager()