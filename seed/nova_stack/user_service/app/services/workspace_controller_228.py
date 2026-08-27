"""Workspace & Multi-Tenancy Controller 228."""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("user.workspace.228")

class WorkspaceController228:
    """Manages workspace team quotas, project allocations, and privacy compliance data exports."""
    
    def __init__(self, workspace_id: str = "ws_228"):
        self.workspace_id = workspace_id
        self.projects: Dict[str, Dict[str, Any]] = {}

    async def create_project(self, project_name: str, owner_email: str, quota_mb: int = 5000) -> Dict[str, Any]:
        proj_id = f"prj_228_{int(datetime.utcnow().timestamp())}"
        project = {
            "project_id": proj_id,
            "project_name": project_name,
            "owner_email": owner_email,
            "quota_mb": quota_mb,
            "workspace_id": self.workspace_id,
            "created_at": datetime.utcnow().isoformat()
        }
        self.projects[proj_id] = project
        logger.info(f"[Workspace-228] Created project {proj_id} ({project_name}) for {owner_email}")
        return project

    async def update_storage_usage(self, project_id: str, added_mb: int) -> bool:
        if project_id not in self.projects:
            return False
        current = self.projects[project_id].get("used_mb", 0)
        self.projects[project_id]["used_mb"] = current + added_mb
        return True
