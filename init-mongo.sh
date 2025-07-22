#!/bin/bash

# Restaure les données seed si présentes
if [ -d /mongo_seed ] && [ "$(ls -A /mongo_seed)" ]; then
 echo "📦 Restauration des données seed..."
 mongorestore /mongo_seed
else
 echo "⚠️ Aucune donnée seed, restauration ignorée."
fi
