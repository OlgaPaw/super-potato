from typing import List

from fastapi import Depends, FastAPI, HTTPException

from ...domain import services
from ..data_storage import database, db_repository

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


@books_api.get("/authors", response_model=List[services.Author])
def list_authors(
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> List[services.Author]:
    return services.list_authors(author_repository)


@books_api.post("/authors", response_model=services.Author)
def create_author(
    data: services.AuthorAPICreate,
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> services.Author:
    try:
        return services.create_author(author_repository, data)
    except services.AuthorCreateException as err:
        raise HTTPException(status_code=422, detail=str(err)) from err


@books_api.get("/authors/{author_id}", response_model=services.Author)
def get_author(
    author_id: int,
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> services.Author:
    try:
        return services.get_author(author_repository, author_id)
    except services.AuthorGetException as err:
        raise HTTPException(status_code=404, detail="Item not found") from err


@books_api.delete("/authors/{author_id}", status_code=204)
def delete_author(
    author_id: int,
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> None:
    try:
        return services.delete_author(author_repository, author_id)
    except services.AuthorDeleteException as err:
        raise HTTPException(status_code=404, detail="Item not found") from err


@books_api.get("/books", response_model=List[services.Book])
def list_books(book_repository: db_repository.BookRepository = Depends(get_book_repository)) -> List[services.Book]:
    return services.list_books(book_repository)


@books_api.post("/books", response_model=services.Book)
def create_book(
    data: services.BookAPICreate,
    book_repository: db_repository.BookRepository = Depends(get_book_repository),
    author_repository: db_repository.AuthorRepository = Depends(get_autor_repository),
) -> services.Book:
    try:
        return services.create_book(author_repository, book_repository, data)
    except services.BookCreateException as err:
        raise HTTPException(status_code=422, detail=str(err)) from err
