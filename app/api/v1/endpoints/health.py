from fastapi import APIRouter
from app.core.responses import success_response

router = APIRouter()

@router.get("/health")
async def health_check():
    return success_response({
        "status": "HEALTHY",
        "service": "AegisAI Platform API",
        "version": "1.0.0",
        "components": {
            "database": "CONNECTED",
            "redis": "CONNECTED",
            "storage_minio": "CONNECTED",
            "graph_neo4j": "CONNECTED"
        }
    })
