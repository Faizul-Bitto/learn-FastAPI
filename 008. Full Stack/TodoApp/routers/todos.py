from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request,Cookie
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from .auth import get_current_user, verify_token_for_cookies
from ..database import SessionLocal
from ..models import Todos
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/todos", tags=["todos"])


# Database Integration
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
templates = Jinja2Templates(directory="TodoApp/templates")


# Request Field Validation
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


### Pages ###
def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


@router.get("/todo-page")
async def render_todo_page(
        request: Request,
        db: db_dependency,
):

        access_token = request.cookies.get('access_token')

        if not access_token:
            return redirect_to_login()

        user = verify_token_for_cookies(access_token)

        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()

        return templates.TemplateResponse(
            request=request,
            name="todo.html",
            context={
                "request": request,
                "todos": todos,
                "user": user
            }
        )


@router.get("/add-todo-page")
async def render_todo_page(
        request: Request
):
        access_token = request.cookies.get('access_token')

        if not access_token:
            return redirect_to_login()

        user = verify_token_for_cookies(access_token)

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(
            request=request,
            name="add-todo.html",
            context={
                "request": request,
                "user": user
            }
        )


@router.get("/edit-todo-page/{todo_id}")
async def render_todo_page(request: Request, todo_id: int, db: db_dependency):
        access_token = request.cookies.get('access_token')

        if not access_token:
            return redirect_to_login()

        user = verify_token_for_cookies(access_token)

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse(
            request=request,
            name="edit-todo.html",
            context={
                "request": request,
                "todo": todo,
                "user": user
            }
        )

# Get all Todos
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    todos = db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()

    return todos


# Get Todo by id
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return todo


# Create Todo
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, create_todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    todo = Todos(**create_todo_request.model_dump(), owner_id=user.get("user_id"))

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


# Update Todo
@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    update_todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    todo.title = update_todo_request.title
    todo.description = update_todo_request.description
    todo.priority = update_todo_request.priority
    todo.complete = update_todo_request.complete

    db.add(todo)
    db.commit()


# Delete Todo
@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("user_id")
    ).delete()

    db.commit()
