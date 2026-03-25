"""
EducaTYCs API - Educational opportunities for Yucatán.

A service-learning project that aggregates educational opportunities
(courses, workshops, scholarships) relevant to Yucatán, Mexico.
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import init_db
from app.routers import opportunities_router
from app.scheduler import start_scheduler, stop_scheduler
from app.config import get_settings


settings = get_settings()
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("educatycs.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and scheduler on startup."""
    # Startup
    init_db()
    logger.info("Database initialized")

    if settings.scheduler_interval_hours > 0:
        start_scheduler(interval_hours=settings.scheduler_interval_hours)
        logger.info(
            "Scheduler started with %s-hour interval",
            settings.scheduler_interval_hours,
        )

    yield

    # Shutdown
    stop_scheduler()
    logger.info("Scheduler stopped")


app = FastAPI(
    title="EducaTYCs API",
    description="API para oportunidades educativas en Yucatán",
    version="0.4.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rate limiting storage
request_counts: dict[str, tuple[int, int]] = {}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Sliding-window rate limiting middleware with stale-key cleanup."""
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)

    # In-memory rate limiting (for production use Redis or similar)
    client_ip = request.client.host if request.client else "unknown"
    now = int(time.time())
    window = settings.rate_limit_window_seconds

    # Prune expired counters to avoid unbounded memory growth.
    expired_ips = [
        ip for ip, (_, started_at) in request_counts.items() if now - started_at >= window
    ]
    for ip in expired_ips:
        request_counts.pop(ip, None)

    count, started_at = request_counts.get(client_ip, (0, now))
    if now - started_at >= window:
        count = 0
        started_at = now

    if count >= settings.rate_limit_per_minute:
        logger.warning(
            "Rate limit exceeded ip=%s path=%s limit=%s window_seconds=%s",
            client_ip,
            request.url.path,
            settings.rate_limit_per_minute,
            window,
        )
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."},
        )

    request_counts[client_ip] = (count + 1, started_at)
    response = await call_next(request)
    return response


# Include    response routers
app.include_router(opportunities_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Return a stable 500 response and log full exception context."""
    logger.exception("Unhandled error path=%s method=%s", request.url.path, request.method)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.4.0"}
