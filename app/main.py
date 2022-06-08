from fastapi import FastAPI

from . import repository, services

books_api = FastAPI()

book_repository = repository.BookRepository()
authors_repository = repository.AuthorRepository()


@books_api.get("/")
def home() -> dict:
    return {"Hello": "World"}


@books_api.get("/authors", response_model=list[services.Author])
def list_authors() -> list[services.Author]:
    return services.list_authors(authors_repository)


@books_api.post("/authors", response_model=services.Author)
def create_author(data: services.Author) -> services.Author:
    return services.create_author(authors_repository, data)


@books_api.get("/books", response_model=list[services.Book])
def list_books() -> list[services.Book]:
    return services.list_books(book_repository)


@books_api.post("/books", response_model=services.Book)
def create_book(data: services.Book) -> services.Book:
    return services.create_book(book_repository, data)
