from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class BookBaseSchema(BaseModel):
    id: int = Field(..., title="ID of the book (required)")
    title: str = Field(..., title="Title of the book (required)")
    content: str | None = None
    category: str | None = None
    published: bool = Field(..., title="Is the book published? (required)")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListBookResponse(BaseModel):
    status: str
    results: int
    books: List[BookBaseSchema]
