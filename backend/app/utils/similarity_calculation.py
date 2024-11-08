from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_weighted_similarity(query_vector, combined_matrix, df, target_calories=None, target_time=None):
    """
    Calculate weighted similarity scores between the query vector and the combined matrix.
    """
    base_similarity = cosine_similarity(query_vector, combined_matrix).flatten()
    
    penalties = np.ones_like(base_similarity)
    
    if target_calories is not None:
        calorie_diff = np.abs(df['Calories'].values - target_calories)
        calorie_penalty = 1 - (calorie_diff / df['Calories'].max())
        penalties *= calorie_penalty
        
    if target_time is not None:
        time_diff = np.abs(df['TotalTime_minutes'].values - target_time)
        time_penalty = 1 - (time_diff / df['TotalTime_minutes'].max())
        penalties *= time_penalty
    
    return base_similarity * penalties