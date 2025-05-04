# Système de Recommandation Hybride

Ce projet implémente un système de recommandation hybride combinant le filtrage basé sur le contenu et le filtrage collaboratif pour un site web marchand.

## Fonctionnalités

- Recommandations basées sur le contenu ("Montrez-moi plus que ce qui ressemble à ce que j'ai aimé")
- Filtrage collaboratif ("Dites-moi ce qui est populaire parmi mes pairs")
- Interface web pour visualiser et noter les produits
- Système d'authentification des utilisateurs

## Prérequis

- Python 3.x
- MySQL Server
- pip ou pipenv

## Installation

1. Cloner le projet
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer la base de données :
- Créer une base de données MySQL
- Modifier les informations de connexion dans `flask_app/config/mySQLConnection.py`
- Exécuter le script SQL :
```bash
mysql -u root -p < database_schema.sql
```

## Structure du Projet

```
project/
├── database_schema.sql    # Schéma de la base de données
├── requirements.txt       # Dépendances Python
├── server.py             # Point d'entrée de l'application
└── flask_app/
    ├── config/           # Configuration (BD, etc.)
    ├── controllers/      # Contrôleurs
    ├── models/          # Modèles de données
    └── templates/       # Templates HTML
```

## Utilisation

1. Démarrer le serveur :
```bash
python server.py
```

2. Accéder à l'application dans votre navigateur à l'adresse : http://localhost:5000

## Algorithmes de Recommandation

### Filtrage Basé sur le Contenu
- Utilise TF-IDF pour la vectorisation des caractéristiques des produits
- Calcule les similarités avec les métriques Jaccard et euclidienne

### Filtrage Collaboratif
- Système de notation de 0 à 5 étoiles
- Calcul des similarités entre utilisateurs
- Recommandations basées sur les 4 voisins les plus proches

## Évaluation des Recommandations

Les recommandations sont générées en combinant :
1. Les produits similaires basés sur le contenu
2. Les produits populaires parmi les utilisateurs similaires
3. Une pondération hybride pour équilibrer les deux approches