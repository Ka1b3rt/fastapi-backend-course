from fastapi import FastAPI # type: ignore
import json

app = FastAPI()

@app.get("/tasks")
def get_tasks():
    with open('tasks.json', 'r', encoding = 'utf-8') as f:
            tasks = json.load(f)
    return tasks

@app.post("/tasks")
def create_task(task_id: int, title: str, status: bool):
    with open('tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    task = {
        "task_id": task_id,
        "title": title,
        "status": status
        }
    tasks["Tasks"].append(task)
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f)
    return task



@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str, status: bool):
    with open('tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)    
    for task in tasks['Tasks']:
        if task['task_id'] == (task_id):
            task['title'] = title
            task['status'] = status
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f)
    return task
    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with open('tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)    
    for task in tasks['Tasks']:
        if task['task_id'] == task_id:
            tasks['Tasks'].remove(task)
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f)
    return task
