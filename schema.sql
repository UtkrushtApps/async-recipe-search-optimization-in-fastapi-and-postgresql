-- Suboptimal schema: Unnormalized, missing constraints and indexes
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER,
    instructions TEXT
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER,
    ingredient_id INTEGER
    -- Missing PK, FKs, no index
);
-- No foreign key constraints, no indexes on search/filter columns, unnormalized relationships
