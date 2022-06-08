from typing import Protocol

from pydantic import BaseModel


### Interface definition for repository
class Author(BaseModel):
    name: str


class Book(BaseModel):
    title: str
    author: Author


class BookRepository(Protocol):
    def add(self, book: Book) -> Book:
        ...

    def list(self) -> list[Book]:
        ...


class AuthorRepository(Protocol):
    def add(self, author: Author) -> Author:
        ...

    def list(self) -> list[Author]:
        ...


### service methods
def list_books(book_repository: BookRepository) -> list[Book]:
    return book_repository.list()


def create_book(book_repository: BookRepository, book: Book) -> Book:
    return book_repository.add(book)


def list_authors(authors_repository: AuthorRepository) -> list[Author]:
    return authors_repository.list()


def create_author(authors_repository: AuthorRepository, author: Author) -> Author:
    return authors_repository.add(author)
