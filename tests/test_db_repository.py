# pylint: disable=redefined-outer-name

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.database import Base
from app.adapters.db_repository import AuthorRepository, BookRepository
from app.domain.services import AuthorCreate, BookCreate


@pytest.fixture
def test_db():
    sqlalchemy_database_url = "sqlite:///./test.db"
    engine = create_engine(sqlalchemy_database_url, connect_args={"check_same_thread": False})
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    yield test_session()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def author_repo(test_db):
    return AuthorRepository(test_db)


@pytest.fixture
def book_repo(test_db):
    return BookRepository(test_db)


def test_create_author(author_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    author_repo.add(author)
    assert len(author_repo.list()) == 1


def test_create_book(author_repo, book_repo):
    author = AuthorCreate(name="Juliusz Słowacki")
    db_author = author_repo.add(author)

    book = BookCreate(title='Balladyna', author=db_author)
    book_repo.add(book)
    assert len(book_repo.list()) == 1
