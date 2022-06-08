from typing import Union

from fastapi import FastAPI

from . import services

books_api = FastAPI()


@books_api.get("/")
def home():
    return {"Hello": "World"}


@books_api.get("/authors")
def list_authors() -> list[services.Author]:
    return services.list_authors()


@books_api.post("/authors")
def create_author(data: services.Author) -> services.Author:
    return services.create_author(data)


@books_api.get("/books")
def list_books() -> list[services.Book]:
    return services.list_books()


@books_api.post("/books")
def create_book(data: services.Book) -> services.Book:
    return services.create_book(data)
