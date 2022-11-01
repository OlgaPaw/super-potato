# pylint: disable=redefined-outer-name
import pytest

from ...adapters.mem_repository import AuthorRepository as MemAuthorRepository
from ...adapters.mem_repository import BookRepository as MemBookRepository
from ..services import (
    AuthorAPICreate,
    AuthorRepository,
    BookAPICreate,
    BookCreateException,
    BookRepository,
    create_book,
)


@pytest.fixture
def test_book_repository() -> BookRepository:
    return MemBookRepository()


@pytest.fixture
def test_author_repository() -> AuthorRepository:
    return MemAuthorRepository()


def test_create_book_non_existing_author(test_author_repository, test_book_repository):
    book = BookAPICreate(title='Balladyna', author_id=1)
    with pytest.raises(BookCreateException, match='Author not found'):
        create_book(test_author_repository, test_book_repository, book)


def test_create_book_duplicated_author_title_not_allowed(test_author_repository, test_book_repository):
    author = AuthorAPICreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    with pytest.raises(BookCreateException, match='Book for this author and tittle alredy exists.'):
        create_book(test_author_repository, test_book_repository, book)


def test_create_book_same_title_different_author_allowed(test_author_repository, test_book_repository):
    author = AuthorAPICreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    author = AuthorAPICreate(name="Adam Mickiewicz")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)


def test_create_book_same_author_different_title_allowed(test_author_repository, test_book_repository):
    author = AuthorAPICreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna 1', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    book = BookAPICreate(title='Balladyna 2', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)
