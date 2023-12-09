import pandas as pd
import psycopg2
from sqlalchemy import create_engine

db_connection = 'postgresql://projet_bartendai:BartendAI@localhost:5432/BartendAI'
engine = create_engine(db_connection)

df = pd.read_csv('all_drinks.csv')
if 'Unnamed: 0' in df.columns:
    df = df.drop('Unnamed: 0', axis=1)

df.to_sql('cocktails', engine, if_exists='append', index=False)
