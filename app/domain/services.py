from typing import List

from pydantic import BaseModel
from typing_extensions import Protocol


### Interface definition for repository
class AuthorAPICreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AuthorCreate(AuthorAPICreate):
    pass


class Author(AuthorCreate):
    id: int


class BookAPICreate(BaseModel):
    title: str
    author_id: int

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    author: Author

    class Config:
        orm_mode = True


class Book(BookCreate):
    id: int


class RepositoryException(Exception):
    """raised on failed Repository operation"""


class BookRepository(Protocol):
    def add(self, book: BookCreate) -> Book:
        ...

    def list(self) -> List[Book]:
        ...


class AuthorRepository(Protocol):
    def add(self, author: AuthorCreate) -> Author:
        ...

    def list(self) -> List[Author]:
        ...

    def get(self, pk: int) -> Author:
        ...

    def delete(self, pk: int) -> None:
        ...


### Service errors
class BaseBookServiceException(Exception):
    """Raised when service method failed."""


class AuthorCreateException(BaseBookServiceException):
    """Raised when author create failed."""


class AuthorGetException(BaseBookServiceException):
    """Raised when author get failed."""


class AuthorDeleteException(BaseBookServiceException):
    """Raised when author delete failed."""


### service methods
def list_books(book_repository: BookRepository) -> List[Book]:
    return book_repository.list()


def create_book(author_repository: AuthorRepository, book_repository: BookRepository, book: BookAPICreate) -> Book:
    author = author_repository.get(book.author_id)
    book_ = BookCreate(title=book.title, author=author)
    return book_repository.add(book_)


def list_authors(author_repository: AuthorRepository) -> List[Author]:
    return author_repository.list()


def create_author(author_repository: AuthorRepository, author: AuthorAPICreate) -> Author:
    author_ = AuthorCreate(name=author.name)
    try:
        return author_repository.add(author_)
    except RepositoryException as err:
        raise AuthorCreateException(err) from err


def get_author(author_repository: AuthorRepository, author_id: int) -> Author:
    try:
        return author_repository.get(author_id)
    except RepositoryException as err:
        raise AuthorGetException(err) from err


def delete_author(author_repository: AuthorRepository, author_id: int) -> None:
    try:
        return author_repository.delete(author_id)
    except RepositoryException as err:
        raise AuthorDeleteException(err) from err
