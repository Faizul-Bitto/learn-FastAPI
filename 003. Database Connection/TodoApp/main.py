from typing import Annotated

from fastapi import FastAPI, Depends, Path, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

# Get all Todos
@app.get("/todos", status_code=status.HTTP_200_OK)
async def read_all_todos(db:db_dependency):
    todos = db.query(Todos).all()

    return todos

# Get Todo by id
@app.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db:db_dependency, id:int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return todo

# Create Todo
@app.post("/todo/create", status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency, todo_request:TodoRequest):
    todo = Todos(**todo_request.model_dump())

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo

# Update Todo
@app.put("/todo/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_request:TodoRequest, id:int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    db.add(todo)
    db.commit()

@app.delete("/todo/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()