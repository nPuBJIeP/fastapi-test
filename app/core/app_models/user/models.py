from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    amount: float

