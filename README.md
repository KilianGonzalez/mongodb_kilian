# Ejemplo MongoDB Atlas con Python

Este proyecto demuestra cómo conectarse a MongoDB Atlas utilizando Python y realizar operaciones CRUD básicas (Crear, Leer, Actualizar y Eliminar).

## Requisitos previos

- Python 3.6 o superior
- Una cuenta de MongoDB Atlas (puedes crear una gratis en [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas))

## Dependencias

Este proyecto utiliza las siguientes bibliotecas:
- `pymongo`: Cliente oficial de MongoDB para Python
- `dnspython`: Necesario para las conexiones URI de MongoDB Atlas

Puedes instalarlas con:

```bash
pip install pymongo dnspython
```

## Configuración

Antes de ejecutar el ejemplo, necesitas:

1. Crear un cluster en MongoDB Atlas
2. Obtener tu cadena de conexión (URI) desde la plataforma de MongoDB Atlas
3. Reemplazar la URI en el archivo `main.py` con tu propia cadena de conexión:

```python
uri = "mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"
```

Asegúrate de:
- Reemplazar `<username>` con tu nombre de usuario de MongoDB Atlas
- Reemplazar `<password>` con tu contraseña
- Reemplazar `<cluster-url>` con la URL de tu cluster
- Reemplazar `<dbname>` con el nombre de la base de datos

## Ejecutar el ejemplo

Para ejecutar el ejemplo:

```bash
python main.py
```

## Características del ejemplo

El código de ejemplo demuestra:

1. **Conexión**: Cómo conectarse a MongoDB Atlas
2. **Inserción**: Cómo insertar documentos en una colección
3. **Consulta**: Cómo buscar documentos con y sin filtros
4. **Actualización**: Cómo actualizar documentos existentes
5. **Eliminación**: Cómo eliminar documentos

## Recursos adicionales

- [Documentación de PyMongo](https://pymongo.readthedocs.io/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [MongoDB University](https://university.mongodb.com/) - Cursos gratuitos de MongoDB 