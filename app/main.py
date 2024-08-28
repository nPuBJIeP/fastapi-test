from fastapi import FastAPI, HTTPException, Depends, APIRouter

from app.user import user_router
from app.balance import balance_router

app = FastAPI()

router = APIRouter()

app.include_router(user_router)
app.include_router(balance_router)
