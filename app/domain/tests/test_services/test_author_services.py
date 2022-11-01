import pytest

from ....adapters.mem_repository import AuthorRepository as MemAuthorRepository
from ...services import (
    AuthorAPICreate,
    AuthorCreate,
    AuthorCreateException,
    AuthorDeleteException,
    AuthorGetException,
    create_author,
    delete_author,
    get_author,
    list_authors,
)


def test_create_author(test_author_repository: MemAuthorRepository):
    author = AuthorAPICreate(name="Juliusz Słowacki")
    create_author(test_author_repository, author)


def test_create_author_duplicated_name_not_allowed(test_author_repository: MemAuthorRepository):
    author = AuthorAPICreate(name="Juliusz Słowacki")
    create_author(test_author_repository, author)

    with pytest.raises(AuthorCreateException, match='Author name already exists'):
        create_author(test_author_repository, author)


def test_list_author_empty(test_author_repository: MemAuthorRepository):
    authors = list_authors(test_author_repository)
    assert authors == []


def test_list_authors(test_author_repository: MemAuthorRepository):
    author1 = AuthorCreate(name="Juliusz Słowacki")
    db_author1 = test_author_repository.add(author1)

    author2 = AuthorCreate(name="Adam Mickiewicz")
    db_author2 = test_author_repository.add(author2)

    authors = list_authors(test_author_repository)
    assert any(author.name == db_author1.name for author in authors)
    assert any(author.name == db_author2.name for author in authors)


def test_get_author(test_author_repository: MemAuthorRepository):
    author_create = AuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author_create)

    author = get_author(test_author_repository, db_author.id)
    assert author_create.name == db_author.name == author.name


def test_get_non_existing_author(test_author_repository: MemAuthorRepository):
    with pytest.raises(AuthorGetException, match='Author not found'):
        get_author(test_author_repository, 0)


def test_delete_author(test_author_repository: MemAuthorRepository):
    author_create = AuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author_create)

    delete_author(test_author_repository, db_author.id)

    assert len(test_author_repository.list()) == 0


def test_delete_non_existing_author(test_author_repository: MemAuthorRepository):
    with pytest.raises(AuthorDeleteException, match='Author not found'):
        delete_author(test_author_repository, 0)


def test_update_author():
    pass


def test_partial_update_author():
    pass
