import sqlite3
import json
import os
from datetime import datetime
from langchain_core.tools import tool

# ==========================================
# Tool 1.
# ==========================================
@tool
def consultar_inventario(db_path: str, categoria: str) -> str:
    """
    Consulta la base de datos SQL local de la empresa para buscar productos.
    Útil para saber qué artículos están disponibles, su stock y precios.
    Args:
        db_path (str): La ruta a la base de datos SQLite.
        categoria (str): La categoría del producto (ej. 'Electrónica', 'Oficina').
    """
    
    # valida que la base de datos exista
    if not os.path.exists(db_path):
        return "Error: La base de datos no existe. Por favor, ejecuta el script de configuración primero."
    
    try:
        # realiza la consulta
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre, Marca, Precio, Stock FROM productos WHERE categoria = ?", (categoria,))
        resultados = cursor.fetchall()
        conn.close()
        
        # en caso de que no hay resultados
        if not resultados:
            return f"No se encontraron productos en la categoría: {categoria}."
        
        # devuelve la información formateada
        respuesta = f"Productos en {categoria}:\n"
        for nombre, marca, precio, stock in resultados:
            respuesta += f"- {nombre} ({marca}): ${precio} (Stock: {stock})\n"
        return respuesta
    
    except sqlite3.Error as e:
        return f"Error al consultar la base de datos: {str(e)}"

# ==========================================
# Tool 2.
# ==========================================
@tool
def buscar_cliente(db_path: str, nombre: str) -> str:
    """
    Busca la información de contacto de un cliente en el sistema CRM/SFA de la empresa.
    Útil para obtener el correo electrónico, teléfono o la empresa de un cliente.
    
    IMPORTANTE PARA EL LLM: Si esta herramienta devuelve un mensaje de AMBIGÜEDAD indicando 
    que hay múltiples coincidencias, DEBES detener tu ejecución y preguntarle directamente 
    al usuario a cuál de los clientes se refiere antes de continuar o usar otra herramienta.
    
    Args:
        db_path (str): La ruta a la base de datos SQLite.
        nombre (str): El nombre o apellido del cliente a buscar (ej. 'Ana', 'Carlos').
    """
    
    if not os.path.exists(db_path):
        return "Error: La base de datos de clientes no está disponible."
        
    try:
        # se reliza la consulta con un LIKE
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre, Empresa, Email, Telefono FROM clientes WHERE nombre LIKE ?", (f"%{nombre}%",))
        resultados = cursor.fetchall()
        conn.close()
        
        # Si no hay resultados
        if len(resultados) == 0:
            return f"No se encontró ningún cliente que coincida con el nombre: '{nombre}'."
            
        # Si hay solo un resultado
        elif len(resultados) == 1:
            cliente = resultados[0]
            return f"Datos del cliente - Nombre: {cliente[0]} | Empresa: {cliente[1]} | Email: {cliente[2]} | Tel: {cliente[3]}"
            
        # Si hay múltiples resultados (Human-In-The-Loop)
        else:
            nombres_encontrados = [fila[0] for fila in resultados]
            nombres_str = ", ".join(nombres_encontrados)
            return f"AMBIGÜEDAD: Se encontraron múltiples clientes que coinciden con '{nombre}': {nombres_str}. Pídele al usuario que especifique el apellido."
            
    except sqlite3.Error as e:
        return f"Error en la base de datos al buscar el cliente: {str(e)}"

# ==========================================
# Tool 3.
# ==========================================

