Run
===

Requirements ::

    python 3.7+
    pip install poetry

`poetry` is a package manager - a tool that helps to install the right dependencies for the project. 
See https://python-poetry.org/docs/

First run ::

    which python3.7                         # get the path for python3.7 or higher
    poetry env use /full/path/to/python3.7  # Select the right python version
    poetry install                          # install the dependencies
    poetry run alembic upgrade head         # create a database structure

Start the project ::

    poetry run uvicorn app.main:books_api --port 7777

Open your browser to: http://127.0.0.1:7777/docs

To browse DB data use `pycharm Database tool <https://www.jetbrains.com/help/pycharm/sqlite.html>`_ or `sqlite3`::

    sqlite3 sql_app.db

Development ::

    pre-commit install # install git commit hooks