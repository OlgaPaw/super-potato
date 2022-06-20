# pylint: disable=redefined-outer-name

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters import database, db_repository, mem_repository
from app.domain.services import AuthorCreate, BookCreate


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