@tool
def consultar_tabla_bd(db_path: str, tabla: str) -> str:
    """
    Consulta los registros generales de una tabla en la base de datos local.
    Útil cuando el usuario pide ver "todos los clientes", "todos los usuarios" o "todos los productos".
    
    Args:
        db_path (str): La ruta a la base de datos SQLite.
        tabla (str): El nombre de la tabla a consultar. DEBE ser exactamente 'clientes' o 'productos'.
    """
    
    # Hay que tener mucho cuidado con las alucinaciones
    tablas_permitidas = ["clientes", "productos"]
    tabla_limpia = tabla.lower().strip()
    
    # en caso de que el LLM use "usuarios" en vez de "clientes"
    if tabla_limpia == "usuarios":
        tabla_limpia = "clientes"
        
    if tabla_limpia not in tablas_permitidas:
        return f"Error: La tabla '{tabla}' no existe en esta base de datos. Solo puedes consultar 'clientes' o 'productos'."
        
    try:
        # Hacemos la consulta
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Nunca devolver todos los registros sin un límite, para evitar saturar al LLM
        query = f"SELECT * FROM {tabla_limpia} LIMIT 50"
        cursor.execute(query)
        
        # Extraemos los nombres de las columnas automáticamente para darle contexto al LLM
        columnas = [descripcion[0] for descripcion in cursor.description]
        resultados = cursor.fetchall()
        conn.close()
        
        # Si la tabla está vacía
        if not resultados:
            return f"La tabla '{tabla_limpia}' está vacía."
            
        # Devolvemos los resultados formateados, mostrando el nombre de cada columna para que el LLM entienda mejor la información
        respuesta = f"--- Mostrando registros de la tabla '{tabla_limpia}' (Límite 50) ---\n"
        for fila in resultados:
            fila_str = ", ".join([f"{col}: {val}" for col, val in zip(columnas, fila)])
            respuesta += f"- {fila_str}\n"
            
        return respuesta
        
    except sqlite3.Error as e:
        return f"Error crítico de SQL: {str(e)}"
    

# ==========================================
# Tool 4.
# ==========================================

@tool
def obtener_contacto_cliente(db_path: str, nombre: str) -> str:
    """
    Consulta los datos de contacto de un cliente específico en la base de datos.
    Útil para obtener rápidamente el contacto telefónico de un cliente.
    
    Args:
        db_path (str): La ruta a la base de datos SQLite.
        nombre (str): El nombre completo del cliente (ej. 'Ana Pérez').
    """
    
    if not os.path.exists(db_path):
        return "Error: La base de datos de clientes no está disponible."
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Telefono, Email FROM clientes WHERE Nombre Like ?", (f"%{nombre}%",))
        resultado = cursor.fetchone()
        conn.close()
        
        if len(resultado) == 0:
            return f"No se encontró ningún cliente con el nombre: '{nombre}'."
        elif len(resultado) == 1:
            return f"El número de teléfono de {nombre} es: {resultado[0]} y su email es: {resultado[1]}"
        else:
            return f"AMBIGUEDAD: Se encontraron múltiples clientes con el nombre '{nombre}'. Pide al usuario que especifique el apellido para obtener el contacto correcto."

    except sqlite3.Error as e:
        return f"Error en la base de datos al obtener el teléfono del cliente: {str(e)}"
    

# ==========================================
# Tool 5.
# ==========================================

@tool
def buscar_articulo(db_path: str, termino: str) -> str:
    """
    Busca un artículo específico en la base de datos de inventario.
    Útil para encontrar rápidamente el stock y precio de un producto específico.
    
    Args:
        db_path (str): La ruta a la base de datos SQLite.
        termino (str): El nombre o parte del nombre del artículo a buscar (ej. 'Laptop', 'Silla').
    """
    
    if not os.path.exists(db_path):
        return "Error: La base de datos no existe. Por favor, ejecuta el script de configuración primero."
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre, Marca, Precio, Stock FROM productos WHERE Nombre LIKE ?", (f"%{termino}%",))
        resultados = cursor.fetchall()
        conn.close()
        
        if not resultados:
            return f"No se encontraron artículos que coincidan con: '{termino}'."
        
        respuesta = f"Resultados para '{termino}':\n"
        for nombre, marca, precio, stock in resultados:
            respuesta += f"- {nombre} ({marca}): ${precio} (Stock: {stock})\n"
        return respuesta
    
    except sqlite3.Error as e:
        return f"Error al consultar la base de datos: {str(e)}"