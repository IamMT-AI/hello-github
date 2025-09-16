"""
API Gateway - Main application entry point
Handles incoming requests and routes them to appropriate services.
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 API Gateway starting up...")
    yield
    # Shutdown
    print("📴 API Gateway shutting down...")


app = FastAPI(
    title="AI Cartoon Figurine API Gateway",
    description="MVP Week 1 - API Gateway for AI cartoon figurine generation",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(upload.router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Cartoon Figurine API Gateway - MVP Week 1", "status": "ok"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": time.time(),
        "services": {
            "api_gateway": "running",
            "stylize2d": "external",  # Will be checked via service discovery later
            "fusion": "library",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
