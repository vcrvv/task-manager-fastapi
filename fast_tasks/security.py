from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, PyJWTError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_tasks.database import get_session
from fast_tasks.models import User
from fast_tasks.schemas import TokenData
from fast_tasks.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(data: dict):
    # Copia os dados
    to_encode = data.copy()
    
    # Adiciona 30 minutos para expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    # Atualiza o dicionario com o tempo de expiração
    to_encode.update({'exp': expire})
    
    # Gera e retorna codigo JWT
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt



def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    # exceção HTTP que sera lançado sempre que houver problema com as credenciais
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # Decodifica o token usando a chave secreta e o algoritmo especifico
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Extrai valor do campo 'sub'
        username = payload.get('sub')
        
        # Se nao houver, levanta a exceção
        if not username:
            raise credentials_exception
        
        # Cria objeto com o username
        token_data = TokenData(username=username)
        
    except ExpiredSignatureError:
        raise credentials_exception
    except PyJWTError:
        raise credentials_exception
       

    # Busca no banco o usuario correspondente
    user = session.scalar(select(User).where(User.email == token_data.username))

    if not user:
        raise credentials_exception

    return user