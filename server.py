from flask import Flask, render_template, request, redirect, url_for

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



if __name__ == '__main__':
    app.run(debug=True)
