import pymongo
from pymongo import MongoClient
import datetime

def conectar_atlas():
    """
    Función para conectarse a MongoDB Atlas.
    Retorna una instancia del cliente de MongoDB.
    
    Nota: Reemplaza la URI con tu propia cadena de conexión de MongoDB Atlas.
    """
    # Cadena de conexión de MongoDB Atlas (reemplaza con tu propia URI)
    uri = "mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"
    
    # Crea una nueva instancia del cliente de MongoDB
    cliente = MongoClient(uri)
    
    try:
        # Verifica la conexión
        cliente.admin.command('ping')
        print("Conexión exitosa a MongoDB Atlas!")
    except Exception as e:
        print(f"Error al conectar a MongoDB Atlas: {e}")
        return None
        
    return cliente

def ejemplo_operaciones_crud():
    """
    Demostración de operaciones CRUD básicas con MongoDB.
    """
    # Conexión a MongoDB Atlas
    cliente = conectar_atlas()
    if not cliente:
        return
    
    # Selecciona la base de datos y colección
    db = cliente["ejemplo_db"]
    coleccion = db["usuarios"]
    
    # Limpia la colección para el ejemplo
    coleccion.delete_many({})
    
    print("\n--- OPERACIONES CRUD EN MONGODB ---")
    
    # CREATE - Insertar documentos
    print("\n1. Insertando documentos:")
    
    nuevos_usuarios = [
        {
            "nombre": "Ana García",
            "email": "ana@ejemplo.com",
            "edad": 28,
            "activo": True,
            "fecha_registro": datetime.datetime.now()
        },
        {
            "nombre": "Carlos Rodríguez",
            "email": "carlos@ejemplo.com",
            "edad": 34,
            "activo": True,
            "fecha_registro": datetime.datetime.now()
        }
    ]
    
    resultado = coleccion.insert_many(nuevos_usuarios)
    print(f"Documentos insertados con IDs: {resultado.inserted_ids}")
    
    # READ - Buscar documentos
    print("\n2. Buscando documentos:")
    
    # Buscar todos los documentos
    print("\nTodos los usuarios:")
    for usuario in coleccion.find():
        print(f"  - {usuario['nombre']} ({usuario['email']})")
    
    # Buscar con filtros
    print("\nUsuarios mayores de 30 años:")
    for usuario in coleccion.find({"edad": {"$gt": 30}}):
        print(f"  - {usuario['nombre']} (Edad: {usuario['edad']})")
    
    # UPDATE - Actualizar documentos
    print("\n3. Actualizando documentos:")
    
    filtro = {"nombre": "Ana García"}
    actualizacion = {"$set": {"edad": 29, "ultima_actualizacion": datetime.datetime.now()}}
    
    resultado = coleccion.update_one(filtro, actualizacion)
    print(f"Documentos modificados: {resultado.modified_count}")
    
    # Verificar la actualización
    usuario_actualizado = coleccion.find_one({"nombre": "Ana García"})
    print(f"Usuario actualizado: {usuario_actualizado['nombre']} (Edad: {usuario_actualizado['edad']})")
    
    # DELETE - Eliminar documentos
    print("\n4. Eliminando documentos:")
    
    filtro_eliminar = {"nombre": "Carlos Rodríguez"}
    resultado = coleccion.delete_one(filtro_eliminar)
    print(f"Documentos eliminados: {resultado.deleted_count}")
    
    # Verificar eliminación
    total_usuarios = coleccion.count_documents({})
    print(f"Total de usuarios restantes: {total_usuarios}")
    
    # Cerrar la conexión
    cliente.close()

if __name__ == "__main__":
    ejemplo_operaciones_crud()
