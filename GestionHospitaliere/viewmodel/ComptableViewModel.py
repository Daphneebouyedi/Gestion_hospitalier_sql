# viewmodel/ComptableViewModel.py

from PySide6.QtCore import QObject, Signal
from sqlalchemy.orm import Session
from viewmodel.database import SessionLocal
from models.models import Facturation, Patient, Comptable, Feuille
from datetime import datetime
import os

class ComptableViewModel(QObject):
    facture_retrieved = Signal(bool, list)
    facture_details_retrieved = Signal(dict)
    facture_updated = Signal(bool)

    def __init__(self, comptable_id):
        super().__init__()
        self.comptable_id = comptable_id

    def get_comptable_name(self):
        session: Session = SessionLocal()
        try:
            comptable = session.query(Comptable).filter_by(id_Comptable=self.comptable_id).first()
            if comptable:
                return f"{comptable.prenom_Comptable} {comptable.nom_Comptable}"
            else:
                return "Comptable Inconnu"
        except Exception as e:
            print(f"Erreur lors de la récupération du nom du comptable : {e}")
            return "Comptable Inconnu"
        finally:
            session.close()

    def get_factures(self, est_paye=False):
        session: Session = SessionLocal()
        try:
            factures = session.query(Facturation).join(Patient).filter(
                Facturation.est_Payee == est_paye
            ).all()
            facture_list = []
            for facture in factures:
                facture_list.append({
                    'id_Facturation': facture.id_Facturation,
                    'nom': facture.patient.nom_Patient,
                    'prenom': facture.patient.prenom_Patient,
                    'montant': float(facture.montant),
                    'date_emission': facture.date_emission.strftime("%d/%m/%Y"),
                    'date_Paiement': facture.date_Paiement.strftime("%d/%m/%Y") if facture.date_Paiement else "",
                    'acteur': facture.acteur or "",
                    'telephone_Acteur': facture.telephone_Acteur or "",
                    'description': facture.feuille.Pathologie if facture.feuille and facture.feuille.Pathologie else ""
                })
            self.facture_retrieved.emit(est_paye, facture_list)
        except Exception as e:
            print(f"Erreur lors de la récupération des factures : {e}")
            self.facture_retrieved.emit(est_paye, [])
        finally:
            session.close()

    def get_facture_details(self, facture_id):
        session: Session = SessionLocal()
        try:
            facture = session.query(Facturation).filter_by(id_Facturation=facture_id).first()
            if facture:
                details = {
                    'id_Facturation': facture.id_Facturation,
                    'nom': facture.patient.nom_Patient,
                    'prenom': facture.patient.prenom_Patient,
                    'montant': float(facture.montant),
                    'date_emission': facture.date_emission.strftime("%d/%m/%Y"),
                    'date_Paiement': facture.date_Paiement.strftime("%d/%m/%Y") if facture.date_Paiement else "",
                    'acteur': facture.acteur or "",
                    'telephone_Acteur': facture.telephone_Acteur or "",
                    'description': facture.feuille.Pathologie if facture.feuille and facture.feuille.Pathologie else "",
                    'est_Payee': facture.est_Payee
                }
                self.facture_details_retrieved.emit(details)
            else:
                self.facture_details_retrieved.emit({})
        except Exception as e:
            print(f"Erreur lors de la récupération des détails de la facture : {e}")
            self.facture_details_retrieved.emit({})
        finally:
            session.close()

    def update_facture_status(self, facture_id, est_paye):
        session: Session = SessionLocal()
        try:
            facture = session.query(Facturation).filter_by(id_Facturation=facture_id).first()
            if facture:
                facture.est_Payee = est_paye
                facture.date_Paiement = datetime.utcnow() if est_paye else None
                facture.id_Comptable = self.comptable_id
                session.commit()
                self.facture_updated.emit(True)
            else:
                self.facture_updated.emit(False)
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut de la facture : {e}")
            session.rollback()
            self.facture_updated.emit(False)
        finally:
            session.close()

    def get_facture_pdf(self, facture_id):
        pdf_directory = "factures_pdfs"
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory)
        pdf_path = os.path.join(pdf_directory, f"facture_{facture_id}.pdf")
        return pdf_path

    def disconnect_database(self):
        pass
