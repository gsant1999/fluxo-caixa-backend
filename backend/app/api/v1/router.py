from fastapi import APIRouter
from app.api.v1 import auth, sales

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])

