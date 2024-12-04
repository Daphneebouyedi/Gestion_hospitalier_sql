# viewmodel/ReceptionViewModel.py

import mysql.connector
from mysql.connector import Error
from PySide6.QtGui import QColor
from datetime import datetime, date

class ReceptionViewModel:
    def __init__(self, receptionist_id):
        self.receptionist_id = receptionist_id
        self.db_config = {
            'host': 'localhost',          # Remplacez par votre hôte MySQL si différent
            'user': 'root',               # Remplacez par votre nom d'utilisateur MySQL
            'password': 'RYK_mysql-24', # Remplacez par votre mot de passe MySQL
            'database': 'gestion_Hopital_db'
        }
        self.connection = None
        self.connect_to_database()

    def connect_to_database(self):

        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                print("Connexion à la base de données réussie.")
        except Error as e:
            print(f"Erreur de connexion à la base de données : {e}")
            self.connection = None

    def disconnect_database(self):

        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("Connexion à la base de données fermée.")

    def prepare_patient_data(self):

        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return []

        data = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT nom_Patient, prenom_Patient, date_naissance, telephone_Patient_1, genre_Patient
                FROM Patient
            """
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                nom = row['nom_Patient']
                prenom = row['prenom_Patient']
                date_naissance = row['date_naissance']
                age = self.calculate_age(date_naissance)
                telephone = row['telephone_Patient_1']
                genre = row['genre_Patient']
                row_data = [nom, prenom, age, telephone, genre]
                data.append(row_data)

            cursor.close()
        except Error as e:
            print(f"Erreur lors de la récupération des données des patients : {e}")

        return data

    def calculate_age(self, birth_date):

        today = date.today()
        try:
            birthday = birth_date.replace(year=today.year)
        except ValueError:

            birthday = birth_date.replace(year=today.year, month=birth_date.month + 1, day=1)
        if birthday > today:
            return today.year - birth_date.year - 1
        else:
            return today.year - birth_date.year

    def get_patient_table_background(self, row):

        return QColor(240, 240, 240) if row % 2 == 0 else None

    def add_patient(self, nom, prenom, age, telephone1, telephone2, email, address, genre):

        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return False

        try:
            cursor = self.connection.cursor()

            # Calculer date_naissance à partir de l'âge
            today = date.today()
            birth_year = today.year - age
            date_naissance = today.replace(year=birth_year)

            query = """
                INSERT INTO Patient (nom_Patient, prenom_Patient, genre_Patient, telephone_Patient_1, telephone_Patient_2, email_Patient, adresse_Patient, date_naissance)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nom, prenom, genre, telephone1, telephone2, email, address, date_naissance))
            patient_id = cursor.lastrowid  # Récupérer l'ID du patient inséré

            # Création du dossier médical pour le patient
            dossier_query = """
                INSERT INTO Dossier_Medical (groupe_Sanguin, statut_Rhesus, observation, date_Ouverture, id_Receptionniste, id_Patient)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Valeurs par défaut pour le dossier médical
            groupe_Sanguin = 'O'
            statut_Rhesus = 'Positif'
            observation = ''
            date_Ouverture = datetime.now()
            id_Receptionniste = self.receptionist_id
            cursor.execute(dossier_query, (groupe_Sanguin, statut_Rhesus, observation, date_Ouverture, id_Receptionniste, patient_id))

            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erreur lors de l'ajout du patient : {e}")
            return False

    def get_receptionist_name(self):

        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return "Utilisateur Inconnu"

        try:
            cursor = self.connection.cursor()
            query = "SELECT nom_Receptionniste, prenom_Receptionniste FROM Receptionniste WHERE id_Receptionniste = %s"
            cursor.execute(query, (self.receptionist_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                nom = result[0]
                prenom = result[1]
                return f"{prenom} {nom}"
            else:
                return "Utilisateur Inconnu"
        except Error as e:
            print(f"Erreur lors de la récupération du nom du réceptionniste : {e}")
            return "Utilisateur Inconnu"
