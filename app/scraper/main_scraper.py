#!/usr/bin/env python3
"""
🔥 SCRAPER PRINCIPAL - BLOG DU MODÉRATEUR
Scraper optimisé pour 15 articles avec structure HTML actuelle
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BlogScraper:
    """Scraper pour blogdumoderateur.com - 15 articles maximum"""
    
    def __init__(self):
        self.base_url = "https://www.blogdumoderateur.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_articles(self, max_articles: int = 15) -> List[Dict]:
        """
        Scrape les articles du blog
        
        Args:
            max_articles: Nombre maximum d'articles (15 par défaut)
            
        Returns:
            Liste des articles scrapés
        """
        logger.info(f"🚀 Début du scraping - Maximum {max_articles} articles")
        
        try:
            # Requête principale
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Sélecteur pour les articles basé sur la structure fournie
            articles_elements = soup.select('article[id^="post-"]')
            
            if not articles_elements:
                logger.warning("⚠️ Aucun article trouvé avec le sélecteur principal")
                return []
            
            logger.info(f"📄 {len(articles_elements)} articles trouvés")
            
            articles = []
            
            for i, article_elem in enumerate(articles_elements[:max_articles], 1):
                try:
                    article_data = self._extract_article_data(article_elem, i)
                    if article_data:
                        articles.append(article_data)
                        logger.info(f"✅ Article {i}/15: {article_data['title'][:50]}...")
                    
                    # Pause courtoise
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"❌ Erreur article {i}: {e}")
                    continue
            
            logger.info(f"🎯 Scraping terminé: {len(articles)}/15 articles récupérés")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Erreur de scraping: {e}")
            return []
    
    def _extract_article_data(self, article_elem, index: int) -> Optional[Dict]:
        """Extraction des données d'un article"""
        
        try:
            # ID de l'article
            article_id = article_elem.get('id', f'post-{index}')
            
            # Titre dans .entry-header a h3.entry-title
            title_elem = article_elem.select_one('.entry-header a h3.entry-title')
            title = title_elem.get_text(strip=True) if title_elem else "Titre non trouvé"
            
            # URL dans .entry-header a
            url_elem = article_elem.select_one('.entry-header a')
            url = url_elem.get('href') if url_elem else ""
            
            # Date dans time.entry-date
            date_elem = article_elem.select_one('time.entry-date')
            date_str = ""
            if date_elem:
                # Priorité au datetime
                date_str = date_elem.get('datetime', '')
                if not date_str:
                    date_str = date_elem.get_text(strip=True)
            
            # Formatage de la date
            formatted_date = self._format_date(date_str)
            
            # Extraction de l'extrait depuis la page de l'article
            excerpt = self._get_excerpt_from_article(url)
            
            # Catégorie dans .favtag
            category_elem = article_elem.select_one('.favtag')
            category = category_elem.get_text(strip=True) if category_elem else "Non classé"
            
            # Image
            img_elem = article_elem.select_one('.post-thumbnail img')
            image_url = ""
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-lazy-src', '')
            
            return {
                'id': article_id,
                'title': title,
                'url': url,
                'date': formatted_date,
                'excerpt': excerpt,
                'category': category,
                'image_url': image_url,
                'author': "Blog du Modérateur",  # Par défaut
                'scraped_at': datetime.now().strftime("%d/%m/%Y à %H:%M")
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur extraction article: {e}")
            return None
    
    def _get_excerpt_from_article(self, url: str) -> str:
        """Récupère l'extrait depuis la page de l'article"""
        
        if not url:
            return "Pas de description disponible."
        
        try:
            # Requête vers la page de l'article
            response = self.session.get(url, timeout=8)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Essai de différents sélecteurs pour l'extrait
            selectors = [
                '.entry-content p:first-of-type',
                '.post-content p:first-of-type', 
                '.content p:first-of-type',
                'article p:first-of-type',
                '.entry-excerpt',
                'meta[name="description"]'
            ]
            
            for selector in selectors:
                if selector.startswith('meta'):
                    # Cas spécial pour meta description
                    meta_elem = soup.select_one(selector)
                    if meta_elem and meta_elem.get('content'):
                        return meta_elem.get('content')[:250] + "..."
                else:
                    excerpt_elem = soup.select_one(selector)
                    if excerpt_elem:
                        text = excerpt_elem.get_text(strip=True)
                        if len(text) > 50:  # Assez de contenu
                            return text[:250] + "..." if len(text) > 250 else text
            
            return "Description disponible sur la page de l'article."
            
        except Exception as e:
            logger.warning(f"⚠️ Impossible de récupérer l'extrait depuis {url}: {e}")
            return "Consultez l'article pour plus de détails."
    
    def _format_date(self, date_str: str) -> str:
        """Formatage lisible des dates"""
        
        if not date_str:
            return "Date inconnue"
        
        try:
            # Format ISO avec timezone (2025-07-10T10:58:00+02:00)
            if 'T' in date_str and '+' in date_str:
                dt = datetime.fromisoformat(date_str.replace('+02:00', ''))
                return dt.strftime("%d/%m/%Y à %H:%M")
            
            # Format français direct (10 juillet 2025)
            if 'juillet' in date_str or 'janvier' in date_str:
                return date_str
            
            # Autres formats
            return date_str
            
        except Exception:
            return date_str

def main():
    """Test du scraper"""
    scraper = BlogScraper()
    articles = scraper.scrape_articles(max_articles=15)
    
    print(f"\n🎯 RÉSULTATS:")
    print(f"   📊 Articles récupérés: {len(articles)}")
    
    if articles:
        print(f"\n📖 PREMIERS ARTICLES:")
        for i, article in enumerate(articles[:3], 1):
            print(f"{i}. {article['title']}")
            print(f"   📅 {article['date']}")
            print(f"   🏷️ {article['category']}")
            print()

if __name__ == "__main__":
    main()
