from dataclasses import dataclass
from typing import Any, List

from ...domain.interfaces import AuthorRepository as AuthorRespositoryBase
from ...domain.interfaces import BookRepository as BookRespositoryBase
from ...domain.interfaces import DBAuthor, DBAuthorCreate, DBBook, DBBookCreate, RepositoryException
from . import database


@dataclass
class BaseRepository:
    database: database.SessionLocal


@dataclass
class BookRepository(BaseRepository, BookRespositoryBase):

    def add(self, book: DBBookCreate) -> DBBook:
        if self.filter(title=book.title, author_id=book.author.id):
            raise RepositoryException("DBBook for this author and tittle alredy exists.")

        book = database.DBBook(title=book.title, author_id=book.author.id)
        self.database.add(book)
        self.database.commit()
        self.database.refresh(book)
        return DBBook.from_orm(book)

    def list(self) -> List[DBBook]:
        return self.database.query(database.DBBook).all()

    def filter(self, **kwargs: Any) -> List[DBBook]:
        return self.database.query(database.DBBook).filter_by(**kwargs).all()


@dataclass
class AuthorRepository(BaseRepository, AuthorRespositoryBase):

    def add(self, author: DBAuthorCreate) -> DBAuthor:
        author = database.DBAuthor(name=author.name)
        if self.filter(name=author.name):
            raise RepositoryException("DBAuthor name already exists")
        self.database.add(author)
        self.database.commit()
        self.database.refresh(author)
        return DBAuthor.from_orm(author)

    def list(self) -> List[DBAuthor]:
        return self.database.query(database.DBAuthor).all()

    def filter(self, **kwargs: Any) -> List[DBAuthor]:
        return self.database.query(database.DBAuthor).filter_by(**kwargs).all()

    def get(self, pk: int) -> DBAuthor:
        author = self.database.get(database.DBAuthor, pk)
        if not author:
            raise RepositoryException("DBAuthor not found")
        return DBAuthor.from_orm(author)

    def delete(self, pk: int) -> None:
        author = self.database.get(database.DBAuthor, pk)
        if not author:
            raise RepositoryException("DBAuthor not found")
        self.database.delete(author)
        self.database.commit()
