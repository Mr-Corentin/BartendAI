import pytest  
from server import csv_data, clean_dataset, recommend_cocktail, tf_cosine_indices


def test_init_data_recommendation():
    data = csv_data()
    assert data is not None
    df = clean_dataset(data)
    assert df is not None
    cosine_sim, indices = tf_cosine_indices(df)
    assert cosine_sim is not None
    assert indices is not None

def test_recommend_cocktail():
    data = csv_data()
    df = clean_dataset(data)
    cosine_sim, indices = tf_cosine_indices(df)
    coktail_name = df.sample(1)['strDrink']
    print(coktail_name)
    cocktail_reco = recommend_cocktail(coktail_name)
    assert cocktail_reco is not None

    cocktail_reco2 = recommend_cocktail(coktail_name)
    assert cocktail_reco2 is not None

    assert cocktail_reco['strDrink'] == cocktail_reco2['strDrink']



