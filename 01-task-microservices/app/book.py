from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.exc import OperationalError
from .database import get_db

router = APIRouter()


@router.get("/")
def get_books(
    db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ""
):
    try:
        skip = (page - 1) * limit
        total = db.query(models.Book).filter(models.Book.title.contains(search)).count()
        books = (
            db.query(models.Book)
            .filter(models.Book.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )
        return {
            "status": "success",
            "total": total,
            "results": len(books),
            "books": books,
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


# Error handling included: added try-except to handle database errors
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(payload: schemas.BookBaseSchema, db: Session = Depends(get_db)):
    try:
        new_book = models.Book(**payload.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return {"status": "success", "book": new_book}
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


# Error handling included: added try-except to handle database errors
@router.patch("/{bookId}")
def update_book(
    bookId: str, payload: schemas.BookBaseSchema, db: Session = Depends(get_db)
):
    try:
        book_query = db.query(models.Book).filter(models.Book.id == bookId)
        db_book = book_query.first()

        if not db_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No book with this id: {bookId} found",
            )

        update_data = payload.dict(exclude_unset=True)
        book_query.filter(models.Book.id == bookId).update(
            update_data, synchronize_session=False
        )
        db.commit()
        db.refresh(db_book)
        return {"status": "success", "book": db_book}
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


@router.get("/{bookId}")
def get_book(bookId: str, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter(models.Book.id == bookId).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No book with this id: {bookId} found",
            )
        return {"status": "success", "book": book}
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


@router.delete("/{bookId}")
def delete_book(bookId: str, db: Session = Depends(get_db)):
    try:
        book_query = db.query(models.Book).filter(models.Book.id == bookId)
        book = book_query.first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No book with this id: {bookId} found",
            )
        book_query.delete(synchronize_session=False)
        db.commit()
        return {"status": "success", "message": "Book deleted successfully"}
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


@router.delete("/")
def delete_all_books(db: Session = Depends(get_db)):
    try:
        # Delete all book records
        db.query(models.Book).delete(synchronize_session=False)
        db.commit()
        return {"status": "success", "message": "All books deleted successfully"}
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )
