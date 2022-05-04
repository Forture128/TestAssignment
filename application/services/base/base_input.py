from typing import Optional

from pydantic.main import BaseModel


class Sort(BaseModel):
    field: str
    desc: Optional[bool] = False


class PaginatedPage(BaseModel):
    page: Optional[int] = 0
    size: Optional[int] = None
