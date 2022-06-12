from fastapi.testclient import TestClient

from app.adapters.mem_repository import AuthorRepository, BookRepository
from app.main import books_api, get_autor_repository, get_book_repository

author_repo = AuthorRepository()
book_repo = BookRepository()


def get_autor_test_repository():
    return author_repo


def get_book_test_repository():
    return book_repo


books_api.dependency_overrides[get_autor_repository] = get_autor_test_repository
books_api.dependency_overrides[get_book_repository] = get_book_test_repository
client = TestClient(books_api)


def test_empty_author_list():
    response = client.get('/authors')
    assert response.status_code == 200
    assert response.json() == []


def test_create_author():
    data = {"name": "Adam Mickiewicz"}
    response = client.post('/authors', json=data)
    assert response.status_code == 200
    assert response.json() == {"name": "Adam Mickiewicz", "id": 0}

    response = client.get('/authors')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_empty_book_list():
    response = client.get('/books')
    assert response.status_code == 200
    assert response.json() == []


def test_create_book():
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
