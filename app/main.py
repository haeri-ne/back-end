from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, menus, foods, logs, statistics, votes, scores, comments
from app.database import init_db
from app.config import get_settings
from app.middlewares.logging import LoggingMiddleware

settings = get_settings()
init_db()

app = FastAPI(
    title="My API",
    description="FastAPI Backend for Food & Menu Management",
    version="1.0.0"
)

origins = settings.cors_origin_list

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(menus.router, prefix="/api/v1", tags=["menus"])
app.include_router(foods.router, prefix="/api/v1", tags=["foods"])
app.include_router(logs.router, prefix="/api/v1", tags=["logs"])
app.include_router(statistics.router, prefix="/api/v1", tags=["statistics"])
app.include_router(votes.router, prefix="/api/v1", tags=["votes"])
app.include_router(scores.router, prefix="/api/v1", tags=["scores"])
app.include_router(comments.router, prefix="/api/v1", tags=["comments"])


@app.get("/api/v1/health", tags=["system"])
async def health_check():
    """
    API Health Check 엔드포인트.
    서버가 정상적으로 실행 중인지 확인하기 위해 사용됨.
    """
    return {"status": "OK"}
