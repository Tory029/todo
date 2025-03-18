from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, String, Column, Enum, DateTime, ForeignKey
from schemas.todos import TodoStatus

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String)
    status = Column(Enum(TodoStatus), default=TodoStatus.todo)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    todos = relationship("TodoList", back_populates="todo_list")

class TodoList(Base):
    __tablename__ = "todo_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String)
    status = Column(String)
    list_id = Column(Integer, ForeignKey("todo_lists.id"))

    todo_list = relationship("Todo", back_populates="todos")