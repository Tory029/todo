from fastapi import APIRouter, Depends, HTTPException
from schemas.todos import TodoSchema, TodoUpdate, TodoRead
from sqlalchemy.orm import Session
from models.todos import Todo
from database.db import get_db


router = APIRouter()

@router.post("/todos/")
async def create_todo(todo_schema: TodoSchema, db: Session = Depends(get_db)):
    todo = Todo(name=todo_schema.name, description=todo_schema.description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get("/todos/")
def read_list_todo(db: Session = Depends(get_db)):
    todo = db.query(Todo).all()
    return todo

@router.get("todos/{todos_id}")
def read_todo(todo_schema: TodoRead, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == TodoSchema.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="No todo were found")
    return todo


@router.put("/todos/{todos_id}")
def update_todo(todo_schema: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == TodoSchema.id).first()
    if todo is None:
        raise HTTPException(detail="No todos were found")

    todo.name = todo_schema.name
    todo.description = todo_schema.description
    todo.status = todo_schema.status
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/todos/{todos_id}")
def delete_todo(todo_schema: TodoRead, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_schema.id).first()
    if todo is None:
        raise HTTPException(detail="No todos were found")

    db.delete(todo)
    db.commit()
    return {"todo": "deleted"}