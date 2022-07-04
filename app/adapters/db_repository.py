from dataclasses import dataclass
from typing import Any, List

from ..domain.services import Author, AuthorCreate
from ..domain.services import AuthorRepository as AuthorRespositoryBase
from ..domain.services import Book, BookCreate
from ..domain.services import BookRepository as BookRespositoryBase
from ..domain.services import RepositoryException
from . import database


@dataclass
class BaseRepository:
    database: database.SessionLocal


@dataclass
class BookRepository(BaseRepository, BookRespositoryBase):
    def add(self, book: BookCreate) -> Book:
        book = database.Book(title=book.title, author_id=book.author.id)
        self.database.add(book)
        self.database.commit()
        self.database.refresh(book)
        return Book.from_orm(book)

    def list(self) -> list[Book]:
        return self.database.query(database.Book).all()


@dataclass
class AuthorRepository(BaseRepository, AuthorRespositoryBase):
    def add(self, author: AuthorCreate) -> Author:
        author = database.Author(name=author.name)
        if self.filter(name=author.name):
            raise RepositoryException("Author name already exists")
        self.database.add(author)
        self.database.commit()
        self.database.refresh(author)
        return Author.from_orm(author)

    def list(self) -> list[Author]:
        return self.database.query(database.Author).all()

    def filter(self, **kwargs: dict[str, Any]) -> List[Author]:
        return self.database.query(database.Author).filter_by(**kwargs).all()

    def get(self, pk: int) -> Author:
        author = self.database.get(database.Author, pk)
        if not author:
            raise RepositoryException("Author not found")
        return Author.from_orm(author)
