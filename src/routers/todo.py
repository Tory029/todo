from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import Todo_, TodoBase, TodoCreate, TodoUpdate
from sqlalchemy.orm import Session
from models import Todo, TodoList
from db import get_db, SessionLocal
#from routers.service import update_todo_list_status
from typing import Optional, List


router = APIRouter(tags=["todo"])


@router.post("/todos/", response_model=Todo_)
async def create_todo(
    todo: TodoCreate,

    db: SessionLocal = Depends(get_db)
    ):
    
    db_todo = Todo(name = todo.name, description = todo.description, status=todo.status)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/todos/", response_model=List[Todo_])
async def read_todo(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    ):

    query = db.query(Todo)

    while status:
        query = query.filter(TodoList.status == status)

    total_todos = db.execute(query).scalars()
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

@router.get("/todos/{todo_id}", response_model=Todo_)
async def get_todo(todo_id: int, db: SessionLocal = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="No todo were found")
    return todo


@router.put("/todos/{todo_id}", response_model=Todo_)
async def update_todo(
    todo_id: int,
    todo: TodoUpdate, 
    db: SessionLocal = Depends(get_db)
    ):
    
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(detail="No todos were found")

    todo.name = todo.name
    todo.description = todo.description
    todo.status = todo.status

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: int, 
    db: SessionLocal = Depends(get_db)
    ):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(detail="No todos were found")

    db.delete(todo)
    db.commit()
    return {"todo": "deleted"}
