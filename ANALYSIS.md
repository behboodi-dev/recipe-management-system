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
- Supporting optional profile images for users.
- Supporting an optional main image for each recipe.

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

OTP verification is the initial authentication method. The design does not require a permanent OTP field in the `users` table. If persistent OTP verification records are needed during implementation, they should be handled separately from core account and profile information. Such records may include expiration and usage status, and must be managed securely.

### FR-02: User Profiles

The system must allow users to create and manage their profiles. Users may complete profile information, such as their username, email address, display name, bio, and optional profile image, after their initial registration.

A user profile is optional and may be created after account registration. The system will initially support one profile image per user.

### FR-03: Recipe Management

The system must allow users to create and manage their own recipes. Users must be able to view recipes created by other users, but only the recipe owner may edit or delete a recipe.

### FR-04: Cooking Details and Recipe Images

The system must store recipe information, including its title, description, cooking instructions, preparation time, cooking time, and number of servings.

The system must support an optional main image for each recipe. Image files will be stored outside the relational database, while the database will store the corresponding URL or storage path.

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

Personal information associated with deleted accounts will be anonymized according to the account-deletion policy, while the user record is retained to preserve recipe ownership and referential integrity. Specifically, the `phone_number` and `phone_verified_at` will be set to `NULL`, and the associated `user_profiles` record will be deleted. The user's favorite records will be removed, while their recipes will be preserved and attributed to a generic label such as "Deleted User". Deleted accounts must not be able to authenticate or manage content.

---

## 2.1 Design Assumptions and Open Questions

The original project description does not specify every business rule. The following assumptions define the proposed initial scope and should be reviewed before implementation.

### Account and Phone Number Rules

- Users initially authenticate using a phone number and OTP. Password-based authentication is deferred to a future iteration.
- A phone number becomes the user's registered phone number only after successful OTP verification.
- A permanent user account is created only after successful OTP verification.
- Unverified registration attempts do not create records in the `users` table.
- Registered phone numbers must be unique among accounts. Phone numbers should be normalized to a consistent international format before uniqueness is checked.
- Unverified phone numbers and OTP challenges should be handled separately from permanent account records. OTP challenges must have an expiration time and must not be reusable after successful verification.
- A deleted account cannot authenticate or manage content.
- In PostgreSQL, a `UNIQUE` constraint allows multiple `NULL` values. This design is compatible with phone number anonymization, as the `phone_number` is set to `NULL` when an account is deleted.

### Profile Rules

- A profile is optional and may be created after registration.
- A user can have at most one profile.
- A profile may contain an optional profile image.
- When an account is deleted, its `user_profiles` record will be deleted to remove associated profile information. The corresponding `users` record will be retained as a soft-deleted record to preserve recipe ownership.
- The profile-removal behavior is a design decision and should be confirmed before implementation.

### Recipe Visibility and Ownership

- Recipes are publicly viewable, including recipes created by users whose accounts have been deleted.
- Only the owner of an active account may edit or delete their own recipes.
- Personal profile information of deleted accounts is not shown.
- Deleting an account does not delete the recipes owned by that account.

### Recipe Images

- Each recipe may have one optional main image in the initial version.
- Image files are stored outside PostgreSQL. The database stores their URL or storage path.
- Each user may have one optional profile image.
- Support for multiple images per recipe is outside the initial scope.
- **Naming Clarification:** The column names `avatar_url` and `image_url` are used for consistency, but during implementation, it must be explicitly decided whether the stored value is a full URL or a relative storage path/key. This decision will be documented before coding begins.
- When an account is deleted, the user's profile image will be removed from storage when applicable.
- Recipe images will be preserved while the associated recipes remain available.
- The application must handle image replacement and deletion to avoid leaving unused files in storage.

### Ingredient Naming and Reuse

- Each ingredient has one canonical name in the initial version.
- Ingredient names must be unique according to the chosen normalization and comparison rules.
- Alternative names, translations, and synonyms are not supported in the initial version. They may be added later through an ingredient-alias table.
- An ingredient may be used in multiple recipes.
- The same ingredient may appear only once in a recipe in the initial version. If it is needed in multiple parts of the recipe, its quantities must be combined into one ingredient entry.
- If separate quantities are required for different steps, the ingredient relationship design must be extended before implementation.
- The `UNIQUE(name)` constraint alone does not resolve all variations. For example, uppercase/lowercase differences or extra spaces may cause seemingly identical names to be treated as different. A name-normalization rule must be defined during implementation.

### Categories, Units, and Favorites

- Categories and measurement units are shared across the system.
- Each recipe may belong to multiple categories.
- Each recipe ingredient references one predefined measurement unit.
- A user may save multiple recipes as favorites, but the same recipe cannot be saved more than once by the same user.
- Removing a favorite does not delete the recipe itself.

### Database Constraints and Implementation Details

