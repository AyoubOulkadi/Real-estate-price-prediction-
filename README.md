# Real-estate-price-prediction-
Ce projet consiste à collecter des données immobilières à partir du site **SAROUTY** en utilisant Selenium via une **instance EC2 d'Amazon Web Services (AWS)**. Les données collectées sont ensuite stockées dans un **bucket S3 pour un traitement ultérieur**.

Ensuite, les données sont nettoyées, transformées et ingérées à l'aide d'**AWS Glue**. Le nettoyage et la transformation des données consistent à éliminer les doublons, à remplir les valeurs manquantes, à supprimer les données non pertinentes et à effectuer des transformations de données pour mieux les adapter à l'apprentissage automatique.

Une fois les données préparées, un modèle de machine learning est créé pour prédire les prix immobiliers en utilisant les autres colonnes. Pour automatiser le processus de scraping et de nettoyage des données, un fichier DAG est créé à l'aide de Airflow pour planifier et exécuter les tâches en fonction d'un calendrier spécifique.

**Dans l'ensemble, ce projet vise à fournir une méthode efficace pour collecter et traiter des données immobilières à grande échelle, afin de fournir des prévisions précises et des informations utiles pour les analystes immobiliers, les investisseurs et les professionnels de l'immobilier.**


<h2> Architecture du projet </h2>


**EC2 instance** exécute un script Python utilisant Selenium pour extraire les données depuis SAROUTY.
Les données collectées sont stockées dans un format tabulaire csv dans un fichier sur l'instance EC2.

**Stockage des données dans un bucket S3**:
Les données collectées sont transférées depuis l'instance EC2 vers un bucket S3 sur AWS à l'aide de la bibliothèque Python boto3.

**Nettoyage des données avec AWS Glue** :

Les données stockées dans le bucket S3 sont traitées par AWS Glue, qui peut être utilisé pour effectuer les étapes de nettoyage des données et de feature engineering.
**AWS Glue** est un service de traitement de données entièrement géré qui peut traiter les données stockées dans S3, éliminer les doublons, remplir les valeurs manquantes et appliquer des transformations de données.
Les données nettoyées et transformées sont stockées dans un autre bucket S3.

**Création d'un modèle de machine learning**:

Les données nettoyées et transformées sont utilisées pour créer un modèle de machine learning qui prédit les prix de l'immobilier.
Les bibliothèques de machine learning populaires telles que scikit-learn peuvent être utilisées pour créer le modèle.
Le modèle est entraîné sur les données et évalué pour déterminer son exactitude.

**Automatisation du processus avec Airflow**:

Un fichier DAG est créé avec Apache Airflow pour automatiser le processus de scraping et de nettoyage des données.
Le DAG peut être configuré pour s'exécuter à une fréquence spécifique (par exemple, une fois par jour) pour maintenir les données à jour.
Airflow peut également envoyer des notifications par e-mail pour informer les utilisateurs du succès ou de l'échec du processus de scraping et de nettoyage.
