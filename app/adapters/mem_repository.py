from dataclasses import dataclass, field
from typing import Any, List

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
        if self.filter(title=book.title, author=book.author):
            raise RepositoryException("Book for this author and tittle alredy exists.")
        self.books[max_id] = book_
        return book_

    def list(self) -> List[Book]:
        return list(self.books.values())

    def filter(self, **kwargs: Any) -> List[Book]:
        return [
            book for book in self.books.values()
            if all(getattr(book, key, None) == value for key, value in kwargs.items())
        ]


@dataclass
class AuthorRepository(AuthorRespositoryBase):
    authors: dict[int, Author] = field(default_factory=dict)

    def add(self, author: AuthorCreate) -> Author:
        max_id = len(self.authors)
        if author.name in [a.name for a in self.authors.values()]:
            raise RepositoryException("Author name already exists")
        self.authors[max_id] = Author(name=author.name, id=max_id)
        return self.authors[max_id]

    def list(self) -> List[Author]:
        return list(self.authors.values())

    def get(self, pk: int) -> Author:
        try:
            return self.authors[pk]
        except KeyError as err:
            raise RepositoryException("Author not found") from err

    def delete(self, pk: int) -> None:
        author = self.get(pk)
        del self.authors[author.id]

    def filter(self, **kwargs: Any) -> List[Author]:
        return [
            author for author in self.authors.values()
            if all(getattr(author, key, None) == value for key, value in kwargs.items())
        ]
