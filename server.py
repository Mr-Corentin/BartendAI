from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine


load_dotenv()
secret_key = os.getenv('SECRET_KEY', 'ACBCEUFIZ13azdeuicz13452_ufjd')


app = Flask(__name__)
app.secret_key = secret_key

def csv_data():
    data=pd.read_csv("all_drinks.csv")
    ingredient_cols = [col for col in data.columns if 'strIngredient' in col]

    data["recipe_id"] = data.index
    data['ingredients'] = data[ingredient_cols].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)

    data['ingredients'] = data['ingredients'].str.replace(r'\s+', ' ', regex=True).str.strip()

    data['strDrink'] = data['strDrink'].str.lower()
    data['ingredients'] = data['ingredients'].str.lower()

    data['strCategory'] = data['strCategory'].str.lower()
    data['strAlcoholic'] = data['strAlcoholic'].str.lower()
    return data


def clean_dataset(data):
    
    df = data.drop_duplicates(subset='strDrink')

    df['isAlcoholic'] = df['strAlcoholic'].apply(lambda x: 1 if x == 'alcoholic' else 0)
    df = df[['idDrink','strDrink', 'ingredients', 'strCategory', 'isAlcoholic']]
    return df

def tf_cosine_indices(df):
    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(df['ingredients'])


    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df['strDrink']).drop_duplicates()
    return cosine_sim, indices


data = csv_data()
df = clean_dataset(data)
cosine_sim, indices = tf_cosine_indices(df)

def give_recomendation(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les cocktails favoris de l'utilisateur
    cursor.execute("SELECT idDrink FROM likes WHERE user_id = %s", (user_id,))
    favorite_drinks = [row[0] for row in cursor.fetchall()]

    # Récupérer le dernier cocktail liké par l'utilisateur pour la recommandation
    cursor.execute("SELECT idDrink FROM likes WHERE user_id = %s ORDER BY time DESC LIMIT 1", (user_id,))
    idDrink = cursor.fetchone()

    cursor.close()
    conn.close()

    if not idDrink:
        return data.sample(1)

    try:
        like_name = df.loc[df["idDrink"] == idDrink[0]]['strDrink'].values[0]
        reco_cocktail = recommend_cocktail(like_name, favorite_drinks)

        if reco_cocktail is None or reco_cocktail['idDrink'] in favorite_drinks:
            return data.sample(1)

        return data[data['strDrink'] == reco_cocktail['strDrink']]
    except Exception as e:
        print(f"Error in give_recommendation: {e}")
        return data.sample(1)


def recommend_cocktail(cocktail_name, exclude_ids):
    try:
        idx = indices[cocktail_name]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Filtrer les cocktails déjà dans les favoris
        sim_scores = [score for score in sim_scores if df.iloc[score[0]]['idDrink'] not in exclude_ids]

        if not sim_scores:
            return None

        return df.iloc[sim_scores[0][0]]
    except Exception as e:
        print(f"Error in recommend_cocktail: {e}")
        return None





def get_cocktail_details(query):
    df = pd.read_csv('all_drinks.csv')
    cocktail_details = df[df['strDrink'].str.contains(query, case=False, na=False)].iloc[0].to_dict()
    return cocktail_details


@app.route('/home')
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    df = pd.read_csv('all_drinks.csv')
    
    random_cocktails = df.sample(10)
    
    cocktails_list = random_cocktails.to_dict('records')
    
    return render_template('home_page.html', cocktails=cocktails_list)

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    cocktail_id = request.form.get('cocktail_id')
    print(f"Cocktail {cocktail_id} ajouté aux favoris")
    return redirect(url_for('home'))


@app.route('/search_cocktails', methods=['GET'])
def search_cocktails():
    search_query = request.args.get('query')
    if search_query:

        cocktail_details = get_cocktail_details(search_query)
        for key, value in cocktail_details.items():
            if isinstance(value, float) and np.isnan(value):  
                cocktail_details[key] = None

        if cocktail_details:
            return render_template('cocktail_details.html', details=cocktail_details)
        else:
            return render_template('cocktail_not_found.html', query=search_query)
    else:
        return redirect(url_for('home'))



db_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'database': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}

def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']  # À hasher avant de stocker
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')





@app.route('/swipe', methods=['GET'])
def swipe():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    recipe = give_recomendation(user_id)
    recipe = {
        'name': recipe['strDrink'].values[0],
        'category': recipe['strCategory'].values[0],
        'alcoholic': recipe['strAlcoholic'].values[0],
        'ingredients': recipe['ingredients'].values[0],
        'image': recipe['strDrinkThumb'].values[0],
        'idDrink': recipe['idDrink'].values[0]
    }
    return render_template('swipe.html', recipe=recipe)

@app.route('/like', methods=['POST'])
def like():
    user_id = session.get('user_id')
    idDrink = request.form.get('recipe_id')
    if user_id and idDrink:
        print(f"User {user_id} likes recipe {idDrink}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO likes (user_id, idDrink) VALUES (%s, %s)", (user_id, idDrink))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('swipe'))

@app.route('/pass', methods=['POST'])
def pass_recipe():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    idDrink = request.form.get('recipe_id')
    recipe = data.sample(1)
    while recipe['idDrink'].values[0] == idDrink:
        recipe = data.sample(1)
    recipe = {
        'name': recipe['strDrink'].values[0],
        'category': recipe['strCategory'].values[0],
        'alcoholic': recipe['strAlcoholic'].values[0],
        'ingredients': recipe['ingredients'].values[0],
        'image': recipe['strDrinkThumb'].values[0],
        'idDrink': recipe['idDrink'].values[0]
    }
    return render_template('swipe.html', recipe=recipe)


@app.route('/favorites')
def favorites():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idDrink FROM likes WHERE user_id = %s", (user_id,))
    favorite_ids = cursor.fetchall()
    cursor.close()
    conn.close()

    favorites_details = []
    for idDrink in favorite_ids:
        cocktail_details = get_cocktail_details_by_id(idDrink[0])
        if cocktail_details:
            favorites_details.append(cocktail_details)
    
    return render_template('favorites.html', favorites=favorites_details)

def get_cocktail_details_by_id(cocktail_id):
    df = pd.read_csv('all_drinks.csv')  # Assurez-vous de ne pas charger le CSV à chaque appel
    cocktail_details = df.loc[df['idDrink'] == cocktail_id].to_dict('records')
    return cocktail_details[0] if cocktail_details else None

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
    user_info = cursor.fetchone()
    cursor.close()
    conn.close()

    if user_info:
        return render_template('profile.html', username=user_info[0], email=user_info[1])
    

def delete_test_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username=%s)", (username,))
    exists = cursor.fetchone()[0]
    if exists:
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
    cursor.close()
    conn.close()

def check_favorite_exists(user_id, cocktail_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = %s AND idDrink = %s)", (user_id, cocktail_id))
            return cursor.fetchone()[0]
    finally:
        conn.close()


@app.route('/')
def index():
    return redirect(url_for('login'))


def init_table_coktail():
    load_dotenv()
    db_config = {
        'host': os.getenv('POSTGRES_HOST'),
        'database': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD')
    }
    db_connection = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    engine = create_engine(db_connection)


    df_co = pd.read_csv('all_drinks.csv')

    # Insérer les données dans PostgreSQL
    df_co.to_sql('cocktails', engine, if_exists='append', index=False)
if __name__ == '__main__':
    #init_table_coktail()
    app.run(host='0.0.0.0', port=5000, debug=True)
