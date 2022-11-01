import pytest

from ...interfaces import BookRepository, DBAuthorCreate, DBBookCreate
from ...services import AuthorRepository, BookCreate, BookCreateException, create_book, list_books


def test_create_book(test_author_repository: AuthorRepository, test_book_repository: BookRepository):
    author = DBAuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookCreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)


def test_create_book_non_existing_author(
    test_author_repository: AuthorRepository, test_book_repository: BookRepository
):
    book = BookCreate(title='Balladyna', author_id=1)
    with pytest.raises(BookCreateException, match='DBAuthor not found'):
        create_book(test_author_repository, test_book_repository, book)


def test_create_book_duplicated_author_title_not_allowed(
    test_author_repository: AuthorRepository, test_book_repository: BookRepository
):
    author = DBAuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookCreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    with pytest.raises(BookCreateException, match='DBBook for this author and tittle alredy exists.'):
        create_book(test_author_repository, test_book_repository, book)


def test_create_book_same_title_different_author_allowed(
    test_author_repository: AuthorRepository, test_book_repository: BookRepository
):
    author = DBAuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookCreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    author = DBAuthorCreate(name="Adam Mickiewicz")
    db_author = test_author_repository.add(author)

    book = BookCreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)


def test_create_book_same_author_different_title_allowed(
    test_author_repository: AuthorRepository, test_book_repository: BookRepository
):
    author = DBAuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookCreate(title='Balladyna 1', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    book = BookCreate(title='Balladyna 2', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)


def test_book_list(test_author_repository: AuthorRepository, test_book_repository: BookRepository):
    author = DBAuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book1 = DBBookCreate(title="Balladyna 1", author=db_author)
    db_book1 = test_book_repository.add(book1)
    book2 = DBBookCreate(title="Balladyna 2", author=db_author)
    db_book2 = test_book_repository.add(book2)

    books = list_books(test_book_repository)
    assert any(book.title == db_book1.title for book in books)
    assert any(book.title == db_book2.title for book in books)


def test_empty_book_list(test_book_repository: BookRepository):
    books = list_books(test_book_repository)
    assert books == []


def test_get_book():
    pass


def test_get_non_existing_book():
    pass


def test_delete_book():
    pass


def test_delete_non_existing_book():
    pass


def test_update_book():
    pass


def test_partial_update_book():
    pass
