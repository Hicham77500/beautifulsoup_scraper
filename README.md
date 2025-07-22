# 📰 Blog du Modérateur Scraper

Scraper optimisé pour récupérer 15 articles du Blog du Modérateur avec descriptions complètes et interface web moderne.

## 🚀 Quick Start

```bash
# 1. Installation
cd Beautifulsoup_scraper
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# 2. Scraping des articles
python scrape_direct.py

# 3. Interface web
python interface_simple.py
# ➡️ Ouvrir http://localhost:8080
```

## 📁 Architecture Clean

```
📁 Beautifulsoup_scraper/
├── 📁 app/                    # Code principal organisé
│   ├── 📁 database/          # Service MongoDB
│   │   ├── mongo_service.py  # Gestion base de données
│   │   └── __init__.py
│   ├── 📁 scraper/           # Module de scraping
│   │   ├── main_scraper.py   # Scraper principal (15 articles + descriptions)
│   │   └── __init__.py
│   └── __init__.py
├── 📁 mongo_seed/            # Données initiales pour Docker
├── scrape_direct.py          # ⭐ Script principal de scraping
├── interface_simple.py       # ⭐ Interface web Flask (port 8080)
├── check_mongodb.py          # Diagnostic MongoDB
├── docker-compose.yml        # MongoDB local + auto-import
├── init-mongo.sh            # Script d'initialisation Docker
├── requirements.txt         # Dépendances Python
└── README.md               # Documentation
```

## 🛠️ Installation Détaillée

### Prérequis
- Python 3.8+
- MongoDB Atlas OU Docker
- Navigateur web moderne

### Setup Complet
```bash
# Clone et activation environnement
cd Beautifulsoup_scraper
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# Windows: .venv\Scripts\activate

# Installation dépendances
pip install -r requirements.txt
```

### Configuration MongoDB

**Option A: MongoDB Atlas (Cloud)**
- Configuration par défaut dans `app/database/mongo_service.py`
- Connexion automatique avec certificat SSL

**Option B: MongoDB Local (Docker)**
```bash
# Démarrage conteneur MongoDB
docker-compose up -d

# Le conteneur utilise le port 27018 (évite les conflits)
# Restauration automatique des données via init-mongo.sh
```

## 🎯 Utilisation

### 1. Scraping des Articles
```bash
# Lance le scraping de 15 articles avec descriptions complètes
python scrape_direct.py
```
**Fonctionnalités :**
- Récupération de 15 articles maximum
- Extraction des descriptions depuis les pages individuelles
- Formatage des dates lisibles
- Sauvegarde automatique en MongoDB
- Logging détaillé

### 2. Interface Web
```bash
# Démarre l'interface web
python interface_simple.py
```
**Accès :** http://localhost:8080

**Fonctionnalités :**
- Affichage des 15 articles avec descriptions
- Recherche en temps réel (titre, description, catégorie)
- Design responsive et moderne
- Statistiques de la base de données
- Liens directs vers les articles

### 3. Diagnostic MongoDB
```bash
# Vérification de la base de données
python check_mongodb.py
```

## 🐳 Docker Setup

### Démarrage MongoDB + Données
```bash
# 1. Démarrage du conteneur MongoDB
docker-compose up -d

# 2. Vérification
docker ps  # Doit montrer le conteneur 'mongodb'

# 3. Scraping dans le conteneur local
python scrape_direct.py

# 4. Interface web
python interface_simple.py
```

### Auto-import des Données
- Le script `init-mongo.sh` restaure automatiquement les données du dossier `mongo_seed/`
- Idéal pour le professeur : `docker-compose up` et tout est prêt !

## 🔧 Configuration Avancée

### Variables d'Environnement (.env)
```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27018/  # Local Docker
# OU
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/  # Atlas

# Interface Web
PORT=8080  # Port de l'interface (défaut: 8080)
```

## � Workflow Complet

```bash
# 1. Setup initial
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Scraping + Interface (MongoDB Atlas)
python scrape_direct.py && python interface_simple.py

# 3. OU Scraping + Interface (Docker Local)
docker-compose up -d
python scrape_direct.py && python interface_simple.py

# 4. Accès interface
# ➡️ http://localhost:8080
```

## ✅ Points Clés

- **🎯 15 articles** avec descriptions complètes
- **⚡ Interface rapide** sur port 8080 (évite les conflits)
- **🐳 Docker ready** pour déploiement facile
- **🔍 Recherche temps réel** dans l'interface
- **📱 Design responsive** mobile-friendly
- **🛡️ Architecture clean** et maintenable

---

**Développé pour IPSSI - Clean Architecture & Modern Web Scraping**
