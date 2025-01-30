from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_tasks.app import app
from fast_tasks.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app) # Arrange - prepara o ambiente

    response = client.get('/') # Act - chama o Sistema Sob Teste(o que sera testado)
    assert response.status_code == HTTPStatus.OK # Assert - verifica se a respota é o que é esperado
    # no caso a resposta esperada é status 200
    assert response.json() == {'message': 'Olá Mundo!'} # Assert
    # no caso um json com esses dados

def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
    
    
def test_read_users(client):
    response = client.get('/users')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}
    
    
def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}    
    
    
def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'teste', 
        'email': 'teste@teste.com', 
        'id': 1,
    }     
    
    
def test_get_user_not_found(client):
    response = client.get('/users/100')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
    
    
def test_update_user(client, user):
    response = client.put(f'/users/{user.id}',
        json={
            'username': 'teste',
            'email': 'teste@teste.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@teste.com',
        'id': 1,
    }
    

def test_update_user_not_found(client):
    response = client.put(
        '/users/100',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail':'User not found'}
      
       
def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put( 
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username or Email already exists'}
    
                           
def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/100')    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail':'User not found'}

