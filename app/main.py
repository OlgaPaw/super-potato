from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper

from .adapters import database, db_repository
from .domain import services

books_api = FastAPI()


def get_database() -> database.SessionLocal:
    database_ = database.SessionLocal()
    try:
        yield database_
    finally:
        database_.close()


def get_autor_repository(database_: database.SessionLocal = Depends(get_database)) -> db_repository.AuthorRepository:
    return db_repository.AuthorRepository(database_)


def get_book_repository(database_: database.SessionLocal = Depends(get_database)) -> db_repository.BookRepository:
    return db_repository.BookRepository(database_)


@books_api.get("/")
def home() -> dict:
    return {"Hello": "World"}


@books_api.get("/authors", response_model=list[services.Author])
def list_authors(
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> list[services.Author]:
    return services.list_authors(author_repository)


@books_api.post("/authors", response_model=services.Author)
def create_author(
    data: services.AuthorAPICreate,
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> services.Author:
    try:
        return services.create_author(author_repository, data)
    except services.RepositoryException as err:
        raise RequestValidationError([ErrorWrapper(ValueError(f"Invalid data: {str(err)}"), ("query", ))]) from err


@books_api.get("/books", response_model=list[services.Book])
def list_books(book_repository: db_repository.BookRepository = Depends(get_book_repository)) -> list[services.Book]:
    return services.list_books(book_repository)


@books_api.post("/books", response_model=services.Book)
def create_book(
    data: services.BookAPICreate,
    book_repository: db_repository.BookRepository = Depends(get_book_repository),
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> services.Book:
    return services.create_book(author_repository, book_repository, data)
