# Recipe Management System

A Recipe Management System built with **Python**, **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**.

This project focuses on relational database design, data integrity, backend development, and RESTful API implementation. It provides a structured architecture that separates API routes, business logic, database models, and data validation.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Database Design](#database-design)
- [Design Decisions](#design-decisions)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Database Connection Test](#database-connection-test)
- [Documentation](#documentation)
- [Security Notes](#security-notes)
- [License](#license)

---

## Project Overview

The Recipe Management System is designed to help users create, manage, organize, and save cooking recipes.

The system's database and backend architecture support:

- User accounts and optional user profiles.
- Recipe creation and management.
- Preparation time, cooking time, and serving information.
- Ordered cooking instructions.
- Ingredients with quantities and measurement units.
- Recipe categorization.
- Personalized favorite recipes.

The project is developed in three main phases:

1. **Database Design:** Designing a normalized PostgreSQL database schema.
2. **Python Implementation:** Implementing SQLAlchemy ORM models, database connectivity, and service-layer operations.
3. **API Development:** Building RESTful API endpoints using FastAPI.

---

## Features

- **PostgreSQL:** Relational database management system.
- **10 Database Tables:** A normalized schema covering users, profiles, recipes, ingredients, units, categories, and related tables.
- **SQLAlchemy ORM:** Mapping database tables to Python classes.
- **Data Integrity:** Foreign keys, check constraints, unique indexes, and composite primary keys.
- **Soft Deletion:** User accounts are designed to be soft-deleted to preserve recipe ownership and referential integrity.
- **Case-Insensitive Uniqueness:** Unique indexes prevent duplicate values regardless of letter case for supported fields.
- **Automatic Timestamps:** Database triggers maintain `updated_at` values for supported tables.
- **Pydantic Schemas:** Request validation and response serialization.
- **Service Layer:** Business logic is separated from API route handlers.
- **FastAPI:** API development with automatically generated interactive documentation.
- **Automated Testing:** Tests for supported models, database operations, and data integrity rules.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database interaction |
| Psycopg | PostgreSQL database driver |
| Pydantic | Data validation and serialization |
| python-dotenv | Environment variable management |
| Uvicorn | ASGI application server |
| Pytest | Automated testing |

---

## Database Design

The database consists of 10 tables:

1. **`users`**: Stores core account information, phone verification data, timestamps, and soft-deletion information.
2. **`user_profiles`**: Stores optional profile information, such as usernames, email addresses, bios, and avatar URLs.
3. **`recipes`**: Stores recipe information, including ownership, title, description, preparation time, cooking time, servings, and image URL.
4. **`recipe_steps`**: Stores ordered cooking instructions for recipes.
5. **`ingredients`**: Stores the master list of ingredients.
6. **`units`**: Stores standardized measurement units, such as grams, milliliters, and teaspoons.
7. **`categories`**: Stores recipe categories.
8. **`recipe_ingredients`**: Connects recipes to ingredients and stores quantities and measurement units.
9. **`recipe_categories`**: Connects recipes to multiple categories.
10. **`favorites`**: Stores the relationship between users and their favorite recipes.

The database schema is defined in:

`sql/schema.sql`

---

## Design Decisions

### PostgreSQL

PostgreSQL was selected because of its support for relational integrity, advanced constraints, transactions, and timezone-aware timestamps.

### User Soft Deletion

User accounts are designed to be soft-deleted rather than physically removed.

This approach preserves recipe ownership and referential integrity while allowing account-related information to be handled according to the project's business rules.

### Case-Insensitive Uniqueness

Case-insensitive unique indexes are used for supported fields, such as usernames, email addresses, and ingredient names, as defined in the database schema.

### Image Storage

Actual image files are stored outside the database. The database stores only image URLs or storage paths.

### Ingredient Normalization

Ingredients are stored separately from recipes. The `recipe_ingredients` table connects recipes to ingredients and stores their quantities and measurement units.

### Automatic Timestamps

Database triggers maintain `updated_at` values for supported tables when records are modified.

For additional details about functional requirements, business rules, and database constraints, see `ANALYSIS.md`.

---

## Project Structure

The project follows a layered architecture to separate API handling, business logic, data validation, and database operations.

```text
recipe_management/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── recipes.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── user_profile.py
│   │   ├── recipe.py
│   │   └── favorite.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── recipe.py
│   │   └── favorite.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── user.py
│       ├── recipe.py
│       ├── recipe_service.py
│       └── favorite.py
│
├── docs/
│   └── screenshots/
│
├── sql/
│   └── schema.sql
│
├── tests/
│   ├── __init__.py
│   ├── test_user_model.py
│   ├── test_user_crud.py
│   ├── test_user_profile_model.py
│   ├── test_recipe_model.py
│   ├── test_recipe_crud.py
│   ├── test_favorite_model.py
│   └── test_favorite_crud.py
│
├── .env.example
├── .gitignore
├── ANALYSIS.md
├── README.md
├── requirements.txt
└── TEST_RESULTS.md
```

**Note:** The `.env` file contains local environment variables and must not be committed to Git. The `.venv/` directory contains the local Python virtual environment and is also excluded from version control.

---

## Installation and Setup

### Prerequisites

Make sure the following software is installed:

- Python 3.10 or later.
- PostgreSQL.
- Git.

### 1. Clone the Repository

```bash
git clone https://github.com/behboodi-dev/recipe-management-system.git

cd recipe_management
```

Replace `YOUR_USERNAME` with your actual GitHub username and use the repository's actual URL.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the PostgreSQL Database

Using the PostgreSQL command line:

```bash
createdb recipe_db
```

Alternatively, create a database named `recipe_db` using pgAdmin.

### 6. Apply the Database Schema

Run the SQL schema file:

```bash
psql -d recipe_db -f sql/schema.sql
```

Make sure PostgreSQL is running and the database exists before executing this command.

---

## Environment Configuration

Create a `.env` file in the project root based on `.env.example`.

Example configuration:

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=recipe_db
```

Update the values according to your local PostgreSQL configuration.

**Security Note:** Never commit `.env` to Git or expose database credentials in a public repository.

The `.gitignore` file should exclude:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
```

---

## Running the Application

Make sure your virtual environment is activated and the database configuration is correct.

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

Once the server is running, open:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Swagger UI allows you to inspect available endpoints, provide request data, execute API calls, and review responses.

---

## API Endpoints

Recipe API routes are defined in:

`app/api/routes/recipes.py`

The available endpoints should be checked in the running application's Swagger UI at `/docs`.

The Recipe API is intended to support operations such as:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/recipes/` | Retrieve the recipe list |
| GET | `/recipes/{recipe_id}` | Retrieve a recipe by ID |
| POST | `/recipes/` | Create a new recipe |
| PUT | `/recipes/{recipe_id}` | Update an existing recipe |
| DELETE | `/recipes/{recipe_id}` | Delete a recipe |

The table describes the intended Recipe API operations. Confirm that each operation is registered and working in Swagger UI before treating it as implemented.

---

## Testing

The project uses Pytest for automated testing.

To run the available test suite:

```bash
pytest tests/ -v
```

To run a specific test module:

```bash
pytest tests/test_user_model.py -v
```

Other test modules can be executed individually.

The test results and previously performed checks are documented in:

`TEST_RESULTS.md`

---

## Database Connection Test

To verify that the application can connect to PostgreSQL, run:

```bash
python -m app.database
```

Expected output:

```text
Database connection successful!
Test result: 1
```

This test verifies that the application can establish a database connection and execute a simple SQL query.

---

## Documentation

Additional project documentation:

- **`ANALYSIS.md`** — Functional requirements, business rules, and system analysis.
- **`sql/schema.sql`** — PostgreSQL database schema and constraints.
- **`docs/screenshots/`** — Database and project screenshots.
- **`TEST_RESULTS.md`** — Results of database and application tests.

---

## Security Notes

- Database credentials must be stored in `.env`, not directly in source code.
- The `.env` file must be excluded from Git.
- Any temporary user-identification mechanism used during development must be replaced with proper authentication before production deployment.
- Database constraints and ownership checks should be enforced by the backend and database, not only by client-side validation.

---

## License

This project is currently under development. A license can be added when the project's distribution terms are decided.