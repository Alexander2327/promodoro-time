from fastapi import HTTPException, Request
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status


class CustomExceptionModel(BaseModel):
    status_code: int
    detail: str
    message: str | None = None


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str | None = None):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


class NotFoundException(CustomException):
    def __init__(self, detail: str, message: str | None = None):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND, message=message)


class BadRequestException(CustomException):
    def __init__(self, detail: str, message: str | None = None):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, message=message)


class UnauthorizedException(CustomException):
    def __init__(self, detail: str, message: str | None = None):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED, message=message)


async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    error = jsonable_encoder(
        CustomExceptionModel(status_code=exc.status_code, message=exc.message, detail=exc.detail)
    )
    return JSONResponse(status_code=exc.status_code, content=error)