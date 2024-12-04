import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuration de la connexion à la base de données
db_config = {
    'host': 'localhost',  # Remplacez par votre hôte MySQL
    'user': 'root',       # Remplacez par votre utilisateur MySQL
    'password': 'RYK_mysql-24',  # Remplacez par votre mot de passe MySQL
    'database': 'gestion_Hopital_db'
}

# Connexion à la base de données
try:
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    print("Connexion à la base de données réussie.")
except mysql.connector.Error as err:
    print(f"Erreur de connexion : {err}")
    exit(1)

fake = Faker('fr_FR')
Faker.seed(0)
random.seed(0)

# Listes pour stocker les IDs générés
user_ids_medecin = []
user_ids_comptable = []
user_ids_receptionniste = []
medecin_ids = []
comptable_ids = []
salle_ids = []
receptionniste_ids = []
chambre_ids = []
patient_ids = []
dossier_ids = []
feuille_ids = []
traitement_ids = []
facturation_ids = []

# 1. Insertion dans la table Users
print("Insertion des utilisateurs pour chaque rôle...")

roles = {
    'Medecin': 200,
    'Comptable': 200,
    'Receptionniste': 200
}

for role, count in roles.items():
    for _ in range(count):
        user_name = fake.unique.user_name()[:50]  # Limiter à 50 caractères
        plain_password = fake.password(length=10)[:50]  # Générer des mots de passe en clair, max 50 caractères

        try:
            cursor.execute("""
                INSERT INTO Users (user_Name, password, role)
                VALUES (%s, %s, %s)
            """, (user_name, plain_password, role))
            user_id = cursor.lastrowid
            if role == 'Medecin':
                user_ids_medecin.append(user_id)
            elif role == 'Comptable':
                user_ids_comptable.append(user_id)
            elif role == 'Receptionniste':
                user_ids_receptionniste.append(user_id)
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'insertion d'un utilisateur ({role}) : {err}")

print("Utilisateurs insérés avec succès.")

# 2. Insertion dans la table Medecin
print("Insertion des médecins...")
specialites = [
    'Cardiologie', 'Neurologie', 'Pédiatrie', 'Orthopédie',
    'Dermatologie', 'Gynécologie', 'Chirurgie', 'Psychiatrie'
]

for user_id in user_ids_medecin:
    nom = fake.last_name()
    prenom = fake.first_name()
    specialite = random.choice(specialites)
    email = fake.unique.email()[:50]  # Limiter à 50 caractères
    tel1 = ''.join(filter(str.isdigit, fake.unique.phone_number()))[:15]  # Limiter à 15 caractères
    tel2 = ''.join(filter(str.isdigit, fake.phone_number()))[:15] if random.choice([True, False]) else None
    adresse = fake.address().replace('\n', ', ')[:50]  # Limiter à 50 caractères
    genre = random.choice(['Homme', 'Femme'])

    try:
        cursor.execute("""
            INSERT INTO Medecin (
                nom_Medecin, prenom_Medecin, specialite, email_Medecin,
                telephone_Medecin_1, telephone_Medecin_2, adresse_Medecin,
                genre_Medecin, id_User
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, specialite, email, tel1, tel2, adresse, genre, user_id))
        medecin_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'un médecin : {err}")

print("Médecins insérés avec succès.")

# 3. Insertion dans la table Comptable
print("Insertion des comptables...")

for user_id in user_ids_comptable:
    nom = fake.last_name()
    prenom = fake.first_name()
    tel1 = ''.join(filter(str.isdigit, fake.unique.phone_number()))[:15]
    tel2 = ''.join(filter(str.isdigit, fake.phone_number()))[:15] if random.choice([True, False]) else None
    email = fake.unique.email()[:50]

    try:
        cursor.execute("""
            INSERT INTO Comptable (
                nom_Comptable, prenom_Comptable, telephone_Comptable_1,
                telephone_Comptable_2, mail_Comptable, id_User
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nom, prenom, tel1, tel2, email, user_id))
        comptable_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'un comptable : {err}")

print("Comptables insérés avec succès.")

