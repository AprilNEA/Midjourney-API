from pydantic import BaseModel
from fastapi import status, Request, HTTPException
from app.schema import ResponseCode


class HTTPExceptionDetail(BaseModel):
    internal_code: ResponseCode
    msg: str


def http_exception(code, msg):
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail=HTTPExceptionDetail(internal_code=code, msg=msg),
    )


def get_setting(request: Request) -> int:
    return request.state.setting
