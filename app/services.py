from pydantic import BaseModel

from app.repository import AuthorRepository, BookRepository

class Author(BaseModel):
    name: str


class Book(BaseModel):
    title: str
    author: Author


book_repository = BookRepository()
authors_repository = AuthorRepository()

def list_books():
    return book_repository.list()

def create_book(book: Book):
    return book_repository.add(book)

def list_authors():
    return authors_repository.list()

def create_author(author: Author):
    return authors_repository.add(author)
