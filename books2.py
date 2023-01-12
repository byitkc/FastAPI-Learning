from typing import Optional
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status,
    Form,
    Header,
)
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return: int):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        title="Description of the book", min_length=1, max_length=255)
    rating: int = Field(ge=0, le=100)

    class Config:
        schema_extra = {
            "example": {
                "id": uuid4(),
                "title": "Book Title",
                "author": "Book's Author",
                "description": "A good book description",
                "rating": 75,
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        None, title="Description of the book", min_length=1, max_length=255)

    class Config:
        schema_extra = {
            "example": {
                "id": uuid4(),
                "title": "Book Title",
                "author": "Book's Author",
                "description": "A good book description",
            }
        }


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(
    request: Request,
    exception: NegativeNumberException
):
    return JSONResponse(
        status_code=418,
        content={"message": f"Cannot return {exception.books_to_return} books"}
    )


@app.post("/login")
async def login(book_id: UUID, username: str = Header(None), password: str = Header(None)):
    if username != "FastAPIUser" or password != "test1234!":
        raise HTTPException(status_code=403, detail="Invalid User", headers={
            "X-Header-Error": "Invalid User"})
    book = await read_book(book_id)
    return book


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) == 0:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise raise_item_not_found()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise raise_item_not_found()


@app.post("/book", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/book/{book_id}")
async def update_book(book_id: UUID, book: Book):
    i = 0
    for x in BOOKS:
        if x.id == book_id:
            BOOKS[i] = book
            return BOOKS[i]
        i += 1
    raise raise_item_not_found()


@app.delete("/book/{book_id}")
async def delete_book(book_id: UUID):
    i = 0
    for x in BOOKS:
        if x.id == book_id:
            del BOOKS[i]
            return {"message": f"Deleted book ID: {book_id}"}
    raise raise_item_not_found()


def raise_item_not_found():
    return HTTPException(status_code=404, detail=f"Book not found", headers={
        "X-Header-Error": "Nothing to be seen at the UUID"})


def create_books_no_api():
    book1 = Book(id=uuid4(), title="Title 1", author="Author 1",
                 description="Description 1", rating=60)
    book2 = Book(id=uuid4(), title="Title 2", author="Author 2",
                 description="Description 2", rating=60)
    book3 = Book(id=uuid4(), title="Title 3", author="Author 3",
                 description="Description 3", rating=60)
    book4 = Book(id=uuid4(), title="Title 4", author="Author 4",
                 description="Description 4", rating=60)
    book5 = Book(id=uuid4(), title="Title 5", author="Author 5",
                 description="Description 5", rating=60)
    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)
    BOOKS.append(book5)
