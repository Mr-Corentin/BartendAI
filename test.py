import pytest  
from server import csv_data, clean_dataset

def test_creation_df():
    data = csv_data()
    assert data is not None
    df = clean_dataset(data)
    assert df is not None