
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base  # Assurez-vous que Base est importé depuis votre fichier de modèles

DATABASE_URI = 'mysql+pymysql://root:RYK_mysql-24@localhost/gestion_Hopital_db'
engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()

def init_db():
    Base.metadata.create_all(bind=engine)