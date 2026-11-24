from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import Pagination
from app.repositories import db
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=dict)
def get_books(
    q: str | None = None,
    genre: str | None = None,
    available_only: bool = False,
    sort: Literal["title", "-title", "year", "-year"] = "title",
    pagination: Pagination = Depends()  # noqa: B008
):
    books = list(db.books_db.values())
    # Фильтрация
    if q:
        books = [b for b in books if q.lower() in b["title"].lower()]
    if genre:
        books = [b for b in books if b["genre"] == genre]
    if available_only:
        books = [b for b in books if b["available"]]
    
    # Сортировка
    reverse = sort.startswith("-")
    sort_field = sort.lstrip("-")
    books.sort(key=lambda x: x[sort_field], reverse=reverse)

    total = len(books)
    paginated_books = books[pagination.offset : pagination.offset + pagination.size]
    
    return {"items": paginated_books, "total": total, "page": pagination.page, "size": pagination.size}

@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: str):
    if book_id not in db.books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return db.books_db[book_id]

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    # Проверка на дубликат ISBN
    for b in db.books_db.values():
        if b["isbn"] == book.isbn:
            raise HTTPException(status_code=409, detail="Book with this ISBN already exists")
    
    new_book = book.model_dump()
    new_book["id"] = db.generate_id()
    db.books_db[new_book["id"]] = new_book
    return new_book

@router.patch("/{book_id}", response_model=BookRead)
def update_book(book_id: str, book_update: BookUpdate):
    if book_id not in db.books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    
    stored_book = db.books_db[book_id]
    update_data = book_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        stored_book[key] = value
        
    db.books_db[book_id] = stored_book
    return stored_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str):
    if book_id not in db.books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del db.books_db[book_id]
