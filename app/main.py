import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import menus, foods
from app.database import init_db

load_dotenv()

init_db()


app = FastAPI(
    title="My API",
    description="FastAPI Backend for Food & Menu Management",
    version="1.0.0"
)

origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menus.router, prefix="/api/v1", tags=["menus"])
app.include_router(foods.router, prefix="/api/v1", tags=["foods"])


@app.get("/api/v1/health", tags=["system"])
async def health_check():
    """
    API Health Check 엔드포인트.
    서버가 정상적으로 실행 중인지 확인하기 위해 사용됨.
    """
    return {"status": "OK"}