from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import uvicorn
from app import book, models
from fastapi import Depends, FastAPI, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="01-task-microservice",
    description="This is the first task of microservices section on the course",
    version="0.1.0",
    contact={
        "name": "Youssef Harby",
        "url": "https://github.com/Youssef-Harby",
        "email": "me@youssefharby.com",
    },
)

origins = [
    "http://localhost:8000",
]


def swagger_ui_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_favicon_url="https://raw.githubusercontent.com/go-swagger/go-swagger/master/docs/favicon.ico",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.4.2/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.4.2/swagger-ui.css",
    )


applications.get_swagger_ui_html = swagger_ui_patch

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(book.router, tags=["Books"], prefix="/api/books")


@app.get("/api/healthchecker")
def health_check(db: SessionLocal = Depends(get_db)):
    try:
        # Perform a simple database query
        db.execute(text("SELECT 1"))
        return {"message": "OK", "database": "up"}
    except OperationalError:
        return {"message": "Service Unhealthy", "database": "down"}, 503


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
