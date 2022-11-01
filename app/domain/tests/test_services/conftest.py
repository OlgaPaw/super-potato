import pytest

from ....adapters.data_storage.mem_repository import AuthorRepository as MemAuthorRepository
from ....adapters.data_storage.mem_repository import BookRepository as MemBookRepository
from ...services import AuthorRepository, BookRepository


@pytest.fixture
def test_book_repository() -> BookRepository:
    return MemBookRepository()


@pytest.fixture
def test_author_repository() -> AuthorRepository:
    return MemAuthorRepository()
