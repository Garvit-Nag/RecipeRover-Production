from dataclasses import dataclass
from typing import List

@dataclass
class Recipe:
    RecipeId: int
    Name: str
    RecipeCategory: str
    RecipeIngredientParts: List[str]
    Keywords: List[str]
    keywords_name: List[str]  # Add this line
    Calories: float
    TotalTime_minutes: int
    AggregatedRating: float
    ReviewCount: int
    Description: str
    RecipeIngredientQuantities: List[str]
    RecipeInstructions: List[str]
    Images: List[str]
    Similarity: float  # Add this line if it's not already present