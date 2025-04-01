"""
Módulo que define el frame para la visualización gráfica del análisis de punto de equilibrio.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FrameGraficos(ttk.Frame):
    """
    Frame para mostrar visualizaciones gráficas del análisis de punto de equilibrio.
    """
    
    def __init__(self, parent, controlador):
        """
        Inicializa el frame de gráficos.
        
        Args:
            parent: El widget padre (normalmente un Notebook)
            controlador: Instancia de la clase principal de la aplicación
        """
        super().__init__(parent)
        self.controlador = controlador
        
        # Configurar el frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        # Variables para los gráficos
        self.figure = None
        self.canvas = None
        
        # Crear widgets
        self.crear_widgets()
        
    def crear_widgets(self):
        """Crea los widgets del frame."""
        # Título
        ttk.Label(self, text="Visualización Gráfica", 
                 style="Heading.TLabel").grid(row=0, column=0, pady=20, sticky="n")
        
        # Frame para controles de visualización
        frame_controles = ttk.Frame(self)
        frame_controles.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Opciones de visualización
        ttk.Label(frame_controles, text="Tipo de gráfico:").pack(side=tk.LEFT, padx=5)
        
        self.combo_tipo_grafico = ttk.Combobox(
            frame_controles, 
            values=["Punto de Equilibrio (Costos e Ingresos)", "Utilidad vs. Volumen", "Margen de Contribución"],
            state="readonly",
            width=40
        )
        self.combo_tipo_grafico.current(0)  # Seleccionar el primer item por defecto
        self.combo_tipo_grafico.pack(side=tk.LEFT, padx=5)
        self.combo_tipo_grafico.bind("<<ComboboxSelected>>", self.cambiar_tipo_grafico)
        
        # Frame para el gráfico
        self.frame_grafico = ttk.Frame(self)
        self.frame_grafico.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Inicializar el gráfico vacío
        self.inicializar_grafico()
        
        # Frame para leyenda e interpretación
        frame_leyenda = ttk.LabelFrame(self, text="Interpretación del Gráfico")
        frame_leyenda.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_leyenda = ttk.Label(
            frame_leyenda, 
            text=(
                "Este gráfico muestra la relación entre costos e ingresos. "
                "El punto de equilibrio se encuentra en la intersección de la línea de costos totales "
                "y la línea de ingresos totales."
            ),
            wraplength=700,
            justify="left"
        )
        self.lbl_leyenda.pack(padx=10, pady=10, anchor="w")
    
    def inicializar_grafico(self):
        """Inicializa el gráfico sin datos."""
        # Crear figura y ejes
        self.figure, self.ax = plt.subplots(figsize=(8, 6), tight_layout=True)
        
        # Añadir canvas para mostrar la figura en Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Mostrar mensaje inicial
        self.ax.text(
            0.5, 0.5, 
            "No hay datos para mostrar.\nCalcule el punto de equilibrio primero.", 
            ha='center', va='center', 
            fontsize=12
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Actualizar el canvas
        self.canvas.draw()
    
    def actualizar_grafico(self):
        """Actualiza el gráfico con los datos actuales del modelo."""
        # Verificar si hay datos para graficar
        if not self.controlador.modelo["datos_grafico"] is not None:
            return
        
        # Obtener el tipo de gráfico seleccionado
        tipo_grafico = self.combo_tipo_grafico.get()
        
        # Limpiar el gráfico actual
        self.ax.clear()
        
        # Mostrar el gráfico según el tipo seleccionado
        if tipo_grafico == "Punto de Equilibrio (Costos e Ingresos)":
            self.graficar_punto_equilibrio()
        elif tipo_grafico == "Utilidad vs. Volumen":
            self.graficar_utilidad()
        elif tipo_grafico == "Margen de Contribución":
            self.graficar_margen_contribucion()
        
        # Actualizar el canvas
        self.canvas.draw()
    
    def graficar_punto_equilibrio(self):
        """Genera el gráfico de punto de equilibrio (costos e ingresos)."""
        # Obtener datos del modelo
        datos = self.controlador.modelo["datos_grafico"]
        pe_unidades = self.controlador.modelo["resultados"]["pe_unidades"]
        pe_valor = self.controlador.modelo["resultados"]["pe_valor"]
        
        # Graficar costos fijos
        self.ax.plot(datos['unidades'], datos['costos_fijos'], 
                    label='Costos Fijos', color='blue', linestyle='--')
        
        # Graficar costos variables
        self.ax.plot(datos['unidades'], datos['costos_variables'], 
                    label='Costos Variables', color='green', linestyle='--')
        
        # Graficar costos totales
        self.ax.plot(datos['unidades'], datos['costos_totales'], 
                    label='Costos Totales', color='red')
        
        # Graficar ingresos
        self.ax.plot(datos['unidades'], datos['ingresos'], 
                    label='Ingresos', color='purple')
        
        # Marcar el punto de equilibrio
        self.ax.plot([pe_unidades], [pe_valor], 'ro', markersize=8, 
                    label=f'Punto de Equilibrio: {pe_unidades:.2f} unidades')
        
        # Líneas punteadas para el punto de equilibrio
        self.ax.axvline(x=pe_unidades, color='gray', linestyle=':', alpha=0.7)
        self.ax.axhline(y=pe_valor, color='gray', linestyle=':', alpha=0.7)
        
        # Configurar ejes y leyenda
        self.ax.set_xlabel('Unidades')
        self.ax.set_ylabel('Valor ($)')
        self.ax.set_title('Análisis de Punto de Equilibrio')
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Actualizar la leyenda
        self.lbl_leyenda.config(
            text=(
                "Este gráfico muestra la relación entre costos e ingresos. "
                f"El punto de equilibrio se encuentra en {pe_unidades:.2f} unidades, "
                f"con un valor de ventas de ${pe_valor:.2f}. "
                "En este punto, los ingresos totales igualan a los costos totales, "
                "resultando en una utilidad de cero."
            )
        )
    
    def graficar_utilidad(self):
        """Genera el gráfico de utilidad vs. volumen."""
        # Obtener datos del modelo
        datos = self.controlador.modelo["datos_grafico"]
        pe_unidades = self.controlador.modelo["resultados"]["pe_unidades"]
        
        # Graficar utilidad
        self.ax.plot(datos['unidades'], datos['utilidades'], 
                    label='Utilidad', color='green')
        
        # Línea de utilidad cero
        self.ax.axhline(y=0, color='red', linestyle='-', alpha=0.5)
        
        # Marcar el punto de equilibrio
        self.ax.plot([pe_unidades], [0], 'ro', markersize=8, 
                    label=f'Punto de Equilibrio: {pe_unidades:.2f} unidades')
        
        # Línea vertical en el punto de equilibrio
        self.ax.axvline(x=pe_unidades, color='gray', linestyle=':', alpha=0.7)
        
        # Áreas de utilidad y pérdida
        x = datos['unidades'].values
        y = datos['utilidades'].values
        self.ax.fill_between(x, y, 0, where=(y > 0), color='green', alpha=0.3, label='Área de Utilidad')
        self.ax.fill_between(x, y, 0, where=(y < 0), color='red', alpha=0.3, label='Área de Pérdida')
        
        # Configurar ejes y leyenda
        self.ax.set_xlabel('Unidades')
        self.ax.set_ylabel('Utilidad ($)')
        self.ax.set_title('Utilidad vs. Volumen')
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Actualizar la leyenda
        self.lbl_leyenda.config(
            text=(
                "Este gráfico muestra la relación entre el volumen de ventas y la utilidad. "
                f"El punto de equilibrio se encuentra en {pe_unidades:.2f} unidades, donde la utilidad es cero. "
                "El área verde representa la zona de utilidad (>0), mientras que "
                "el área roja representa la zona de pérdida (<0)."
            )
        )
    
    def graficar_margen_contribucion(self):
        """Genera el gráfico de margen de contribución."""
        # Obtener datos del modelo
        datos = self.controlador.modelo["datos_grafico"]
        costos_fijos = self.controlador.modelo["costos_fijos"]
        margen_contribucion = (
            self.controlador.modelo["precio_venta"] - 
            self.controlador.modelo["costo_variable"]
        )
        pe_unidades = self.controlador.modelo["resultados"]["pe_unidades"]
        
        # Crear serie de unidades y calcular margen de contribución total
        unidades = datos['unidades'].values
        margen_contribucion_total = unidades * margen_contribucion
        
        # Graficar margen de contribución total
        self.ax.plot(unidades, margen_contribucion_total, 
                    label='Margen de Contribución Total', color='blue')
        
        # Graficar línea de costos fijos
        self.ax.axhline(y=costos_fijos, color='red', linestyle='-', 
                       label=f'Costos Fijos: ${costos_fijos:.2f}')
        
        # Marcar el punto de equilibrio
        self.ax.plot([pe_unidades], [costos_fijos], 'ro', markersize=8, 
                    label=f'Punto de Equilibrio: {pe_unidades:.2f} unidades')
        
        # Línea vertical en el punto de equilibrio
        self.ax.axvline(x=pe_unidades, color='gray', linestyle=':', alpha=0.7)
        
        # Áreas de utilidad y pérdida
        self.ax.fill_between(unidades, margen_contribucion_total, costos_fijos, 
                           where=(margen_contribucion_total > costos_fijos), 
                           color='green', alpha=0.3, label='Área de Utilidad')
        self.ax.fill_between(unidades, margen_contribucion_total, costos_fijos, 
                           where=(margen_contribucion_total < costos_fijos), 
                           color='red', alpha=0.3, label='Área de Pérdida')
        
        # Configurar ejes y leyenda
        self.ax.set_xlabel('Unidades')
        self.ax.set_ylabel('Valor ($)')
        self.ax.set_title('Análisis de Margen de Contribución')
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Actualizar la leyenda
        self.lbl_leyenda.config(
            text=(
                "Este gráfico muestra el margen de contribución total en relación con los costos fijos. "
                f"El punto de equilibrio se encuentra en {pe_unidades:.2f} unidades, donde el margen de contribución "
                f"total iguala a los costos fijos (${costos_fijos:.2f}). "
                "El área verde representa la zona de utilidad, donde el margen de contribución excede los costos fijos, "
                "mientras que el área roja representa la zona de pérdida."
            )
        )
    
    def cambiar_tipo_grafico(self, event=None):
        """Maneja el evento de cambio de tipo de gráfico."""
        # Solo actualizar si hay datos
        if self.controlador.modelo["datos_grafico"] is not None:
            self.actualizar_grafico()