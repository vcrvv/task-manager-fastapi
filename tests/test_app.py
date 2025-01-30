from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_tasks.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app) # Arrange - prepara o ambiente

    response = client.get('/') # Act - chama o Sistema Sob Teste(o que sera testado)
    assert response.status_code == HTTPStatus.OK # Assert - verifica se a respota é o que é esperado
    # no caso a resposta esperada é status 200
    assert response.json() == {'message': 'Olá Mundo!'} # Assert
    # no caso um json com esses dados

def test_create_user(client):
    # com fixture
    response = client.post(
        '/users/',
        json={
            'username':'alice',
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
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }    

def test_get_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }     
    
def test_get_user_not_found(client):
    response = client.get('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
    
def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
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
                           
def test_delete_user(client):
    response = client.delete('/users/1')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}

def test_delete_user_not_found(client):
    response = client.delete('/users/100')
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail':'User not found'}

