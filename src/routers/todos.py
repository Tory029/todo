from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.todos import TodoSchema, TodoUpdate, TodoRead
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.todos import Todo
from database.db import get_db
from typing import Optional


router = APIRouter()


@router.post("/todos/")
async def create_todo(
    todo_schema: TodoSchema, 
    db: Session = Depends(get_db)
):

    todo = Todo(name=todo_schema.name, description=todo_schema.description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get("/todos/", response_model=dict)
def read_list_todo(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = select(Todo)
    while status:
        query = query.where(Todo.status == status)

    total_todos = db.execute(query).scalars().all()
    total_pages = (total_todos + page_size-1) // page_size

    start = (page -1) * page_size
    paginated_todos = db.execute(query.offset(start).limit(page_size)).scalars().all()
    
    return {
        "page": page,
        "page_size": page_size,
        "total_tasks": total_todos,
        "total_pages": total_pages,
        "tasks": paginated_todos,
    }


@router.get("todos/{todos_id}")
def read_todo(
    todo_schema: TodoRead, 
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == TodoSchema.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="No todo were found")
    return todo


@router.put("/todos/{todos_id}")
def update_todo(
    todo_schema: TodoUpdate, 
    db: Session = Depends(get_db)
):
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
def delete_todo(
    todo_schema: TodoRead, 
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_schema.id).first()
    if todo is None:
        raise HTTPException(detail="No todos were found")

    db.delete(todo)
    db.commit()
    return {"todo": "deleted"}