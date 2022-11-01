# pylint: disable=redefined-outer-name

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.data_storage import database, db_repository, mem_repository
from app.domain.services import AuthorCreate, BookCreate, RepositoryException


@pytest.fixture
def test_db():
    sqlalchemy_database_url = "sqlite:///./test.db"
    engine = create_engine(sqlalchemy_database_url, connect_args={"check_same_thread": False})
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    database.Base.metadata.create_all(bind=engine)
    yield test_session()
    database.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_author_repo(test_db):
    return db_repository.AuthorRepository(test_db)


@pytest.fixture
def db_book_repo(test_db):
    return db_repository.BookRepository(test_db)


@pytest.fixture
def mem_author_repo():
    return mem_repository.AuthorRepository()


@pytest.fixture
def mem_book_repo():
    return mem_repository.BookRepository()


@pytest.fixture(params=['db_author_repo', 'mem_author_repo'])
def author_repo(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(params=['db_book_repo', 'mem_book_repo'])
def book_repo(request):
    return request.getfixturevalue(request.param)


def test_create_author(author_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    author_repo.add(author)
    assert len(author_repo.list()) == 1


def test_create_author_duplicate_name(author_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    author_repo.add(author)
    with pytest.raises(RepositoryException):
        author_repo.add(author)


def test_get_author(author_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = author_repo.add(author)

    assert author_repo.get(db_author.id).name == "Juliusz Słowacki"


def test_get_non_existing_author(author_repo):
    with pytest.raises(RepositoryException):
        author_repo.get(0)


def test_delete_author(author_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = author_repo.add(author)

    author_repo.delete(db_author.id)
    with pytest.raises(RepositoryException):
        author_repo.get(db_author.id)


def test_delete_non_existing_author(author_repo):
    with pytest.raises(RepositoryException):
        author_repo.delete(0)


@pytest.mark.parametrize(
    'author_repo, book_repo', [
        ('db_author_repo', 'db_book_repo'),
        ('mem_author_repo', 'mem_book_repo'),
    ],
    indirect=True
)
def test_create_book(author_repo, book_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = author_repo.add(author)

    book = BookCreate(title='Balladyna', author=db_author)
    book_repo.add(book)
    assert len(book_repo.list()) == 1


@pytest.mark.parametrize(
    'author_repo, book_repo', [
        ('db_author_repo', 'db_book_repo'),
        ('mem_author_repo', 'mem_book_repo'),
    ],
    indirect=True
)
def test_create_book_duplicated_author_title_not_allowed(author_repo, book_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = author_repo.add(author)

    book = BookCreate(title='Balladyna', author=db_author)
    book_repo.add(book)
    assert len(book_repo.list()) == 1

    book = BookCreate(title='Balladyna', author=db_author)
    with pytest.raises(RepositoryException):
        book_repo.add(book)


@pytest.mark.parametrize(
    'author_repo, book_repo', [
        ('db_author_repo', 'db_book_repo'),
        ('mem_author_repo', 'mem_book_repo'),
    ],
    indirect=True
)
def test_create_book_same_title_different_author_allowed(author_repo, book_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = author_repo.add(author)

    book = BookCreate(title='Balladyna', author=db_author)
    book_repo.add(book)
    assert len(book_repo.list()) == 1

    author = AuthorCreate(name="Adam Mickiewicz")
    db_author = author_repo.add(author)

    book = BookCreate(title='Balladyna', author=db_author)
    book_repo.add(book)
    assert len(book_repo.list()) == 2


@pytest.mark.parametrize(
    'author_repo, book_repo', [
        ('db_author_repo', 'db_book_repo'),
        ('mem_author_repo', 'mem_book_repo'),
    ],
    indirect=True
)
def test_create_book_same_author_different_tittle_allowed(author_repo, book_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = author_repo.add(author)

    book = BookCreate(title='Balladyna 1', author=db_author)
    book_repo.add(book)
    assert len(book_repo.list()) == 1

    book = BookCreate(title='Balladyna 2', author=db_author)
    book_repo.add(book)
    assert len(book_repo.list()) == 2
