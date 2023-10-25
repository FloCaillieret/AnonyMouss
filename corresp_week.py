import json

# Charger les fichiers JSON source et target
with open('source.json', 'r') as source_file:
    source_data = json.load(source_file)

with open('target.json', 'r') as target_file:
    target_data = json.load(target_file)

# Créer un dictionnaire pour stocker la correspondance entre les IDs source et target
res = {}

# Parcourir les IDs du fichier source
for source_id, source_weeks in source_data.items():
    # Parcourir les IDs du fichier target
    for target_id, target_weeks in target_data.items():
        # Vérifier si les semaines correspondent
        if set(source_weeks) == set(target_weeks):
            if source_id not in res:
                res[source_id] = []
            res[source_id].append(target_id)

# Enregistrer le résultat dans un fichier JSON
with open('res.json', 'w') as res_file:
    json.dump(res, res_file, sort_keys=True, indent=4)
