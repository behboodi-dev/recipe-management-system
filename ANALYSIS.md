# Recipe Management System

## 1. Project Overview

### 1.1 Purpose

The Recipe Management System is designed to allow users to create profiles, add and manage cooking recipes, organize recipes into categories, record ingredients and cooking details, and save their favorite recipes.

### 1.2 Target Users

The system is intended for users who want to create, manage, organize, and save cooking recipes.

### 1.3 Main Features

The main features of the system include:

- Creating and managing user profiles.
- Adding and managing cooking recipes.
- Storing recipe details, including preparation time, cooking time, servings, and instructions.
- Organizing recipes into categories.
- Recording ingredients and their quantities for each recipe.
- Saving and accessing favorite recipes.

### 1.4 Project Scope

This project focuses on analyzing and designing a relational database to support the system's core features. The database design will define the required entities, their attributes, relationships, and data integrity constraints.

**Selected DBMS: PostgreSQL**

PostgreSQL was selected as the database management system for this project. This choice is based on the following reasons:

- It provides robust support for relational data integrity through foreign keys and check constraints.
- It offers native support for `TIMESTAMPTZ` (timestamp with time zone), which is essential for recording accurate timestamps across different time zones.
- It supports the `NUMERIC` data type with high precision, which is required for storing ingredient quantities.
- It provides strong support for composite primary keys and cascading foreign-key relationships, which are used in the junction tables.
- It is a widely adopted, open-source, and well-documented database system suitable for both development and production environments.

---

## 2. Functional Requirements

### FR-01: User Registration and Authentication

The system must allow users to register and authenticate using a phone number and a one-time password (OTP). Password-based authentication is outside the initial implementation scope and may be introduced in a later version.

### FR-02: User Profiles

The system must allow users to create and manage their profiles. Users may complete profile information, such as their username and email address, after their initial registration.

### FR-03: Recipe Management

The system must allow users to create and manage their own recipes. Users must be able to view recipes created by other users, but only the recipe owner may edit or delete a recipe.

### FR-04: Cooking Details

The system must store recipe information, including its title, description, cooking instructions, preparation time, cooking time, and number of servings.

### FR-05: Recipe Categories

The system must allow a recipe to be associated with multiple categories and support retrieving recipes by category.

### FR-06: Recipe Ingredients

The system must store the ingredients used in each recipe, including the quantity and unit of measurement for each ingredient.

### FR-07: Favorite Recipes

The system must allow users to add recipes to their favorites, view their saved favorites, and remove recipes from their favorites. A user must not have duplicate favorite entries for the same recipe.

### Notes

These requirements are based on the initial project description and the design decisions made during analysis. Details not specified by the original description must be treated as design assumptions and documented for review before implementation.

### Account Deletion Policy

The system must preserve recipes when a user deletes their account.

The initial design will use a soft-delete approach for user accounts. Instead of immediately removing the user record, the system will mark the account as deleted while retaining the record required to preserve recipe ownership and referential integrity.

The `users` table will include a nullable `deleted_at` timestamp. A non-null value indicates that the account has been marked as deleted.

Personal information associated with deleted accounts will be anonymized according to the account-deletion policy, while the user record is retained to preserve recipe ownership and referential integrity.

Recipes belonging to deleted accounts must remain available according to the system's visibility rules. Deleted accounts must not be able to authenticate or manage content.

---

## 3. Entity Definitions

### 3.1 Users

The `users` table stores the core account information required to identify and manage a user.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique identifier for each user |
| `phone_number` | `VARCHAR(20)` | Unique; nullable for account anonymization | User's phone number |
| `phone_verified_at` | `TIMESTAMPTZ` | Nullable | Timestamp when the phone number was verified |
| `created_at` | `TIMESTAMPTZ` | Not Null | Account creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Not Null | Last account update timestamp |
| `deleted_at` | `TIMESTAMPTZ` | Nullable | Timestamp when the account was marked as deleted |

The system will initially use phone-number verification through OTP for authentication. Password-based authentication may be introduced in a later version.

OTP codes are temporary authentication data and will not be stored as permanent user profile attributes.

Accounts will use a soft-delete policy. When an account is deleted, personal information will be anonymized while the user record is retained to preserve recipe ownership and referential integrity.

### 3.2 User Profiles

The `user_profiles` table stores optional profile information separately from the core account data.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `user_id` | `BIGINT` | Primary Key, Foreign Key | References `users.id` |
| `username` | `VARCHAR(50)` | Unique when provided | User's chosen username |
| `email` | `VARCHAR(254)` | Unique when provided | User's email address |
| `display_name` | `VARCHAR(100)` | Nullable | Name displayed to other users |
| `bio` | `TEXT` | Nullable | Optional profile description |

A user may register and authenticate before completing their profile. A profile record may be created later when the user provides additional information.

The `user_id` column serves as both the primary key and a foreign key, ensuring that each user can have at most one profile.

Profile information must be anonymized or removed according to the account-deletion policy when the associated account is deleted.

### 3.3 Authentication Scope

OTP verification is the initial authentication method. The design does not require a permanent OTP field in the `users` table.

If persistent OTP verification records are needed during implementation, they should be handled separately from core account and profile information. Such records may include expiration and usage status, and must be managed securely.

