from datetime import date, datetime, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

from database import create_task, delete_task, get_task, initialize_database, list_tasks, update_task

app = FastAPI(title="TaskFlow API", version="1.0.0")

# Allow common local development servers to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TaskStatus = Literal["todo", "in-progress", "done"]
TaskPriority = Literal["low", "medium", "high"]


class TaskInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    status: TaskStatus = "todo"
    priority: TaskPriority = "medium"
    due_date: date | None = None

    @validator("title")
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Task title must not be blank")
        return value

    @validator("description")
    def trim_description(cls, value: str) -> str:
        return value.strip()


class Task(TaskInput):
    id: int
    created_at: datetime
    updated_at: datetime


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "TaskFlow API is running", "docs": "/docs"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def add_task(task: TaskInput) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return create_task(
        title=task.title,
        description=task.description,
        task_status=task.status,
        priority=task.priority,
        due_date=task.due_date.isoformat() if task.due_date else None,
        created_at=now,
        updated_at=now,
    )


@app.get("/tasks", response_model=list[Task])
def get_tasks() -> list[dict]:
    return list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_one_task(task_id: int) -> dict:
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def replace_task(task_id: int, task: TaskInput) -> dict:
    if get_task(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated = update_task(
        task_id=task_id,
        title=task.title,
        description=task.description,
        task_status=task.status,
        priority=task.priority,
        due_date=task.due_date.isoformat() if task.due_date else None,
        updated_at=datetime.now(timezone.utc).isoformat(),
    )
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int) -> Response:
    if not delete_task(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
