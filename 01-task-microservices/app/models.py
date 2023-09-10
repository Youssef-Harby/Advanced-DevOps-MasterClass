from .database import Base as db
from sqlalchemy import Column, Integer, DateTime, func, String, Boolean


class Base(db):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    createdAt = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updatedAt = Column(DateTime(timezone=True), default=None, onupdate=func.now())


class Book(Base):
    __tablename__ = "book"
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=True)
    published = Column(Boolean, nullable=False, default=True)
