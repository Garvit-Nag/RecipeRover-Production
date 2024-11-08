import os
import joblib
from scipy.sparse import save_npz, load_npz
import pandas as pd
from app.utils.data_preprocessing import preprocess_data
from app.utils.feature_engineering import create_feature_matrices

def load_or_create_data(csv_file_path, precomputed_dir, feature_weights):
    files = ['df', 'tfidf_vectorizer_ingredients', 'tfidf_vectorizer_keywords',
             'tfidf_vectorizer_keywords_name', 'category_dummies', 'scaler']
    
    if all(os.path.exists(os.path.join(precomputed_dir, f'{f}.joblib')) for f in files) and \
       os.path.exists(os.path.join(precomputed_dir, 'combined_matrix.npz')):
        return load_precomputed_data(precomputed_dir)
    else:
        return compute_and_save_data(csv_file_path, precomputed_dir, feature_weights)

def load_precomputed_data(precomputed_dir):
    data = {}
    for f in ['df', 'tfidf_vectorizer_ingredients', 'tfidf_vectorizer_keywords',
              'tfidf_vectorizer_keywords_name', 'category_dummies', 'scaler']:
        data[f] = joblib.load(os.path.join(precomputed_dir, f'{f}.joblib'))
    data['combined_matrix'] = load_npz(os.path.join(precomputed_dir, 'combined_matrix.npz'))
    return data

def compute_and_save_data(csv_file_path, precomputed_dir, feature_weights):
    df = preprocess_data(pd.read_csv(csv_file_path))
    results = create_feature_matrices(df, feature_weights)
    combined_matrix, tfidf_vectorizer_ingredients, tfidf_vectorizer_keywords, \
    tfidf_vectorizer_keywords_name, category_dummies, scaler = results

    os.makedirs(precomputed_dir, exist_ok=True)
    data = {
        'df': df,
        'tfidf_vectorizer_ingredients': tfidf_vectorizer_ingredients,
        'tfidf_vectorizer_keywords': tfidf_vectorizer_keywords,
        'tfidf_vectorizer_keywords_name': tfidf_vectorizer_keywords_name,
        'category_dummies': category_dummies,
        'scaler': scaler,
        'combined_matrix': combined_matrix
    }
    for name, obj in data.items():
        if name == 'combined_matrix':
            save_npz(os.path.join(precomputed_dir, f'{name}.npz'), obj)
        else:
            joblib.dump(obj, os.path.join(precomputed_dir, f'{name}.joblib'))
    return data