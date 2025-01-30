from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from pwdlib import PasswordHash
from jwt import DecodeError, decode, encode

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_tasks.database import get_session
from fast_tasks.models import User
from fast_tasks.schemas import TokenData


SECRET_KEY = 'secret'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_context.hash(password)  

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )
    
    # payload / adiciona tempo de expiração ao token
    to_encode.update({'exp': expire}) 
    
    # codifica em token JWT e retorna o token
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    
    # exceção HTTP que sera lançado sempre que houver problema com as credenciais
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    
    try:
        # Decodifica o token usando a chave secreta e o algoritmo especifico
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extrai valor do campo 'sub'
        username: str = payload.get('sub')
        
        # Se nao houver, levanta a exceção
        if not username:
            raise credentials_exception
        
        # Cria objeto com o username
        token_data = TokenData(username=username)
        
    except DecodeError:
        raise credentials_exception
    
    # Busca no banco o usuario correspondente
    user = session.scalar(select(User).where(User.email == token_data.username))
    
    if not user:
        raise credentials_exception
    
    return user
    