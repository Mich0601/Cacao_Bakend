from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conexión a MongoDB
MONGODB_URI="mongodb+srv://Michelle:Mich0601@cluster0.iq4zu.mongodb.net/commentsDB?retryWrites=true&w=majority"
try:
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client.get_database()
    print("Conexión exitosa a MongoDB")
    print("Bases de datos disponibles:", client.list_database_names())
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
