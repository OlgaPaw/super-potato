from dataclasses import dataclass, field

from .services import Author, Book


@dataclass
class BookRepository:
    books: list[Book] = field(default_factory=list)

    def add(self, book: Book) -> Book:
        self.books.append(book)
        return book

    def list(self) -> list[Book]:
        return self.books


@dataclass
class AuthorRepository:
    authors: list[Author] = field(default_factory=list)

    def add(self, author: Author) -> Author:
        self.authors.append(author)
        return author

    def list(self) -> list[Author]:
        return self.authors
