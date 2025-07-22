#!/usr/bin/env python3
"""
🔍 DIAGNOSTIC MONGODB
Vérification rapide de la base de données
"""

import sys
import os
from pymongo import MongoClient

# Import du service MongoDB
from app.database.mongo_service import MongoService

# Votre URI MongoDB
MONGODB_URI = "mongodb+srv://hguendouz:xE1N0X15zAOb1HQu@cluster0.mtowgph.mongodb.net/"

def inspect_mongodb():
    """Inspection complète de votre MongoDB"""
    
    print("🔍 INSPECTION MONGODB")
    print("="*50)
    print(f"📡 URI: {MONGODB_URI[:50]}...")
    print()
    
    try:
        # Connexion
        client = MongoClient(
            MONGODB_URI,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=10000
        )
        
        # Test connexion
        client.admin.command('ping')
        print("✅ Connexion réussie")
        
        # Base scraper_db
        db = client['scraper_db']
        
        # Collection articles
        collection = db['articles']
        
        # Statistiques générales
        total_articles = collection.count_documents({})
        print(f"📊 Total articles: {total_articles}")
        
        # CORRECTION: Vérification réelle du nombre d'articles (doit être 15)
        if total_articles != 15:
            print(f"⚠️ ATTENTION: {total_articles} articles trouvés, attendu: 15")
        
        if total_articles > 0:
            # Articles récents
            recent_articles = list(collection.find().sort('scraped_at', -1).limit(5))
            
            print("\n📖 DERNIERS ARTICLES:")
            print("-" * 30)
            for i, article in enumerate(recent_articles, 1):
                title = article.get('title', 'Sans titre')[:60]
                author = article.get('author', 'Auteur inconnu')
                url = article.get('url', 'Pas d\'URL')
                scraped_at = article.get('scraped_at', 'Date inconnue')
                
                # AMÉLIORATION: Formatage des dates plus lisible
                if isinstance(scraped_at, str):
                    if 'T' in scraped_at:
                        # Format ISO
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(scraped_at.replace('Z', '+00:00').replace('+02:00', ''))
                            scraped = dt.strftime("%d/%m/%Y à %H:%M")
                        except:
                            scraped = scraped_at[:19]
                    else:
                        scraped = scraped_at
                else:
                    scraped = str(scraped_at)[:19] if scraped_at else 'Date inconnue'
                
                print(f"{i}. {title}")
                print(f"   👤 {author}")
                print(f"   🔗 {url}")
                print(f"   📅 {scraped}")
                print()
            
            # Auteurs uniques
            authors_pipeline = [
                {'$group': {'_id': '$author', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            authors = list(collection.aggregate(authors_pipeline))
            
            print("👤 AUTEURS:")
            print("-" * 15)
            for author_data in authors[:10]:
                author = author_data['_id'] or 'Auteur inconnu'
                count = author_data['count']
                print(f"   {author}: {count} article(s)")
        
        else:
            print("⚠️ Aucun article trouvé dans la collection")
        
        # Toutes les collections
        all_collections = db.list_collection_names()
        print(f"\n📂 Collections disponibles: {all_collections}")
        
        client.close()
        
        print("\n" + "="*50)
        print("🎯 RÉSUMÉ:")
        print(f"   ✅ Base de données: ACTIVE")
        print(f"   📊 Articles: {total_articles}")
        print(f"   🔗 Interface: http://localhost:5555")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    inspect_mongodb()
