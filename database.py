from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class Patient(db.Model):
    __tablename__ = 'patients'
   
    id = db.Column(db.Integer, primary_key=True)
    code_patient = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_naissance = db.Column(db.String(20), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
   
    # Paramètres vitaux
    poids = db.Column(db.Float, nullable=False)
    taille = db.Column(db.Float, nullable=False)
    imc = db.Column(db.Float)
    tension = db.Column(db.String(20))
    frequence_cardiaque = db.Column(db.Integer)
   
    # Antécédents
    antecedents_medicaux = db.Column(db.Text)
    antecedents_chirurgicaux = db.Column(db.Text)
    allergies = db.Column(db.String(200))
    tabagisme = db.Column(db.String(20))
    alcool = db.Column(db.String(20))
   
    # Symptômes
    motif_consultation = db.Column(db.String(200))
    date_symptomes = db.Column(db.String(20))
    douleur = db.Column(db.Integer)
    traitements_cours = db.Column(db.Text)
   
    # Examens
    examen_clinique = db.Column(db.Text)
    resultats_biologiques = db.Column(db.Text)
   
    date_collecte = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<Patient {self.nom} {self.prenom}>'