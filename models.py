from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column, Enum
import enum


Base = declarative_base()

class TodoStatus(enum.Enum):
       todo = "todo"
       in_progress = "in_progress"
       done = "done"


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String)
    status = Column(Enum(TodoStatus), default=TodoStatus.todo)
