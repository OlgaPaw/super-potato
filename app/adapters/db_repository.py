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
        if self.filter(title=book.title, author_id=book.author.id):
            raise RepositoryException("Author name already exists")

        book = database.Book(title=book.title, author_id=book.author.id)
        self.database.add(book)
        self.database.commit()
        self.database.refresh(book)
        return Book.from_orm(book)

    def list(self) -> List[Book]:
        return self.database.query(database.Book).all()

    def filter(self, **kwargs: Any) -> List[Book]:
        return self.database.query(database.Book).filter_by(**kwargs).all()


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

    def list(self) -> List[Author]:
        return self.database.query(database.Author).all()

    def filter(self, **kwargs: Any) -> List[Author]:
        return self.database.query(database.Author).filter_by(**kwargs).all()

    def get(self, pk: int) -> Author:
        author = self.database.get(database.Author, pk)
        if not author:
            raise RepositoryException("Author not found")
        return Author.from_orm(author)

    def delete(self, pk: int) -> None:
        author = self.database.get(database.Author, pk)
        if not author:
            raise RepositoryException("Author not found")
        self.database.delete(author)
        self.database.commit()
