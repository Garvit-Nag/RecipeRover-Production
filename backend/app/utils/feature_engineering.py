from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack
import pandas as pd
import numpy as np

def create_feature_matrices(df, feature_weights):
    """
    Create feature matrices for the recommendation system.
    """
    tfidf_vectorizer_ingredients = TfidfVectorizer(
        stop_words='english',
        max_features=5000,
        ngram_range=(1, 2),
        min_df=1
    )
    
    ingredients_text = df['RecipeIngredientParts'].apply(lambda x: ' '.join(x) if x else '')
    tfidf_matrix_ingredients = tfidf_vectorizer_ingredients.fit_transform(ingredients_text)

    tfidf_vectorizer_keywords = TfidfVectorizer(stop_words='english', max_features=3000)
    tfidf_vectorizer_keywords_name = TfidfVectorizer(stop_words='english', max_features=3000)
    
    keywords_text = df['Keywords'].apply(lambda x: ' '.join(x) if x else '')
    keywords_name_text = df['keywords_name'].apply(lambda x: ' '.join(x) if x else '')
    
    tfidf_matrix_keywords = tfidf_vectorizer_keywords.fit_transform(keywords_text)
    tfidf_matrix_keywords_name = tfidf_vectorizer_keywords_name.fit_transform(keywords_name_text)

    category_dummies = pd.get_dummies(df['RecipeCategory'])
    category_matrix = category_dummies.values

    dietary_columns = ['is_vegetarian', 'is_vegan', 'is_gluten free', 'is_dairy free', 
                     'is_low carb', 'is_keto', 'is_paleo']
    dietary_matrix = df[dietary_columns].values

    scaler = MinMaxScaler()
    calories_matrix = scaler.fit_transform(df[['Calories']].values)
    time_matrix = scaler.fit_transform(df[['TotalTime_minutes']].values)
    rating_matrix = scaler.fit_transform(df[['AggregatedRating']].values)

    combined_matrix = hstack([
        tfidf_matrix_ingredients * feature_weights['ingredients'],
        category_matrix * feature_weights['category'],
        dietary_matrix * feature_weights['dietary'],
        calories_matrix * feature_weights['calories'],
        time_matrix * feature_weights['time'],
        tfidf_matrix_keywords * feature_weights['keywords'],
        tfidf_matrix_keywords_name * feature_weights['keywords_name'],
        rating_matrix * 0.05  # Small weight for ratings in base similarity
    ])

    return (combined_matrix, tfidf_vectorizer_ingredients, tfidf_vectorizer_keywords, 
            tfidf_vectorizer_keywords_name, category_dummies, scaler)

def create_query_vector(combined_matrix, tfidf_vectorizer_ingredients, tfidf_vectorizer_keywords,
                        tfidf_vectorizer_keywords_name, category_dummies, scaler, feature_weights, **kwargs):
    """
    Create a query vector based on user input.
    """
    query_vector = np.zeros((1, combined_matrix.shape[1]))
    current_position = 0

    if kwargs.get('ingredients'):
        ingredients_query = tfidf_vectorizer_ingredients.transform([' '.join(kwargs['ingredients'])])
        query_vector[:, :ingredients_query.shape[1]] = ingredients_query.toarray() * feature_weights['ingredients']
        current_position += ingredients_query.shape[1]

    category_vector = np.zeros((1, category_dummies.shape[1]))
    if kwargs.get('category') and kwargs['category'] in category_dummies.columns:
        category_index = category_dummies.columns.get_loc(kwargs['category'])
        category_vector[0, category_index] = 1
    query_vector[:, current_position:current_position + category_dummies.shape[1]] = (
        category_vector * feature_weights['category']
    )
    current_position += category_dummies.shape[1]

    dietary_columns = ['is_vegetarian', 'is_vegan', 'is_gluten free', 'is_dairy free', 
                       'is_low carb', 'is_keto', 'is_paleo']
    dietary_vector = np.zeros((1, len(dietary_columns)))
    if kwargs.get('dietary_preference') in dietary_columns:
        dietary_index = dietary_columns.index(kwargs['dietary_preference'])
        dietary_vector[0, dietary_index] = 1
    query_vector[:, current_position:current_position + len(dietary_columns)] = (
        dietary_vector * feature_weights['dietary']
    )
    current_position += len(dietary_columns)

    calories_vector = np.zeros((1, 1))
    time_vector = np.zeros((1, 1))
    
    if kwargs.get('calories'):
        calories_vector[0, 0] = kwargs['calories']
    if kwargs.get('time'):
        time_vector[0, 0] = kwargs['time']
        
    calories_vector = scaler.transform(calories_vector)
    time_vector = scaler.transform(time_vector)
    
    query_vector[:, current_position:current_position + 1] = calories_vector * feature_weights['calories']
    current_position += 1
    query_vector[:, current_position:current_position + 1] = time_vector * feature_weights['time']
    current_position += 1

    if kwargs.get('keywords'):
        keywords_query = tfidf_vectorizer_keywords.transform([' '.join(kwargs['keywords'])])
        query_vector[:, current_position:current_position + keywords_query.shape[1]] = (
            keywords_query.toarray() * feature_weights['keywords']
        )
        current_position += keywords_query.shape[1]

    if kwargs.get('keywords_name'):
        keywords_name_query = tfidf_vectorizer_keywords_name.transform([' '.join(kwargs['keywords_name'])])
        query_vector[:, current_position:current_position + keywords_name_query.shape[1]] = (
            keywords_name_query.toarray() * feature_weights['keywords_name']
        )

    return query_vector