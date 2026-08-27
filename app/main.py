from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.middleware import RequestContextMiddleware
from app.api.v1.router import api_router
from app.observability.metrics import get_metrics_output

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("=== AegisAI Platform Server Initializing ===")
    yield
    logger.info("=== AegisAI Platform Server Shutting Down ===")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AegisAI — Enterprise AI Knowledge & Incident Copilot",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/metrics", tags=["Observability"])
async def metrics():
    data, content_type = get_metrics_output()
    return Response(content=data, media_type=content_type)

@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "ONLINE",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)
