Run
===

Requirements ::
    python 3.10+
    pip install poetry

Start the project ::

    poetry install
    poetry shell
    alembic upgrade head   
    uvicorn app.main:books_api --port 7777

Open your browser to: http://127.0.0.1:7777/docs

To browse DB data use `pycharm Database tool <https://www.jetbrains.com/help/pycharm/sqlite.html>`_ or `sqlite3`::

    sqlite3 sql_app.db