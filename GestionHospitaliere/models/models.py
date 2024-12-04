from sqlalchemy import (
    create_engine, Column, Integer, String, Date, DateTime, DECIMAL,
    Boolean, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id_User = Column(Integer, primary_key=True, autoincrement=True)
    user_Name = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)  # Stockage des hashs sécurisés
    role = Column(String(50), nullable=False)

    medecin = relationship('Medecin', uselist=False, back_populates='user')
    comptable = relationship('Comptable', uselist=False, back_populates='user')
    receptionniste = relationship('Receptionniste', uselist=False, back_populates='user')


class Medecin(Base):
    __tablename__ = 'Medecin'

    id_Medecin = Column(Integer, primary_key=True, autoincrement=True)
    nom_Medecin = Column(String(50), nullable=False)
    prenom_Medecin = Column(String(50), nullable=False)
    specialite = Column(String(50), nullable=False)
    email_Medecin = Column(String(50), nullable=False, unique=True)
    telephone_Medecin_1 = Column(String(15), nullable=False, unique=True)
    telephone_Medecin_2 = Column(String(15), nullable=True)
    adresse_Medecin = Column(String(50), nullable=True)
    genre_Medecin = Column(String(10), nullable=True)
    id_User = Column(Integer, ForeignKey('Users.id_User'), unique=True, nullable=False)

    __table_args__ = (
        CheckConstraint("genre_Medecin IN ('Homme', 'Femme')", name='check_genre_Medecin'),
    )

    user = relationship('User', back_populates='medecin')
    traitements = relationship('Traitement', back_populates='medecin')


class Comptable(Base):
    __tablename__ = 'Comptable'

    id_Comptable = Column(Integer, primary_key=True, autoincrement=True)
    nom_Comptable = Column(String(50), nullable=False)
    prenom_Comptable = Column(String(50), nullable=False)
    telephone_Comptable_1 = Column(String(15), nullable=False, unique=True)
    telephone_Comptable_2 = Column(String(15), nullable=True)
    mail_Comptable = Column(String(50), unique=True, nullable=True)
    id_User = Column(Integer, ForeignKey('Users.id_User'), unique=True, nullable=False)

    user = relationship('User', back_populates='comptable')
    facturations = relationship('Facturation', back_populates='comptable')


class Salle(Base):
    __tablename__ = 'Salle'

    id_Salle = Column(Integer, primary_key=True, autoincrement=True)
    nom_Salle = Column(String(50), nullable=False, unique=True)
    type_Salle = Column(String(50), nullable=False)

    traitements = relationship('Traitement', back_populates='salle')


class Receptionniste(Base):
    __tablename__ = 'Receptionniste'

    id_Receptionniste = Column(Integer, primary_key=True, autoincrement=True)
    nom_Receptionniste = Column(String(50), nullable=False)
    prenom_Receptionniste = Column(String(50), nullable=False)
    email_Receptionniste = Column(String(50), nullable=False, unique=True)
    telephone_Receptionniste_1 = Column(String(15), nullable=False, unique=True)
    telephone_Receptionniste_2 = Column(String(15), nullable=True)
    id_User = Column(Integer, ForeignKey('Users.id_User'), unique=True, nullable=False)

    user = relationship('User', back_populates='receptionniste')
    dossiers_medicaux = relationship('DossierMedical', back_populates='receptionniste')


class Chambre(Base):
    __tablename__ = 'Chambre'

    id_Chambre = Column(Integer, primary_key=True, autoincrement=True)
    capacite = Column(Integer, nullable=False)
    numero_Lit = Column(Integer, unique=True, nullable=True)

    __table_args__ = (
        CheckConstraint('capacite > 0', name='check_capacite_positive'),
    )

    patients = relationship('Patient', back_populates='chambre')


