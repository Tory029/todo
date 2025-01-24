from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.todos import TodoResponse, TodoRead, TodoListResponse, TodoCreate, TodoListCreate
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.todos import Todo, TodoList
from database.db import get_db, SessionLocal
from typing import Optional


router = APIRouter(tags=["todo"])

@router.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: SessionLocal = Depends(get_db)):
    todo = Todo(name = TodoCreate.name, description = TodoCreate.descriptioon)
    db.add(todo)
    db.refresh(todo)
    db.commit()

@router.get("/todos/")
def read_list_todo(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):

    query = select(Todo)
    while status:
        query = query.where(TodoList.status == status)

    total_todos = db.execute(query).scalars().count()
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

@router.get("todos/{todo_id}")
def read_todo(todo_id: int, db: SessionLocal = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="No todo were found")
    return todo


@router.put("/todos/{todo_id}")
def update_todo(todo_schema: TodoResponse, db: SessionLocal = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == TodoResponse.id).first()
    if todo is None:
        raise HTTPException(detail="No todos were found")

    todo.name = todo_schema.name
    todo.description = todo_schema.description
    todo.status = todo_schema.status
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int, 
    db: SessionLocal = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(detail="No todos were found")

    db.delete(todo)
    db.commit()
    return {"todo": "deleted"}