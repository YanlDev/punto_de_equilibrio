"""
Módulo que define el frame para mostrar los resultados del análisis de punto de equilibrio.
"""

import tkinter as tk
from tkinter import ttk

class FrameResultados(ttk.Frame):
    """
    Frame para mostrar los resultados del análisis de punto de equilibrio.
    """
    
    def __init__(self, parent, controlador):
        """
        Inicializa el frame de resultados.
        
        Args:
            parent: El widget padre (normalmente un Notebook)
            controlador: Instancia de la clase principal de la aplicación
        """
        super().__init__(parent)
        self.controlador = controlador
        
        # Configurar el frame
        self.columnconfigure(0, weight=1)
        
        # Crear widgets
        self.crear_widgets()
        
    def crear_widgets(self):
        """Crea los widgets del frame."""
        # Título
        ttk.Label(self, text="Resultados del Análisis", 
                 style="Heading.TLabel").grid(row=0, column=0, pady=20, sticky="n")
        
        # Frame para mostrar los resultados
        self.frame_resultados = ttk.LabelFrame(self, text="Punto de Equilibrio")
        self.frame_resultados.grid(row=1, column=0, padx=50, pady=10, sticky="ew")
        self.frame_resultados.columnconfigure(1, weight=1)
        
        # Etiquetas para mostrar los resultados
        ttk.Label(self.frame_resultados, text="Punto de Equilibrio en Unidades:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.lbl_pe_unidades = ttk.Label(self.frame_resultados, text="-", style="Result.TLabel")
        self.lbl_pe_unidades.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Punto de Equilibrio en Valor Monetario:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.lbl_pe_valor = ttk.Label(self.frame_resultados, text="-", style="Result.TLabel")
        self.lbl_pe_valor.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.frame_resultados, text="Ratio de Margen de Contribución:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        self.lbl_ratio_mc = ttk.Label(self.frame_resultados, text="-", style="Result.TLabel")
        self.lbl_ratio_mc.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Frame para el margen de seguridad
        self.frame_margen = ttk.LabelFrame(self, text="Margen de Seguridad")
        self.frame_margen.grid(row=2, column=0, padx=50, pady=10, sticky="ew")
        self.frame_margen.columnconfigure(1, weight=1)
        
        ttk.Label(self.frame_margen, text="Margen de Seguridad en Unidades:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.lbl_ms_unidades = ttk.Label(self.frame_margen, text="-", style="Result.TLabel")
        self.lbl_ms_unidades.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.frame_margen, text="Margen de Seguridad en Valor:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.lbl_ms_valor = ttk.Label(self.frame_margen, text="-", style="Result.TLabel")
        self.lbl_ms_valor.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.frame_margen, text="Margen de Seguridad en Porcentaje:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        self.lbl_ms_porcentaje = ttk.Label(self.frame_margen, text="-", style="Result.TLabel")
        self.lbl_ms_porcentaje.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Frame para utilidad y apalancamiento
        self.frame_utilidad = ttk.LabelFrame(self, text="Utilidad y Apalancamiento")
        self.frame_utilidad.grid(row=3, column=0, padx=50, pady=10, sticky="ew")
        self.frame_utilidad.columnconfigure(1, weight=1)
        
        ttk.Label(self.frame_utilidad, text="Utilidad Estimada:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.lbl_utilidad = ttk.Label(self.frame_utilidad, text="-", style="Result.TLabel")
        self.lbl_utilidad.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.frame_utilidad, text="Grado de Apalancamiento Operativo:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.lbl_gao = ttk.Label(self.frame_utilidad, text="-", style="Result.TLabel")
        self.lbl_gao.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Agregar botón para generar informe
        self.btn_informe = ttk.Button(
            self, text="Generar Informe Detallado", command=self.generar_informe)
        self.btn_informe.grid(row=4, column=0, pady=30)
        
        # Área de interpretación
        frame_interpretacion = ttk.LabelFrame(self, text="Interpretación de Resultados")
        frame_interpretacion.grid(row=5, column=0, sticky="ew", padx=50, pady=10)
        frame_interpretacion.columnconfigure(0, weight=1)
        
        self.texto_interpretacion = tk.Text(frame_interpretacion, height=8, wrap=tk.WORD)
        self.texto_interpretacion.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.texto_interpretacion.config(state=tk.DISABLED)  # Solo lectura
    
    def actualizar_resultados(self):
        """Actualiza los resultados mostrados con los datos actuales del modelo."""
        # Verificar si hay resultados para mostrar
        if not self.controlador.modelo["resultados"]:
            return
        
        # Obtener resultados del modelo
        resultados = self.controlador.modelo["resultados"]
        
        # Actualizar etiquetas
        self.lbl_pe_unidades.config(text=f"{resultados['pe_unidades']:.2f} unidades")
        self.lbl_pe_valor.config(text=f"${resultados['pe_valor']:.2f}")
        self.lbl_ratio_mc.config(text=f"{resultados['ratio_mc'] * 100:.2f}%")
        
        # Actualizar margen de seguridad
        margen = resultados['margen_seguridad']
        self.lbl_ms_unidades.config(text=f"{margen['unidades']:.2f} unidades")
        self.lbl_ms_valor.config(text=f"${margen['valor']:.2f}")
        self.lbl_ms_porcentaje.config(text=f"{margen['porcentaje']:.2f}%")
        
        # Actualizar utilidad y apalancamiento
        self.lbl_utilidad.config(text=f"${resultados['utilidad_estimada']:.2f}")
        
        # El GAO podría ser muy alto o indefinido
        gao = resultados['gao']
        if gao > 1000:
            self.lbl_gao.config(text="Muy alto (>1000)")
        else:
            self.lbl_gao.config(text=f"{gao:.2f}")
        
        # Generar interpretación de resultados
        self.actualizar_interpretacion()
    
    def actualizar_interpretacion(self):
        """Genera e inserta una interpretación de los resultados actuales."""
        modelo = self.controlador.modelo
        resultados = modelo["resultados"]
        
        # Habilitar la edición del widget Text
        self.texto_interpretacion.config(state=tk.NORMAL)
        self.texto_interpretacion.delete(1.0, tk.END)  # Limpiar contenido anterior
        
        # Obtener datos relevantes
        pe_unidades = resultados["pe_unidades"]
        pe_valor = resultados["pe_valor"]
        ratio_mc = resultados["ratio_mc"]
        unidades_esperadas = modelo["unidades_esperadas"]
        
        # Crear texto de interpretación
        interpretacion = (
            f"Con un costo fijo de ${modelo['costos_fijos']:.2f}, un precio de venta de "
            f"${modelo['precio_venta']:.2f} y un costo variable unitario de "
            f"${modelo['costo_variable']:.2f}, el punto de equilibrio se alcanza al "
            f"vender {pe_unidades:.2f} unidades, lo que representa un valor de ventas "
            f"de ${pe_valor:.2f}.\n\n"
        )
        
        # Añadir interpretación sobre el ratio de margen de contribución
        interpretacion += (
            f"El ratio de margen de contribución es {ratio_mc * 100:.2f}%, lo que significa "
            f"que por cada peso de ventas, {ratio_mc * 100:.2f} centavos contribuyen a cubrir "
            f"los costos fijos y generar utilidades.\n\n"
        )
        
        # Interpretar el margen de seguridad si hay unidades esperadas
        if unidades_esperadas > 0:
            margen = resultados["margen_seguridad"]
            if margen["unidades"] > 0:
                interpretacion += (
                    f"Con una proyección de ventas de {unidades_esperadas:.2f} unidades, "
                    f"existe un margen de seguridad de {margen['unidades']:.2f} unidades "
                    f"({margen['porcentaje']:.2f}%), lo que indica que las ventas pueden "
                    f"caer hasta en un {margen['porcentaje']:.2f}% antes de incurrir en pérdidas.\n\n"
                )
            else:
                interpretacion += (
                    f"La proyección de ventas ({unidades_esperadas:.2f} unidades) es menor "
                    f"que el punto de equilibrio ({pe_unidades:.2f} unidades), lo que indica "
                    f"que con este nivel de ventas se incurrirá en pérdidas.\n\n"
                )
        
        # Añadir la interpretación al widget
        self.texto_interpretacion.insert(tk.END, interpretacion)
        self.texto_interpretacion.config(state=tk.DISABLED)  # Volver a solo lectura
    
    def generar_informe(self):
        """Genera un informe detallado de los resultados."""
        # Esta funcionalidad se implementará más adelante
        tk.messagebox.showinfo("Información", "Funcionalidad en desarrollo")