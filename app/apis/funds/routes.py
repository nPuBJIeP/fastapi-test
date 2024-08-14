from main import app, db
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


@app.post("/balance/add")
async def add_balance(data: BalanceAddRequest):
    pass


@app.post("/balance/withdraw")
async def add_balance(data: BalanceWithdrawRequest):
    pass


@app.post("/balance/transfer")
async def add_balance(data: BalanceTransferRequest):
    pass
