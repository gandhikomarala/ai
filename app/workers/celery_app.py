from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "aegisai_workers",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=1
)

@celery_app.task(name="app.workers.tasks.ingest_document")
def task_ingest_document(document_id: str):
    return {"status": "SUCCESS", "document_id": document_id, "chunks_created": 12}

@celery_app.task(name="app.workers.tasks.index_repository")
def task_index_repository(repo_id: str):
    return {"status": "SUCCESS", "repository_id": repo_id, "files_indexed": 48}