- **Phone Number Consistency:** Since a phone number is only stored after successful OTP verification, the `phone_number` and `phone_verified_at` columns must remain consistent. Both must be `NULL` for an unverified account, and both must be populated (or set to `NULL`) together according to the deletion policy.
- **Phone Verification Consistency:** The `phone_number` and `phone_verified_at` columns must either both contain values or both be `NULL`. This rule should be enforced by a database check constraint where appropriate.
- **Timestamps:** The `created_at` column will be initialized with the current timestamp upon record creation. The `updated_at` column will also be initialized upon creation and must be updated automatically on every record modification. The exact mechanism for updating `updated_at` (application-level logic vs. a database trigger) will be chosen during SQL implementation.
- **Case Insensitivity for Usernames and Emails:** To prevent user confusion and impersonation, uniqueness checks for `username` and `email` will be **case-insensitive**. This means `ChefAli` and `chefali` will be considered the same identifier. The original casing provided by the user will be preserved for display purposes. At the database level, this will be enforced using unique indexes on `LOWER(username)` and `LOWER(email)`. Empty or whitespace-only usernames and email addresses are not valid profile identifiers. Optional values should be stored as `NULL` when not provided.
- **Foreign Key Deletion Behavior:** 
  - When a recipe is physically deleted, its associated `recipe_steps`, `recipe_ingredients`, `recipe_categories`, and `favorites` records should be removed via cascading foreign-key relationships.
  - When a user account is deleted, its recipes must be preserved. Deletion of the user record must not cascade to the `recipes` table.
  - User accounts are soft-deleted during normal account deletion. Physical deletion of a user record is outside the initial scope and must not remove recipes owned by that user.

These assumptions are proposed for the initial version. Any change to them should be documented before database implementation.

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
| `avatar_url` | `TEXT` | Nullable | URL or storage path of the user's profile image |

A user may register and authenticate before completing their profile. A profile record may be created later when the user provides additional information.

The `user_id` column serves as both the primary key and a foreign key, ensuring that each user can have at most one profile.

The profile image is optional; a user must be able to register and complete their profile without uploading an image.

When an account is deleted, its associated `user_profiles` record will be deleted. The corresponding `users` record will be retained as a soft-deleted record, with `phone_number` and `phone_verified_at` set to `NULL`. Recipes owned by the user will be preserved, and the user's favorite records will be removed.

### 3.3 Recipes

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
| `image_url` | `TEXT` | Nullable | URL or storage path of the recipe's main image |
| `created_at` | `TIMESTAMPTZ` | Not Null | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Not Null | Last update timestamp |

Each recipe belongs to one user. A user can create multiple recipes, and all users can view recipes created by other users. Only the recipe owner can edit or delete their own recipes.

In the initial version, one main image is considered per recipe. If multiple images of different cooking steps are needed later, a separate table such as `recipe_images` can be added.

**Design note:** It is recommended not to store the image file directly in PostgreSQL. Files should be kept in image storage, and the database should only store their URL or path. This is a design decision for the initial version, not something required by the original project description.

### 3.4 Recipe Steps

The `recipe_steps` table stores individual cooking instructions in a defined order. Each step belongs to one recipe.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique step identifier |
| `recipe_id` | `BIGINT` | Foreign Key, Not Null | References `recipes.id` |
| `step_number` | `INTEGER` | Not Null, Check > 0 | Position of the step within the recipe |
| `instruction` | `TEXT` | Not Null | Instructions for this step |

A unique constraint on `(recipe_id, step_number)` prevents duplicate step numbers within the same recipe. Steps are retrieved in ascending order of `step_number`.

When a recipe is deleted, its associated steps should also be deleted through a cascading foreign-key relationship.

### 3.5 Ingredients

The `ingredients` table stores the distinct ingredients that can be used in recipes.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique ingredient identifier |
| `name` | `VARCHAR(150)` | Not Null, Unique | Ingredient name |
| `created_at` | `TIMESTAMPTZ` | Not Null | Record creation timestamp |

Each ingredient is stored once and can be referenced by multiple recipes.

### 3.6 Units

The `units` table stores the standardized measurement units available for recipe ingredients.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique unit identifier |
| `name` | `VARCHAR(50)` | Not Null, Unique | Full name of the measurement unit |
| `symbol` | `VARCHAR(20)` | Not Null, Unique | Standard unit symbol or abbreviation |

Example units include Gram (`g`), Milliliter (`ml`), Piece (`piece`), Teaspoon (`tsp`), and Tablespoon (`tbsp`).

### 3.7 Recipe Ingredients

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

### 3.8 Categories

The `categories` table stores the shared categories used to organize recipes.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | Primary Key, Identity | Unique category identifier |
| `name` | `VARCHAR(100)` | Not Null, Unique | Category name |
| `description` | `TEXT` | Nullable | Optional category description |
| `created_at` | `TIMESTAMPTZ` | Not Null | Record creation timestamp |

Categories are shared across the system and can be associated with multiple recipes.

### 3.9 Recipe Categories

The `recipe_categories` table resolves the many-to-many relationship between recipes and categories.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `recipe_id` | `BIGINT` | Primary Key, Foreign Key | References `recipes.id` |
| `category_id` | `BIGINT` | Primary Key, Foreign Key | References `categories.id` |

The combination of `recipe_id` and `category_id` forms a composite primary key. This prevents the same category from being assigned to the same recipe more than once.

Each recipe may belong to multiple categories, and each category may contain multiple recipes.

### 3.10 Favorites

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