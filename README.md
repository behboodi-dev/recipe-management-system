# Recipe Management System

A relational database design and analysis project for a Recipe Management System, built with **PostgreSQL**. This project focuses on defining the required entities, their attributes, relationships, and data integrity constraints to support a full-featured cooking application.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Database Design](#database-design)
- [Design Assumptions & Decisions](#design-assumptions--decisions)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Testing](#testing)

---

## Project Overview

The Recipe Management System is designed to allow users to:
- Create and manage user profiles.
- Add and manage cooking recipes with detailed information (prep time, cook time, servings, etc.).
- Organize recipes into multiple categories.
- Record ingredients and their exact quantities and units.
- Save recipes to a personalized favorites list.

This project is currently in the **database design and analysis phase**. The goal is to produce a robust, normalized, and scalable relational schema that will serve as the foundation for a future application.

---

## Features

-  **PostgreSQL** as the selected DBMS.
-  **10 fully normalized tables** (Users, Profiles, Recipes, Steps, Ingredients, Units, Categories, and junction tables).
-  **Data Integrity**: Strict foreign keys, `CHECK` constraints, and composite primary keys.
-  **Soft-Delete Policy**: User accounts are anonymized and soft-deleted to preserve recipe ownership.
-  **Case-Insensitive Uniqueness**: Enforced via unique indexes on `LOWER(username)` and `LOWER(email)`.
-  **Automatic Timestamps**: `updated_at` columns are managed automatically via database triggers.
-  **ERD & SQL Schema**: Complete visual and code-based schema available in the repository.

---

## Database Design

The database consists of 10 tables divided into core entities and junction tables:

1.  **`users`**: Core account data (phone number, timestamps, soft-delete flag).
2.  **`user_profiles`**: Optional profile info (username, email, bio, avatar).
3.  **`recipes`**: Main recipe data (owner, title, times, servings, image).
4.  **`recipe_steps`**: Ordered instructions for each recipe.
5.  **`ingredients`**: Master list of distinct ingredients.
6.  **`units`**: Standardized measurement units (g, ml, tsp, etc.).
7.  **`categories`**: Shared categories for organizing recipes.
8.  **`recipe_ingredients`**: Resolves the many-to-many relationship between recipes and ingredients (includes quantity and unit).
9.  **`recipe_categories`**: Resolves the many-to-many relationship between recipes and categories.
10. **`favorites`**: Resolves the many-to-many relationship between users and their favorite recipes.

---

## Design Assumptions & Decisions

The following design decisions were made to ensure data integrity and a realistic application flow:

- **PostgreSQL Selected:** Chosen for its robust `TIMESTAMPTZ`, `NUMERIC` precision, and advanced constraint support.
- **Soft-Deletion for Users:** When a user deletes their account, their record is retained (with `deleted_at` set), and their personal info (phone, profile) is anonymized/removed. However, their **recipes are preserved** to maintain referential integrity.
- **Case-Insensitive Uniqueness:** Usernames and emails are checked case-insensitively (using unique indexes on `LOWER(...)`) to prevent user confusion and impersonation.
- **Image Storage:** Only image URLs or storage paths are stored in the database. Actual image files are handled externally.
- **Ingredient Normalization:** Ingredient names are unique. If a recipe uses an ingredient multiple times, quantities must be combined.
- **Automatic Timestamps:** A PostgreSQL trigger (`set_updated_at`) automatically updates the `updated_at` column on any modification.

> For a full detailed breakdown of all functional requirements and constraints, please refer to the `ANALYSIS.md` file in this repository.

---

## Installation & Setup

To run this database schema locally, you need PostgreSQL installed.

```bash
# 1. Create the database
createdb recipe_db

# 2. Run the schema script
psql -d recipe_db -f sql/schema.sql