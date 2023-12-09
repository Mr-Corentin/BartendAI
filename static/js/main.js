function addToFavorites(event, cocktailId) {
    event.preventDefault(); 
    console.log("Bouton like cliqué pour le cocktail ID:", cocktailId);

    fetch('/add_to_favorites', {
        method: 'POST',
        body: JSON.stringify({ cocktail_id: cocktailId }),
        headers: {
            'Content-Type': 'application/json'        }
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // ou `response.text()` si la réponse est une chaîne de caractères
        }
        throw new Error('La requête a échoué');
    })
    .then(data => {
        if (data.success) {
            // Trouvez l'icône de favori et changez son apparence
            var icon = document.getElementById("favorite-icon-img-" + cocktailId);
            icon.classList.add("favorite-icon-img-liked");
            // Si vous utilisez des images PNG au lieu de SVG, changez le `src` de l'image
            // icon.src = "chemin/vers/votre/image/de/coeur/rempli.png";
        } else {
            throw new Error('Erreur lors de l\'ajout aux favoris');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

