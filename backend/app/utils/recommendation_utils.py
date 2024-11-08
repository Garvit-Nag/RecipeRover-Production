import logging
from app.models.recipe import Recipe
from app.utils.feature_engineering import create_query_vector
from app.utils.similarity_calculation import calculate_weighted_similarity

logger = logging.getLogger(__name__)

async def get_top_recommendations(df, combined_matrix, tfidf_vectorizer_ingredients,
                                  tfidf_vectorizer_keywords, tfidf_vectorizer_keywords_name,
                                  category_dummies, scaler, feature_weights, image_search_service,
                                  category=None, dietary_preference=None, ingredients=None, 
                                  calories=None, time=None, keywords=None, keywords_name=None, top_n=5):
    logger.info(f"Starting recommendation process for category: {category}, dietary_preference: {dietary_preference}")
    
    query_vector = create_query_vector(combined_matrix, tfidf_vectorizer_ingredients,
                                       tfidf_vectorizer_keywords, tfidf_vectorizer_keywords_name,
                                       category_dummies, scaler, feature_weights,
                                       category=category, dietary_preference=dietary_preference,
                                       ingredients=ingredients, calories=calories, time=time,
                                       keywords=keywords, keywords_name=keywords_name)

    similarity_scores = calculate_weighted_similarity(query_vector, combined_matrix, df, calories, time)
    
    if category:
        similarity_scores *= (df['RecipeCategory'] == category)

    top_indices = similarity_scores.argsort()[-top_n*3:][::-1]
    logger.info(f"Found {len(top_indices)} potential recommendations")

    results = []
    async with image_search_service as image_service:
        for idx in top_indices:
            if len(results) >= top_n:
                break

            recipe = df.iloc[idx]
            
            if category and recipe['RecipeCategory'] != category:
                continue

            try:
                image_urls = await image_service.search_recipe_images(recipe['Name'], recipe['Images'], 3)
            except Exception as e:
                logger.error(f"Error searching images for {recipe['Name']}: {str(e)}")
                image_urls = []

            results.append(Recipe(
                RecipeId=int(recipe['RecipeId']),
                Name=recipe['Name'],
                RecipeCategory=recipe['RecipeCategory'],
                RecipeIngredientParts=recipe['RecipeIngredientParts'],
                Keywords=recipe['Keywords'],
                keywords_name=recipe['keywords_name'],
                Calories=float(recipe['Calories']),
                TotalTime_minutes=int(recipe['TotalTime_minutes']),
                AggregatedRating=float(recipe['AggregatedRating']),
                ReviewCount=int(recipe['ReviewCount']),
                Description=recipe['Description'],
                RecipeIngredientQuantities=recipe['RecipeIngredientQuantities'],
                RecipeInstructions=recipe['RecipeInstructions'],
                Images=image_urls,
                Similarity=float(similarity_scores[idx])
            ))

    logger.info(f"Returning {len(results)} recommendations")
    return results[:top_n]