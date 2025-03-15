from connection import get_db

def identificar_tipo(documento):
    """
    Intenta identificar si un documento es una serie o una película
    basándose en el contenido del resumen
    """
    summary = documento.get("summary", "").lower()
    
    # Identificar por palabras clave en el resumen
    if "sèrie" in summary or "serie" in summary:
        return "Serie"
    elif "pel·lícula" in summary or "pelicula" in summary:
        return "Película"
    
    # Lista de títulos conocidos de series
    series_conocidas = [
        "game of thrones", "the last of us", "one piece", 
        "dragon ball", "merlí", "small axe"
    ]
    
    # Verificar si el título está en nuestra lista de series conocidas
    if documento.get("title", "").lower() in series_conocidas:
        return "Serie"
    
    # Por defecto, asumimos que es una película
    return "Película"

def main():
    # Obtener conexión a la base de datos (reutilizando la conexión de connection.py)
    db = get_db()
    print("\n=== Conexión a MongoDB Atlas establecida ===\n")
    
    # Referencia a la colección (si no existe, se creará cuando insertemos documentos)
    coleccion = db["M06"]
    
    # Mostrar todos los títulos y directores
    print("=== 1.LISTADO DE TODOS LOS TÍTULOS Y DIRECTORES ===")
    peliculas = list(coleccion.find({}, {"title": 1, "director": 1, "_id": 0}))
    
    if len(peliculas) > 0:
        for pelicula in peliculas:
            titulo = pelicula.get("title", "Sin título")
            director = pelicula.get("director", "Director desconocido")
            print(f"Título: {titulo} | Director: {director}")
        print(f"\nTotal de películas encontradas: {len(peliculas)}")
    else:
        print("No se encontraron películas en la colección.")
    
    # 2. Mostrar título y año ordenado por años
    print("\n=== 2. TÍTULOS Y AÑOS ORDENADOS POR AÑO ===")
    ordenadas_por_anio = list(coleccion.find({}, {"title": 1, "year": 1, "_id": 0}).sort("year", 1))
    
    if len(ordenadas_por_anio) > 0:
        for item in ordenadas_por_anio:
            titulo = item.get("title", "Sin título")
            anio = item.get("year", "Año desconocido")
            print(f"Año: {anio} | Título: {titulo}")
        print(f"\nTotal de películas mostradas: {len(ordenadas_por_anio)}")
    else:
        print("No se encontraron películas con información de año.")
    
    # 3. Buscar series con la palabra "professor" en el resumen
    print("\n=== 3. SERIES CON LA PALABRA 'PROFESSOR' EN EL RESUMEN ===")
    query_professor = {"summary": {"$regex": "professor", "$options": "i"}}  # Cambiado a summary en lugar de plot
    series_professor = list(coleccion.find(query_professor, {"title": 1, "summary": 1, "_id": 0}))
    
    if len(series_professor) > 0:
        for serie in series_professor:
            titulo = serie.get("title", "Sin título")
            resumen = serie.get("summary", "Sin resumen")
            print(f"Título: {titulo}")
            print(f"Resumen: {resumen}")
            print("-" * 50)
        print(f"\nTotal de coincidencias encontradas: {len(series_professor)}")
    else:
        print("No se encontraron series con 'professor' en el resumen.")
    
    # 4. Mostrar título, año y reparto de películas/series posteriores a 2018
    print("\n=== 4. TÍTULOS, AÑOS Y REPARTO DE PELÍCULAS/SERIES POSTERIORES A 2018 ===")
    query_recientes = {"year": {"$gt": 2018}}
    peliculas_recientes = list(coleccion.find(query_recientes, {"title": 1, "year": 1, "cast": 1, "summary": 1, "_id": 0}))
    
    if len(peliculas_recientes) > 0:
        for pelicula in peliculas_recientes:
            titulo = pelicula.get("title", "Sin título")
            anio = pelicula.get("year", "Año desconocido")
            reparto = pelicula.get("cast", [])
            tipo = identificar_tipo(pelicula)
            
            print(f"Título: {titulo} | Año: {anio} | Tipo: {tipo}")
            if reparto:
                print("Reparto:")
                for actor in reparto:
                    print(f"  - {actor}")
            else:
                print("Reparto: No disponible")
            print("-" * 50)
        print(f"\nTotal de películas posteriores a 2018: {len(peliculas_recientes)}")
    else:
        print("No se encontraron películas posteriores a 2018.")
    
    # 5. Clasificar todos los contenidos entre películas y series
    print("\n=== 5. CLASIFICACIÓN DE CONTENIDOS POR TIPO ===")
    todos_contenidos = list(coleccion.find({}, {"title": 1, "year": 1, "summary": 1, "_id": 0}))
    
    peliculas = []
    series = []
    
    for contenido in todos_contenidos:
        tipo = identificar_tipo(contenido)
        if tipo == "Película":
            peliculas.append(contenido)
        else:
            series.append(contenido)
    
    print(f"PELÍCULAS ({len(peliculas)}):")
    for pelicula in peliculas:
        print(f"  - {pelicula.get('title')} ({pelicula.get('year')})")
    
    print(f"\nSERIES ({len(series)}):")
    for serie in series:
        print(f"  - {serie.get('title')} ({serie.get('year')})")
    
    # 6. Añadir una nueva película/serie a la colección
    print("\n=== 6. AÑADIENDO UNA NUEVA PELÍCULA A LA COLECCIÓN ===")
    nueva_pelicula = {
        "title": "Dune: Parte Dos",
        "year": 2024,
        "director": "Denis Villeneuve",
        "cast": ["Timothée Chalamet", "Zendaya", "Javier Bardem"],
        "summary": "Paul Atreides se une a los Fremen y comienza su viaje para convertirse en Muad'Dib mientras busca venganza contra los conspiradores que destruyeron a su familia.",
    }
    
    # Comprobar si la película ya existe para evitar duplicados
    pelicula_existente = coleccion.find_one({"title": nueva_pelicula["title"], "year": nueva_pelicula["year"]})
    
    if pelicula_existente:
        print(f"La película '{nueva_pelicula['title']}' ya existe en la colección.")
    else:
        resultado = coleccion.insert_one(nueva_pelicula)
        print(f"Película '{nueva_pelicula['title']}' añadida correctamente.")
        print(f"ID del documento: {resultado.inserted_id}")

if __name__ == "__main__":
    main()
