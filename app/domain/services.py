from typing import List

from pydantic import BaseModel

from .interfaces import (
    AuthorRepository,
    BookRepository,
    DBAuthor,
    DBAuthorCreate,
    DBBook,
    DBBookCreate,
    RepositoryException,
)


### Service models
class BookCreate(BaseModel):
    title: str
    author_id: int

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


### Service errors
class BaseBookServiceException(Exception):
    """Raised when service method failed."""


class AuthorCreateException(BaseBookServiceException):
    """Raised when author create failed."""


class AuthorGetException(BaseBookServiceException):
    """Raised when author get failed."""


class AuthorDeleteException(BaseBookServiceException):
    """Raised when author delete failed."""


class BookCreateException(BaseBookServiceException):
    """Raised when book create failed."""


### service methods
def list_books(book_repository: BookRepository) -> List[DBBook]:
    return book_repository.list()


def create_book(author_repository: AuthorRepository, book_repository: BookRepository, book: BookCreate) -> DBBook:
    try:
        author = author_repository.get(book.author_id)
        book_ = DBBookCreate(title=book.title, author=author)
        return book_repository.add(book_)
    except RepositoryException as err:
        raise BookCreateException(err) from err


def list_authors(author_repository: AuthorRepository) -> List[DBAuthor]:
    return author_repository.list()


def create_author(author_repository: AuthorRepository, author: AuthorCreate) -> DBAuthor:
    author_ = DBAuthorCreate(name=author.name)
    try:
        return author_repository.add(author_)
    except RepositoryException as err:
        raise AuthorCreateException(err) from err


def get_author(author_repository: AuthorRepository, author_id: int) -> DBAuthor:
    try:
        return author_repository.get(author_id)
    except RepositoryException as err:
        raise AuthorGetException(err) from err


def delete_author(author_repository: AuthorRepository, author_id: int) -> None:
    try:
        return author_repository.delete(author_id)
    except RepositoryException as err:
        raise AuthorDeleteException(err) from err
