import pytest
import numpy as np
import pandas as pd
from utils.recsys import (
    build_item_feature_matrix, 
    build_item_similarity_matrix,
    recommend,
    recommend_recent_profile,
    recommend_all_profile,
)

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'id':           [1, 2, 3, 4, 5],
        'name':         ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
        'year':         [2000, 2005, 2010, 2015, 2020],
        'status':       ['completed', 'completed', 'completed', 'waiting', 'waiting'],
        'type':         ['movie', 'movie', 'series', 'movie', 'series'],
        'country':      ['US', 'Korea', 'Japan', 'US', 'Korea'],
        'genres':       ['action,drama', 'horror,thriller', 'action,sci-fi', 'drama', 'horror,drama'],
        'rating':       [8.0, 6.0, 9.0, None, None],
        'watched_date': ['2021-05-10', '2022', '2023-03', None, None],
        # 'note':         [None, None, None, None, None],  # already remove note column in cli.py
    })


# build_item_feature_matrix()
def test_feature_matrix_drops_metadata_columns(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    for col in ['id', 'name', 'status', 'type', 'country', 'genres', 'rating', 'watched_date']:
        assert col not in feature_matrix.columns

def test_feature_matrix_genres_one_hot(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    assert 'action' in feature_matrix.columns
    assert 'drama' in feature_matrix.columns
    assert 'horror' in feature_matrix.columns
    assert 'sci-fi' in feature_matrix.columns

def test_feature_matrix_row_count(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    assert len(feature_matrix) == len(sample_df)


# build_item_similarity_matrix()
def test_similarity_matrix_is_square(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    sim_matrix = build_item_similarity_matrix(feature_matrix, sample_df)
    assert sim_matrix.shape[0] == sim_matrix.shape[1]

def test_similarity_matrix_diagonal_is_one(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    sim_matrix = build_item_similarity_matrix(feature_matrix, sample_df)
    diagonal = np.diag(sim_matrix.values)  # correct way to get diagonal
    assert np.allclose(diagonal, 1.0)

def test_similarity_matrix_index_matches_movie_ids(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    sim_matrix = build_item_similarity_matrix(feature_matrix, sample_df)
    assert list(sim_matrix.index) == list(sample_df['id'])
    assert list(sim_matrix.columns) == list(sample_df['id'])

def test_similarity_matrix_is_symmetric(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    sim_matrix = build_item_similarity_matrix(feature_matrix, sample_df)
    assert np.allclose(sim_matrix.values, sim_matrix.values.T)


# recommend()
def test_recommend_returns_top_k(sample_df):
    result = recommend(1, sample_df, top_k=2)
    assert len(result) == 2

def test_recommend_excludes_watched(sample_df):
    result = recommend(1, sample_df, top_k=5)
    assert 'completed' not in result['status'].values

def test_recommend_unknown_id_returns_message(sample_df):
    result = recommend(999, sample_df)
    assert isinstance(result, str)
    assert '999' in result

def test_recommend_excludes_query_movie(sample_df):
    result = recommend(1, sample_df, top_k=5)
    assert 1 not in result['id'].values


# recommend_recent_profile()
def test_recommend_recent_profile_returns_top_k(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    result = recommend_recent_profile(sample_df, feature_matrix, top_k=2)
    assert len(result) == 2

def test_recommend_recent_profile_excludes_watched(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    result = recommend_recent_profile(sample_df, feature_matrix, top_k=5)
    assert 'completed' not in result['status'].values


# recommend_all_profile()
def test_recommend_all_profile_returns_top_k(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    result = recommend_all_profile(sample_df, feature_matrix, top_k=2)
    assert len(result) == 2

def test_recommend_all_profile_excludes_watched(sample_df):
    feature_matrix = build_item_feature_matrix(sample_df)
    result = recommend_all_profile(sample_df, feature_matrix, top_k=5)
    assert 'completed' not in result['status'].values


# thanks, claude.ai <3, too lazy too write :((