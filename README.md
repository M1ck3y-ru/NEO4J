# 📊 Exercice Neo4j - Système de Gestion Clients/Commandes/Produits

Ce projet implémente un système de gestion des relations clients-commandes-produits utilisant Neo4j comme base de données graphe, avec une API REST développée en Python Flask.

![Screenshot de l'application](screenshot/Screenshot%202025-06-03%20at%2011.20.26.png)
## 🎯 Objectifs

- Modéliser les interactions entre clients, commandes et produits dans un graphe
- Exploiter les données via des requêtes Cypher optimisées
- Exposer les fonctionnalités via une API REST avec interface web
- Générer des recommandations basées sur les comportements d'achat

## 📋 Prérequis

- **Neo4j** (Desktop ou Docker)
- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)

## 🚀 Installation et Configuration

### 1. Installation de Neo4j

#### Docker
```bash
docker run \
    --name neo4j-exercise \
    -p7474:7474 -p7687:7687 \
    -d \
    --env NEO4J_AUTH=neo4j/password123 \
    neo4j:latest
```

### 2. Insertion des Données

1. Accéder à l'interface Neo4j Browser : http://localhost:7474
2. Se connecter avec : `neo4j` / `password123`

### 3. Installation de l'Application Python

```bash
# Se placer dans le dossier de l'application
cd neo4j-exercise/app

# Créer un environnement virtuel Python (recommandé)
python3 -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate
# Sur Windows :
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera accessible sur : http://localhost:5001

> **Note :** Nous utilisons un environnement virtuel Python pour isoler les dépendances du projet et éviter les conflits avec d'autres projets Python sur le système.

### 4. Désactiver l'environnement virtuel
```bash
# Quand vous avez terminé de travailler sur le projet
deactivate
```

## 📊 Modèle de Données

### Schéma du Graphe
disponible dans la documentation.



## 🖥️ Utilisation de l'Interface Web

1. **Accéder à l'application** : http://localhost:5001
2. **Statistiques générales** : Cliquer sur "Charger les statistiques"
3. **Recherche par client** : Sélectionner un client pour voir ses achats
4. **Suggestions** : Obtenir des recommandations personnalisées
5. **Recherche par produit** : Voir qui a acheté un produit spécifique

> 🤖 **Interface réalisé avec l'aide de Claude AI** !

## 📈 Données d'Exemple

Le jeu de données inclut :
- **5 clients** (Alice, Bob, Claire, David, Emma)
- **8 produits** (iPhone, MacBook, AirPods, iPad, etc.)
- **6 commandes** avec relations complexes
- **Différentes catégories** : Smartphone, Ordinateur, Audio, Tablette

## 📚 Ressources Supplémentaires

- [Documentation Neo4j](https://neo4j.com/docs/)
- [Guide Cypher](https://neo4j.com/developer/cypher/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Driver Neo4j Python](https://neo4j.com/developer/python/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 📄 Licence

Ce projet est développé à des fins éducatives dans le cadre d'un exercice