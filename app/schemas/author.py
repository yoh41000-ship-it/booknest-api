
from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Имя автора")
    bio: str | None = Field(None, max_length=500)

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    bio: str | None = Field(None, max_length=500)

class AuthorRead(AuthorBase):
    id: str