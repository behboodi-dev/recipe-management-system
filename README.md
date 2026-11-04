# Recipe Management System

A full-stack Recipe Management System built with **Python**, **PostgreSQL**, and **SQLAlchemy**. This project includes database design, CRUD operations, and automated testing.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Database Design](#database-design)
- [Design Assumptions & Decisions](#design-assumptions--decisions)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Usage](#usage)

---

## Project Overview

The Recipe Management System allows users to:

- Create and manage user profiles.
- Add and manage cooking recipes, including preparation time, cooking time, and servings.
- Organize recipes into categories.
- Record ingredients with their exact quantities and measurement units.
- Save recipes to a personalized favorites list.

The project is developed in two main phases:

1. **Database Design:** A normalized PostgreSQL database schema (`sql/schema.sql`).
2. **Python Implementation:** SQLAlchemy models, CRUD operations, and automated tests.

---

## Features

-  **PostgreSQL:** PostgreSQL is used as the database management system (DBMS).
-  **10 Normalized Tables:** Includes users, profiles, recipes, steps, ingredients, units, categories, and junction tables.
-  **Data Integrity:** Foreign keys, `CHECK` constraints, and composite primary keys ensure data consistency.
-  **Soft-Delete Policy:** User accounts are anonymized and soft-deleted while preserving recipe ownership.
-  **Case-Insensitive Uniqueness:** Unique indexes on `LOWER(username)` and `LOWER(email)` prevent duplicate usernames and email addresses regardless of letter case.
-  **Automatic Timestamps:** `updated_at` columns are automatically maintained using database triggers.
-  **CRUD Operations:** Create, Read, Update, and Delete operations are implemented for Users, Recipes, and Favorites.
-  **Automated Testing:** Pytest-based tests cover CRUD operations and database constraints.
- **ERD & SQL Schema:** Both the visual Entity-Relationship Diagram and the SQL schema are included in the repository.

---

## Database Design

The database consists of 10 tables divided into core entities and junction tables:

1. **`users`**: Stores core account information, including phone numbers, timestamps, and soft-delete information.
2. **`user_profiles`**: Stores optional profile information, such as usernames, email addresses, bios, and avatar URLs.
3. **`recipes`**: Stores recipe information, including the owner, title, preparation time, cooking time, servings, and image URL.
4. **`recipe_steps`**: Stores ordered cooking instructions for each recipe.
5. **`ingredients`**: Stores a master list of distinct ingredients.
6. **`units`**: Stores standardized measurement units, such as grams (g), milliliters (ml), and teaspoons (tsp).
7. **`categories`**: Stores shared categories used to organize recipes.
8. **`recipe_ingredients`**: Resolves the many-to-many relationship between recipes and ingredients, including quantity and measurement unit.
9. **`recipe_categories`**: Resolves the many-to-many relationship between recipes and categories.
10. **`favorites`**: Resolves the many-to-many relationship between users and their favorite recipes.

---

## Design Assumptions & Decisions

- **PostgreSQL Selection:** PostgreSQL was selected for its robust `TIMESTAMPTZ` support, precise `NUMERIC` data types, and advanced constraint capabilities.
- **Soft Deletion for Users:** When a user deletes their account, the user record is retained with `deleted_at` set. Personal information, such as phone numbers and profile data, is anonymized or removed. However, the user's recipes are preserved to maintain referential integrity.
- **Case-Insensitive Uniqueness:** Usernames and email addresses are checked case-insensitively using unique indexes on `LOWER(username)` and `LOWER(email)` to prevent duplicate accounts and impersonation.
- **Image Storage:** Only image URLs or storage paths are stored in the database. Actual image files are managed externally.
- **Ingredient Normalization:** Ingredient names are unique. If an ingredient is used multiple times in a recipe, its quantities must be combined.
- **Automatic Timestamps:** A PostgreSQL trigger (`set_updated_at`) automatically updates the `updated_at` column whenever a record is modified.

> For a detailed breakdown of functional requirements, business rules, and database constraints, please refer to the `ANALYSIS.md` file in this repository.

---

## Installation & Setup

To run this project locally, you need **Python 3.10+** and **PostgreSQL** installed.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/recipe-management-system.git
cd recipe-management-system
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the Database

```bash
createdb recipe_db
```

Alternatively, you can create the database using PostgreSQL tools such as pgAdmin.

### 5. Run the Database Schema

```bash
psql -d recipe_db -f sql/schema.sql
```

This command creates the database tables, constraints, indexes, and triggers defined in the SQL schema.

### 6. Configure Environment Variables

Create a `.env` file in the project root directory based on `.env.example`.

Example:

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
```

Replace the example credentials with your actual PostgreSQL configuration.

**Important:** Never commit your `.env` file or expose your database credentials in a public repository.

---

## Project Structure

```text
recipe-management-system/
│
├── app/
│   ├── __init__.py
│   ├── database.py             
│   │
│   ├── crud/                   
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── recipe.py
│   │   └── favorite.py
│   │
│   └── models/                
│       ├── __init__.py
│       ├── base.py
│       ├── user.py
│       ├── user_profile.py
│       ├── recipe.py
│       └── favorite.py
│
├── tests/                     
│   ├── __init__.py
│   ├── test_user_model.py
│   ├── test_user_crud.py
│   ├── test_recipe_crud.py
│   ├── test_favorite_crud.py
│   └── ...
│
├── sql/
│   └── schema.sql              
│
├── docs/
│   | 
│   └── screenshots/
│
├── .env.example
├── .gitignore
├── ANALYSIS.md
├── README.md
└── requirements.txt
```

---

## Testing

This project uses **pytest** for automated testing.

The tests cover CRUD operations, model structure, database connectivity, and data integrity constraints.

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Tests

**User CRUD Tests:**

```bash
pytest tests/test_user_crud.py -v
```

**Recipe CRUD Tests:**

```bash
pytest tests/test_recipe_crud.py -v
```

**Favorite CRUD Tests:**

```bash
pytest tests/test_favorite_crud.py -v
```

---

## Usage

### Basic CRUD Example (Python)

The following example demonstrates how to create a user, add a recipe, and retrieve it from the database.

```python
from app.database import SessionLocal
from app.crud.user import create_user, get_user
from app.crud.recipe import create_recipe, get_recipe


# Create a database session
with SessionLocal() as session:

    # Create a user
    user = create_user(
        session,
        phone_number="+989121234567"
    )

    print(f"User created: {user.id}")

    # Create a recipe
    recipe = create_recipe(
        session,
        user_id=user.id,
        title="My First Recipe",
        prep_time_minutes=10,
        cook_time_minutes=20,
        servings=2,
    )

    print(f"Recipe created: {recipe.id}")

    # Retrieve the recipe
    found = get_recipe(session, recipe.id)

    print(f"Found recipe: {found.title}")
```

### Test the Database Connection

To verify that the application can connect to PostgreSQL, run:

```bash
python -m app.database
```

Expected output:

```text
Database connection successful!
Test result: 1
```

---

## Documentation

For more information about the database design, functional requirements, and implementation decisions, see:

- `ANALYSIS.md` – Detailed system analysis and requirements.
- `sql/schema.sql` – PostgreSQL database schema.
