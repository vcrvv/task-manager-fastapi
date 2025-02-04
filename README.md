# Task Manager API com FastAPI [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Uma API moderna para gerenciamento de tarefas com autenticação JWT, construída em FastAPI e PostgreSQL.

## Funcionalidades
- Autenticação JWT com OAuth2
- CRUD completo de tarefas e usuários
- Dockerização completa (API + PostgreSQL)
- Documentação interativa via Swagger/Redoc
- Testes automatizados com pytest

## Tecnologias
- **Linguagem** Python
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL + SQLAlchemy ORM
- **Autenticação:** JWT + OAuth2PasswordBeare
- **Testes:** pytest + HTTPX
- **Infra:** Docker Compose
- **Validação:** Pydantic v2


## Instalação
```bash
# Clone o repositório
git clone https://github.com/vcrvv/task-manager-fastapi.git
cd task-manager-fastapi
```

## Variáveis de Ambiente
- Crie um arquivo `.env` na raiz do projeto:
```.env
DATABASE_URL=postgresql://postgres:postgres@db:5432/taskdb
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Inicialização com Docker
```bash
# Cria e inicia os containers
docker-compose up --build
```

## Inicialização com Poetry
```bash
# Instale as dependências
poetry install

# Altere a variável de ambiente "DATABASE_URL" no arquivo ".env" para o uso do SQLite
DATABASE_URL="sqlite:///./database.db"

# Ative o ambiente virtual
poetry shell

# Execute as migrações do banco de dados
alembic upgrade head

# Inicie o servidor de desenvolvimento
task run
```

## Testes com pytest
```bash
# Ative o ambiente virtual (se não estiver ativo)
poetry shell

# Comando para iniciar os testes
task test
```

## Endpoints da API

### Autenticação
- `POST /auth/token` - Obter token de acesso
- `POST /auth/refresh_token` - Atualizar token de acesso

### Usuários
- `POST /users/` - Criar novo usuário
- `GET /users/` - Listar usuários (paginado)
- `GET /users/{user_id}` - Obter detalhes do usuário
- `PUT /users/{user_id}` - Atualizar usuário
- `DELETE /users/{user_id}` - Excluir usuário

### Tarefas
- `POST /todos/` - Criar nova tarefa
- `GET /todos/` - Listar tarefas (com filtro)
- `PATCH /todos/{todo_id}` - Atualizar tarefa
- `DELETE /todos/{todo_id}` - Excluir tarefa

## Documentação da API
Acesse a documentação interativa após iniciar o servidor:
 - Swagger UI: http://localhost:8000/docs
 - Redoc: http://localhost:8000/redoc


