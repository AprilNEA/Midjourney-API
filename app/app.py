from loguru import logger
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import schema
from app.routes import v1_router
from app.database import db_startup

app = FastAPI(title="Midjourney API", description="", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  Initialize database, etc.
@app.on_event("startup")
async def startup():
    logger.info("Initialize database...")
    await db_startup()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """
    截获所有的 HTTPException
    """
    logger.debug(exc)
    try:
        return JSONResponse(
            {
                "success": False,
                "code": int(exc.detail.internal_code.value),
                "msg": str(exc.detail.msg),
            }
        )
    except:
        return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """
    请求中包含无效数据时，FastAPI 内部会触发该 RequestValidationError。
    """
    try:
        return JSONResponse(
            {
                "success": False,
                "code": schema.ResponseCode.ValidationError.value,
                "msg": str(exc),
            }
        )
    except:
        return await request_validation_exception_handler(request, exc)


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "code": schema.ResponseCode.UnknownError.value,
            "msg": "unknown error",
            "data": {
                "request": {
                    "url": str(request.url),
                    "headers": str(request.headers),
                },
                "exception": str(exc),
            },
        },
    )


app.include_router(
    v1_router,
    prefix="/v1",
    tags=["v1"],
)
