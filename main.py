import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Todo, TodoStatus
from db import init_db, session_local

app = FastAPI()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos/")
async def create_todo(name: str, description: str, db: Session = Depends(get_db)):
    todo = Todo(name=name, description=description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.get("/todos/")
def read_list_todo(db: Session = Depends(get_db)):
    todo = db.query(Todo).all()
    return todo

@app.get("todos/{todos_id}")
def read_todo(todos_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todos_id).first()
    if todo is None:
        raise
    HTTPException(status_code=404, detail="No todo were found")
    return todo


@app.put("/todos/{todos_id}")
def update_todo(todo_id: int, name: str, description: str, status: TodoStatus, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise
    HTTPException(detail="No todos were found")

    todo.name = name
    todo.description = description
    todo.status = status
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todos_id}")
def delete_todo(todo_id = int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise
    HTTPException(detail="No todos were found")

    db.delete(todo)
    db.commit()
    return {"todo": "deleted"}

if __name__ == '__main__':
    init_db(),
    uvicorn.run(
        "main:app", 
        reload=True,
        host="localhost",
        port=5433
    )