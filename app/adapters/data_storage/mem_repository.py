from dataclasses import dataclass, field
from typing import Any, List

from ...domain.interfaces import AuthorRepository as AuthorRespositoryBase
from ...domain.interfaces import BookRepository as BookRespositoryBase
from ...domain.interfaces import DBAuthor, DBAuthorCreate, DBBook, DBBookCreate, RepositoryException


@dataclass
class BookRepository(BookRespositoryBase):
    books: dict[int, DBBook] = field(default_factory=dict)

    def add(self, book: DBBookCreate) -> DBBook:
        max_id = len(self.books)
        book_ = DBBook(id=max_id, title=book.title, author=book.author)
        if self.filter(title=book.title, author=book.author):
            raise RepositoryException("DBBook for this author and tittle alredy exists.")
        self.books[max_id] = book_
        return book_

    def list(self) -> List[DBBook]:
        return list(self.books.values())

    def filter(self, **kwargs: Any) -> List[DBBook]:
        return [
            book for book in self.books.values()
            if all(getattr(book, key, None) == value for key, value in kwargs.items())
        ]


@dataclass
class AuthorRepository(AuthorRespositoryBase):
    authors: dict[int, DBAuthor] = field(default_factory=dict)

    def add(self, author: DBAuthorCreate) -> DBAuthor:
        max_id = len(self.authors)
        if author.name in [a.name for a in self.authors.values()]:
            raise RepositoryException("DBAuthor name already exists")
        self.authors[max_id] = DBAuthor(name=author.name, id=max_id)
        return self.authors[max_id]

    def list(self) -> List[DBAuthor]:
        return list(self.authors.values())

    def get(self, pk: int) -> DBAuthor:
        try:
            return self.authors[pk]
        except KeyError as err:
            raise RepositoryException("DBAuthor not found") from err

    def delete(self, pk: int) -> None:
        author = self.get(pk)
        del self.authors[author.id]

    def filter(self, **kwargs: Any) -> List[DBAuthor]:
        return [
            author for author in self.authors.values()
            if all(getattr(author, key, None) == value for key, value in kwargs.items())
        ]
