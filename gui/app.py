"""
Módulo principal para la interfaz gráfica de la aplicación de análisis de punto de equilibrio.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar frames
from gui.frames.datos_entrada import FrameDatosEntrada
from gui.frames.resultados import FrameResultados
from gui.frames.graficos import FrameGraficos
from gui.frames.sensibilidad import FrameSensibilidad
from gui.frames.multiproducto import FrameMultiProducto

# Importar funcionalidades del core (modelo)
from core.equilibrio import AnalizadorEquilibrio


class AplicacionPuntoEquilibrio:
    """
    Clase principal que define la ventana y componentes de la aplicación
    de análisis de punto de equilibrio.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación.
        
        Args:
            root (tk.Tk): La ventana raíz de la aplicación
        """
        self.root = root
        self.root.title("Analizador de Punto de Equilibrio")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear el contenedor principal
        self.contenedor_principal = ttk.Frame(self.root)
        self.contenedor_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear sistema de pestañas
        self.notebook = ttk.Notebook(self.contenedor_principal)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Variables del modelo (datos compartidos)
        self.inicializar_modelo()
        
        # Instanciar los frames principales (vistas)
        self.frame_datos = FrameDatosEntrada(self.notebook, self)
        self.frame_resultados = FrameResultados(self.notebook, self)
        self.frame_graficos = FrameGraficos(self.notebook, self)
        self.frame_sensibilidad = FrameSensibilidad(self.notebook, self)
        self.frame_multiproducto = FrameMultiProducto(self.notebook, self)
        
        # Añadir pestañas al notebook
        self.notebook.add(self.frame_datos, text="Datos de Entrada")
        self.notebook.add(self.frame_resultados, text="Resultados")
        self.notebook.add(self.frame_graficos, text="Gráficos")
        self.notebook.add(self.frame_sensibilidad, text="Análisis de Sensibilidad")
        self.notebook.add(self.frame_multiproducto, text="Análisis Multiproducto")
        
        # Crear barra de menú
        self.crear_menu()
        
        # Vincular eventos (parte del controlador)
        self.notebook.bind("<<NotebookTabChanged>>", self.cambio_pestaña)
        
    def inicializar_modelo(self):
        """Inicializa el modelo de datos de la aplicación."""
        # Datos básicos para el análisis
        self.modelo = {
            "costos_fijos": 0.0,
            "precio_venta": 0.0,
            "costo_variable": 0.0,
            "analizador": None,  # Instancia de AnalizadorEquilibrio
            "datos_grafico": None,  # DataFrame para gráficos
            "resultados": {},  # Resultados del análisis
            "unidades_esperadas": 0.0,
            "productos_multiple": []  # Para análisis multiproducto
        }
    
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación."""
        self.estilo = ttk.Style()
        
        # Usar tema predeterminado del sistema
        if sys.platform == "win32":
            self.estilo.theme_use('vista')
        elif sys.platform == "darwin":
            self.estilo.theme_use('aqua')
        else:
            self.estilo.theme_use('clam')
            
        # Configurar estilos específicos
        self.estilo.configure('TFrame', background='#f5f5f5')
        self.estilo.configure('TLabel', font=('Arial', 10))
        self.estilo.configure('TButton', font=('Arial', 10))
        self.estilo.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        self.estilo.configure('Result.TLabel', font=('Arial', 11), foreground='#0066cc')
        
    def crear_menu(self):
        """Crea la barra de menú de la aplicación."""
        self.menu_principal = tk.Menu(self.root)
        self.root.config(menu=self.menu_principal)
        
        # Menú Archivo
        self.menu_archivo = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.menu_archivo.add_command(label="Nuevo análisis", command=self.nuevo_analisis)
        self.menu_archivo.add_command(label="Guardar escenario", command=self.guardar_escenario)
        self.menu_archivo.add_command(label="Cargar escenario", command=self.cargar_escenario)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.root.quit)
        
        # Menú Exportar
        self.menu_exportar = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Exportar", menu=self.menu_exportar)
        self.menu_exportar.add_command(label="Exportar a PDF", command=self.exportar_pdf)
        self.menu_exportar.add_command(label="Exportar a Excel", command=self.exportar_excel)
        
        # Menú Ayuda
        self.menu_ayuda = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        self.menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.menu_ayuda.add_command(label="Manual de uso", command=self.mostrar_manual)
    
    # Métodos del controlador
    def calcular_punto_equilibrio(self):
        """
        Calcula el punto de equilibrio utilizando los datos actuales.
        Este método es parte del controlador que conecta la vista con el modelo.
        """
        try:
            # Obtener datos del formulario (a través de la vista)
            costos_fijos = self.frame_datos.obtener_costos_fijos()
            precio_venta = self.frame_datos.obtener_precio_venta()
            costo_variable = self.frame_datos.obtener_costo_variable()
            unidades_esperadas = self.frame_datos.obtener_unidades_esperadas()
            
            # Actualizar el modelo
            self.modelo["costos_fijos"] = costos_fijos
            self.modelo["precio_venta"] = precio_venta
            self.modelo["costo_variable"] = costo_variable
            self.modelo["unidades_esperadas"] = unidades_esperadas
            
            # Crear instancia del analizador (parte del modelo)
            self.modelo["analizador"] = AnalizadorEquilibrio(
                costos_fijos=costos_fijos,
                precio_venta=precio_venta,
                costo_variable_unitario=costo_variable
            )
            
            # Realizar cálculos
            analizador = self.modelo["analizador"]
            pe_unidades = analizador.punto_equilibrio_unidades()
            pe_valor = analizador.punto_equilibrio_valor()
            ratio_mc = analizador.ratio_margen_contribucion()
            
            # Calcular margen de seguridad si las unidades esperadas son mayores al punto de equilibrio
            if unidades_esperadas > pe_unidades:
                margen_seguridad = analizador.margen_seguridad(unidades_esperadas)
                utilidad_estimada = analizador.utilidad_estimada(unidades_esperadas)
                gao = analizador.grado_apalancamiento_operativo(unidades_esperadas)
            else:
                margen_seguridad = {"unidades": 0, "valor": 0, "porcentaje": 0}
                utilidad_estimada = 0
                gao = 0
            
            # Generar datos para el gráfico
            self.modelo["datos_grafico"] = analizador.generar_datos_grafico(
                unidades_max=max(pe_unidades * 2, unidades_esperadas * 1.2) if unidades_esperadas > 0 else None
            )
            
            # Almacenar resultados en el modelo
            self.modelo["resultados"] = {
                "pe_unidades": pe_unidades,
                "pe_valor": pe_valor,
                "ratio_mc": ratio_mc,
                "margen_seguridad": margen_seguridad,
                "utilidad_estimada": utilidad_estimada,
                "gao": gao
            }
            
            # Actualizar vistas
            self.actualizar_vistas()
            
            # Cambiar a la pestaña de resultados
            self.notebook.select(1)  # Índice 1 corresponde a la pestaña de resultados
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al calcular: {str(e)}")
            return False
    
    def actualizar_vistas(self):
        """Actualiza todas las vistas con los datos actuales del modelo."""
        # Actualizar cada frame con los datos actualizados
        self.frame_resultados.actualizar_resultados()
        self.frame_graficos.actualizar_grafico()
        self.frame_sensibilidad.actualizar_datos()
        
    def cambio_pestaña(self, event):
        """Maneja el evento de cambio de pestaña."""
        # Obtener el índice de la pestaña seleccionada
        tab_index = self.notebook.index(self.notebook.select())
        
        # Si se selecciona una pestaña diferente a la de datos de entrada
        # y no hay resultados calculados, mostrar un mensaje
        if tab_index > 0 and self.modelo["analizador"] is None:
            messagebox.showinfo(
                "Información requerida", 
                "Primero debe ingresar los datos y calcular el punto de equilibrio."
            )
            self.notebook.select(0)  # Volver a la pestaña de datos de entrada
    
    # Métodos para el menú
    def nuevo_analisis(self):
        """Reinicia el análisis actual."""
        if messagebox.askyesno("Nuevo análisis", "¿Desea iniciar un nuevo análisis? Los datos no guardados se perderán."):
            self.inicializar_modelo()
            self.frame_datos.limpiar_campos()
            self.actualizar_vistas()
            self.notebook.select(0)  # Volver a la pestaña de datos de entrada
    
    def guardar_escenario(self):
        """Guarda el escenario actual."""
        # Esta funcionalidad se implementará más adelante
        messagebox.showinfo("Información", "Funcionalidad en desarrollo")
    
    def cargar_escenario(self):
        """Carga un escenario guardado."""
        # Esta funcionalidad se implementará más adelante
        messagebox.showinfo("Información", "Funcionalidad en desarrollo")
    
    def exportar_pdf(self):
        """Exporta los resultados a PDF."""
        # Esta funcionalidad se implementará más adelante
        messagebox.showinfo("Información", "Funcionalidad en desarrollo")
    
    def exportar_excel(self):
        """Exporta los resultados a Excel."""
        # Esta funcionalidad se implementará más adelante
        messagebox.showinfo("Información", "Funcionalidad en desarrollo")
    
    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación."""
        messagebox.showinfo(
            "Acerca de", 
            "Analizador de Punto de Equilibrio v1.0\n"
            "Desarrollado con Python y Tkinter\n\n"
            "© 2025 - Todos los derechos reservados"
        )
    
    def mostrar_manual(self):
        """Muestra el manual de uso."""
        # Esta funcionalidad se implementará más adelante
        messagebox.showinfo("Información", "Funcionalidad en desarrollo")