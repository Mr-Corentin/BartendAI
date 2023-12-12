# BartendAI

## Description
BartendAI est une application web permettant d'ajouter des cocktails à ses favoris. L'utilisateur peut se créer un compte, se connecter et rechercher des cocktails. Il y a une fonctionnalité de recommandation de cocktails sur la page swipe, permettant à l'utilisateur de liker ou de passer les cocktails qui lui sont proposés. Il a ensuite la possibilités de voir sur une autre page les favoris de l'utilisateur. Il peut aussi se déconnecter. 

## Technologies Utilisées
- Python avec le framework Flask pour le backend.
- PostgreSQL pour la gestion de la base de données.
- Pandas et Scikit-Learn pour l'analyse des données et les algorithmes de recommandation.
- HTML et CSS pour le frontend

## Installation et Configuration avec Docker

Assurez-vous que [Docker](https://www.docker.com/get-started) est installé et fonctionne sur votre machine.

Cloner le dépôt, accéder au répertoir et build le docker :

```sh
git clone https://github.com/Mr-Corentin/BartendAI.git
cd BARTENDAI
docker-compose up --build

```
Il faut ensuite aller à l'adresse suivante: 

http://localhost:5000

## Tests

Les tests unitaires sont dans le fichier test_unitaire.py, les tests d'intégration sont dans le dossier integration test et les tests end to end sont dans le fichier test_E2E.py.

Les tests sont intégrés dans le git action


