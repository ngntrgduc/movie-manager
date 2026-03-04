import pandas as pd
from utils.constants import UNWATCHED_STATUS

def build_item_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Build a numeric feature matrix for item-based recommendation."""
    df_features = df.copy()
    df_features = df_features.drop(columns=['rating', 'watched_date'])

    # Min-max scaling year column
    min_year, max_year =  df['year'].min(), df['year'].max()
    df_features['year'] = (df['year'] - min_year) / (max_year - min_year)

    country_features = df['country'].str.get_dummies()
    type_features = df['type'].str.get_dummies()
    genres_features = df['genres'].str.get_dummies(',')

    return pd.concat(
        [
            df_features.drop(columns=['id', 'name', 'status', 'type', 'country', 'genres']), 
            type_features, country_features, genres_features
        ], axis=1
    )


def build_item_similarity_matrix(feature_matrix, df: pd.DataFrame) -> pd.DataFrame:
    """Compute cosine similarity between all items."""
    from sklearn.metrics.pairwise import cosine_similarity

    similarity_matrix = cosine_similarity(feature_matrix)
    return pd.DataFrame(
        similarity_matrix, 
        index=df['id'], 
        columns=df['id']
    )

def recommend(movie_id: int, df: pd.DataFrame, top_k : int = 5) -> pd.DataFrame:
    """Recommend similar unwatched movies based on cosine similarity."""

    feature_matrix = build_item_feature_matrix(df) 
    similarity_df = build_item_similarity_matrix(feature_matrix, df)

    if movie_id not in similarity_df.index:
        return f"Movie ID {movie_id} not found."

    sim_scores = similarity_df.loc[movie_id].drop(movie_id)  # remove itself

    # Keep unwatched movies
    valid_ids = df[df['status'] == UNWATCHED_STATUS]['id']
    sim_scores = sim_scores[sim_scores.index.isin(valid_ids)]
    
    top_movies = sim_scores.sort_values(ascending=False).head(top_k)    

    return df[df['id'].isin(top_movies.index)]


# def build_user_profile(vector) -> np.array:
#     # TODO: weighted rating
#     return np.mean(vector, axis=0)