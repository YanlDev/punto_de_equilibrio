"""
Módulo principal para la interfaz gráfica de la aplicación de análisis de punto de equilibrio.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import datetime

# Para las funcionalidades de guardar/cargar
from utils.guardar_cargar import guardar_escenario as guardar, cargar_escenario as cargar
from utils.exportar import exportar_a_pdf, exportar_a_excel

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
        # Verificar si hay datos para guardar
        if self.modelo["analizador"] is None:
            messagebox.showinfo("Información", 
                               "Primero debe calcular el punto de equilibrio para guardar el escenario.")
            return

        # Solicitar nombre para el escenario
        nombre_escenario = filedialog.asksaveasfilename(
            defaultextension=".peq",
            filetypes=[("Archivos de Punto de Equilibrio", "*.peq"), ("Todos los archivos", "*.*")],
            title="Guardar escenario como"
        )

        if not nombre_escenario:
            return  # El usuario canceló

        # Guardar escenario utilizando la función de utilidad
        ruta_guardado = guardar(self.modelo, nombre_escenario)

        if ruta_guardado:
            messagebox.showinfo("Guardar escenario", 
                               f"Escenario guardado correctamente en:\n{ruta_guardado}")

    def cargar_escenario(self):
        """Carga un escenario guardado."""
        # Solicitar archivo a cargar
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos de Punto de Equilibrio", "*.peq"), ("Todos los archivos", "*.*")],
            title="Cargar escenario"
        )

        if not ruta_archivo:
            return  # El usuario canceló

        # Cargar escenario utilizando la función de utilidad
        modelo_cargado = cargar(ruta_archivo)

        if modelo_cargado:
            # Actualizar el modelo con los datos cargados
            self.modelo.update(modelo_cargado)

            # Recrear el analizador si los datos básicos están disponibles
            if (self.modelo["costos_fijos"] > 0 and self.modelo["precio_venta"] > 0 and 
                self.modelo["costo_variable"] > 0):
                from core.equilibrio import AnalizadorEquilibrio
                self.modelo["analizador"] = AnalizadorEquilibrio(
                    costos_fijos=self.modelo["costos_fijos"],
                    precio_venta=self.modelo["precio_venta"],
                    costo_variable_unitario=self.modelo["costo_variable"]
                )

                # Regenerar datos para gráficos si no existen
                if self.modelo["datos_grafico"] is None and self.modelo["analizador"] is not None:
                    self.modelo["datos_grafico"] = self.modelo["analizador"].generar_datos_grafico(
                        unidades_max=self.modelo["unidades_esperadas"] * 1.2 
                        if self.modelo["unidades_esperadas"] > 0 else None
                    )

            # Actualizar la interfaz con los datos cargados
            self.frame_datos.actualizar_campos_desde_modelo()
            self.actualizar_vistas()

            messagebox.showinfo("Cargar escenario", "Escenario cargado correctamente.")
    
    def exportar_pdf(self):
        """Exporta los resultados a PDF."""
        # Verificar si hay resultados para exportar
        if not self.modelo["resultados"]:
            messagebox.showinfo("Información", 
                               "Primero debe calcular el punto de equilibrio para exportar los resultados.")
            return

        # Solicitar ubicación para guardar el PDF
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            title="Exportar a PDF"
        )

        if not ruta_archivo:
            return  # El usuario canceló

        # Exportar a PDF utilizando la función de utilidad
        try:
            ruta_exportada = exportar_a_pdf(self.modelo, ruta_archivo)
            messagebox.showinfo("Exportar a PDF", 
                               f"Informe exportado correctamente a:\n{ruta_exportada}")
        except Exception as e:
            messagebox.showerror("Error al exportar", 
                                f"Ocurrió un error al exportar a PDF: {str(e)}")

    def exportar_excel(self):
        """Exporta los resultados a Excel."""
        # Verificar si hay resultados para exportar
        if not self.modelo["resultados"]:
            messagebox.showinfo("Información", 
                               "Primero debe calcular el punto de equilibrio para exportar los resultados.")
            return

        # Solicitar ubicación para guardar el Excel
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            title="Exportar a Excel"
        )

        if not ruta_archivo:
            return  # El usuario canceló

        # Exportar a Excel utilizando la función de utilidad
        try:
            ruta_exportada = exportar_a_excel(self.modelo, ruta_archivo)
            messagebox.showinfo("Exportar a Excel", 
                               f"Datos exportados correctamente a:\n{ruta_exportada}")
        except Exception as e:
            messagebox.showerror("Error al exportar", 
                                f"Ocurrió un error al exportar a Excel: {str(e)}")
    
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
        # Crear una nueva ventana para el manual
        import tkinter as tk
        from tkinter import ttk
        import os

        # Verificar si existe el directorio para el manual
        if not os.path.exists("assets/docs"):
            os.makedirs("assets/docs")

        # Verificar si existe el archivo del manual (si no, crearlo)
        ruta_manual = "assets/docs/manual_usuario.txt"
        if not os.path.exists(ruta_manual):
            # Crear contenido básico del manual
            contenido_manual = """
            MANUAL DE USUARIO - ANALIZADOR DE PUNTO DE EQUILIBRIO
            ====================================================

            INTRODUCCIÓN
            -----------
            Esta aplicación permite realizar análisis de punto de equilibrio,
            una herramienta fundamental para la toma de decisiones financieras
            y de gestión empresarial.

            FUNCIONALIDADES PRINCIPALES
            --------------------------
            1. Cálculo del Punto de Equilibrio
               - En unidades
               - En valor monetario

            2. Análisis de Sensibilidad
               - Evaluar el impacto de cambios en costos fijos, precio de venta
                 y costo variable unitario

            3. Análisis Multiproducto
               - Calcular el punto de equilibrio para múltiples productos

            4. Visualización Gráfica
               - Gráficos de punto de equilibrio
               - Utilidad vs. Volumen
               - Margen de Contribución

            CÓMO UTILIZAR LA APLICACIÓN
            --------------------------
            1. Datos de Entrada:
               - Ingrese los costos fijos totales
               - Ingrese el precio de venta unitario
               - Ingrese el costo variable unitario
               - Opcionalmente, ingrese las unidades esperadas de venta
               - Haga clic en "Calcular Punto de Equilibrio"

            2. Resultados:
               - Vea el punto de equilibrio en unidades y valor
               - Consulte el margen de seguridad
               - Analice la utilidad estimada

            3. Gráficos:
               - Seleccione el tipo de gráfico que desea visualizar
               - Interprete la información proporcionada

            4. Análisis de Sensibilidad:
               - Seleccione la variable a analizar
               - Establezca los rangos de variación
               - Interprete cómo afectan los cambios al punto de equilibrio

            5. Análisis Multiproducto:
               - Agregue los diferentes productos
               - Establezca el mix de ventas
               - Calcule el punto de equilibrio combinado

            GUARDAR Y CARGAR ESCENARIOS
            --------------------------
            - Utilice el menú "Archivo" para guardar el escenario actual
            - Cargue escenarios previamente guardados para continuar su análisis

            EXPORTAR RESULTADOS
            ------------------
            - Exporte a PDF para informes formales
            - Exporte a Excel para análisis adicionales

            CONTACTO Y SOPORTE
            -----------------
            Para soporte técnico o consultas sobre la aplicación:
            - Email: soporte@analizadorpe.com
            - Teléfono: (01) 234-5678
            """

            # Guardar el manual en el archivo
            with open(ruta_manual, "w") as f:
                f.write(contenido_manual)

        # Crear ventana para mostrar el manual
        ventana_manual = tk.Toplevel(self.root)
        ventana_manual.title("Manual de Usuario")
        ventana_manual.geometry("700x500")
        ventana_manual.minsize(600, 400)

        # Configurar estilo
        frame_manual = ttk.Frame(ventana_manual, padding="10")
        frame_manual.pack(fill=tk.BOTH, expand=True)

        # Cargar el contenido del manual
        with open(ruta_manual, "r") as f:
            contenido = f.read()

        # Crear widget de texto para mostrar el manual
        texto_manual = tk.Text(frame_manual, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(frame_manual, orient="vertical", command=texto_manual.yview)
        texto_manual.configure(yscrollcommand=scrollbar.set)

        # Empaquetar widgets
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        texto_manual.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Insertar contenido
        texto_manual.insert(tk.END, contenido)
        texto_manual.config(state=tk.DISABLED)  # Solo lectura

        # Botón para cerrar
        ttk.Button(ventana_manual, text="Cerrar", command=ventana_manual.destroy).pack(pady=10)

        # Centrar la ventana en la pantalla
        ventana_manual.update_idletasks()
        ancho = ventana_manual.winfo_width()
        alto = ventana_manual.winfo_height()
        x = (ventana_manual.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_manual.winfo_screenheight() // 2) - (alto // 2)
        ventana_manual.geometry(f"{ancho}x{alto}+{x}+{y}")