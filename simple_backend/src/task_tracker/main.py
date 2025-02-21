from fastapi import FastAPI, HTTPException, Path, Body # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Optional
import requests # type: ignore

app = FastAPI()

# Конфигурация MockAPI
MOCKAPI_BASE_URL = "https://67b85410699a8a7baef39d0f.mockapi.io/api/v1/tasks/Tasks"  # Замените на ваш URL

# Pydantic модель для задачи
class Task(BaseModel):
    id: Optional[int] = None  # ID может быть None, так как MockAPI генерирует его автоматически
    title: str
    description: Optional[str] = None
    completed: bool = False

# Вспомогательные функции для работы с MockAPI
def fetch_tasks() -> List[dict]:
    """Получить все задачи из MockAPI."""
    response = requests.get(MOCKAPI_BASE_URL)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=500, detail="Failed to fetch tasks from MockAPI")

def fetch_task(task_id: int) -> Optional[dict]:
    """Получить задачу по ID из MockAPI."""
    response = requests.get(f"{MOCKAPI_BASE_URL}/{task_id}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    raise HTTPException(status_code=500, detail="Failed to fetch task from MockAPI")

def create_task_in_mockapi(task: Task) -> dict:
    """Создать задачу в MockAPI."""
    response = requests.post(MOCKAPI_BASE_URL, json=task.dict())
    if response.status_code == 201:
        return response.json()
    raise HTTPException(status_code=500, detail="Failed to create task in MockAPI")

def update_task_in_mockapi(task_id: int, updated_task: Task) -> dict:
    """Обновить задачу в MockAPI."""
    response = requests.put(f"{MOCKAPI_BASE_URL}/{task_id}", json=updated_task.dict())
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Task not found in MockAPI")
    raise HTTPException(status_code=500, detail="Failed to update task in MockAPI")

def delete_task_in_mockapi(task_id: int) -> dict:
    """Удалить задачу в MockAPI."""
    response = requests.delete(f"{MOCKAPI_BASE_URL}/{task_id}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Task not found in MockAPI")
    raise HTTPException(status_code=500, detail="Failed to delete task in MockAPI")

# Эндпоинты FastAPI

# GET /tasks - Получить все задачи
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return fetch_tasks()

# POST /tasks - Создать новую задачу
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    return create_task_in_mockapi(task)

# PUT /tasks/{task_id} - Обновить существующую задачу
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int = Path(..., description="ID задачи для обновления"),
    updated_task: Task = Body(..., description="Новые данные задачи"),
):
    # Проверяем, что задача существует
    if not fetch_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task_in_mockapi(task_id, updated_task)

# DELETE /tasks/{task_id} - Удалить задачу
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int = Path(..., description="ID задачи для удаления")):
    # Проверяем, что задача существует
    if not fetch_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return delete_task_in_mockapi(task_id)