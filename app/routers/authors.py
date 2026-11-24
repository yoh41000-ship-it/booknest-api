from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import Pagination
from app.repositories import db
from app.schemas.author import AuthorCreate, AuthorRead
from app.schemas.book import BookRead

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=list[AuthorRead])
def get_authors(pagination: Pagination = Depends()):  # noqa: B008
    authors = list(db.authors_db.values())
    return authors[pagination.offset : pagination.offset + pagination.size]

@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate):
    new_author = author.model_dump()
    new_author["id"] = db.generate_id()
    db.authors_db[new_author["id"]] = new_author
    return new_author

@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: str):  # <-- Вот здесь должно быть get_author, а не get_authors!
    if author_id not in db.authors_db:
        raise HTTPException(status_code=404, detail="Author not found")
    return db.authors_db[author_id]

@router.get("/{author_id}/books", response_model=list[BookRead])
def get_author_books(author_id: str):
    if author_id not in db.authors_db:
        raise HTTPException(status_code=404, detail="Author not found")
    return [b for b in db.books_db.values() if b["author_id"] == author_id]