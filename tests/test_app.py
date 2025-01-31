from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    #client = TestClient(app) # Arrange - prepara o ambiente

    response = client.get('/') # Act - chama o Sistema Sob Teste(o que sera testado)
    assert response.status_code == HTTPStatus.OK # Assert - verifica se a respota é o que é esperado
    # no caso a resposta esperada é status 200
    assert response.json() == {'message': 'Olá Mundo!'} # Assert
    # no caso um json com esses dados

