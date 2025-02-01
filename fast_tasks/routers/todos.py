from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pytest import Session
from sqlalchemy import select

from fast_tasks.database import get_session
from fast_tasks.models import Todo, User
from fast_tasks.schemas import Message, TodoList, TodoPublic, TodoSchema, FilterTodo, TodoUpdate
from fast_tasks.security import get_current_user


router = APIRouter(prefix='/todos', tags=['todos'])
T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: CurrentUser, session: T_Session):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(session: T_Session, user: CurrentUser, todo_filter: Annotated[FilterTodo, Query()]):
    query = select(Todo).where(Todo.user_id == user.id)
    
    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))
    
    if todo_filter.description:
        query = query.filter(Todo.description.contains(todo_filter.description))
    
    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)
    
    todos = session.scalars(query.offset(todo_filter.offset).limit(todo_filter.limit)).all()
    
    return {'todos': todos}



@router.patch('/{todo_id}', response_model=TodoPublic)
def path_todo(todo_id: int, session: T_Session, user: CurrentUser, todo: TodoUpdate):
    db_todo = session.scalar(select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id))
    
    if not db_todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')
    
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    return db_todo    


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}