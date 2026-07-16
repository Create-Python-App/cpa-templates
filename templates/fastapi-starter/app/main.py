"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import router as v1_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
)

if settings.cors_origin_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(v1_router, prefix=settings.api_prefix)


@app.get("/ping", tags=["infra"], include_in_schema=False)
async def ping() -> JSONResponse:
    """Minimal health probe for load balancers."""
    return JSONResponse({"status": "ok"})


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint with navigation hints."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "docs": "/docs",
        "health": f"{settings.api_prefix}/healthz",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
