"""
Aplicación para Análisis de Punto de Equilibrio

Este programa permite calcular y visualizar el punto de equilibrio para
un negocio, así como realizar análisis de sensibilidad y escenarios multiproducto.
"""

import os
import sys
import tkinter as tk
from gui.app import AplicacionPuntoEquilibrio

# Verificar si se están creando directorios necesarios
def verificar_directorios():
    """Verifica que existan los directorios necesarios para la aplicación."""
    directorios = [
        'gui',
        'gui/frames',
        'gui/utils',
        'core',
        'utils',
        'assets',
        'assets/icons'
    ]
    
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"Directorio creado: {directorio}")

# Punto de entrada de la aplicación
def main():
    """Función principal que inicia la aplicación."""
    # Verificar directorios
    verificar_directorios()
    
    # Crear ventana principal
    root = tk.Tk()
    
    # Establecer icono y título
    root.title("Analizador de Punto de Equilibrio")
    
    # Intentar establecer el icono si existe
    icono_path = os.path.join("assets", "icons", "icon.ico")
    if os.path.exists(icono_path):
        root.iconbitmap(icono_path)
    
    # Iniciar la aplicación
    app = AplicacionPuntoEquilibrio(root)
    
    # Iniciar el bucle principal
    root.mainloop()

# Ejecutar la aplicación si este script es el punto de entrada
if __name__ == "__main__":
    main()