import pytest

from ....adapters.data_storage import mem_repository
from ...interfaces import AuthorRepository, BookRepository


@pytest.fixture
def test_book_repository() -> BookRepository:
    return mem_repository.BookRepository()


@pytest.fixture
def test_author_repository() -> AuthorRepository:
    return mem_repository.AuthorRepository()
