from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, String, Column, Enum, DateTime, ForeignKey
from src.schemas import TodoStatus


Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TodoStatus), default=TodoStatus.todo)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    todo_list_id = Column(Integer, ForeignKey("todo_lists.id"))


class TodoList(Base):
    __tablename__ = "todo_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default=TodoStatus.todo)

    todos = relationship("Todo", backref="todo_list", cascade="all, delete-orphan")
