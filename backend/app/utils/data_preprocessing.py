import pandas as pd
import numpy as np
import ast
import logging
import re

logger = logging.getLogger(__name__)

def parse_r_vector(s):
    """
    Parse R vector format strings like c("word1", "word2") into Python lists.
    
    Args:
        s: String in R vector format
        
    Returns:
        List of strings
    """
    if pd.isna(s):
        return []
    
    try:
        # Remove the c() wrapper and split by commas
        if isinstance(s, str) and s.startswith('c(') and s.endswith(')'):
            # Extract content between c( and )
            content = s[2:-1].strip()
            
            # Use regex to properly split quoted strings
            pattern = r'"([^"]*)"'
            matches = re.findall(pattern, content)
            
            # Filter out empty strings and NA values
            ingredients = [item.strip() for item in matches if item.strip() and item.lower() != 'na']
            return ingredients
        elif isinstance(s, list):
            return s
        else:
            return []
    except Exception as e:
        logger.warning(f"Error parsing R vector: {s}, Error: {str(e)}")
        return []

def preprocess_data(df):
    """
    Preprocess the dataframe by handling boolean, numerical, and list-like columns.
    """
    bool_columns = ['is_vegetarian', 'is_vegan', 'is_gluten free', 'is_dairy free', 
                    'is_low carb', 'is_keto', 'is_paleo']
    for col in bool_columns:
        df[col] = df[col].map({'TRUE': 1, 'FALSE': 0, True: 1, False: 0}).fillna(0).astype(int)
    
    numerical_columns = ['Calories', 'TotalTime_minutes', 'AggregatedRating', 'ReviewCount']
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)
    
    # Handle R vector format columns
    r_vector_columns = ['RecipeIngredientParts', 'RecipeInstructions', 'RecipeIngredientQuantities']
    for col in r_vector_columns:
        df[col] = df[col].apply(parse_r_vector)
    
    # Handle regular list columns
    list_columns = ['Keywords', 'keywords_name']
    for col in list_columns:
        df[col] = df[col].apply(parse_list_string)
    
    return df

def parse_list_string(s):
    """
    Safely parse list-like strings.
    """
    if pd.isna(s):
        return []
    try:
        if isinstance(s, str):
            parsed = ast.literal_eval(s)
            return parsed if isinstance(parsed, list) else [s]
        elif isinstance(s, list):
            return s
        return []
    except (ValueError, SyntaxError):
        return [s] if s else []

def parse_recipe_ingredients(ingredient_parts):
    """
    Parse RecipeIngredientParts field handling R vector format.
    """
    return parse_r_vector(ingredient_parts)

def parse_list_field(field):
    """
    Parse a list field, handling various input types including R vectors.
    """
    if pd.isna(field):
        return []
    if isinstance(field, list):
        return field
    elif isinstance(field, str):
        if field.startswith('c('):
            return parse_r_vector(field)
        try:
            parsed = ast.literal_eval(field)
            return parsed if isinstance(parsed, list) else []
        except (ValueError, SyntaxError):
            return []
    return []