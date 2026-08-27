import io
import hashlib
from typing import Optional, BinaryIO
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.bucket = settings.S3_BUCKET_NAME
        self.endpoint = settings.S3_ENDPOINT
        # In-memory storage fallback for local standalone testing
        self._local_storage = {}

    def compute_sha256(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    async def upload_file(self, file_path: str, data: bytes, content_type: str) -> str:
        self._local_storage[file_path] = data
        return f"s3://{self.bucket}/{file_path}"

    async def get_file(self, file_path: str) -> bytes:
        if file_path.startswith(f"s3://{self.bucket}/"):
            file_path = file_path.replace(f"s3://{self.bucket}/", "")
        return self._local_storage.get(file_path, b"")

    async def delete_file(self, file_path: str) -> bool:
        if file_path in self._local_storage:
            del self._local_storage[file_path]
            return True
        return False

storage_service = StorageService()
