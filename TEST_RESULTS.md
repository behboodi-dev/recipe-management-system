# Test Results — Recipe Management System

## 1. Overview

- **Project:** Recipe Management System
- **Database Management System:** PostgreSQL
- **Status:** All executed tests passed
- **Purpose:** Verify table operations, data integrity constraints, relationships, and automatic timestamp updates.

## 2. Test Summary

| Test | Description | Expected Result | Result |
|---|---|---|---|
| 1 | Insert a user using default values | User is created and an ID is generated automatically | PASS |
| 2 | Insert a user profile | Profile is created successfully | PASS |
| 3 | Insert a duplicate username with different casing and surrounding spaces | Database rejects the duplicate username | PASS |
| 4 | Query units and ingredients | Existing records are returned, or empty results are returned if no records exist | PASS |
| 5 | Insert a recipe with valid values | Recipe is created successfully | PASS |
| 6 | Insert recipes with negative preparation time or zero servings | Database rejects invalid values | PASS |
| 7 | Insert a recipe step and repeat the same step number for the same recipe | First insert succeeds; duplicate step number is rejected | PASS |
| 8 | Insert a measurement unit and an ingredient | Both records are created successfully | PASS |
| 9 | Associate an ingredient with a recipe, then repeat the same association | First insert succeeds; duplicate association is rejected | PASS |
| 10 | Insert a recipe ingredient with quantity zero | Database rejects the invalid quantity | PASS |
| 11 | Create a category and associate it with a recipe, then repeat the association | First association succeeds; duplicate association is rejected | PASS |
| 12 | Add a recipe to a user's favorites, then repeat the same favorite | First insert succeeds; duplicate favorite is rejected | PASS |
| 13 | Update a recipe title | Title changes and `updated_at` is automatically updated | PASS |
| 14 | Query recipes with their ingredients, units, and categories | Related data is returned through joins | PASS |

## 3. Schema Verification

The following checks were completed successfully:

- All 10 expected tables exist in the `public` schema.
- Foreign-key relationships and deletion rules were inspected.
- Valid test records could be inserted.
- Relevant constraints rejected invalid or duplicate data.
- The automatic `updated_at` trigger worked as expected.
- Queries joining recipes, ingredients, units, and categories returned the expected relationships.

## 4. Conclusion

All tests listed above were reported as successful. The results indicate that the database schema and the tested integrity constraints behave as expected for the scenarios covered.

**Note:** These tests cover the database schema and selected operations. They do not constitute a complete test of application-level features such as OTP delivery, authorization, image storage, or the full account-deletion workflow.