### 3.4 Recipes

The `recipes` table stores the main information for each recipe.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique recipe identifier |
| `user_id` | `BIGINT` | Foreign Key, Not Null | References `users.id` |
| `title` | `VARCHAR(200)` | Not Null | Recipe title |
| `description` | `TEXT` | Nullable | Optional recipe description |
| `prep_time_minutes` | `INTEGER` | Not Null, Check >= 0 | Preparation time in minutes |
| `cook_time_minutes` | `INTEGER` | Not Null, Check >= 0 | Cooking time in minutes |
| `servings` | `INTEGER` | Not Null, Check > 0 | Number of servings |
| `created_at` | `TIMESTAMPTZ` | Not Null | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Not Null | Last update timestamp |

Each recipe belongs to one user. A user can create multiple recipes, and all users can view recipes created by other users. Only the recipe owner can edit or delete their own recipes.

### 3.5 Recipe Steps

The `recipe_steps` table stores individual cooking instructions in a defined order. Each step belongs to one recipe.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique step identifier |
| `recipe_id` | `BIGINT` | Foreign Key, Not Null | References `recipes.id` |
| `step_number` | `INTEGER` | Not Null, Check > 0 | Position of the step within the recipe |
| `instruction` | `TEXT` | Not Null | Instructions for this step |

A unique constraint on `(recipe_id, step_number)` prevents duplicate step numbers within the same recipe. Steps are retrieved in ascending order of `step_number`.

When a recipe is deleted, its associated steps should also be deleted through a cascading foreign-key relationship.

### 3.6 Ingredients

The `ingredients` table stores the distinct ingredients that can be used in recipes.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique ingredient identifier |
| `name` | `VARCHAR(150)` | Not Null, Unique | Ingredient name |
| `created_at` | `TIMESTAMPTZ` | Not Null | Record creation timestamp |

Each ingredient is stored once and can be referenced by multiple recipes.

### 3.7 Units

The `units` table stores the standardized measurement units available for recipe ingredients.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique unit identifier |
| `name` | `VARCHAR(50)` | Not Null, Unique | Full name of the measurement unit |
| `symbol` | `VARCHAR(20)` | Not Null, Unique | Standard unit symbol or abbreviation |

Example units include Gram (`g`), Milliliter (`ml`), Piece (`piece`), Teaspoon (`tsp`), and Tablespoon (`tbsp`).

### 3.8 Recipe Ingredients

The `recipe_ingredients` table resolves the many-to-many relationship between recipes and ingredients. It also stores the quantity and measurement unit required for each ingredient in a specific recipe.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique recipe-ingredient record identifier |
| `recipe_id` | `BIGINT` | Foreign Key, Not Null | References `recipes.id` |
| `ingredient_id` | `BIGINT` | Foreign Key, Not Null | References `ingredients.id` |
| `quantity` | `NUMERIC(10,3)` | Not Null, Check > 0 | Quantity of the ingredient |
| `unit_id` | `BIGINT` | Foreign Key, Not Null | References `units.id` |

A unique constraint on `(recipe_id, ingredient_id)` prevents an ingredient from being recorded more than once in the same recipe.

The `unit_id` foreign key ensures that each recipe ingredient uses a predefined measurement unit rather than arbitrary text. Ingredient quantities and units are stored in the junction table because they depend on the specific recipe-ingredient relationship.

### 3.9 Categories

The `categories` table stores the shared categories used to organize recipes.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique category identifier |
| `name` | `VARCHAR(100)` | Not Null, Unique | Category name |
| `description` | `TEXT` | Nullable | Optional category description |
| `created_at` | `TIMESTAMPTZ` | Not Null | Record creation timestamp |

Categories are shared across the system and can be associated with multiple recipes.

### 3.10 Recipe Categories

The `recipe_categories` table resolves the many-to-many relationship between recipes and categories.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `recipe_id` | `BIGINT` | Primary Key, Foreign Key | References `recipes.id` |
| `category_id` | `BIGINT` | Primary Key, Foreign Key | References `categories.id` |

The combination of `recipe_id` and `category_id` forms a composite primary key. This prevents the same category from being assigned to the same recipe more than once.

Each recipe may belong to multiple categories, and each category may contain multiple recipes.

### 3.11 Favorites

The `favorites` table stores the recipes that users have saved as favorites.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `user_id` | `BIGINT` | Primary Key, Foreign Key, Not Null | References `users.id` |
| `recipe_id` | `BIGINT` | Primary Key, Foreign Key, Not Null | References `recipes.id` |
| `created_at` | `TIMESTAMPTZ` | Not Null | Timestamp when the recipe was added to favorites |

The combination of `user_id` and `recipe_id` forms a composite primary key. This prevents a user from adding the same recipe to their favorites more than once.

A user can save multiple recipes, and a recipe can be saved by multiple users. Users can view their saved recipes and remove recipes from their favorites without modifying or deleting the recipes themselves.

When a recipe is physically deleted, its associated favorite records should also be deleted through a cascading foreign-key relationship.

When a user deletes their account, the account is soft-deleted and the user's recipes are preserved. The user's favorite records should be removed as part of the account-deletion process.

These deletion behaviors are design assumptions and should be confirmed before implementation.