# Utiliser une image de base légère avec Python
FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt .
COPY main.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande de démarrage du conteneur
CMD ["python", r"C:\datalake\Real-estate-price-prediction\src\data_collection\main.py"]
