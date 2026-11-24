from typing import Literal

from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: str = Field(..., pattern=r"^\d{13}$", description="13 цифр")
    genre: Literal["fiction", "fantasy", "science", "history"]
    year: int = Field(..., ge=1000, le=2026)
    available: bool = True
    author_id: str = Field(..., description="ID автора")

    # Пользовательский валидатор 1: проверка года издания
    @field_validator("year")
    @classmethod
    def check_year(cls, v: int) -> int:
        if v < 1000 or v > 2026:
            raise ValueError("Год должен быть между 1000 и 2026")
        return v

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    isbn: str | None = Field(None, pattern=r"^\d{13}$")
    genre: Literal["fiction", "fantasy", "science", "history"] | None = None
    year: int | None = Field(None, ge=1000, le=2026)
    available: bool | None = None
    author_id: str | None = None

class BookRead(BookBase):
    id: str