class Patient(Base):
    __tablename__ = 'Patient'

    id_Patient = Column(Integer, primary_key=True, autoincrement=True)
    nom_Patient = Column(String(50), nullable=False)
    prenom_Patient = Column(String(50), nullable=False)
    genre_Patient = Column(String(10), nullable=True)
    date_naissance = Column(Date, nullable=False)
    telephone_Patient_1 = Column(String(15), nullable=False)
    telephone_Patient_2 = Column(String(15), nullable=True)
    email_Patient = Column(String(50), nullable=True)
    adresse_Patient = Column(String(50), nullable=True)
    id_Chambre = Column(Integer, ForeignKey('Chambre.id_Chambre'), nullable=True)

    chambre = relationship('Chambre', back_populates='patients')
    dossier_medical = relationship('DossierMedical', back_populates='patient', uselist=False)
    facturations = relationship('Facturation', back_populates='patient')


class DossierMedical(Base):
    __tablename__ = 'Dossier_Medical'

    id_dossier = Column(Integer, primary_key=True, autoincrement=True)
    groupe_Sanguin = Column(String(5), nullable=False)
    statut_Rhesus = Column(String(10), nullable=False)
    observation = Column(String(500), nullable=True)
    date_Ouverture = Column(DateTime, default=datetime.utcnow)
    id_Receptionniste = Column(Integer, ForeignKey('Receptionniste.id_Receptionniste'), nullable=False)
    id_Patient = Column(Integer, ForeignKey('Patient.id_Patient'), unique=True, nullable=False)

    receptionniste = relationship('Receptionniste', back_populates='dossiers_medicaux')
    patient = relationship('Patient', back_populates='dossier_medical')
    feuilles = relationship('Feuille', back_populates='dossier_medical')


class Feuille(Base):
    __tablename__ = 'Feuille'

    id_Feuille = Column(Integer, primary_key=True, autoincrement=True)
    date_Debut = Column(DateTime, default=datetime.utcnow)
    date_Fin = Column(DateTime, nullable=True)
    poids = Column(DECIMAL(5, 2), nullable=True)
    Taille = Column(String(50), nullable=True)
    Pathologie = Column(String(300), nullable=True)
    id_dossier = Column(Integer, ForeignKey('Dossier_Medical.id_dossier'), nullable=False)

    __table_args__ = (
        CheckConstraint('date_Fin >= date_Debut', name='check_date_Fin'),
    )

    dossier_medical = relationship('DossierMedical', back_populates='feuilles')
    traitements = relationship('Traitement', back_populates='feuille')
    facturations = relationship('Facturation', back_populates='feuille')


class Traitement(Base):
    __tablename__ = 'Traitement'

    id_Traitement = Column(Integer, primary_key=True, autoincrement=True)
    remarque_Traitement = Column(String(300), nullable=True)
    conclusion = Column(String(100), nullable=True)
    date_heure = Column(DateTime, default=datetime.utcnow)
    id_Salle = Column(Integer, ForeignKey('Salle.id_Salle'), nullable=False)
    id_Medecin = Column(Integer, ForeignKey('Medecin.id_Medecin'), nullable=False)
    id_Feuille = Column(Integer, ForeignKey('Feuille.id_Feuille'), nullable=False)

    salle = relationship('Salle', back_populates='traitements')
    medecin = relationship('Medecin', back_populates='traitements')
    feuille = relationship('Feuille', back_populates='traitements')


class Facturation(Base):
    __tablename__ = 'Facturation'

    id_Facturation = Column(Integer, primary_key=True, autoincrement=True)
    date_emission = Column(DateTime, default=datetime.utcnow)
    est_Payee = Column(Boolean, default=False)
    date_Paiement = Column(DateTime, nullable=True)
    montant = Column(DECIMAL(10, 2), nullable=False)
    acteur = Column(String(50), nullable=True)
    telephone_Acteur = Column(String(15), nullable=True)
    id_Patient = Column(Integer, ForeignKey('Patient.id_Patient'), nullable=False)
    id_Comptable = Column(Integer, ForeignKey('Comptable.id_Comptable'), nullable=True)
    id_Feuille = Column(Integer, ForeignKey('Feuille.id_Feuille'), nullable=False)

    patient = relationship('Patient', back_populates='facturations')
    comptable = relationship('Comptable', back_populates='facturations')
    feuille = relationship('Feuille', back_populates='facturations')
