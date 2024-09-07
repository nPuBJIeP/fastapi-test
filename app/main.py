from fastapi import FastAPI, APIRouter

from app.handlers.user_handlers import user_router
from app.handlers.balance_handlers import balance_router

app = FastAPI()


router = APIRouter()

app.include_router(user_router)
app.include_router(balance_router)
