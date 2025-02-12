from fastapi import APIRouter, Depends, HTTPException
from models.todos import TodoList, Todo
from schemas.todos import TodoListCreate, TodoListResponse, TodoCreate
from database.db import get_db, SessionLocal
from sqlalchemy.orm import Session
from typing import List


router2 = APIRouter(tags=["todo_list"])


@router2.post("/todos_lists/", response_model=TodoListResponse)
def create_todo(todo_list: TodoListCreate, status: str, db: SessionLocal = Depends(get_db)):
    todo = TodoList(name=todo_list.name, description=todo_list.description, status=status)
    db.add(todo)
    db.refresh(todo)
    db.commit()

@router2.get("todos_lists/", response_model=List[TodoListResponse])
def get_todos_list(db: SessionLocal = Depends(get_db)):
    return db.query(TodoList).all()

@router2.delete("todos_list/{list_id}", response_model=dict)
def delete_todos_list(list_id: int, db: Session = Depends(get_db)):
    db_todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not db_todo_list:
        raise HTTPException(status_code=404, detail="No todo were found")
    
    db.delete(db_todo_list)
    db.commit()

