import enum
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column, Enum, DateTime
from schemas.todos import TodoUpdate, TodoStatus

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String)
    status = Column(Enum(TodoStatus), default=TodoStatus.todo)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def to_read_model(self) -> TodoUpdate:
          return TodoUpdate(
                id=self.id,
                name=self.name,
                description=self.description,
                status=self.status,
                #created_at=self.created_at,
                #closed_at=self.updated_at,
          )