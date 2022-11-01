import pytest

from ....adapters.mem_repository import AuthorRepository as MemAuthorRepository
from ....adapters.mem_repository import BookRepository as MemBookRepository
from ...services import AuthorCreate, BookAPICreate, BookCreate, BookCreateException, create_book, list_books


def test_create_book(test_author_repository: MemAuthorRepository, test_book_repository: MemBookRepository):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)


def test_create_book_non_existing_author(
    test_author_repository: MemAuthorRepository, test_book_repository: MemBookRepository
):
    book = BookAPICreate(title='Balladyna', author_id=1)
    with pytest.raises(BookCreateException, match='Author not found'):
        create_book(test_author_repository, test_book_repository, book)


def test_create_book_duplicated_author_title_not_allowed(
    test_author_repository: MemAuthorRepository, test_book_repository: MemBookRepository
):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    with pytest.raises(BookCreateException, match='Book for this author and tittle alredy exists.'):
        create_book(test_author_repository, test_book_repository, book)


def test_create_book_same_title_different_author_allowed(
    test_author_repository: MemAuthorRepository, test_book_repository: MemBookRepository
):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    author = AuthorCreate(name="Adam Mickiewicz")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)


def test_create_book_same_author_different_title_allowed(
    test_author_repository: MemAuthorRepository, test_book_repository: MemBookRepository
):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book = BookAPICreate(title='Balladyna 1', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)

    book = BookAPICreate(title='Balladyna 2', author_id=db_author.id)
    create_book(test_author_repository, test_book_repository, book)


def test_book_list(test_author_repository: MemAuthorRepository, test_book_repository: MemBookRepository):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = test_author_repository.add(author)

    book1 = BookCreate(title="Balladyna 1", author=db_author)
    db_book1 = test_book_repository.add(book1)
    book2 = BookCreate(title="Balladyna 2", author=db_author)
    db_book2 = test_book_repository.add(book2)

    books = list_books(test_book_repository)
    assert any(book.title == db_book1.title for book in books)
    assert any(book.title == db_book2.title for book in books)


def test_empty_book_list(test_book_repository: MemBookRepository):
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
