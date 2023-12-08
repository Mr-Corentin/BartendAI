from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)
import random
import pandas as pd
import numpy as np
# Importez pandas ou toute autre bibliothèque nécessaire pour charger vos données

def get_cocktail_details(query):
    df = pd.read_csv('all_drinks.csv')
    cocktail_details = df[df['strDrink'].str.contains(query, case=False, na=False)].iloc[0].to_dict()
    return cocktail_details
    pass


@app.route('/')
def home():
    # Chargez vos données de cocktails, ici un exemple avec pandas
    df = pd.read_csv('all_drinks.csv')
    
    # Sélectionnez un nombre aléatoire de cocktails, disons 10 pour cet exemple
    random_cocktails = df.sample(10)
    
    # Convertissez le DataFrame en une liste de dictionnaires pour le passer au template
    cocktails_list = random_cocktails.to_dict('records')
    
    # Rendre le template en passant la liste de cocktails
    return render_template('home_page.html', cocktails=cocktails_list)

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    cocktail_id = request.form.get('cocktail_id')
    # Ajoutez ici la logique pour enregistrer le cocktail en tant que favori dans la base de données
    print(f"Cocktail {cocktail_id} ajouté aux favoris")
    # Redirigez l'utilisateur où vous le souhaitez après l'ajout : par exemple, la page d'accueil
    return redirect(url_for('home'))


@app.route('/search_cocktails', methods=['GET'])
def search_cocktails():
    search_query = request.args.get('query')
    if search_query:
        # Vous pouvez implémenter une logique pour trouver le cocktail par son nom.
        # Supposons que vous avez une fonction get_cocktail_details qui renvoie les détails d'un cocktail.
        cocktail_details = get_cocktail_details(search_query)
        cocktail_details = cocktail_details.replace({np.nan: None})

        if cocktail_details:
            return render_template('cocktail_details.html', details=cocktail_details)
        else:
            # Gestion du cas où le cocktail n'est pas trouvé
            return render_template('cocktail_not_found.html', query=search_query)
    else:
        # Gestion du cas où aucune requête de recherche n'est fournie
        return redirect(url_for('home'))



load_dotenv()

app = Flask(__name__)

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

def give_recomendation(user_id):
    pass



@app.route('/swipe', methods=['GET'])
def swipe():
    user_id = session.get('user_id')  # Assurez-vous que l'utilisateur est connecté
    if not user_id:
        return redirect(url_for('login'))  # Redirigez vers la page de connexion si l'utilisateur n'est pas connecté

    recipe = give_recomendation(user_id)  # Obtenez une recommandation de cocktail
    return render_template('swipe.html', recipe=recipe)

@app.route('/like', methods=['POST'])
def like():
    user_id = session.get('user_id')
    recipe_id = request.form.get('recipe_id')
    if user_id and recipe_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO likes (user_id, recipe_id) VALUES (%s, %s)", (user_id, recipe_id))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('swipe'))

@app.route('/pass', methods=['POST'])
def pass_recipe():
    return redirect(url_for('swipe'))





if __name__ == '__main__':
    app.run(debug=True)
