from datetime import datetime
from pydantic import BaseModel


class TodoSchema(BaseModel):
    name: str
    description: str
    created_at: datetime.now
    closed_at: datetime.now

    class Config:
        from_attributes = True


class TodoRead(BaseModel):
    id: int


class TodoUpdate(TodoSchema):
    id: int
    status: any