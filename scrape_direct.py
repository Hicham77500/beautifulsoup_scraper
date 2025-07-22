#!/usr/bin/env python3
"""
🎯 SCRAPER DIRECT - SANS BOUCLE
Exécution directe du scraping + MongoDB
"""

import sys
import os
from datetime import datetime
import logging

# Configuration des imports
from app.scraper.main_scraper import BlogScraper
from app.database.mongo_service import MongoService

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Exécution directe du scraping"""
    
    print("🚀 SCRAPING DIRECT - 15 ARTICLES")
    print("=" * 40)
    
    try:
        # 1. Initialisation
        print("📡 Initialisation du scraper...")
        scraper = BlogScraper()
        mongo_service = MongoService()
        
        # 2. Scraping
        print("🔍 Scraping en cours...")
        articles = scraper.scrape_articles(max_articles=15)
        
        if not articles:
            print("❌ Aucun article récupéré")
            return
        
        print(f"✅ {len(articles)} articles scrapés")
        
        # 3. Sauvegarde MongoDB
        print("💾 Sauvegarde dans MongoDB...")
        success = mongo_service.save_articles(articles)
        
        if success:
            print("✅ Sauvegarde réussie")
        else:
            print("❌ Erreur de sauvegarde")
            return
        
        # 4. Vérification
        print("🔍 Vérification...")
        saved_articles = mongo_service.get_articles(15)
        print(f"📊 Articles en base: {len(saved_articles)}")
        
        # 5. Aperçu
        print("\n📖 PREMIERS ARTICLES:")
        for i, article in enumerate(articles[:3], 1):
            print(f"{i}. {article['title'][:50]}...")
            print(f"   📅 {article['date']}")
            print(f"   🏷️ {article['category']}")
        
        print("\n🎯 SCRAPING TERMINÉ AVEC SUCCÈS!")
        print("💡 Utilisez 'python src/web/interface.py' pour l'interface")
        
        mongo_service.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        logger.error(f"Erreur critique: {e}")

if __name__ == "__main__":
    main()
