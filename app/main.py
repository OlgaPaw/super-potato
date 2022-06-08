from typing import Union

from fastapi import FastAPI

books_api = FastAPI()


@books_api.get("/")
def home():
    return {"Hello": "World"}
