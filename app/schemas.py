from pydantic import BaseModel, Field


class BalanceTransferRequest(BaseModel):
    sender_id: int
    recipient_id: int
    amount: float = Field(gt=0)


class BalanceAddRequest(BaseModel):
    user_id: int
    amount: float = Field(gt=0)


class BalanceWithdrawRequest(BaseModel):
    user_id: int
    amount: float = Field(gt=0)


class CreateUserRequest(BaseModel):
    user_id: int
    balance: float


class UserResponse(BaseModel):
    user_id: int
    balance: float


class BalanceTransferResponse(BaseModel):
    sender: UserResponse
    recipient: UserResponse
