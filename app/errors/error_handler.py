from fastapi import HTTPException, Request, Response
from fastapi import status
from pymongo.errors import DuplicateKeyError

from app.errors import messages
from app.errors.exceptions import UserExistsError, UserNotFoundError, InsufficientFundsError

from typing import Callable
from fastapi.routing import APIRoute
import logging

logger = logging.getLogger("app")


class ErrorHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except UserExistsError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
            except UserNotFoundError as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
            except InsufficientFundsError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
            except DuplicateKeyError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_EXISTS)
            # except Exception as err:
            #     logger.exception(err)
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")

        return custom_route_handler
