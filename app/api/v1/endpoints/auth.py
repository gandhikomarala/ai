from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.security.passwords import verify_password, get_password_hash
from app.security.jwt import create_access_token, create_refresh_token
from app.core.responses import success_response

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    organization_name: str

@router.post("/login")
async def login(req: LoginRequest):
    # Simulated auth check
    if req.email and len(req.password) >= 6:
        token = create_access_token(subject=req.email, claims={"role": "ENGINEER", "org": "NovaStack"})
        refresh = create_refresh_token(subject=req.email)
        return success_response({
            "access_token": token,
            "refresh_token": refresh,
            "token_type": "bearer",
            "user": {
                "email": req.email,
                "full_name": "Demo Engineer",
                "role": "ENGINEER",
                "organization": "NovaStack Technologies"
            }
        })
    raise HTTPException(status_code=401, detail="Invalid email or password")

@router.post("/register")
async def register(req: RegisterRequest):
    token = create_access_token(subject=req.email, claims={"role": "ORG_ADMIN", "org": req.organization_name})
    return success_response({
        "access_token": token,
        "user": {
            "email": req.email,
            "full_name": req.full_name,
            "role": "ORG_ADMIN",
            "organization": req.organization_name
        }
    })
