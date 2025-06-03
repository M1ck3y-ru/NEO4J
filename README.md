# 📊 Exercice Neo4j - Système de Gestion Clients/Commandes/Produits

Ce projet implémente un système de gestion des relations clients-commandes-produits utilisant Neo4j comme base de données graphe, avec une API REST développée en Python Flask.

## 🎯 Objectifs

- Modéliser les interactions entre clients, commandes et produits dans un graphe
- Exploiter les données via des requêtes Cypher optimisées
- Exposer les fonctionnalités via une API REST avec interface web
- Générer des recommandations basées sur les comportements d'achat

## 🏗️ Architecture du Projet

```
neo4j-exercise/
├── app/
│   ├── app.py                 # Application Flask principale
│   └── requirements.txt       # Dépendances Python
├── data/
│   └── data_insertion.cypher  # Script d'insertion des données
├── queries/
│   └── queries.cypher         # Collection de requêtes Cypher
├── docs/
│   └── rapport.md             # Rapport de synthèse
└── README.md                  # Ce fichier
```

## 📋 Prérequis

- **Neo4j** (Desktop ou Docker)
- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)

## 🚀 Installation et Configuration

### 1. Installation de Neo4j

#### Option A : Neo4j Desktop (Recommandée)
1. Télécharger depuis [neo4j.com/download](https://neo4j.com/download/)
2. Créer un nouveau projet
3. Créer une base de données locale avec le mot de passe : `password123`
4. Démarrer la base de données

#### Option B : Docker
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
3. Copier et exécuter le contenu du fichier `data/data_insertion.cypher`

### 3. Installation de l'Application Python

```bash
# Cloner le projet
cd neo4j-exercise/app

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera accessible sur : http://localhost:5000

## 📊 Modèle de Données

### Schéma du Graphe

```
(Client) -[A_EFFECTUÉ]-> (Commande) -[CONTIENT]-> (Produit)
```

### Types de Nœuds

**Client**
- `id` : Identifiant unique
- `nom` : Nom complet
- `email` : Adresse email
- `age` : Âge du client
- `ville` : Ville de résidence

**Commande**
- `id` : Identifiant unique
- `date` : Date de commande (YYYY-MM-DD)
- `total` : Montant total

**Produit**
- `id` : Identifiant unique
- `nom` : Nom du produit
- `prix` : Prix unitaire
- `categorie` : Catégorie du produit
- `marque` : Marque du produit

### Relations

- **A_EFFECTUÉ** : Relation entre Client et Commande
- **CONTIENT** : Relation entre Commande et Produit
  - Propriété : `quantite` (nombre d'unités)

## 🔍 Fonctionnalités Principales

### API Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Interface web principale |
| `/api/clients` | GET | Liste de tous les clients |
| `/api/products` | GET | Liste de tous les produits |
| `/api/stats` | GET | Statistiques générales |
| `/api/products-by-client?client=nom` | GET | Produits achetés par un client |
| `/api/clients-by-product?product=nom` | GET | Clients ayant acheté un produit |
| `/api/suggestions?client=nom` | GET | Suggestions pour un client |
| `/api/orders-by-product?product=nom` | GET | Commandes contenant un produit |

### Requêtes Cypher Clés

**1. Produits achetés par un client**
```cypher
MATCH (c:Client {nom: "Alice Dupont"})-[:A_EFFECTUE]->(cmd:Commande)-[:CONTIENT]->(p:Produit)
RETURN p.nom as produit, p.prix as prix
ORDER BY p.nom;
```

**2. Suggestions basées sur les comportements**
```cypher
MATCH (client:Client {nom: "Alice Dupont"})-[:A_EFFECTUE]->(cmd1:Commande)-[:CONTIENT]->(p1:Produit)
MATCH (autres:Client)-[:A_EFFECTUE]->(cmd2:Commande)-[:CONTIENT]->(p1)
MATCH (autres)-[:A_EFFECTUE]->(cmd3:Commande)-[:CONTIENT]->(suggestion:Produit)
WHERE client <> autres 
  AND NOT (client)-[:A_EFFECTUE]->(:Commande)-[:CONTIENT]->(suggestion)
RETURN suggestion.nom as produit_suggere, COUNT(*) as score
ORDER BY score DESC;
```

## 🖥️ Utilisation de l'Interface Web

1. **Accéder à l'application** : http://localhost:5000
2. **Statistiques générales** : Cliquer sur "Charger les statistiques"
3. **Recherche par client** : Sélectionner un client pour voir ses achats
4. **Suggestions** : Obtenir des recommandations personnalisées
5. **Recherche par produit** : Voir qui a acheté un produit spécifique

## 📈 Données d'Exemple

Le jeu de données inclut :
- **5 clients** (Alice, Bob, Claire, David, Emma)
- **8 produits** (iPhone, MacBook, AirPods, iPad, etc.)
- **6 commandes** avec relations complexes
- **Différentes catégories** : Smartphone, Ordinateur, Audio, Tablette

## 🔧 Configuration Avancée

### Modification des Paramètres de Connexion

Dans `app.py`, ajuster si nécessaire :
```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"
```

### Ajout de Nouvelles Données

Utiliser l'interface Neo4j Browser ou ajouter des requêtes dans `data_insertion.cypher` :
```cypher
CREATE (c:Client {id: 6, nom: "Nouveau Client", email: "nouveau@email.com", age: 30});
```

## 🧪 Tests et Validation

### Vérification du Graphe
```cypher
// Visualiser l'ensemble du graphe
MATCH (n) RETURN n LIMIT 25;

// Statistiques rapides
MATCH (c:Client) RETURN COUNT(c) as nb_clients;
MATCH (p:Produit) RETURN COUNT(p) as nb_produits;
MATCH (cmd:Commande) RETURN COUNT(cmd) as nb_commandes;
```

### Test des API
```bash
# Test de l'API
curl http://localhost:5000/api/stats
curl "http://localhost:5000/api/products-by-client?client=Alice%20Dupont"
```

## 🐛 Résolution de Problèmes

### Problèmes de Connexion Neo4j
- Vérifier que Neo4j est démarré
- Contrôler les ports 7474 (HTTP) et 7687 (Bolt)
- Valider les identifiants de connexion

### Erreurs Python
- Installer les dépendances : `pip install neo4j flask`
- Vérifier la version Python (3.8+)

### Base de Données Vide
- Exécuter le script `data_insertion.cypher`
- Vérifier les contraintes d'unicité

## 📝 Développement

### Ajout de Nouvelles Fonctionnalités

1. **Nouvelle requête** : Ajouter dans `queries.cypher`
2. **Nouveau endpoint** : Créer une route dans `app.py`
3. **Interface web** : Modifier le template HTML

### Structure des Réponses JSON
```json
{
  "client": "Alice Dupont",
  "produit": "iPhone 15",
  "prix": 999.0
}
```

## 📊 Métriques et Performance

- **Temps de réponse** : < 100ms pour les requêtes simples
- **Capacité** : Optimisé pour des milliers de nœuds
- **Indexation** : Contraintes d'unicité sur les IDs

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créer une branche feature
3. Tester les modifications
4. Soumettre une pull request

## 📚 Ressources Supplémentaires

- [Documentation Neo4j](https://neo4j.com/docs/)
- [Guide Cypher](https://neo4j.com/developer/cypher/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Driver Neo4j Python](https://neo4j.com/developer/python/)

## 📄 Licence

Ce projet est développé à des fins éducatives dans le cadre d'un exercice sur les bases de données graphe.
