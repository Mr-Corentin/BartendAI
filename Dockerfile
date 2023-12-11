# Utiliser une image de base Python
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application Flask dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python", "server.py"]