from typing import Optional
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    "book1": {"title": "Title One", "author": "Author One"},
    "book2": {"title": "Title Two", "author": "Author Two"},
    "book3": {"title": "Title Three", "author": "Author Three"},
    "book4": {"title": "Title Four", "author": "Author Four"},
    "book5": {"title": "Title Five", "author": "Author Five"},
}

# Query Parameters


@app.get("/")
async def readAllBooks(skipBook: Optional[str] = None):
    if skipBook:
        newBooks = BOOKS.copy()
        del newBooks[skipBook]
        return newBooks
    return BOOKS


@app.get("/book")
async def readBook(bookName: str):
    return BOOKS[bookName]


@app.post("/")
async def createBook(bookTitle, bookAuthor):
    currentBookId = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split("k")[-1])
            if x > currentBookId:
                currentBookId = x
    BOOKS[f'book{currentBookId + 1}'] = {"title": bookTitle,
                                         "author": bookAuthor}
    return BOOKS[f'book{currentBookId + 1}']


@app.put("/{bookName}")
async def updateBook(bookName: str, bookTitle: str, bookAuthor: str):
    bookInformation = {"title": bookTitle, "author": bookAuthor}
    BOOKS[bookName] = bookInformation
    return bookInformation


@app.delete("/")
async def deleteBook(bookName: str):
    if not bookName in BOOKS:
        return {"error": f"The book {bookName} does not exist."}
    del BOOKS[bookName]
    return {"message": f"Deleted book {bookName}"}

# @app.get("/{bookName}")
# async def readBook(bookName: str):
#     return BOOKS[bookName]
