from motor.motor_asyncio import AsyncIOMotorClient


def get_mongodb_client():
    db_client = AsyncIOMotorClient("mongodb://localhost:27017")
    # db_client = AsyncIOMotorClient("mongodb://npubjiep:27017,npubjiep:27018,npubjiep:27019?replicaSet=rs")
    try:
        yield db_client
    finally:
        db_client.close()


