from pydantic import BaseModel
from typing import List, Optional

class RecipeCreate(BaseModel):
    name: str
    category_id: int
    instructions: str
    ingredients: List[str]

class RecipeOut(BaseModel):
    id: int
    name: str
    category: Optional[str]
    instructions: str
    ingredients: List[str]