# 4. Insertion dans la table Receptionniste
print("Insertion des réceptionnistes...")

for user_id in user_ids_receptionniste:
    nom = fake.last_name()
    prenom = fake.first_name()
    email = fake.unique.email()[:50]
    tel1 = ''.join(filter(str.isdigit, fake.unique.phone_number()))[:15]
    tel2 = ''.join(filter(str.isdigit, fake.phone_number()))[:15] if random.choice([True, False]) else None

    try:
        cursor.execute("""
            INSERT INTO Receptionniste (
                nom_Receptionniste, prenom_Receptionniste, email_Receptionniste,
                telephone_Receptionniste_1, telephone_Receptionniste_2, id_User
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nom, prenom, email, tel1, tel2, user_id))
        receptionniste_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'un réceptionniste : {err}")

print("Réceptionnistes insérés avec succès.")

# 5. Insertion dans la table Salle
print("Insertion des salles...")
type_salles = [
    'Opération', 'Consultation', 'Réanimation', 'Urgence',
    'Imagerie', 'Pharmacie', 'Laboratoire', 'Administration'
]

for i in range(1, 201):
    try:
        nom_salle = f"Salle {fake.unique.lexify(text='??')}{i}"[:50]
    except Exception:
        nom_salle = f"Salle {fake.lexify(text='??')}{i}"[:50]
    type_salle = random.choice(type_salles)

    try:
        cursor.execute("""
            INSERT INTO Salle (nom_Salle, type_Salle)
            VALUES (%s, %s)
        """, (nom_salle, type_salle))
        salle_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'une salle : {err}")

print("Salles insérées avec succès.")

# 6. Insertion dans la table Chambre
print("Insertion des chambres...")

for i in range(1, 201):
    capacite = random.randint(1, 4)
    numero_lit = 100 + i  # Assure l'unicité

    try:
        cursor.execute("""
            INSERT INTO Chambre (capacite, numero_Lit)
            VALUES (%s, %s)
        """, (capacite, numero_lit))
        chambre_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'une chambre : {err}")

print("Chambres insérées avec succès.")

# 7. Insertion dans la table Patient
print("Insertion des patients...")
genres = ['Homme', 'Femme']

for _ in range(200):
    nom = fake.last_name()
    prenom = fake.first_name()
    genre = random.choice(genres)
    date_naissance = fake.date_of_birth(minimum_age=0, maximum_age=100).strftime('%Y-%m-%d')
    tel1 = ''.join(filter(str.isdigit, fake.unique.phone_number()))[:15]
    tel2 = ''.join(filter(str.isdigit, fake.phone_number()))[:15] if random.choice([True, False]) else None
    email = fake.unique.email()[:50]
    adresse = fake.address().replace('\n', ', ')[:50]
    id_chambre = random.choice(chambre_ids)

    try:
        cursor.execute("""
            INSERT INTO Patient (
                nom_Patient, prenom_Patient, genre_Patient, date_naissance,
                telephone_Patient_1, telephone_Patient_2, email_Patient,
                adresse_Patient, id_Chambre
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, genre, date_naissance, tel1, tel2, email, adresse, id_chambre))
        patient_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'un patient : {err}")

print("Patients insérés avec succès.")

# 8. Insertion dans la table Dossier_Medical
print("Insertion des dossiers médicaux...")
groupe_sanguin_options = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
statut_rhesus_options = ['Positif', 'Négatif']

