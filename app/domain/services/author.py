from typing import List

from pydantic import BaseModel

from ..interfaces import AuthorRepository, DBAuthor, DBAuthorCreate, RepositoryException
from .base import BaseBookServiceException


class AuthorCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AuthorCreateException(BaseBookServiceException):
    """Raised when author create failed."""


class AuthorGetException(BaseBookServiceException):
    """Raised when author get failed."""


class AuthorDeleteException(BaseBookServiceException):
    """Raised when author delete failed."""


def list_authors(author_repository: AuthorRepository) -> List[DBAuthor]:
    return author_repository.list()


def create_author(author_repository: AuthorRepository, author: AuthorCreate) -> DBAuthor:
    author_ = DBAuthorCreate(name=author.name)
    try:
        return author_repository.add(author_)
    except RepositoryException as err:
        raise AuthorCreateException(err) from err


def get_author(author_repository: AuthorRepository, author_id: int) -> DBAuthor:
    try:
        return author_repository.get(author_id)
    except RepositoryException as err:
        raise AuthorGetException(err) from err


def delete_author(author_repository: AuthorRepository, author_id: int) -> None:
    try:
        return author_repository.delete(author_id)
    except RepositoryException as err:
        raise AuthorDeleteException(err) from err
