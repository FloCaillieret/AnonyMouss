import pandas as pd
from datetime import datetime

# Charger le fichier source.csv
df = pd.read_csv('source.csv', delimiter='\t', header=None, names=['identifiant', 'date_heure', 'longitude', 'latitude'])

# Convertir la colonne date_heure en format datetime
df['date_heure'] = pd.to_datetime(df['date_heure'])

# Fonction pour arrondir l'heure aux intervalles spécifiés
def round_hour(dt):
    hour = (dt.hour // 4) * 4  # arrondir à la dernière heure multiple de 4
    return dt.replace(hour=hour, minute=0, second=0)

# Appliquer la fonction d'arrondi à la colonne date_heure
df['date_heure'] = df['date_heure'].apply(round_hour)

# Arrondir la longitude et la latitude à 3 chiffres après la virgule
df['longitude'] = df['longitude'].round(3)
df['latitude'] = df['latitude'].round(3)

# Sauvegarder le résultat dans Ano.csv
df.to_csv('NotreAnonym.csv', sep='\t', index=False, header=False)
