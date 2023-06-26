"""
Route guard authentication
"""
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schema import ResponseCode
from utils.fastapi import HTTPExceptionDetail
from config import Config


def get_header(request: Request, key: str):
    value = request.headers.get(key)
    if not value:
        raise HTTPException(
            status_code=406,
            detail=HTTPExceptionDetail(
                internal_code=ResponseCode.ValidationError,
                msg=f"missing setting {key}",
            ),
        )
    return value


class SecretBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(SecretBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            SecretBearer, self
        ).__call__(request)

        if not Config.secret:
            return

        if (
            not credentials  # no auth
            or not credentials.scheme == "Bearer"  # wrong format
            or credentials.credentials != Config.secret  # auth failed
        ):
            request.state.auth_status = False
            if not Config.public:
                raise HTTPException(
                    status_code=403,
                    detail=HTTPExceptionDetail(
                        internal_code=ResponseCode.AuthenticationError,
                        msg="invalid authentication scheme",
                    ),
                )
            else:
                request.state.setting = {
                    "user_token": get_header(request, "user_token"),
                    "guild_id": get_header(request, "guild_id"),
                    "channel_id": get_header(request, "channel_id"),
                }
        request.state.auth_status = True
        request.state.setting = None
        return credentials.credentials
