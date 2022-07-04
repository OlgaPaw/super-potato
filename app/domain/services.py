from typing import Protocol

from pydantic import BaseModel


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

    def list(self) -> list[Book]:
        ...


class AuthorRepository(Protocol):
    def add(self, author: AuthorCreate) -> Author:
        ...

    def list(self) -> list[Author]:
        ...

    def get(self, pk: int) -> Author:
        ...


### service methods
def list_books(book_repository: BookRepository) -> list[Book]:
    return book_repository.list()


def create_book(author_repository: AuthorRepository, book_repository: BookRepository, book: BookAPICreate) -> Book:
    author = author_repository.get(book.author_id)
    book_ = BookCreate(title=book.title, author=author)
    return book_repository.add(book_)


def list_authors(author_repository: AuthorRepository) -> list[Author]:
    return author_repository.list()


def create_author(author_repository: AuthorRepository, author: AuthorAPICreate) -> Author:
    author_ = AuthorCreate(name=author.name)
    return author_repository.add(author_)


def get_author(author_repository: AuthorRepository, author_id: int) -> Author:
    return author_repository.get(author_id)
