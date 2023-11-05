import csv
from datetime import datetime, timedelta

# Nom du fichier CSV contenant les données d'entrée
fichier_csv_entree = "donnees_anonyme.csv"

# Nom du fichier CSV de sortie pour les données finales
fichier_csv_sortie = "donnees_finales.csv"

# Ouvrir le fichier CSV d'entrée et lire les données en excluant les lignes contenant "DEL"
data = []
with open(fichier_csv_entree, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t', fieldnames=["id", "date", "lat", "long"])
    next(csv_reader, None)  # Skip the header row
    for row in csv_reader:
        if "DEL" not in row["id"]:
            data.append([row["id"], row["date"], float(row["lat"]), float(row["long"])])

# Convertir les données de date en objets datetime
for entry in data:
    entry[1] = datetime.strptime(entry[1], "%Y-%m-%d %H:%M:%S")

# Définir une durée minimale pour qu'un endroit soit considéré comme un point d'intérêt (1 heure)
duree_minimale = timedelta(hours=2)

# Définir une tolérance pour la latitude (0.01 en plus ou en moins)
tolerance_latitude = 0.02

# Initialiser un dictionnaire pour stocker les points d'intérêt pour chaque utilisateur et chaque semaine
points_d_interet_par_utilisateur_semaine = {}

# Parcourir les données
for entry in data:
    semaine = entry[1].strftime("%Y-%U")  # Format de la semaine "2023-12"
    utilisateur = entry[0]

    if utilisateur not in points_d_interet_par_utilisateur_semaine:
        points_d_interet_par_utilisateur_semaine[utilisateur] = {}

    if semaine not in points_d_interet_par_utilisateur_semaine[utilisateur]:
        points_d_interet_par_utilisateur_semaine[utilisateur][semaine] = []

    # Si la liste est vide, ajoutez le point d'intérêt
    if not points_d_interet_par_utilisateur_semaine[utilisateur][semaine]:
        points_d_interet_par_utilisateur_semaine[utilisateur][semaine].append(entry)
    else:
        # Vérifiez la tolérance de latitude pour ajouter le point d'intérêt
        doublon = False
        for point in points_d_interet_par_utilisateur_semaine[utilisateur][semaine]:
            if abs(entry[2] - point[2]) <= tolerance_latitude:
                doublon = True
                break
        if not doublon:
            points_d_interet_par_utilisateur_semaine[utilisateur][semaine].append(entry)

# Écrire les points d'intérêt dans un fichier CSV de sortie trié par ID, date, latitude, longitude
with open(fichier_csv_sortie, "w", newline="") as output_file:
    csv_writer = csv.writer(output_file, delimiter='\t')
    csv_writer.writerow(["id", "semaine", "lat", "long"])
    
    for utilisateur, semaines in points_d_interet_par_utilisateur_semaine.items():
        for semaine, points in semaines.items():
            sorted_points = sorted(points, key=lambda x: (x[0], x[1], x[2], x[3]))
            for point in sorted_points:
                csv_writer.writerow([point[0], semaine, point[2], point[3]])
