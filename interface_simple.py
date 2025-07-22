#!/usr/bin/env python3
"""
🌐 INTERFACE WEB SIMPLIFIÉE
Interface Flask optimisée - 15 articles avec dates lisibles
"""

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import os

# Import du service MongoDB depuis le nouveau chemin
from app.database.mongo_service import MongoService

app = Flask(__name__)
CORS(app)

# Template HTML compact
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📰 Blog du Modérateur - 15 Articles</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
        .stats { display: flex; gap: 20px; justify-content: center; margin: 15px 0; }
        .stat { background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 5px; }
        .search { text-align: center; margin: 20px 0; }
        .search input { padding: 12px; width: 300px; border: 1px solid #ddd; border-radius: 25px; font-size: 16px; }
        .articles { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .article { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); transition: transform 0.2s; }
        .article:hover { transform: translateY(-2px); }
        .article-title { color: #2c3e50; font-size: 18px; font-weight: bold; margin-bottom: 10px; line-height: 1.3; }
        .article-title a { color: inherit; text-decoration: none; }
        .article-title a:hover { color: #667eea; }
        .article-meta { color: #666; font-size: 14px; margin-bottom: 10px; }
        .article-excerpt { color: #555; line-height: 1.5; margin-bottom: 15px; }
        .article-category { background: #667eea; color: white; padding: 4px 8px; border-radius: 3px; font-size: 12px; display: inline-block; margin-bottom: 10px; }
        .loading { text-align: center; color: #667eea; font-size: 18px; padding: 40px; }
        .no-results { text-align: center; color: #666; padding: 40px; }
        @media (max-width: 768px) { 
            .articles { grid-template-columns: 1fr; }
            .stats { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 Blog du Modérateur</h1>
            <p>15 articles avec dates lisibles</p>
            <div class="stats">
                <div class="stat">📊 <span id="total">-</span> articles</div>
                <div class="stat">🕒 MAJ: <span id="update">-</span></div>
            </div>
        </div>
        
        <div class="search">
            <input type="text" id="search-input" placeholder="🔍 Rechercher dans les articles..." />
        </div>
        
        <div id="articles-container" class="articles">
            <div class="loading">⏳ Chargement des articles...</div>
        </div>
    </div>
    
    <script>
        let allArticles = [];
        
        // Chargement initial
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadArticles();
            
            // Recherche
            document.getElementById('search-input').addEventListener('input', function() {
                const query = this.value.toLowerCase();
                filterArticles(query);
            });
        });
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                document.getElementById('total').textContent = stats.total_articles;
                document.getElementById('update').textContent = stats.last_update;
            } catch (error) {
                console.error('Erreur stats:', error);
            }
        }
        
        async function loadArticles() {
            try {
                const response = await fetch('/api/articles');
                allArticles = await response.json();
                displayArticles(allArticles);
            } catch (error) {
                console.error('Erreur articles:', error);
                document.getElementById('articles-container').innerHTML = 
                    '<div class="no-results">❌ Erreur de chargement</div>';
            }
        }
        
        function filterArticles(query) {
            if (!query) {
                displayArticles(allArticles);
                return;
            }
            
            const filtered = allArticles.filter(article => 
                article.title.toLowerCase().includes(query) ||
                article.excerpt.toLowerCase().includes(query) ||
                article.category.toLowerCase().includes(query)
            );
            
            displayArticles(filtered);
        }
        
        function displayArticles(articles) {
            const container = document.getElementById('articles-container');
            
            if (!articles || articles.length === 0) {
                container.innerHTML = '<div class="no-results">🔍 Aucun résultat trouvé</div>';
                return;
            }
            
            const html = articles.map(article => `
                <div class="article">
                    <div class="article-category">${article.category || 'Non classé'}</div>
                    <div class="article-title">
                        <a href="${article.url}" target="_blank">${article.title}</a>
                    </div>
                    <div class="article-meta">
                        📅 ${article.date_formatted || article.date || 'Date inconnue'} • 
                        👤 ${article.author || 'Auteur inconnu'}
                    </div>
                    <div class="article-excerpt">${article.excerpt || 'Pas de description...'}</div>
                </div>
            `).join('');
            
            container.innerHTML = html;
        }
    </script>
</body>
</html>
"""

# Service MongoDB
mongo_service = MongoService()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def api_stats():
    stats = mongo_service.get_stats()
    return jsonify(stats)

@app.route('/api/articles')
def api_articles():
    articles = mongo_service.get_articles(15)
    return jsonify(articles)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    articles = mongo_service.search_articles(query)
    return jsonify(articles)

if __name__ == '__main__':
    # Port sûr pour éviter ERR_UNSAFE_PORT
    port = 8080
    print(f"🚀 Interface Web - Articles Réorganisés")
    print(f"📱 URL: http://localhost:{port}")
    print("📊 15 articles avec dates lisibles")
    print("-" * 40)
    app.run(host='0.0.0.0', port=port, debug=True)
