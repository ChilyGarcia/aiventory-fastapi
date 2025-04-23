from sqlalchemy import create_engine, MetaData
from databases import Database

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./aiventory.db"

# Crear instancia de la base de datos
database = Database(DATABASE_URL)

# Crear engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear metadata
metadata = MetaData()
