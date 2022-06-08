from dataclasses import dataclass


@dataclass
class BookRepository:
    books = []

    def add(self, book):
        self.books.append(book)
        return book

    def list(self):
        return self.books


@dataclass
class AuthorRepository:
    authors = []

    def add(self, author):
        self.authors.append(author)
        return author

    def list(self):
        return self.authors