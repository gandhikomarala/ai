from typing import Optional, Any
from uuid import UUID
from dataclasses import dataclass
from app.core.exceptions import TenantIsolationViolation

@dataclass
class TenantContext:
    organization_id: UUID
    project_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    user_role: Optional[str] = None

    def validate_access(self, target_org_id: Any, target_project_id: Optional[Any] = None) -> bool:
        if str(self.organization_id) != str(target_org_id):
            raise TenantIsolationViolation(
                f"Tenant isolation breached: current org [{self.organization_id}] tried to access org [{target_org_id}]"
            )
        if self.project_id and target_project_id:
            if str(self.project_id) != str(target_project_id):
                raise TenantIsolationViolation(
                    f"Project isolation breached: current project [{self.project_id}] tried to access project [{target_project_id}]"
                )
        return True
