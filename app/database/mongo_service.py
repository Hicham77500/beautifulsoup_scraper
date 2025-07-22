#!/usr/bin/env python3
"""
🗄️ SERVICE MONGODB - OPTIMISÉ
Gestion MongoDB avec formatage des dates amélioré
"""

from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional
import logging
import os

# Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27018/')
DATABASE_NAME = "scraper_db"
COLLECTION_NAME = "articles"

logger = logging.getLogger(__name__)

class MongoService:
    """Service MongoDB optimisé pour les articles"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Connexion à MongoDB avec certificat Atlas"""
        try:
            # Sélectionne le mode de connexion suivant Atlas ou local
            if MONGODB_URI.startswith('mongodb+srv'):
                ca_path = os.path.join(os.path.dirname(__file__), '../../atlas-cert.pem')
                self.client = MongoClient(
                    MONGODB_URI,
                    tls=True,
                    tlsCAFile=ca_path
                )
            else:
                # Connexion simple pour MongoDB local
                self.client = MongoClient(MONGODB_URI)
            # Test de connexion
            self.client.admin.command('ping')
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            logger.info("✅ MongoDB connecté (certificat Atlas)")
        except Exception as e:
            logger.error(f"❌ Erreur MongoDB: {e}")
            raise
    
    def save_articles(self, articles: List[Dict]) -> bool:
        """Sauvegarde des articles avec mise à jour"""
        
        if not articles:
            return False
        
        try:
            # Nettoyage de la collection
            self.collection.delete_many({})
            logger.info("🗑️ Anciens articles supprimés")
            
            # Insertion des nouveaux articles
            for article in articles:
                # Ajout timestamp
                article['saved_at'] = datetime.now()
                
            result = self.collection.insert_many(articles)
            logger.info(f"💾 {len(result.inserted_ids)} articles sauvegardés")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde: {e}")
            return False
    
    def get_articles(self, limit: int = 15) -> List[Dict]:
        """Récupération des articles avec formatage des dates"""
        
        try:
            # Récupération depuis MongoDB
            cursor = self.collection.find().limit(limit)
            articles = list(cursor)
            
            # Formatage des articles
            formatted_articles = []
            for article in articles:
                # Conversion _id en string
                article['_id'] = str(article['_id'])
                
                # Formatage de la date pour l'affichage
                if 'saved_at' in article:
                    saved_at = article['saved_at']
                    if isinstance(saved_at, datetime):
                        article['date_formatted'] = saved_at.strftime("%d/%m/%Y à %H:%M")
                    else:
                        article['date_formatted'] = str(saved_at)
                else:
                    article['date_formatted'] = article.get('date', 'Date inconnue')
                
                formatted_articles.append(article)
            
            logger.info(f"📄 {len(formatted_articles)} articles récupérés")
            return formatted_articles
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération: {e}")
            return []
    
    def search_articles(self, query: str) -> List[Dict]:
        """Recherche dans les articles"""
        
        if not query:
            return self.get_articles()
        
        try:
            # Recherche dans titre et contenu
            search_filter = {
                '$or': [
                    {'title': {'$regex': query, '$options': 'i'}},
                    {'excerpt': {'$regex': query, '$options': 'i'}},
                    {'category': {'$regex': query, '$options': 'i'}}
                ]
            }
            
            cursor = self.collection.find(search_filter).limit(15)
            articles = list(cursor)
            
            # Formatage
            for article in articles:
                article['_id'] = str(article['_id'])
                if 'saved_at' in article and isinstance(article['saved_at'], datetime):
                    article['date_formatted'] = article['saved_at'].strftime("%d/%m/%Y à %H:%M")
                else:
                    article['date_formatted'] = article.get('date', 'Date inconnue')
            
            logger.info(f"🔍 {len(articles)} articles trouvés pour '{query}'")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Erreur recherche: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Statistiques de la base"""
        
        try:
            total = self.collection.count_documents({})
            
            # Dernier article
            last_article = self.collection.find_one(sort=[('saved_at', -1)])
            last_update = "Aucune donnée"
            
            if last_article and 'saved_at' in last_article:
                if isinstance(last_article['saved_at'], datetime):
                    last_update = last_article['saved_at'].strftime("%d/%m/%Y à %H:%M")
            
            return {
                'total_articles': total,
                'last_update': last_update,
                'status': 'Actif' if total > 0 else 'Vide'
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur stats: {e}")
            return {'total_articles': 0, 'last_update': 'Erreur', 'status': 'Erreur'}
    
    def close(self):
        """Fermeture de la connexion"""
        if self.client:
            self.client.close()
            logger.info("🔒 MongoDB fermé")

def test_mongo():
    """Test rapide du service"""
    service = MongoService()
    
    stats = service.get_stats()
    print(f"📊 Stats: {stats}")
    
    articles = service.get_articles(5)
    print(f"📄 Articles: {len(articles)}")
    
    service.close()

if __name__ == "__main__":
    test_mongo()
