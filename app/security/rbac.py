from typing import List, Dict, Set
from app.core.constants import UserRole
from app.core.exceptions import AuthorizationError

ROLE_HIERARCHY: Dict[UserRole, int] = {
    UserRole.SUPER_ADMIN: 100,
    UserRole.ORG_ADMIN: 80,
    UserRole.PROJECT_ADMIN: 60,
    UserRole.ENGINEER: 40,
    UserRole.ANALYST: 20,
    UserRole.VIEWER: 10
}

ROLE_PERMISSIONS: Dict[UserRole, Set[str]] = {
    UserRole.SUPER_ADMIN: {"*"},
    UserRole.ORG_ADMIN: {
        "org:manage", "project:create", "project:delete", "user:invite", "user:remove",
        "doc:read", "doc:write", "doc:delete", "code:read", "incident:write", "sql:execute"
    },
    UserRole.PROJECT_ADMIN: {
        "project:manage", "doc:read", "doc:write", "doc:delete", "code:read",
        "incident:write", "sql:execute", "eval:run"
    },
    UserRole.ENGINEER: {
        "doc:read", "doc:write", "code:read", "code:search", "incident:read",
        "incident:investigate", "sql:execute", "chat:write"
    },
    UserRole.ANALYST: {
        "doc:read", "incident:read", "sql:execute", "chat:write", "eval:read"
    },
    UserRole.VIEWER: {
        "doc:read", "code:read", "incident:read", "chat:write"
    }
}

def check_permission(user_role: UserRole, required_permission: str) -> bool:
    if user_role == UserRole.SUPER_ADMIN:
        return True
    user_perms = ROLE_PERMISSIONS.get(user_role, set())
    return required_permission in user_perms or "*" in user_perms

def require_role_level(user_role: UserRole, minimum_role: UserRole):
    user_weight = ROLE_HIERARCHY.get(user_role, 0)
    required_weight = ROLE_HIERARCHY.get(minimum_role, 100)
    if user_weight < required_weight:
        raise AuthorizationError(f"Requires minimum role of {minimum_role.value}, user is {user_role.value}")
