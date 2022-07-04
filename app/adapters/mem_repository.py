from dataclasses import dataclass, field

from ..domain.services import Author, AuthorCreate
from ..domain.services import AuthorRepository as AuthorRespositoryBase
from ..domain.services import Book, BookCreate
from ..domain.services import BookRepository as BookRespositoryBase
from ..domain.services import RepositoryException


@dataclass
class BookRepository(BookRespositoryBase):
    books: dict[int, Book] = field(default_factory=dict)

    def add(self, book: BookCreate) -> Book:
        max_id = len(self.books)
        book_ = Book(id=max_id, title=book.title, author=book.author)
        self.books[max_id] = book_
        return book_

    def list(self) -> list[Book]:
        return list(self.books.values())


@dataclass
class AuthorRepository(AuthorRespositoryBase):
    authors: dict[int, Author] = field(default_factory=dict)

    def add(self, author: AuthorCreate) -> Author:
        max_id = len(self.authors)
        if author.name in [a.name for a in self.authors.values()]:
            raise RepositoryException("Author name already exists")
        self.authors[max_id] = Author(name=author.name, id=max_id)
        return self.authors[max_id]

    def list(self) -> list[Author]:
        return list(self.authors.values())

    def get(self, pk: int) -> Author:
        return self.authors[pk]
