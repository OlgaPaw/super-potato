from typing import List

from pydantic import BaseModel

from ..interfaces import AuthorRepository, BookRepository, DBBook, DBBookCreate, RepositoryException
from .base import BaseBookServiceException


class BookCreate(BaseModel):
    title: str
    author_id: int

    class Config:
        orm_mode = True


class BookCreateException(BaseBookServiceException):
    """Raised when book create failed."""


def list_books(book_repository: BookRepository) -> List[DBBook]:
    return book_repository.list()


def create_book(author_repository: AuthorRepository, book_repository: BookRepository, book: BookCreate) -> DBBook:
    try:
        author = author_repository.get(book.author_id)
        book_ = DBBookCreate(title=book.title, author=author)
        return book_repository.add(book_)
    except RepositoryException as err:
        raise BookCreateException(err) from err
