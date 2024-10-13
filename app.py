from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
from pydantic_schemas import TaskCreate, TaskResponse, TaskUpdate, BulkTasks

app = FastAPI()

# Create DB tables
models.Base.metadata.create_all(bind=engine)

@app.post("/v1/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title, is_completed=task.is_completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/v1/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.get("/v1/tasks/{id}", response_model=TaskResponse)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/v1/tasks/{id}", status_code=204)
def update_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.title is not None:
        db_task.title = task.title
    if task.is_completed is not None:
        db_task.is_completed = task.is_completed
    db.commit()
    return

@app.delete("/v1/tasks/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return

# Extra Credit: Bulk Add Tasks
@app.post("/v1/tasks/bulk", status_code=201)
def bulk_add_tasks(bulk: BulkTasks, db: Session = Depends(get_db)):
    tasks = [models.Task(title=task.title, is_completed=task.is_completed) for task in bulk.tasks]
    db.bulk_save_objects(tasks)
    db.commit()
    return {"tasks": [{"id": task.id} for task in tasks]}

# Extra Credit: Bulk Delete Tasks
@app.delete("/v1/tasks/bulk", status_code=204)
def bulk_delete_tasks(ids: list[int], db: Session = Depends(get_db)):
    db.query(models.Task).filter(models.Task.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return
