from fastapi import APIRouter, Depends, HTTPException
from models import TodoList, Todo
from schemas import TodoListCreate, TodoList_, TodoCreate, Todo_, TodoListUpdate
from db import get_db, SessionLocal
from sqlalchemy.orm import Session
from typing import List
#from typing import List


router2 = APIRouter(tags=["todo_list"])


@router2.post("/todo_lists/", response_model=TodoList_)
async def create_todo_list(
    todo_list_create: TodoListCreate, 
    db: SessionLocal = Depends(get_db)
    ):

    db_todo_list = TodoList(id=id, name=todo_list_create.name, descripion=todo_list_create.description, status="todo")
    db.add(db_todo_list)
    db.commit()
    db.refresh(db_todo_list)
    return


@router2.get("todo_lists/", response_model=List[TodoList_])
async def read_todos_lists(db: SessionLocal = Depends(get_db)):
    return db.query(TodoList).all()


@router2.get("todo_lists/{list_id}", response_model=TodoList_)
async def read_todos_list(list_id: int, db: SessionLocal = Depends(get_db)):
    todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if todo_list is None:
        raise HTTPException(status_code=404, detail="No todo_lists were found")
    return todo_list


@router2.put("/todo_list/{list_id}", response_model=TodoList_)
async def update_todos_list(
    list_id: int,
    todo_list_update: TodoListUpdate, 
    db: SessionLocal = Depends(get_db)
    ):
    
    db_todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if db_todo_list is None:
        raise HTTPException(detail="No todos_lists were found")

    db_todo_list.name = todo_list_update.name
    db_todo_list.description = todo_list_update.description

    db.commit()
    db.refresh(db_todo_list)
    return db_todo_list


@router2.delete("todo_list/{list_id}", response_model=dict)
async def delete_todos_list(list_id: int, db: Session = Depends(get_db)):
    db_todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="No todo_lists were found")
    
    db.delete(db_todo_list)
    db.commit()
    return {"message": "todo_list deleted"}


def update_todo_list_status(list_id: int, db: Session):
    todos = db.query(Todo).filter(Todo.todo_list_id == list_id).all()

    if all(todos.status == "done" for todo in todos):
        new_status = "done"
    elif all(todos.status == "todo" for todo in todos):
        new_status = "todo"
    else:
        new_status = "in progress"

    todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    todo_list.status = new_status
    db.commit()


@router2.post("/todo_lists/{list_id}/todos/", response_model=Todo_)
def add_todo_to_list(list_id: int, todo_create: TodoCreate, db: Session = Depends(get_db)):
    todo_create_data = todo_create.model_dump()
    todo_create_data["task_list_id"] = list_id
    new_todo = Todo(name = todo_create.name, description = todo_create.description, status=todo_create.status)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    # Обновляем статус списка задач после добавления новой задачи
    update_todo_list_status(list_id, db)

    return new_todo

