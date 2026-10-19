
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database import get_connection, initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


class Task(BaseModel):
    title: str
    completed: bool = False


@app.get("/")
def home():
    return {"message": "My Task Manager API is running!"}


# READ: Get all tasks
@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    rows = connection.execute("SELECT * FROM tasks").fetchall()
    connection.close()

    return [dict(row) | {"completed": bool(row["completed"])} for row in rows]


# CREATE: Add a task
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (task.title, int(task.completed))
    )

    task_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "completed": task.completed
    }


# UPDATE: Modify a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    connection = get_connection()

    cursor = connection.execute(
        "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
        (updated_task.title, int(updated_task.completed), task_id)
    )

    connection.commit()
    changed = cursor.rowcount
    connection.close()

    if changed == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": task_id,
        "title": updated_task.title,
        "completed": updated_task.completed
    }


# DELETE: Remove a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    changed = cursor.rowcount
    connection.close()

    if changed == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}

app.mount("/app", StaticFiles(directory="static", html=True), name="static")