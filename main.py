# from fastapi import FastAPI
# from motor.motor_asyncio import AsyncIOMotorClient
# from app.apis.user.routes import router as user_router
#
# app = FastAPI()
#
#
# app.include_router(user_router)
#
# db_client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = db_client.user_balance_db
# app.state.db = db


from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.apis.user.routes import router as user_router

app = FastAPI()

app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
# @app.on_event("startup")
# async def startup_db_client():
#     app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
#     app.mongodb = app.mongodb_client['user_database']  # Имя вашей базы данных
#
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     app.mongodb_client.close()


app.include_router(user_router)
