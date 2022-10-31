# pylint: disable=redefined-outer-name
import pytest

from ...adapters.mem_repository import AuthorRepository as MemAuthorRepository
from ...adapters.mem_repository import BookRepository as MemBookRepository
from ..services import AuthorRepository, BookAPICreate, BookCreateException, BookRepository, create_book


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
