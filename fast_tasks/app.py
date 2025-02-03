from http import HTTPStatus

from fastapi import FastAPI

from .schemas import Message
from .routers import auth, users, todos

app = FastAPI()

app.include_router(todos.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Projeto de gerenciamento de tarefas com FastAPI'}

