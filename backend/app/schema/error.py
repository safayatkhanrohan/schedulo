from pydantic import BaseModel
from typing import Optional, List


class ErrorDetail(BaseModel):
    code: str
    message: str
    target: Optional[str] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: List[ErrorDetail] = []
