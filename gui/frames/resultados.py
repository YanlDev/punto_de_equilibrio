"""
Módulo que define el frame para mostrar los resultados del análisis de punto de equilibrio.
"""
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import scrolledtext, messagebox

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
        # Verificar si hay resultados para generar el informe
        if not self.controlador.modelo["resultados"]:
            messagebox.showinfo("Información", 
                               "Primero debe calcular el punto de equilibrio.")
            return
        
        # Crear una nueva ventana para el informe
        ventana_informe = tk.Toplevel(self.master)
        ventana_informe.title("Informe Detallado de Punto de Equilibrio")
        ventana_informe.geometry("800x600")
        ventana_informe.minsize(700, 500)
        
        # Obtener datos necesarios
        modelo = self.controlador.modelo
        resultados = modelo["resultados"]
        
        # Crear el frame principal
        frame_principal = ttk.Frame(ventana_informe, padding=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Agregar título
        ttk.Label(frame_principal, text="INFORME DETALLADO DE ANÁLISIS DE PUNTO DE EQUILIBRIO", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Agregar fecha de generación
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ttk.Label(frame_principal, text=f"Generado el: {fecha_actual}", 
                 font=("Arial", 10, "italic")).pack(pady=(0, 20))
        
        # Crear widget de texto desplazable para el informe

        informe_texto = scrolledtext.ScrolledText(frame_principal, wrap=tk.WORD, 
                                                 width=80, height=25, 
                                                 font=("Courier", 10))
        informe_texto.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Generar el contenido del informe
        contenido_informe = self._generar_contenido_informe()
        
        # Insertar el contenido
        informe_texto.insert(tk.END, contenido_informe)
        informe_texto.config(state=tk.DISABLED)  # Solo lectura
        
        # Agregar botones
        frame_botones = ttk.Frame(ventana_informe)
        frame_botones.pack(fill=tk.X, pady=10)
        
        # Botón para imprimir
        def imprimir_informe():
            self.controlador.exportar_pdf()
            
        ttk.Button(frame_botones, text="Exportar a PDF", 
                  command=imprimir_informe).pack(side=tk.LEFT, padx=10)
        
        # Botón para exportar a Excel
        def exportar_a_excel():
            self.controlador.exportar_excel()
            
        ttk.Button(frame_botones, text="Exportar a Excel", 
                  command=exportar_a_excel).pack(side=tk.LEFT, padx=10)
        
        # Botón para cerrar
        ttk.Button(frame_botones, text="Cerrar", 
                  command=ventana_informe.destroy).pack(side=tk.RIGHT, padx=10)
        
        # Centrar la ventana en la pantalla
        ventana_informe.update_idletasks()
        ancho = ventana_informe.winfo_width()
        alto = ventana_informe.winfo_height()
        x = (ventana_informe.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_informe.winfo_screenheight() // 2) - (alto // 2)
        ventana_informe.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def _generar_contenido_informe(self):
        """Genera el contenido textual del informe."""
        modelo = self.controlador.modelo
        resultados = modelo["resultados"]
        margen = resultados["margen_seguridad"]
        
        # Encabezado
        informe = "=" * 80 + "\n"
        informe += "                   INFORME DE ANÁLISIS DE PUNTO DE EQUILIBRIO\n"
        informe += "=" * 80 + "\n\n"
        
        # Datos básicos
        informe += "DATOS DE ENTRADA\n"
        informe += "-" * 80 + "\n"
        informe += f"Costos Fijos Totales:        ${modelo['costos_fijos']:.2f}\n"
        informe += f"Precio de Venta Unitario:    ${modelo['precio_venta']:.2f}\n"
        informe += f"Costo Variable Unitario:     ${modelo['costo_variable']:.2f}\n"
        informe += f"Margen de Contribución:      ${modelo['precio_venta'] - modelo['costo_variable']:.2f}\n"
        
        if modelo.get('unidades_esperadas', 0) > 0:
            informe += f"Unidades Esperadas de Venta: {modelo['unidades_esperadas']:.2f} unidades\n"
        
        informe += "\n"
        
        # Punto de equilibrio
        informe += "PUNTO DE EQUILIBRIO\n"
        informe += "-" * 80 + "\n"
        informe += f"Punto de Equilibrio (Unidades):   {resultados['pe_unidades']:.2f} unidades\n"
        informe += f"Punto de Equilibrio (Valor):      ${resultados['pe_valor']:.2f}\n"
        informe += f"Ratio de Margen de Contribución:  {resultados['ratio_mc'] * 100:.2f}%\n\n"
        
        # Margen de seguridad (solo si hay unidades esperadas)
        if modelo.get('unidades_esperadas', 0) > 0:
            informe += "MARGEN DE SEGURIDAD\n"
            informe += "-" * 80 + "\n"
            
            if modelo['unidades_esperadas'] > resultados['pe_unidades']:
                informe += f"Margen de Seguridad (Unidades):  {margen['unidades']:.2f} unidades\n"
                informe += f"Margen de Seguridad (Valor):     ${margen['valor']:.2f}\n"
                informe += f"Margen de Seguridad (Porcentaje): {margen['porcentaje']:.2f}%\n\n"
                
                informe += f"Utilidad Estimada:               ${resultados['utilidad_estimada']:.2f}\n"
                informe += f"Grado de Apalancamiento Operativo: {resultados['gao']:.2f}\n\n"
            else:
                informe += "Las unidades esperadas son menores al punto de equilibrio.\n"
                informe += "En el nivel de ventas esperado se incurrirá en pérdidas.\n\n"
                
                # Calcular la pérdida esperada
                perdida = (modelo['unidades_esperadas'] * (modelo['precio_venta'] - modelo['costo_variable'])) - modelo['costos_fijos']
                informe += f"Pérdida Estimada: ${abs(perdida):.2f}\n\n"
        
        # Interpretación
        informe += "INTERPRETACIÓN DE RESULTADOS\n"
        informe += "-" * 80 + "\n"
        
        # Interpretación básica del punto de equilibrio
        interpretacion = (
            f"Con un costo fijo de ${modelo['costos_fijos']:.2f}, un precio de venta de "
            f"${modelo['precio_venta']:.2f} y un costo variable unitario de "
            f"${modelo['costo_variable']:.2f}, el punto de equilibrio se alcanza al "
            f"vender {resultados['pe_unidades']:.2f} unidades, lo que representa un valor de ventas "
            f"de ${resultados['pe_valor']:.2f}.\n\n"
            
            f"El ratio de margen de contribución es {resultados['ratio_mc'] * 100:.2f}%, lo que significa "
            f"que por cada peso de ventas, {resultados['ratio_mc'] * 100:.2f} centavos contribuyen a cubrir "
            f"los costos fijos y generar utilidades."
        )
        
        informe += interpretacion + "\n\n"
        
        # Interpretación del margen de seguridad si hay unidades esperadas
        if modelo.get('unidades_esperadas', 0) > 0:
            unidades_esperadas = modelo['unidades_esperadas']
            pe_unidades = resultados['pe_unidades']
            
            if unidades_esperadas > pe_unidades:
                interpretacion_margen = (
                    f"Con una proyección de ventas de {unidades_esperadas:.2f} unidades, "
                    f"existe un margen de seguridad de {margen['unidades']:.2f} unidades "
                    f"({margen['porcentaje']:.2f}%), lo que indica que las ventas pueden "
                    f"caer hasta en un {margen['porcentaje']:.2f}% antes de incurrir en pérdidas.\n\n"
                    
                    f"Con el nivel de ventas esperado, se estima una utilidad de "
                    f"${resultados['utilidad_estimada']:.2f}.\n\n"
                    
                    f"El grado de apalancamiento operativo (GAO) es {resultados['gao']:.2f}, "
                    f"lo que significa que por cada 1% de cambio en las ventas, la utilidad "
                    f"cambiará en aproximadamente {resultados['gao']:.2f}%."
                )
            else:
                interpretacion_margen = (
                    f"La proyección de ventas ({unidades_esperadas:.2f} unidades) es menor "
                    f"que el punto de equilibrio ({pe_unidades:.2f} unidades), lo que indica "
                    f"que con este nivel de ventas se incurrirá en pérdidas.\n\n"
                    
                    f"Se recomienda aumentar las ventas en al menos "
                    f"{pe_unidades - unidades_esperadas:.2f} unidades para alcanzar el punto de equilibrio, "
                    f"o bien revisar la estructura de costos y precios para mejorar la situación."
                )
            
            informe += interpretacion_margen + "\n\n"
        
        # Recomendaciones
        informe += "RECOMENDACIONES\n"
        informe += "-" * 80 + "\n"
        
        # Recomendaciones generales
        recomendaciones = [
            "Evaluar posibles estrategias para reducir los costos fijos.",
            "Analizar la posibilidad de aumentar el precio de venta, siempre que el mercado lo permita.",
            "Buscar formas de reducir los costos variables por unidad.",
            "Trabajar en estrategias para aumentar el volumen de ventas."
        ]
        
        for i, rec in enumerate(recomendaciones, 1):
            informe += f"{i}. {rec}\n"
        
        informe += "\n"
        
        # Conclusión
        informe += "CONCLUSIÓN\n"
        informe += "-" * 80 + "\n"
        informe += (
            "El análisis de punto de equilibrio es una herramienta fundamental para la toma de "
            "decisiones en la gestión empresarial. Este informe proporciona una base para "
            "evaluar la estructura de costos y precios, así como para establecer objetivos "
            "de ventas que garanticen la rentabilidad del negocio.\n\n"
            
            "Se recomienda realizar análisis de sensibilidad para evaluar el impacto de "
            "posibles cambios en las variables críticas y así prepararse para diferentes "
            "escenarios en el futuro."
        )
        
        informe += "\n\n"
        informe += "=" * 80 + "\n"
        informe += "                                FIN DEL INFORME\n"
        informe += "=" * 80 + "\n"
        
        return informe