from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import schemas
from app.database import get_database

router = APIRouter()

# Fetch all recipes, optionally filtered by category or ingredient
@router.get('/recipes', response_model=List[schemas.RecipeOut])
async def list_recipes(category_id: int = None, ingredient: str = None, database=Depends(get_database)):
    # Suboptimal: no index usage, inefficient LIKE, bad joins
    query = """
    SELECT r.id, r.name, c.name as category, r.instructions
    FROM recipes r
    LEFT JOIN categories c ON r.category_id = c.id
    WHERE 1=1
    """
    where_clauses = []
    values = {}
    if category_id:
        query += " AND r.category_id = :category_id"
        values['category_id'] = category_id
    if ingredient:
        query += " AND r.id IN (
            SELECT recipe_id FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            WHERE i.name ILIKE '%' || :ingredient || '%')"
        values['ingredient'] = ingredient
    rows = await database.fetch_all(query=query, values=values)
    # Inefficiently fetch ingredients per recipe (N+1)
    results = []
    for row in rows:
        ing_rows = await database.fetch_all(
            "SELECT i.name FROM recipe_ingredients ri JOIN ingredients i ON ri.ingredient_id = i.id WHERE ri.recipe_id = :rid",
            {"rid": row["id"]}
        )
        results.append(schemas.RecipeOut(id=row["id"], name=row["name"], category=row["category"], instructions=row["instructions"], ingredients=[i["name"] for i in ing_rows]))
    return results

# Add a recipe (minimal error handling, missing validations)
@router.post('/recipes', response_model=schemas.RecipeOut)
async def add_recipe(recipe: schemas.RecipeCreate, database=Depends(get_database)):
    # No transaction safety
    query = "INSERT INTO recipes (name, category_id, instructions) VALUES (:name, :category_id, :instructions) RETURNING id"
    rid = await database.execute(query=query, values={
        'name': recipe.name,
        'category_id': recipe.category_id,
        'instructions': recipe.instructions
    })
    # Insert ingredients
    for ingredient in recipe.ingredients:
        # Inefficient insert, multiple queries per ingredient
        q = "SELECT id FROM ingredients WHERE name = :name"
        row = await database.fetch_one(q, {"name": ingredient})
        if row: iid = row['id']
        else:
            iid = await database.execute("INSERT INTO ingredients (name) VALUES (:name) RETURNING id", {"name": ingredient})
        await database.execute("INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (:rid, :iid)", {"rid": rid, "iid": iid})
    # Immediate re-query to get result
    data = await database.fetch_one("SELECT r.id, r.name, c.name as category, r.instructions FROM recipes r LEFT JOIN categories c ON r.category_id = c.id WHERE r.id = :rid", {"rid": rid})
    ing_rows = await database.fetch_all("SELECT i.name FROM recipe_ingredients ri JOIN ingredients i ON ri.ingredient_id = i.id WHERE ri.recipe_id = :rid", {"rid": rid})
    return schemas.RecipeOut(id=data['id'], name=data['name'], category=data['category'], instructions=data['instructions'], ingredients=[i['name'] for i in ing_rows])
