from pydantic import BaseModel
from typing import Optional, List
import enum

class TodoStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TodoBase(BaseModel):
    name: str
    description: str
    status: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  

class Todo_(TodoBase):
    id: int

    class Config:
        orm_mode = True

class TodoListBase(BaseModel):
    name: str
    description: str

class TodoListCreate(TodoListBase):
    pass

class TodoListUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TodoList_(TodoListBase):
    id: int
    status: str
    todos: List[Todo_] = []

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    password: str
    todos: dict
