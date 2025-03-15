from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()  # Antes de usar os.getenv()

# Configuración recomendada: Usar variables de entorno para las credenciales
# Le pasamos la variable de entorno a la cadena de conexión desde el archivo .env
CONNECTION_STRING = os.getenv("MONGODB_URI")

# Cliente como variable global (se inicializa una sola vez)
_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        try:
            _client = MongoClient(CONNECTION_STRING)
            print("Conexión a MongoDB establecida")
            return _client
        except Exception as e:
            print(f"Error conectando: {e}")
            raise
    return _client

def get_db(db_name="bbddKilian"):
    global _db
    if _db is None:
        client = get_client()
        _db = client[db_name]
    return _db

# Testeo básico si ejecutas este archivo directamente
if __name__ == "__main__":
    # Test de conexión
    db = get_db()
    print("Colecciones en la base de datos:", db.list_collection_names())