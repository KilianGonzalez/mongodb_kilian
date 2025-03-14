"""
Script para probar la conexión a MongoDB Atlas y realizar operaciones CRUD básicas
"""
import datetime
from connection import get_db

def probar_mongodb_atlas():
    """
    Realiza una prueba completa de conexión a MongoDB Atlas con operaciones CRUD
    """
    print("Iniciando prueba de conexión a MongoDB Atlas...")
    
    # Obtener conexión a la base de datos
    db = get_db()  # Usamos la función de connection.py
    
    # Nombre de la colección de prueba
    coleccion_nombre = "test_crud_collection"
    coleccion = db[coleccion_nombre]
    
    # Limpiar cualquier dato previo en la colección de prueba
    coleccion.delete_many({})
    print(f"\nColección '{coleccion_nombre}' creada/limpiada para la prueba")
    
    # 1. CREATE - Insertar datos
    print("\n1. Insertando documentos...")
    documentos_prueba = [
        {
            "nombre": "Prueba 1", 
            "valor": 42, 
            "fecha": datetime.datetime.now()
        },
        {
            "nombre": "Prueba 2", 
            "valor": 73, 
            "activo": True, 
            "fecha": datetime.datetime.now()
        }
    ]
    
    resultado = coleccion.insert_many(documentos_prueba)
    ids_insertados = resultado.inserted_ids
    print(f"  ✓ Documentos insertados exitosamente con IDs: {ids_insertados}")
    
    # 2. READ - Leer datos
    print("\n2. Leyendo documentos...")
    documentos = list(coleccion.find())
    print(f"  ✓ Total de documentos en la colección: {len(documentos)}")
    for doc in documentos:
        print(f"    - Documento: {doc['nombre']}, Valor: {doc['valor']}")
    
    # 3. UPDATE - Actualizar datos
    print("\n3. Actualizando documentos...")
    filtro = {"nombre": "Prueba 1"}
    actualizacion = {"$set": {"valor": 100, "actualizado": True}}
    resultado = coleccion.update_one(filtro, actualizacion)
    print(f"  ✓ Documentos modificados: {resultado.modified_count}")
    
    # Verificar la actualización
    doc_actualizado = coleccion.find_one(filtro)
    print(f"  ✓ Documento actualizado: {doc_actualizado['nombre']}, Nuevo valor: {doc_actualizado['valor']}")
    
    # 4. DELETE - Eliminar datos
    print("\n4. Eliminando documentos...")
    filtro_eliminar = {"nombre": "Prueba 2"}
    resultado = coleccion.delete_one(filtro_eliminar)
    print(f"  ✓ Documentos eliminados: {resultado.deleted_count}")
    
    # Verificar eliminación
    documentos_restantes = list(coleccion.find())
    print(f"  ✓ Documentos restantes: {len(documentos_restantes)}")
    
    print("\nPrueba completada con éxito. La conexión a MongoDB Atlas funciona correctamente.")

if __name__ == "__main__":
    probar_mongodb_atlas() 