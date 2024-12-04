# viewmodel/LoginViewModel.py

from PySide6.QtCore import QObject, Signal
from sqlalchemy.orm import Session
from viewmodel.database import SessionLocal
from models.models import User, Medecin, Comptable, Receptionniste

class LoginViewModel(QObject):
    login_successful = Signal(str, int)  # Émet le rôle et l'ID spécifique
    login_failed = Signal(str)  # Émet un message d'erreur

    def __init__(self):
        super().__init__()
        self.username = ""
        self.password = ""

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):

        session: Session = SessionLocal()
        try:
            user = session.query(User).filter_by(user_Name=self.username, password=self.password).first()
            if user:
                role = user.role
                user_id = user.id_User
                specific_id = self.get_specific_id(session, role, user_id)
                if specific_id is not None:
                    self.login_successful.emit(role, specific_id)
                else:
                    self.login_failed.emit("ID spécifique au rôle introuvable.")
            else:
                self.login_failed.emit("Nom d'utilisateur ou mot de passe incorrect.")
        except Exception as e:
            self.login_failed.emit(f"Erreur lors de l'authentification : {e}")
        finally:
            session.close()

    def get_specific_id(self, session: Session, role: str, user_id: int):

        if role == "Medecin":
            medecin = session.query(Medecin).filter_by(id_User=user_id).first()
            return medecin.id_Medecin if medecin else None
        elif role == "Comptable":
            comptable = session.query(Comptable).filter_by(id_User=user_id).first()
            return comptable.id_Comptable if comptable else None
        elif role == "Receptionniste":
            receptionniste = session.query(Receptionniste).filter_by(id_User=user_id).first()
            return receptionniste.id_Receptionniste if receptionniste else None
        else:
            return None
