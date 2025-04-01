"""
Módulo que define el frame para el análisis de sensibilidad del punto de equilibrio.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FrameSensibilidad(ttk.Frame):
    """
    Frame para realizar análisis de sensibilidad del punto de equilibrio.
    """
    
    def __init__(self, parent, controlador):
        """
        Inicializa el frame de análisis de sensibilidad.
        
        Args:
            parent: El widget padre (normalmente un Notebook)
            controlador: Instancia de la clase principal de la aplicación
        """
        super().__init__(parent)
        self.controlador = controlador
        
        # Configurar el frame
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=6)
        self.rowconfigure(1, weight=1)
        
        # Variables para el análisis
        self.variable_analisis = tk.StringVar(value="Costos Fijos")
        self.porcentaje_min = tk.StringVar(value="-30")
        self.porcentaje_max = tk.StringVar(value="30")
        self.incrementos = tk.StringVar(value="10")
        
        # Variables para los gráficos
        self.figure = None
        self.canvas = None
        
        # Crear widgets
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crea los widgets del frame."""
        # Título
        ttk.Label(self, text="Análisis de Sensibilidad", 
                 style="Heading.TLabel").grid(row=0, column=0, columnspan=2, pady=20, sticky="n")
        
        # Frame para controles
        frame_controles = ttk.LabelFrame(self, text="Parámetros del Análisis")
        frame_controles.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Variable a analizar
        ttk.Label(frame_controles, text="Variable a analizar:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        
        combo_variables = ttk.Combobox(
            frame_controles, 
            textvariable=self.variable_analisis,
            values=["Costos Fijos", "Precio de Venta", "Costo Variable Unitario"],
            state="readonly"
        )
        combo_variables.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Rango de porcentajes
        ttk.Label(frame_controles, text="Porcentaje mínimo (%):").grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        
        entry_porcentaje_min = ttk.Entry(frame_controles, textvariable=self.porcentaje_min, width=10)
        entry_porcentaje_min.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(frame_controles, text="Porcentaje máximo (%):").grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        
        entry_porcentaje_max = ttk.Entry(frame_controles, textvariable=self.porcentaje_max, width=10)
        entry_porcentaje_max.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(frame_controles, text="Incrementos (%):").grid(
            row=3, column=0, padx=10, pady=10, sticky="w")
        
        entry_incrementos = ttk.Entry(frame_controles, textvariable=self.incrementos, width=10)
        entry_incrementos.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Botón para calcular
        btn_calcular = ttk.Button(
            frame_controles, text="Calcular Sensibilidad", command=self.calcular_sensibilidad)
        btn_calcular.grid(row=4, column=0, columnspan=2, padx=10, pady=20)
        
        # Espacio para mostrar tabla de resultados
        frame_tabla = ttk.LabelFrame(frame_controles, text="Resultados")
        frame_tabla.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # ScrolledText para mostrar resultados en formato tabular
        self.texto_resultados = tk.Text(frame_tabla, height=10, width=30)
        scrollbar = ttk.Scrollbar(frame_tabla, command=self.texto_resultados.yview)
        self.texto_resultados.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para gráficos
        frame_grafico = ttk.LabelFrame(self, text="Visualización de Sensibilidad")
        frame_grafico.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Inicializar el área de gráfico
        self.figure, self.ax = plt.subplots(figsize=(6, 5), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.figure, frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Mostrar mensaje inicial
        self.ax.text(
            0.5, 0.5, 
            "Seleccione los parámetros y\npresione 'Calcular Sensibilidad'", 
            ha='center', va='center', 
            fontsize=12
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
    
    def actualizar_datos(self):
        """Actualiza los datos del frame cuando cambia el modelo."""
        # Este método puede ser llamado cuando se actualiza el modelo,
        # pero no necesitamos hacer nada especial aquí
        pass
    
    def calcular_sensibilidad(self):
        """Calcula y muestra el análisis de sensibilidad."""
        # Verificar si hay un análisis activo
        if self.controlador.modelo["analizador"] is None:
            messagebox.showinfo(
                "Información", 
                "Primero debe calcular el punto de equilibrio en la pestaña de Datos de Entrada."
            )
            return
        
        try:
            # Obtener parámetros del análisis
            variable = self.variable_analisis.get()
            porcentaje_min = float(self.porcentaje_min.get())
            porcentaje_max = float(self.porcentaje_max.get())
            incrementos = float(self.incrementos.get())
            
            # Validar parámetros
            if porcentaje_min >= porcentaje_max:
                raise ValueError("El porcentaje mínimo debe ser menor que el máximo.")
            
            if incrementos <= 0:
                raise ValueError("El incremento debe ser mayor que cero.")
            
            # Obtener los valores base del modelo
            costos_fijos = self.controlador.modelo["costos_fijos"]
            precio_venta = self.controlador.modelo["precio_venta"]
            costo_variable = self.controlador.modelo["costo_variable"]
            
            # Generar los porcentajes a evaluar
            porcentajes = np.arange(porcentaje_min, porcentaje_max + incrementos, incrementos)
            
            # Calcular puntos de equilibrio para cada porcentaje
            resultados = []
            
            for porcentaje in porcentajes:
                # Calcular el valor ajustado según la variable seleccionada
                factor = 1 + (porcentaje / 100)
                
                if variable == "Costos Fijos":
                    costos_fijos_ajustados = costos_fijos * factor
                    pe_unidades = costos_fijos_ajustados / (precio_venta - costo_variable)
                    variable_ajustada = costos_fijos_ajustados
                elif variable == "Precio de Venta":
                    precio_venta_ajustado = precio_venta * factor
                    # Verificar que el precio ajustado sea mayor que el costo variable
                    if precio_venta_ajustado <= costo_variable:
                        continue
                    pe_unidades = costos_fijos / (precio_venta_ajustado - costo_variable)
                    variable_ajustada = precio_venta_ajustado
                else:  # Costo Variable Unitario
                    costo_variable_ajustado = costo_variable * factor
                    # Verificar que el costo variable ajustado sea menor que el precio de venta
                    if costo_variable_ajustado >= precio_venta:
                        continue
                    pe_unidades = costos_fijos / (precio_venta - costo_variable_ajustado)
                    variable_ajustada = costo_variable_ajustado
                
                # Calcular el valor monetario
                pe_valor = pe_unidades * precio_venta
                
                # Almacenar resultados
                resultados.append({
                    "porcentaje": porcentaje,
                    "variable_ajustada": variable_ajustada,
                    "pe_unidades": pe_unidades,
                    "pe_valor": pe_valor
                })
            
            # Mostrar resultados en la tabla
            self.mostrar_tabla_resultados(variable, resultados)
            
            # Graficar resultados
            self.graficar_sensibilidad(variable, resultados)
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
            return False
    
    def mostrar_tabla_resultados(self, variable, resultados):
        """
        Muestra los resultados del análisis en formato de tabla.
        
        Args:
            variable (str): Nombre de la variable analizada
            resultados (list): Lista de diccionarios con los resultados
        """
        # Limpiar contenido previo
        self.texto_resultados.delete(1.0, tk.END)
        
        # Crear encabezado según la variable
        if variable == "Costos Fijos":
            encabezado = "% Cambio | Costos Fijos | PE Unidades | PE Valor\n"
        elif variable == "Precio de Venta":
            encabezado = "% Cambio | Precio Venta | PE Unidades | PE Valor\n"
        else:  # Costo Variable Unitario
            encabezado = "% Cambio | Costo Var. | PE Unidades | PE Valor\n"
        
        self.texto_resultados.insert(tk.END, encabezado)
        self.texto_resultados.insert(tk.END, "-" * 50 + "\n")
        
        # Insertar cada fila de resultados
        for r in resultados:
            fila = f"{r['porcentaje']:+6.1f}% | "
            fila += f"${r['variable_ajustada']:.2f} | "
            fila += f"{r['pe_unidades']:.2f} | "
            fila += f"${r['pe_valor']:.2f}\n"
            
            self.texto_resultados.insert(tk.END, fila)
    
    def graficar_sensibilidad(self, variable, resultados):
        """
        Grafica los resultados del análisis de sensibilidad.
        
        Args:
            variable (str): Nombre de la variable analizada
            resultados (list): Lista de diccionarios con los resultados
        """
        # Limpiar gráfico anterior
        self.ax.clear()
        
        if not resultados:
            self.ax.text(
                0.5, 0.5, 
                "No hay resultados válidos para graficar.\nVerifique los parámetros.", 
                ha='center', va='center', 
                fontsize=12
            )
            self.canvas.draw()
            return
        
        # Extraer datos para el gráfico
        porcentajes = [r["porcentaje"] for r in resultados]
        pe_unidades = [r["pe_unidades"] for r in resultados]
        pe_valor = [r["pe_valor"] for r in resultados]
        
        # Crear gráfico de dos ejes para unidades y valor
        color1 = 'tab:blue'
        self.ax.set_xlabel('Cambio Porcentual (%)')
        self.ax.set_ylabel('Punto de Equilibrio (Unidades)', color=color1)
        line1 = self.ax.plot(porcentajes, pe_unidades, marker='o', color=color1, label='PE Unidades')
        self.ax.tick_params(axis='y', labelcolor=color1)
        
        # Crear segundo eje Y para el valor monetario
        ax2 = self.ax.twinx()
        color2 = 'tab:red'
        ax2.set_ylabel('Punto de Equilibrio (Valor $)', color=color2)
        line2 = ax2.plot(porcentajes, pe_valor, marker='s', color=color2, label='PE Valor')
        ax2.tick_params(axis='y', labelcolor=color2)
        
        # Título según la variable analizada
        self.ax.set_title(f'Sensibilidad del Punto de Equilibrio a Cambios en {variable}')
        
        # Línea vertical en el 0% (valor base)
        self.ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)
        
        # Combinar leyendas de ambos ejes
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        self.ax.legend(lines, labels, loc='best')
        
        # Mostrar grid
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Actualizar el canvas
        self.canvas.draw()