import mysql.connector
from mysql.connector import Error
from PySide6.QtGui import QColor
from datetime import datetime, date


class MedecinViewModel:
    def __init__(self, medecin_id):
        self.medecin_id = medecin_id
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'RYK_mysql-24',
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

    def get_medecin_name(self):
        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return "Utilisateur Inconnu"

        try:
            cursor = self.connection.cursor()
            query = "SELECT nom_Medecin, prenom_Medecin FROM Medecin WHERE id_Medecin = %s"
            cursor.execute(query, (self.medecin_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                nom = result[0]
                prenom = result[1]
                return f"{prenom} {nom}"
            else:
                return "Utilisateur Inconnu"
        except Error as e:
            print(f"Erreur lors de la récupération du nom du médecin : {e}")
            return "Utilisateur Inconnu"

    def get_all_dossiers(self):
        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return []

        data = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    Dossier_Medical.id_dossier,
                    Patient.nom_Patient, 
                    Patient.prenom_Patient,
                    Dossier_Medical.groupe_Sanguin,
                    Dossier_Medical.statut_Rhesus,
                    Dossier_Medical.observation,
                    Dossier_Medical.date_Ouverture
                FROM Dossier_Medical
                JOIN Patient ON Dossier_Medical.id_Patient = Patient.id_Patient
            """
            cursor.execute(query)
            results = cursor.fetchall()

            for row in results:
                id_dossier = row['id_dossier']
                nom_patient = row['nom_Patient']
                prenom_patient = row['prenom_Patient']
                groupe_sanguin = row['groupe_Sanguin']
                statut_rhesus = row['statut_Rhesus']
                observation = row['observation']
                date_ouverture = row['date_Ouverture']
                row_data = [id_dossier, nom_patient, prenom_patient, groupe_sanguin, statut_rhesus, observation, date_ouverture]
                data.append(row_data)

            cursor.close()
        except Error as e:
            print(f"Erreur lors de la récupération des dossiers : {e}")

        return data

    def get_dossier_table_background(self, row):
        return QColor(240, 240, 240) if row % 2 == 0 else None

    def get_dossier_info(self, dossier_id):
        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    Dossier_Medical.id_dossier,
                    Dossier_Medical.groupe_Sanguin,
                    Dossier_Medical.statut_Rhesus,
                    Dossier_Medical.observation,
                    Dossier_Medical.date_Ouverture,
                    Patient.nom_Patient,
                    Patient.prenom_Patient,
                    Patient.date_naissance,
                    Receptionniste.nom_Receptionniste,
                    Receptionniste.prenom_Receptionniste
                FROM Dossier_Medical
                JOIN Patient ON Dossier_Medical.id_Patient = Patient.id_Patient
                JOIN Receptionniste ON Dossier_Medical.id_Receptionniste = Receptionniste.id_Receptionniste
                WHERE Dossier_Medical.id_dossier = %s
            """
            cursor.execute(query, (dossier_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Erreur lors de la récupération des informations du dossier : {e}")
            return None

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

    def get_feuilles_by_dossier_id(self, dossier_id):
        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return []

        data = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    id_Feuille,
                    date_Debut,
                    date_Fin,
                    poids,
                    Taille,
                    Pathologie
                FROM Feuille
                WHERE id_dossier = %s
            """
            cursor.execute(query, (dossier_id,))
            results = cursor.fetchall()

            for row in results:
                id_feuille = row['id_Feuille']
                date_debut = row['date_Debut']
                date_fin = row['date_Fin']
                poids = row['poids']
                taille = row['Taille']
                pathologie = row['Pathologie']
                row_data = [id_feuille, date_debut, date_fin, poids, taille, pathologie]
                data.append(row_data)

            cursor.close()
        except Error as e:
            print(f"Erreur lors de la récupération des feuilles : {e}")

        return data

    def get_feuilles_table_background(self, row):
        return QColor(240, 240, 240) if row % 2 == 0 else None

    def get_feuille_details(self, feuille_id):
        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    id_Feuille,
                    date_Debut,
                    date_Fin,
                    poids,
                    Taille,
                    Pathologie
                FROM Feuille
                WHERE id_Feuille = %s
            """
            cursor.execute(query, (feuille_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Erreur lors de la récupération des détails de la feuille : {e}")
            return None

    def update_feuille(self, feuille_id, feuille_data):
        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return False

        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Feuille
                SET poids = %s, Taille = %s, Pathologie = %s, date_Debut = %s, date_Fin = %s
                WHERE id_Feuille = %s
            """
            cursor.execute(query, (
                feuille_data['poids'],
                feuille_data['Taille'],
                feuille_data['Pathologie'],
                feuille_data['date_Debut'],
                feuille_data['date_Fin'],
                feuille_id
            ))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erreur lors de la mise à jour de la feuille : {e}")
            return False

    def add_feuille(self, poids, taille, pathologie, dossier_id):
        if self.connection is None:
            print("Aucune connexion à la base de données.")
            return False

        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Feuille (date_Debut, poids, Taille, Pathologie, id_dossier)
                VALUES (%s, %s, %s, %s, %s)
            """
            date_debut = datetime.now()
            cursor.execute(query, (date_debut, poids, taille, pathologie, dossier_id))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erreur lors de l'ajout de la feuille : {e}")
            return False
