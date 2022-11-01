from typing import Any, List

from pydantic import BaseModel
from typing_extensions import Protocol


class DBAuthorCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class DBAuthor(DBAuthorCreate):
    id: int


class DBBookCreate(BaseModel):
    title: str
    author: DBAuthor

    class Config:
        orm_mode = True


class DBBook(DBBookCreate):
    id: int


class RepositoryException(Exception):
    """raised on failed Repository operation"""


class BookRepository(Protocol):

    def add(self, book: DBBookCreate) -> DBBook:
        ...

    def list(self) -> List[DBBook]:
        ...

    def filter(self, **kwargs: Any) -> List[DBBook]:
        ...


class AuthorRepository(Protocol):

    def add(self, author: DBAuthorCreate) -> DBAuthor:
        ...

    def list(self) -> List[DBAuthor]:
        ...

    def get(self, pk: int) -> DBAuthor:
        ...

    def delete(self, pk: int) -> None:
        ...

    def filter(self, **kwargs: Any) -> List[DBAuthor]:
        ...
