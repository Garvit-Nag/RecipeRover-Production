import os

class Config:
    CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'recipe_dataset.csv')
    PRECOMPUTED_DIR = 'precomputed'

