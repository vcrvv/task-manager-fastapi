from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    #client = TestClient(app) # Arrange - prepara o ambiente

    response = client.get('/') # Act - chama o Sistema Sob Teste(o que sera testado)
    assert response.status_code == HTTPStatus.OK # Assert - verifica se a respota é o que é esperado
    # no caso a resposta esperada é status 200
    assert response.json() == {'message': 'Olá Mundo!'} # Assert
    # no caso um json com esses dados



def test_create_user_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}
   

def test_create_user_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}

    
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
       
    
      