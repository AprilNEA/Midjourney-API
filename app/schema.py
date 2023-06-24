from enum import IntEnum
from typing import Optional

from pydantic import BaseModel


class ResponseCode(IntEnum):
    Success = 20000

    # Authentication
    AuthenticationError = 40301

    # Request Data Error
    NotFound = 40400
    TriggerNotFound = 40401

    ValidationError = 40601

    # Server Error
    Failed = 50000
    UnknownError = 5001


class ImageGeneration(BaseModel):
    prompt: str
    picurl: Optional[str]


class ImageGenerationResponse(BaseModel):
    message: str = "success"
    trigger_id: str
    trigger_type: str = ""