for patient_id in patient_ids:
    groupe_sanguin = random.choice(groupe_sanguin_options)
    statut_rhesus = random.choice(statut_rhesus_options)
    observation = fake.text(max_nb_chars=500)[:500]
    date_ouverture_dt = fake.date_time_between(start_date='-5y', end_date='now')
    date_ouverture = date_ouverture_dt.strftime('%Y-%m-%d %H:%M:%S')
    id_receptionniste = random.choice(receptionniste_ids)

    try:
        cursor.execute("""
            INSERT INTO Dossier_Medical (
                groupe_Sanguin, statut_Rhesus, observation, date_Ouverture,
                id_Receptionniste, id_Patient
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (groupe_sanguin, statut_rhesus, observation, date_ouverture, id_receptionniste, patient_id))
        dossier_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'un dossier médical : {err}")

print("Dossiers médicaux insérés avec succès.")

# 9. Insertion dans la table Feuille
print("Insertion des feuilles...")

for dossier_id in dossier_ids:
    date_debut_dt = fake.date_time_between(start_date='-5y', end_date='now')
    if random.choice([True, False]):
        date_fin_dt = fake.date_time_between(start_date=date_debut_dt, end_date='now')
        date_fin = date_fin_dt.strftime('%Y-%m-%d %H:%M:%S') if date_fin_dt >= date_debut_dt else None
    else:
        date_fin = None
    date_debut = date_debut_dt.strftime('%Y-%m-%d %H:%M:%S')
    poids = round(random.uniform(40.0, 150.0), 2)  # DECIMAL(5,2)
    taille = f"{random.randint(140, 200)}cm"[:50]
    pathologie = fake.sentence(nb_words=30)[:300]

    try:
        cursor.execute("""
            INSERT INTO Feuille (
                date_Debut, date_Fin, poids, Taille, Pathologie, id_dossier
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (date_debut, date_fin, poids, taille, pathologie, dossier_id))
        feuille_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'une feuille : {err}")

print("Feuilles insérées avec succès.")

# 10. Insertion dans la table Traitement
print("Insertion des traitements...")
for _ in range(200):
    remarque = fake.text(max_nb_chars=300)[:300]
    conclusion = fake.sentence(nb_words=10)[:100]
    date_heure_dt = fake.date_time_between(start_date='-5y', end_date='now')
    date_heure = date_heure_dt.strftime('%Y-%m-%d %H:%M:%S')
    id_salle = random.choice(salle_ids)
    id_medecin = random.choice(medecin_ids)
    id_feuille = random.choice(feuille_ids) if feuille_ids else None

    if id_feuille is None:
        print("Aucune feuille disponible pour l'insertion d'un traitement. Skipping...")
        continue

    try:
        cursor.execute("""
            INSERT INTO Traitement (
                remarque_Traitement, conclusion, date_heure,
                id_Salle, id_Medecin, id_Feuille
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (remarque, conclusion, date_heure, id_salle, id_medecin, id_feuille))
        traitement_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'un traitement : {err}")

print("Traitements insérés avec succès.")

# 11. Insertion dans la table Facturation
print("Insertion des facturations...")
for _ in range(200):
    date_emission_dt = fake.date_time_between(start_date='-5y', end_date='now')
    date_emission = date_emission_dt.strftime('%Y-%m-%d %H:%M:%S')
    est_payee = random.choice([True, False])
    date_paiement = fake.date_time_between(start_date=date_emission_dt, end_date='now').strftime(
        '%Y-%m-%d %H:%M:%S') if est_payee else None
    montant = round(random.uniform(100.0, 10000.0), 2)
    acteur = fake.company()[:50]
    telephone_acteur = ''.join(filter(str.isdigit, fake.phone_number()))[:15]
    id_patient = random.choice(patient_ids)
    id_comptable = random.choice(comptable_ids) if random.random() < 0.8 else None
    id_feuille = random.choice(feuille_ids) if feuille_ids else None

    if id_feuille is None:
        print("Aucune feuille disponible pour l'insertion d'une facturation. Skipping...")
        continue

    try:
        cursor.execute("""
            INSERT INTO Facturation (
                date_emission, est_Payee, date_Paiement, montant,
                acteur, telephone_Acteur, id_Patient, id_Comptable, id_Feuille
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (date_emission, est_payee, date_paiement, montant, acteur,
              telephone_acteur, id_patient, id_comptable, id_feuille))
        facturation_ids.append(cursor.lastrowid)
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion d'une facturation : {err}")

print("Facturations insérées avec succès.")

# Validation des changements
try:
    db.commit()
    print("Toutes les données ont été insérées avec succès.")
except mysql.connector.Error as err:
    print(f"Erreur lors du commit des transactions : {err}")
    db.rollback()

# Fermeture de la connexion
cursor.close()
db.close()
print("Connexion à la base de données fermée.")
