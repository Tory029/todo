from pydantic import BaseModel
from typing import List
import enum

class TodoStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TodoRead(BaseModel):
    id: int

class TodoCreate(BaseModel):
    name: str
    descriptioon: str
    status: str

class TodoResponse(TodoCreate):
    id: int

class TodoListCreate(BaseModel):
    name: str
    description: str

class TodoListResponse(TodoListCreate):
    id: int
    todos: List[TodoResponse] = []