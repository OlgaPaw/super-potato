Run
===

Start the project ::

    poetry install
    poetry shell
    alembic upgrade head   
    uvicorn app.main:app
