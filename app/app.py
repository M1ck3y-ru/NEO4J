from flask import Flask, request, jsonify, render_template_string
from neo4j import GraphDatabase
import json

app = Flask(__name__)

# Configuration Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_query(query, parameters=None):
    """Exécute une requête Neo4j et retourne les résultats"""
    with driver.session() as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]

# Page d'accueil avec interface moderne
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neo4j Analytics Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --bg-primary: #0f0f23;
            --bg-secondary: #1a1a2e;
            --bg-card: #16213e;
            --accent: #00d4ff;
            --accent-dark: #0099cc;
            --text-primary: #ffffff;
            --text-secondary: #b8c5d1;
            --border: #2a3547;
            --success: #00ff88;
            --error: #ff4757;
            --warning: #ffa502;
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-card: linear-gradient(145deg, #1e293b 0%, #334155 100%);
            --shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4);
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            animation: fadeIn 0.8s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--gradient);
            border-radius: 2px;
        }
        
        .header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        .header p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            font-weight: 300;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .card {
            background: var(--bg-card);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient);
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 32px 64px -12px rgba(0, 212, 255, 0.2),
                0 25px 50px -12px rgba(0, 0, 0, 0.4);
            border-color: var(--accent);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .card-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: var(--gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .card-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .form-select, .form-input {
            width: 100%;
            padding: 1rem 1.5rem;
            background: var(--bg-secondary);
            border: 2px solid var(--border);
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }
        
        .form-select:focus, .form-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1);
        }
        
        .btn {
            padding: 1rem 2rem;
            background: var(--gradient);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 212, 255, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-full {
            width: 100%;
        }
        
        .results {
            margin-top: 1.5rem;
            padding: 1.5rem;
            background: var(--bg-secondary);
            border-radius: 12px;
            border: 1px solid var(--border);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .results h3 {
            color: var(--accent);
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .results ul {
            list-style: none;
        }
        
        .results li {
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .results li:last-child {
            border-bottom: none;
        }
        
        .product-name, .client-name {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .price {
            color: var(--success);
            font-weight: 700;
        }
        
        .score {
            background: var(--accent);
            color: var(--bg-primary);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .error {
            color: var(--error);
            background: rgba(255, 71, 87, 0.1);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--error);
        }
        
        .success {
            color: var(--success);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .stat-item {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stat-item:hover {
            transform: scale(1.05);
            border-color: var(--accent);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid var(--border);
            border-radius: 50%;
            border-top-color: var(--accent);
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Neo4j Analytics</h1>
            <p>Système de gestion avancé pour vos données clients et commandes</p>
        </div>
        
        <div class="grid">
            <!-- Statistiques -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">📊</div>
                    <h2 class="card-title">Statistiques Générales</h2>
                </div>
                <button class="btn btn-full" onclick="loadStats()">
                    Charger les statistiques
                </button>
                <div id="stats-results"></div>
            </div>

            <!-- Recherche produits par client -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🔍</div>
                    <h2 class="card-title">Produits par Client</h2>
                </div>
                <div class="form-group">
                    <label class="form-label">Sélectionner un client</label>
                    <select id="client-select" class="form-select">
                        <option value="">Choisir un client...</option>
                    </select>
                </div>
                <button class="btn btn-full" onclick="getProductsByClient()">
                    Rechercher les produits
                </button>
                <div id="client-results"></div>
            </div>

            <!-- Suggestions de produits -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">💡</div>
                    <h2 class="card-title">Suggestions IA</h2>
                </div>
                <div class="form-group">
                    <label class="form-label">Client pour suggestions</label>
                    <select id="suggestion-client" class="form-select">
                        <option value="">Choisir un client...</option>
                    </select>
                </div>
                <button class="btn btn-full" onclick="getSuggestions()">
                    Générer des suggestions
                </button>
                <div id="suggestion-results"></div>
            </div>

            <!-- Clients par produit -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">👥</div>
                    <h2 class="card-title">Clients par Produit</h2>
                </div>
                <div class="form-group">
                    <label class="form-label">Sélectionner un produit</label>
                    <select id="product-select" class="form-select">
                        <option value="">Choisir un produit...</option>
                    </select>
                </div>
                <button class="btn btn-full" onclick="getClientsByProduct()">
                    Trouver les clients
                </button>
                <div id="product-results"></div>
            </div>
        </div>
    </div>

    <script>
        // Animation de chargement
        function showLoading(elementId) {
            document.getElementById(elementId).innerHTML = 
                '<div style="text-align: center; padding: 2rem;"><div class="loading"></div></div>';
        }

        // Charger les listes déroulantes au démarrage
        window.onload = function() {
            loadClients();
            loadProducts();
        };

        function loadClients() {
            fetch('/api/clients')
                .then(response => response.json())
                .then(data => {
                    const clientSelect = document.getElementById('client-select');
                    const suggestionSelect = document.getElementById('suggestion-client');
                    
                    // Vider les sélecteurs
                    clientSelect.innerHTML = '<option value="">Choisir un client...</option>';
                    suggestionSelect.innerHTML = '<option value="">Choisir un client...</option>';
                    
                    data.forEach(client => {
                        const option1 = new Option(client.nom, client.nom);
                        const option2 = new Option(client.nom, client.nom);
                        clientSelect.add(option1);
                        suggestionSelect.add(option2);
                    });
                })
                .catch(error => console.error('Erreur:', error));
        }

        function loadProducts() {
            fetch('/api/products')
                .then(response => response.json())
                .then(data => {
                    const productSelect = document.getElementById('product-select');
                    productSelect.innerHTML = '<option value="">Choisir un produit...</option>';
                    
                    data.forEach(product => {
                        const option = new Option(product.nom, product.nom);
                        productSelect.add(option);
                    });
                })
                .catch(error => console.error('Erreur:', error));
        }

        function loadStats() {
            showLoading('stats-results');
            
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="stats-grid">';
                    html += `<div class="stat-item">
                        <span class="stat-value">${data.total_clients || 0}</span>
                        <span class="stat-label">Clients</span>
                    </div>`;
                    html += `<div class="stat-item">
                        <span class="stat-value">${data.total_produits || 0}</span>
                        <span class="stat-label">Produits</span>
                    </div>`;
                    html += `<div class="stat-item">
                        <span class="stat-value">${data.total_commandes || 0}</span>
                        <span class="stat-label">Commandes</span>
                    </div>`;
                    html += `<div class="stat-item">
                        <span class="stat-value">${data.chiffre_affaires || 0}€</span>
                        <span class="stat-label">CA Total</span>
                    </div>`;
                    html += '</div>';
                    
                    document.getElementById('stats-results').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('stats-results').innerHTML = 
                        '<div class="error">❌ Erreur lors du chargement des statistiques</div>';
                });
        }

        function getProductsByClient() {
            const clientName = document.getElementById('client-select').value;
            if (!clientName) {
                alert('⚠️ Veuillez sélectionner un client');
                return;
            }

            showLoading('client-results');

            fetch(`/api/products-by-client?client=${encodeURIComponent(clientName)}`)
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="results">';
                    html += `<h3>🛍️ Produits achetés par ${clientName}</h3>`;
                    
                    if (data.length === 0) {
                        html += '<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">Aucun produit trouvé</p>';
                    } else {
                        html += '<ul>';
                        data.forEach(item => {
                            html += `<li>
                                <span class="product-name">${item.produit}</span>
                                <span class="price">${item.prix}€</span>
                            </li>`;
                        });
                        html += '</ul>';
                    }
                    html += '</div>';
                    document.getElementById('client-results').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('client-results').innerHTML = 
                        '<div class="error">❌ Erreur lors de la recherche</div>';
                });
        }

        function getSuggestions() {
            const clientName = document.getElementById('suggestion-client').value;
            if (!clientName) {
                alert('⚠️ Veuillez sélectionner un client');
                return;
            }

            showLoading('suggestion-results');

            fetch(`/api/suggestions?client=${encodeURIComponent(clientName)}`)
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="results">';
                    html += `<h3>🤖 Suggestions pour ${clientName}</h3>`;
                    
                    if (data.length === 0) {
                        html += '<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">Aucune suggestion disponible</p>';
                    } else {
                        html += '<ul>';
                        data.forEach(item => {
                            html += `<li>
                                <div>
                                    <span class="product-name">${item.produit_suggere}</span>
                                    <span class="price">${item.prix}€</span>
                                </div>
                                <span class="score">Score: ${item.score}</span>
                            </li>`;
                        });
                        html += '</ul>';
                    }
                    html += '</div>';
                    document.getElementById('suggestion-results').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('suggestion-results').innerHTML = 
                        '<div class="error">❌ Erreur lors de la génération des suggestions</div>';
                });
        }

        function getClientsByProduct() {
            const productName = document.getElementById('product-select').value;
            if (!productName) {
                alert('⚠️ Veuillez sélectionner un produit');
                return;
            }

            showLoading('product-results');

            fetch(`/api/clients-by-product?product=${encodeURIComponent(productName)}`)
                .then(response => response.json())
                .then(data => {
                    let html = '<div class="results">';
                    html += `<h3>👤 Clients ayant acheté ${productName}</h3>`;
                    
                    if (data.length === 0) {
                        html += '<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">Aucun client trouvé</p>';
                    } else {
                        html += '<ul>';
                        data.forEach(item => {
                            html += `<li>
                                <div>
                                    <span class="client-name">${item.client}</span>
                                    <span style="color: var(--text-secondary); font-size: 0.9rem;">${item.email}</span>
                                </div>
                            </li>`;
                        });
                        html += '</ul>';
                    }
                    html += '</div>';
                    document.getElementById('product-results').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('product-results').innerHTML = 
                        '<div class="error">❌ Erreur lors de la recherche</div>';
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Récupère la liste des clients"""
    try:
        query = "MATCH (c:Client) RETURN c.nom as nom ORDER BY c.nom"
        results = run_query(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Récupère la liste des produits"""
    try:
        query = "MATCH (p:Produit) RETURN p.nom as nom ORDER BY p.nom"
        results = run_query(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Récupère les statistiques générales"""
    try:
        stats = {}
        
        # Nombre total de clients
        query = "MATCH (c:Client) RETURN COUNT(c) as count"
        result = run_query(query)
        stats['total_clients'] = result[0]['count']
        
        # Nombre total de produits
        query = "MATCH (p:Produit) RETURN COUNT(p) as count"
        result = run_query(query)
        stats['total_produits'] = result[0]['count']
        
        # Nombre total de commandes
        query = "MATCH (cmd:Commande) RETURN COUNT(cmd) as count"
        result = run_query(query)
        stats['total_commandes'] = result[0]['count']
        
        # Chiffre d'affaires total
        query = "MATCH (cmd:Commande) RETURN SUM(cmd.total) as total"
        result = run_query(query)
        stats['chiffre_affaires'] = result[0]['total']
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products-by-client', methods=['GET'])
def get_products_by_client():
    """Récupère tous les produits achetés par un client"""
    client_name = request.args.get('client')
    if not client_name:
        return jsonify({"error": "Paramètre 'client' requis"}), 400
    
    try:
        query = """
        MATCH (c:Client {nom: $client_name})-[:A_EFFECTUE]->(cmd:Commande)-[:CONTIENT]->(p:Produit)
        RETURN DISTINCT p.nom as produit, p.prix as prix
        ORDER BY p.nom
        """
        results = run_query(query, {"client_name": client_name})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/clients-by-product', methods=['GET'])
def get_clients_by_product():
    """Récupère tous les clients ayant acheté un produit donné"""
    product_name = request.args.get('product')
    if not product_name:
        return jsonify({"error": "Paramètre 'product' requis"}), 400
    
    try:
        query = """
        MATCH (c:Client)-[:A_EFFECTUE]->(cmd:Commande)-[:CONTIENT]->(p:Produit {nom: $product_name})
        RETURN DISTINCT c.nom as client, c.email as email
        ORDER BY c.nom
        """
        results = run_query(query, {"product_name": product_name})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Obtient des suggestions de produits pour un client"""
    client_name = request.args.get('client')
    if not client_name:
        return jsonify({"error": "Paramètre 'client' requis"}), 400
    
    try:
        query = """
        MATCH (client:Client {nom: $client_name})-[:A_EFFECTUE]->(cmd1:Commande)-[:CONTIENT]->(p1:Produit)
        MATCH (autres:Client)-[:A_EFFECTUE]->(cmd2:Commande)-[:CONTIENT]->(p1)
        MATCH (autres)-[:A_EFFECTUE]->(cmd3:Commande)-[:CONTIENT]->(suggestion:Produit)
        WHERE client <> autres 
          AND NOT (client)-[:A_EFFECTUE]->(:Commande)-[:CONTIENT]->(suggestion)
        RETURN suggestion.nom as produit_suggere, suggestion.prix as prix, COUNT(*) as score
        ORDER BY score DESC, suggestion.nom
        LIMIT 5
        """
        results = run_query(query, {"client_name": client_name})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders-by-product', methods=['GET'])
def get_orders_by_product():
    """Récupère les commandes contenant un produit spécifique"""
    product_name = request.args.get('product')
    if not product_name:
        return jsonify({"error": "Paramètre 'product' requis"}), 400
    
    try:
        query = """
        MATCH (cmd:Commande)-[cont:CONTIENT]->(p:Produit {nom: $product_name})
        MATCH (c:Client)-[:A_EFFECTUE]->(cmd)
        RETURN cmd.id as commande_id, cmd.date as date, c.nom as client, cont.quantite as quantite
        ORDER BY cmd.date
        """
        results = run_query(query, {"product_name": product_name})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def close_driver():
    """Ferme la connexion Neo4j"""
    driver.close()

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    finally:
        close_driver()