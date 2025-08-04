# Async Recipe Search Optimization in FastAPI and PostgreSQL

## Task Overview

You are working on the backend for 'QuickBite', a recipe management web app. The application features search and filtering for recipes by ingredients and categories. Users have reported sluggish performance—search by ingredient and category filters are slow and sometimes time out under load. The project is already scaffolded with FastAPI routers and endpoints, with async endpoints in place, but the core database schema and interaction logic need work. Your objective is to design efficient, normalized PostgreSQL tables, set up correct relationships and indexes, and implement all necessary async database access logic to make recipe search fast and scalable via FastAPI routes.

## Guidance

- Current database access blocks the event loop and does not take advantage of async patterns, causing slowdowns.
- Poor schema design: tables for recipes, ingredients, and categories are not normalized and lack proper foreign keys or indexes.
- Recipe search/filter queries rely on inefficient scans instead of indexed lookups; joins and relationships are either missing or implemented suboptimally.
- The project already contains FastAPI routers, Pydantic schemas, and application startup logic—do not restructure or rewrite the general application, only implement and improve the database layer and async logic.
- Implement all interactions with the database using async/postgres-compatible libraries in FastAPI (no blocking code in endpoints).
- Focus areas: table normalization, foreign keys, composite indexes, proper use of asyncpg or databases for async I/O, efficient query writing.

## Database Access

- Host: `<DROPLET_IP>`
- Port: 5432
- Database: recipe_db
- Username: recipemaster
- Password: supersecret
- Use pgAdmin, DBeaver, or `psql` for schema inspection and query testing as needed.

## Objectives

- Produce properly normalized PostgreSQL tables for recipes, ingredients, and categories, using correct data types and constraints.
- Implement all async-compatible database logic for CRUD, search by ingredient, and filter by category within FastAPI endpoints (use async methods in I/O code).
- Ensure all foreign keys and necessary indexes are in place for query acceleration.
- Design queries that leverage indexes rather than full-table scans for search/filter use cases.
- Prioritize responsiveness: All search/filter endpoints should respond quickly under realistic data volumes (hundreds of recipes, dozens of ingredients and categories).

## How to Verify

- Confirm with EXPLAIN ANALYZE that search and filter queries use indexes and execute efficiently.
- Test using the FastAPI endpoints: search by ingredient and filter by category should respond in under 300ms with typical dataset.
- Validate data integrity: adding/removing recipes, ingredients, or categories works as expected and relationships are enforced.
- Asynchronous code must NOT block the FastAPI event loop during database calls; use async DB libraries only.
- Code reviewers will check for presence of keys, constraints, indexes, and async usage in all database code.
