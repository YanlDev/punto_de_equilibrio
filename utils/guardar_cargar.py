"""
Módulo para guardar y cargar escenarios de análisis de punto de equilibrio.

Este módulo proporciona funciones para guardar el estado actual del análisis
y cargar escenarios previamente guardados.
"""

import os
import json
import datetime
import pickle
from tkinter import filedialog, messagebox

def guardar_escenario(modelo, nombre=None, directorio=None):
    """
    Guarda el escenario actual en un archivo.
    
    Args:
        modelo (dict): Diccionario con los datos del modelo
        nombre (str, optional): Nombre para el escenario. Si es None, se usa la fecha/hora.
        directorio (str, optional): Directorio donde guardar. Si es None, se solicita al usuario.
        
    Returns:
        str: Ruta del archivo guardado, o None si no se guardó
    """
    # Si no se proporciona nombre, usar fecha/hora
    if nombre is None:
        nombre = f"escenario_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Asegurar que el nombre tenga la extensión .peq (Punto de Equilibrio)
    if not nombre.lower().endswith('.peq'):
        nombre += '.peq'
    
    # Si no se proporciona directorio, solicitar al usuario
    if directorio is None:
        ruta_completa = filedialog.asksaveasfilename(
            defaultextension=".peq",
            filetypes=[("Archivos de Punto de Equilibrio", "*.peq"), ("Todos los archivos", "*.*")],
            initialfile=nombre
        )
        if not ruta_completa:  # Si el usuario cancela
            return None
    else:
        # Asegurar que el directorio existe
        if not os.path.exists(directorio):
            try:
                os.makedirs(directorio)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el directorio: {str(e)}")
                return None
        
        ruta_completa = os.path.join(directorio, nombre)
    
    try:
        # Preparar datos para guardar
        # No guardar el DataFrame directamente (puede ser grande)
        datos_a_guardar = {
            "metadatos": {
                "fecha_creacion": datetime.datetime.now().isoformat(),
                "version_app": "1.0.0"
            },
            "parametros": {
                "costos_fijos": modelo["costos_fijos"],
                "precio_venta": modelo["precio_venta"],
                "costo_variable": modelo["costo_variable"],
                "unidades_esperadas": modelo.get("unidades_esperadas", 0)
            }
        }
        
        # Guardar resultados si existen
        if modelo.get("resultados"):
            datos_a_guardar["resultados"] = modelo["resultados"]
        
        # Guardar productos si es análisis multiproducto
        if modelo.get("productos_multiple"):
            datos_a_guardar["productos_multiple"] = modelo["productos_multiple"]
        
        # Guardar análisis de sensibilidad si existe
        if modelo.get("analisis_sensibilidad"):
            datos_a_guardar["analisis_sensibilidad"] = modelo["analisis_sensibilidad"]
        
        # Guardar en formato JSON o pickle según complejidad
        try:
            # Intentar guardar como JSON (más portable)
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                json.dump(datos_a_guardar, f, indent=4, default=str)
        except:
            # Si falla (por objetos no serializables), usar pickle
            with open(ruta_completa, 'wb') as f:
                pickle.dump(datos_a_guardar, f)
        
        return ruta_completa
    
    except Exception as e:
        messagebox.showerror("Error al guardar", f"No se pudo guardar el escenario: {str(e)}")
        return None


def cargar_escenario(ruta=None):
    """
    Carga un escenario previamente guardado.
    
    Args:
        ruta (str, optional): Ruta del archivo a cargar. Si es None, se solicita al usuario.
        
    Returns:
        dict: Diccionario con los datos del modelo cargado, o None si no se pudo cargar
    """
    # Si no se proporciona ruta, solicitar al usuario
    if ruta is None:
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos de Punto de Equilibrio", "*.peq"), ("Todos los archivos", "*.*")]
        )
        if not ruta:  # Si el usuario cancela
            return None
    
    try:
        # Intentar cargar como JSON primero (más seguro)
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                datos_cargados = json.load(f)
        except:
            # Si falla, intentar cargar como pickle
            with open(ruta, 'rb') as f:
                datos_cargados = pickle.load(f)
        
        # Extraer parámetros principales
        modelo = {
            "costos_fijos": datos_cargados["parametros"]["costos_fijos"],
            "precio_venta": datos_cargados["parametros"]["precio_venta"],
            "costo_variable": datos_cargados["parametros"]["costo_variable"],
            "unidades_esperadas": datos_cargados["parametros"].get("unidades_esperadas", 0),
            "analizador": None,  # Será recreado por la aplicación
            "datos_grafico": None  # Será recreado por la aplicación
        }
        
        # Restaurar resultados si existen
        if "resultados" in datos_cargados:
            modelo["resultados"] = datos_cargados["resultados"]
        
        # Restaurar productos si es análisis multiproducto
        if "productos_multiple" in datos_cargados:
            modelo["productos_multiple"] = datos_cargados["productos_multiple"]
        
        # Restaurar análisis de sensibilidad si existe
        if "analisis_sensibilidad" in datos_cargados:
            modelo["analisis_sensibilidad"] = datos_cargados["analisis_sensibilidad"]
        
        return modelo
    
    except Exception as e:
        messagebox.showerror("Error al cargar", f"No se pudo cargar el escenario: {str(e)}")
        return None


def crear_respaldo_automatico(modelo, directorio="respaldos"):
    """
    Crea un respaldo automático del escenario actual.
    
    Args:
        modelo (dict): Diccionario con los datos del modelo
        directorio (str, optional): Directorio donde guardar los respaldos. Default es "respaldos".
        
    Returns:
        str: Ruta del archivo de respaldo, o None si no se pudo crear
    """
    # Asegurar que exista el directorio de respaldos
    if not os.path.exists(directorio):
        try:
            os.makedirs(directorio)
        except Exception:
            # Si no se puede crear, guardar en el directorio actual
            directorio = "."
    
    # Crear nombre con timestamp
    nombre = f"respaldo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.peq"
    
    # Usar la función guardar_escenario
    return guardar_escenario(modelo, nombre, directorio)