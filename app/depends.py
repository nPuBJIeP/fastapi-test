from motor.motor_asyncio import AsyncIOMotorClient


def get_mongodb_client():
    db_client = AsyncIOMotorClient("mongodb://localhost:27017")
    try:
        yield db_client
    finally:
        db_client.close()


