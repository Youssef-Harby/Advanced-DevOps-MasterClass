# Books Microservice API

## Description

This is a FastAPI application for managing books. this is a task from the course [Advanced DevOps MasterClass](#).

---

## Requirements

- Python 3.11
- Poetry
- Docker and Docker Compose

---

## Installation and Setup

### Using Poetry

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Youssef-Harby/Advanced-DevOps-MasterClass.git
   cd Advanced DevOps MasterClass
   ```

2. **Install Dependencies**

   ```bash
   poetry install
   ```

3. **Run the Application**

   ```bash
   poetry run start
   ```

### Using Docker Compose

1. **Go to the Direcory**

   ```bash
   cd /01-task-microservices
   ```

2. **Start Services**

   ```bash
   docker compose up -d
   ```

---

## API Endpoints

### Book Operations

- **GET `/`**: Retrieve a list of books.

  - Query Params: `limit`, `page`, `search`
  - Example: `/api/books?limit=10&page=1&search=python`

- **POST `/`**: Add a new book.

  - Body: `{"title": "New Book", "author": "John Doe"}`

- **PATCH `/{bookId}`**: Update an existing book by its ID.

  - Body: `{"title": "Updated Book", "author": "Jane Doe"}`

- **GET `/{bookId}`**: Retrieve a specific book by its ID.

- **DELETE `/{bookId}`**: Delete a specific book by its ID.

- **DELETE `/`**: Delete all books.

### Health Check

- **GET `/api/healthchecker`**: Check the health status of the application and db.

---
