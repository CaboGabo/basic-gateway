from pydantic import BaseModel
from typing import Optional


class QueryBase(BaseModel):
    query: str
    time_to_execute_in_mins: float
    hash: Optional[str] = ""


class QueryCreate(QueryBase):
    pass


class Query(QueryBase):
    id: int

    class Config:
        orm_mode = True
