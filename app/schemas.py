from pydantic import BaseModel


class BalanceTransferRequest(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: float


class BalanceAddRequest(BaseModel):
    user_id: int
    amount: float


class BalanceWithdrawRequest(BaseModel):
    user_id: int
    amount: float


class CreateUserRequest(BaseModel):
    user_id: int
    balance: float


class UserResponse(BaseModel):
    user_id: int
    balance: float


class BalanceTransferResponse(BaseModel):
    sender: UserResponse
    recipient: UserResponse
