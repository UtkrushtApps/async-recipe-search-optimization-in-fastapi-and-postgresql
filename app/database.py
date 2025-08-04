from databases import Database

DATABASE_URL = "postgresql+asyncpg://recipemaster:supersecret@db:5432/recipe_db"
database = Database(DATABASE_URL)

async def get_database():
    if not database.is_connected:
        await database.connect()
    return database
