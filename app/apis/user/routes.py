# from pydantic import BaseModel
# from fastapi import APIRouter, Depends, HTTPException, Request
# from app.services.users_services import UsersServices
#
# router = APIRouter()
#
#
# def get_db(request: Request):
#     return request.app.state.db
#
#
# def get_user_service(db=Depends(get_db)):
#     return UsersServices(db)
#
#
# class CreateUserRequest(BaseModel):
#     user_id: int
#     amount: float
#
#
# @router.post("/users/")
# async def create_user(data: CreateUserRequest):
#     print('ololol')
#     # result = await UsersServices.create_user(data)
#     # return result
#     return {'ok'}
# # @app.get("/users/{user_id}")
# # async def get_user(user_id: str):
# #     user = {"user_id": user_id}
# #     await db.balances.find_one(user)
# #     return {"success"}


from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/users/")
async def create_user(request: Request):
    print('okkee')
    # try:
    #     user_collection = request.app.mongodb["users"]  # Коллекция MongoDB, где хранятся пользователи
    #     user_data = await request.json()
    #     new_user = await user_collection.insert_one(user_data)
    #     created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    #     return JSONResponse(status_code=201, content=created_user)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    return {'okok'}