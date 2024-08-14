from pydantic import BaseModel, Field


class Transfer(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: float


class AddFunds(BaseModel):
    user_id: int
    amount: float


class WithdrawFunds(BaseModel):
    user_id: int
    amount: float
