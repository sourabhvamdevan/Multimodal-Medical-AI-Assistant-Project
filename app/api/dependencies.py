

import os
from typing import AsyncGenerator, Any
from fastapi import Request
from qdrant_client import AsyncQdrantClient
from app.core.redis_config import get_redis_connection_pool

async def get_db(request: Request) -> AsyncGenerator[Any, None]:
    """
    Yields a thread-safe transaction context from the SQLite connection pool.
    """
    db = request.app.state.db_session_factory()
    try:
        yield db
    finally:
        await db.close()

async def get_arq_queue(request: Request) -> Any:
    """
    Retrieves the persistent Redis-backed ARQ task broker instance.
    """
    return request.app.state.arq_pool

async def get_redis(request: Request) -> AsyncGenerator[Any, None]:
    """
    Yields an active Redis client for fast key-value lookups or streaming buffers.
    """
    pool = await get_redis_connection_pool()
    from redis.asyncio import Redis
    async with Redis(connection_pool=pool) as client:
        yield client

async def get_qdrant_client() -> AsyncGenerator[AsyncQdrantClient, None]:
    """
    Exposes an asynchronous connection vector context window to Qdrant clusters.
    """
    qdrant_host = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
    client = AsyncQdrantClient(host=qdrant_host, port=qdrant_port)
    try:
        yield client
    finally:
        await client.close()

async def get_langgraph_workflow(request: Request) -> Any:
    """
    Accesses the fully-compiled multi-agent supervisor workspace graph.
    """
    return request.app.state.compiled_agent_graph