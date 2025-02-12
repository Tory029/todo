def update_todo_list_status(db, list_id: int):
    todo_list = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="There are no todo_list")
    todos = db.query(Todo).filter(Todo.id == list_id).all()
    if not todos:
        todo_list.status == "todo"
    else:
        statuses = [todo_list.status for todo in todos]
        if "in_progress" in statuses:
            todo_list.status == "in_progress"
        elif all(status == "done" for status in statuses):
            todo_list.status = "done"
        else:
            todo_list.status = "todo"

            db.commit()