import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

db_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'database': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}
db_connection = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
engine = create_engine(db_connection)

engine = create_engine(db_connection)

df = pd.read_csv('all_drinks.csv')

# Insérer les données dans PostgreSQL
df.to_sql('cocktails', engine, if_exists='append', index=False)
