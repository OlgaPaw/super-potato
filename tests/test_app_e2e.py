# pylint: disable=redefined-outer-name

import pytest
from fastapi.testclient import TestClient

from app.adapters.mem_repository import AuthorRepository, BookRepository
from app.main import books_api, get_autor_repository, get_book_repository


@pytest.fixture
def autor_test_repository():
    auth_repo = AuthorRepository()
    return lambda: auth_repo


@pytest.fixture
def book_test_repository():
    book_repo = BookRepository()
    return lambda: book_repo


@pytest.fixture
def client(book_test_repository, autor_test_repository):
    books_api.dependency_overrides[get_autor_repository] = autor_test_repository
    books_api.dependency_overrides[get_book_repository] = book_test_repository
    return TestClient(books_api)


def test_empty_author_list(client):
    response = client.get('/authors')
    assert response.status_code == 200
    assert response.json() == []


def test_create_author(client):
    data = {"name": "Adam Mickiewicz"}
    response = client.post('/authors', json=data)
    assert response.status_code == 200
    assert response.json() == {"name": "Adam Mickiewicz", "id": 0}

    response = client.get('/authors')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_author(client):
    data = {"name": "Adam Mickiewicz"}
    response = client.post('/authors', json=data)

    expected_data = {"name": "Adam Mickiewicz", "id": 0}
    assert response.status_code == 200
    assert response.json() == expected_data

    response = client.get(f'/authors/{expected_data["id"]}')
    assert response.status_code == 200
    assert response.json() == expected_data


def test_get_non_existing_author(client):
    response = client.get('/authors/0')
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_author(client):
    data = {"name": "Adam Mickiewicz"}
    response = client.post('/authors', json=data)

    expected_data = {"name": "Adam Mickiewicz", "id": 0}
    assert response.status_code == 200
    assert response.json() == expected_data

    response = client.delete(f'/authors/{expected_data["id"]}')
    assert response.status_code == 204

    response = client.get(f'/authors/{expected_data["id"]}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_non_existing_author(client):
    response = client.delete('/authors/0')
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_author_duplicated_name(client):
    data = {"name": "Adam Mickiewicz"}
    response = client.post('/authors', json=data)
    assert response.status_code == 200

    response = client.post('/authors', json=data)
    assert response.status_code == 422
    assert response.json() == {"detail": "Author name already exists"}


def test_empty_book_list(client):
    response = client.get('/books')
    assert response.status_code == 200
    assert response.json() == []


def test_create_book(client):
    author_data = {"name": "Adam Mickiewicz"}
    response = client.post('/authors', json=author_data)
    assert response.status_code == 200
    author_id = response.json()['id']

    book_data = {"title": "Pan Tadeusz", "author_id": author_id}
    response = client.post('/books', json=book_data)
    assert response.status_code == 200
    assert response.json() == {"id": 0, "title": "Pan Tadeusz", "author": {"name": "Adam Mickiewicz", "id": author_id}}

    response = client.get('/books')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_book_non_existing_author(client):
    book_data = {"title": "Pan Tadeusz", "author_id": 0}
    response = client.post('/books', json=book_data)
    assert response.status_code == 422
    assert response.json() == {'detail': 'Author not found'}


def test_create_book_duplicated_title_same_author(client):
    author_data = {"name": "Adam Mickiewicz"}
    response = client.post('/authors', json=author_data)
    assert response.status_code == 200
    author_id = response.json()['id']

    book_data = {"title": "Pan Tadeusz", "author_id": author_id}
    response = client.post('/books', json=book_data)
    assert response.status_code == 200
    assert response.json() == {"id": 0, "title": "Pan Tadeusz", "author": {"name": "Adam Mickiewicz", "id": author_id}}

    response = client.post('/books', json=book_data)
    assert response.status_code == 422
    assert response.json() == {"detail": "Book for this author and tittle alredy exists."}
