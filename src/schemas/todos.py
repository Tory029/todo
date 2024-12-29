from pydantic import BaseModel
import enum

class TodoStatus(enum.Enum):
       todo = "todo"
       in_progress = "in_progress"
       done = "done"


class TodoSchema(BaseModel):
    name: str
    description: str


    class Config:
        from_attributes = True


class TodoUpdate(TodoSchema):
    id: int
    status: TodoStatus


class TodoRead(BaseModel):
    id: int
