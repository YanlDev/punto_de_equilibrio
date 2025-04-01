"""
Módulo que define el frame para la entrada de datos del análisis de punto de equilibrio.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

class FrameDatosEntrada(ttk.Frame):
    """
    Frame para la entrada de datos básicos del análisis de punto de equilibrio.
    """
    
    def __init__(self, parent, controlador):
        """
        Inicializa el frame de entrada de datos.
        
        Args:
            parent: El widget padre (normalmente un Notebook)
            controlador: Instancia de la clase principal de la aplicación
        """
        super().__init__(parent)
        self.controlador = controlador
        
        # Configurar el frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(7, weight=1)  # La última fila se expandirá
        
        # Crear widgets
        self.crear_widgets()
        
    def crear_widgets(self):
        """Crea los widgets del frame."""
        # Título
        ttk.Label(self, text="Análisis de Punto de Equilibrio", 
                 style="Heading.TLabel").grid(row=0, column=0, columnspan=2, pady=20, sticky="n")
        
        # Instrucciones
        ttk.Label(self, text="Ingrese los datos básicos para el análisis:").grid(
            row=1, column=0, columnspan=2, pady=(0, 20), sticky="n")
        
        # Frame para los campos de entrada
        frame_campos = ttk.Frame(self)
        frame_campos.grid(row=2, column=0, columnspan=2, padx=50, sticky="ew")
        frame_campos.columnconfigure(1, weight=1)
        
        # Costos fijos
        ttk.Label(frame_campos, text="Costos Fijos:").grid(
            row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        
        vcmd = (self.register(self.validar_numero), '%P')
        
        self.costos_fijos_var = tk.StringVar()
        self.entrada_costos_fijos = ttk.Entry(
            frame_campos, textvariable=self.costos_fijos_var, validate="key", validatecommand=vcmd)
        self.entrada_costos_fijos.grid(row=0, column=1, sticky="ew", pady=10)
        
        # Precio de venta
        ttk.Label(frame_campos, text="Precio de Venta Unitario:").grid(
            row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.precio_venta_var = tk.StringVar()
        self.entrada_precio_venta = ttk.Entry(
            frame_campos, textvariable=self.precio_venta_var, validate="key", validatecommand=vcmd)
        self.entrada_precio_venta.grid(row=1, column=1, sticky="ew", pady=10)
        
        # Costo variable unitario
        ttk.Label(frame_campos, text="Costo Variable Unitario:").grid(
            row=2, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.costo_variable_var = tk.StringVar()
        self.entrada_costo_variable = ttk.Entry(
            frame_campos, textvariable=self.costo_variable_var, validate="key", validatecommand=vcmd)
        self.entrada_costo_variable.grid(row=2, column=1, sticky="ew", pady=10)
        
        # Unidades esperadas de venta
        ttk.Label(frame_campos, text="Unidades Esperadas de Venta:").grid(
            row=3, column=0, padx=(0, 10), pady=10, sticky="w")
        
        self.unidades_esperadas_var = tk.StringVar()
        self.entrada_unidades_esperadas = ttk.Entry(
            frame_campos, textvariable=self.unidades_esperadas_var, validate="key", validatecommand=vcmd)
        self.entrada_unidades_esperadas.grid(row=3, column=1, sticky="ew", pady=10)
        
        # Botón de calcular
        self.boton_calcular = ttk.Button(
            self, text="Calcular Punto de Equilibrio", command=self.validar_y_calcular)
        self.boton_calcular.grid(row=3, column=0, columnspan=2, pady=30)
        
        # Área de consejos o información
        frame_info = ttk.LabelFrame(self, text="Información")
        frame_info.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        frame_info.columnconfigure(0, weight=1)
        
        info_text = (
            "El punto de equilibrio es el nivel de ventas donde los ingresos totales "
            "son iguales a los costos totales, resultando en una utilidad de cero.\n\n"
            "• Los costos fijos son aquellos que no varían con el nivel de producción.\n"
            "• El precio de venta es el valor al que se vende cada unidad del producto.\n"
            "• El costo variable unitario es el costo que varía directamente con cada unidad producida.\n"
            "• Las unidades esperadas de venta son su proyección para calcular el margen de seguridad."
        )
        
        lbl_info = ttk.Label(frame_info, text=info_text, wraplength=600, justify="left")
        lbl_info.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    def validar_numero(self, valor):
        """
        Valida que el valor ingresado sea un número válido.
        
        Args:
            valor (str): Valor a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if valor == "":
            return True
        
        # Permitir punto decimal y hasta dos cifras decimales
        patron = r'^[0-9]+(\.[0-9]{0,2})?$'
        return bool(re.match(patron, valor))
    
    def validar_y_calcular(self):
        """Valida los campos y llama al método de cálculo del controlador."""
        # Validar que todos los campos estén llenos
        if not (self.costos_fijos_var.get() and self.precio_venta_var.get() and 
                self.costo_variable_var.get()):
            messagebox.showerror(
                "Error de validación", 
                "Debe completar al menos los campos de costos fijos, precio de venta y costo variable."
            )
            return
        
        # Validar que el precio de venta sea mayor que el costo variable
        precio_venta = float(self.precio_venta_var.get())
        costo_variable = float(self.costo_variable_var.get())
        
        if precio_venta <= costo_variable:
            messagebox.showerror(
                "Error de validación", 
                "El precio de venta debe ser mayor que el costo variable unitario."
            )
            return
        
        # Llamar al método de cálculo del controlador
        self.controlador.calcular_punto_equilibrio()
    
    def obtener_costos_fijos(self):
        """
        Obtiene el valor de costos fijos.
        
        Returns:
            float: Valor de costos fijos
        """
        return float(self.costos_fijos_var.get() or 0)
    
    def obtener_precio_venta(self):
        """
        Obtiene el precio de venta unitario.
        
        Returns:
            float: Precio de venta
        """
        return float(self.precio_venta_var.get() or 0)
    
    def obtener_costo_variable(self):
        """
        Obtiene el costo variable unitario.
        
        Returns:
            float: Costo variable unitario
        """
        return float(self.costo_variable_var.get() or 0)
    
    def obtener_unidades_esperadas(self):
        """
        Obtiene las unidades esperadas de venta.
        
        Returns:
            float: Unidades esperadas
        """
        return float(self.unidades_esperadas_var.get() or 0)
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada."""
        self.costos_fijos_var.set("")
        self.precio_venta_var.set("")
        self.costo_variable_var.set("")
        self.unidades_esperadas_var.set("")

    def actualizar_campos_desde_modelo(self):
        """Actualiza los campos de entrada con los datos del modelo actual."""
        modelo = self.controlador.modelo
        
        # Actualizar costos fijos
        if modelo["costos_fijos"] > 0:
            self.costos_fijos_var.set(str(modelo["costos_fijos"]))
        
        # Actualizar precio de venta
        if modelo["precio_venta"] > 0:
            self.precio_venta_var.set(str(modelo["precio_venta"]))
        
        # Actualizar costo variable
        if modelo["costo_variable"] > 0:
            self.costo_variable_var.set(str(modelo["costo_variable"]))
        
        # Actualizar unidades esperadas
        if modelo.get("unidades_esperadas", 0) > 0:
            self.unidades_esperadas_var.set(str(modelo["unidades_esperadas"]))