from fastapi import FastAPI # type: ignore

app = FastAPI()
tasks = []




@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task_id: int, title: str, status: bool):
    task = {
        "task_id": task_id,
        "title": title,
        "status": status
    }
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str, status: bool):
    for task in tasks:
        if task['task_id'] == task_id:
            task['title'] = title
            task['status'] = status
            return task
    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task['task_id'] == task_id:
            tasks.remove(task)
            return task
