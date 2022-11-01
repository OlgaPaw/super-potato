import pytest

from ...interfaces import AuthorRepository, DBAuthorCreate
from ...services import (
    AuthorCreate,
    AuthorCreateException,
    AuthorDeleteException,
    AuthorGetException,
    create_author,
    delete_author,
    get_author,
    list_authors,
)


def test_create_author(test_author_repository: AuthorRepository):
    author = AuthorCreate(name="Juliusz Słowacki")
    create_author(test_author_repository, author)


def test_create_author_duplicated_name_not_allowed(test_author_repository: AuthorRepository):
    author = AuthorCreate(name="Juliusz Słowacki")
    create_author(test_author_repository, author)

    with pytest.raises(AuthorCreateException, match='DBAuthor name already exists'):
        create_author(test_author_repository, author)


def test_list_author_empty(test_author_repository: AuthorRepository):
    authors = list_authors(test_author_repository)
    assert authors == []


def test_list_authors(test_author_repository: AuthorRepository):
    author1 = DBAuthorCreate(name="Juliusz Słowacki")
    db_author1 = test_author_repository.add(author1)

    author2 = DBAuthorCreate(name="Adam Mickiewicz")
    db_author2 = test_author_repository.add(author2)

    authors = list_authors(test_author_repository)
    assert any(author.name == db_author1.name for author in authors)
    assert any(author.name == db_author2.name for author in authors)


def test_get_author(test_author_repository: AuthorRepository):
    author_create = DBAuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author_create)

    author = get_author(test_author_repository, db_author.id)
    assert author_create.name == db_author.name == author.name


def test_get_non_existing_author(test_author_repository: AuthorRepository):
    with pytest.raises(AuthorGetException, match='DBAuthor not found'):
        get_author(test_author_repository, 0)


def test_delete_author(test_author_repository: AuthorRepository):
    author_create = DBAuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author_create)

    delete_author(test_author_repository, db_author.id)

    assert len(test_author_repository.list()) == 0


def test_delete_non_existing_author(test_author_repository: AuthorRepository):
    with pytest.raises(AuthorDeleteException, match='DBAuthor not found'):
        delete_author(test_author_repository, 0)


def test_update_author():
    pass


def test_partial_update_author():
    pass
