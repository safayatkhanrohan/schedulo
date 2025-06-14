from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    message: Optional[str] = None
    trace_id: Optional[str] = None  # Optional for observability
    documentation_url: Optional[str] = None  # Optional for DX
