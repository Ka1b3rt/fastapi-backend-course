from fastapi import FastAPI, HTTPException, Path, Body # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Optional
import json
from pathlib import Path as PathLib

app = FastAPI()

# Pydantic модель для задачи
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Класс для работы с файлом хранения задач
class TaskFileManager:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = PathLib(file_path)
        # Создаем файл, если он не существует
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def load_tasks(self) -> List[dict]:
        """Загружает задачи из файла."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def save_tasks(self, tasks: List[dict]) -> None:
        """Сохраняет задачи в файл."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)

# Инициализация менеджера файлов
task_file_manager = TaskFileManager()

# GET /tasks - Получить все задачи
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    tasks = task_file_manager.load_tasks()
    return tasks

# POST /tasks - Создать новую задачу
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks = task_file_manager.load_tasks()
    # Проверяем, существует ли задача с таким же ID
    if any(t["id"] == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task.dict())
    task_file_manager.save_tasks(tasks)
    return task

# PUT /tasks/{task_id} - Обновить существующую задачу
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int = Path(..., description="ID задачи для обновления"),
    updated_task: Task = Body(..., description="Новые данные задачи"),
):
    # Проверяем, что ID в пути совпадает с ID в теле запроса
    if updated_task.id != task_id:
        raise HTTPException(
            status_code=400,
            detail=f"Task ID in path ({task_id}) does not match ID in body ({updated_task.id})",
        )

    tasks = task_file_manager.load_tasks()
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[index] = updated_task.dict()
            task_file_manager.save_tasks(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE /tasks/{task_id} - Удалить задачу
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int = Path(..., description="ID задачи для удаления")):
    tasks = task_file_manager.load_tasks()
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            task_file_manager.save_tasks(tasks)
            return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")