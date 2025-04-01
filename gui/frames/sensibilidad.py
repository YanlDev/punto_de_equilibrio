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
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        
        # Variables para el análisis
        self.variable_analisis = tk.StringVar(value="Costos Fijos")
        self.porcentaje_min = tk.StringVar(value="-30")
        self.porcentaje_max = tk.StringVar(value="30")
        self.incrementos = tk.StringVar(value="10")
        
        # Variables para los gráficos
        self.figure = None
        self.canvas = None
        self.resultados_calculados = None
        
        # Crear widgets
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crea los widgets del frame."""
        # Título
        ttk.Label(self, text="Análisis de Sensibilidad", 
                 style="Heading.TLabel").grid(row=0, column=0, pady=20, sticky="n")
        
        # Frame para controles
        frame_controles = ttk.LabelFrame(self, text="Parámetros del Análisis")
        frame_controles.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Crear un frame contenedor para colocar los controles en el lado izquierdo
        frame_izquierdo = ttk.Frame(frame_controles)
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Variable a analizar
        ttk.Label(frame_izquierdo, text="Variable a analizar:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        
        combo_variables = ttk.Combobox(
            frame_izquierdo, 
            textvariable=self.variable_analisis,
            values=["Costos Fijos", "Precio de Venta", "Costo Variable Unitario"],
            state="readonly",
            width=25
        )
        combo_variables.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Rango de porcentajes
        ttk.Label(frame_izquierdo, text="Porcentaje mínimo (%):").grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        
        entry_porcentaje_min = ttk.Entry(frame_izquierdo, textvariable=self.porcentaje_min, width=10)
        entry_porcentaje_min.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(frame_izquierdo, text="Porcentaje máximo (%):").grid(
            row=2, column=0, padx=10, pady=10, sticky="w")
        
        entry_porcentaje_max = ttk.Entry(frame_izquierdo, textvariable=self.porcentaje_max, width=10)
        entry_porcentaje_max.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(frame_izquierdo, text="Incrementos (%):").grid(
            row=3, column=0, padx=10, pady=10, sticky="w")
        
        entry_incrementos = ttk.Entry(frame_izquierdo, textvariable=self.incrementos, width=10)
        entry_incrementos.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Botón para calcular
        btn_calcular = ttk.Button(
            frame_izquierdo, text="Calcular Sensibilidad", command=self.calcular_sensibilidad)
        btn_calcular.grid(row=4, column=0, columnspan=2, padx=10, pady=20)
        
        # Botón para ver gráfico detallado
        btn_grafico = ttk.Button(
            frame_izquierdo, text="Ver Gráfico Detallado", command=self.mostrar_grafico_detallado)
        btn_grafico.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        
        # Crear un frame para la explicación/información
        frame_derecho = ttk.LabelFrame(frame_controles, text="Información del Análisis de Sensibilidad")
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto de información
        texto_info = (
            "El Análisis de Sensibilidad evalúa cómo los cambios en variables críticas "
            "afectan el punto de equilibrio.\n\n"
            
            "• Variable a analizar: Seleccione qué variable desea modificar (costos fijos, "
            "precio de venta o costo variable).\n\n"
            
            "• Porcentaje mínimo: Indica la reducción máxima a aplicar a la variable "
            "(valor negativo). Por ejemplo, -30% significa reducir hasta un 30%.\n\n"
            
            "• Porcentaje máximo: Indica el aumento máximo a aplicar a la variable "
            "(valor positivo). Por ejemplo, 30% significa aumentar hasta un 30%.\n\n"
            
            "• Incrementos: Define los intervalos entre cada punto de análisis. "
            "Un valor de 10% generará puntos cada 10% (ej: -30%, -20%, -10%, 0%, +10%, +20%, +30%).\n\n"
            
            "Este análisis le ayuda a entender qué tan sensible es su punto de equilibrio "
            "ante cambios en las distintas variables, permitiéndole identificar "
            "en cuáles debería enfocarse para obtener mejores resultados."
        )
        
        lbl_info = ttk.Label(frame_derecho, text=texto_info, wraplength=400, justify="left")
        lbl_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para mostrar tabla de resultados (abajo, ocupando todo el ancho)
        frame_resultados = ttk.LabelFrame(self, text="Resultados del Análisis de Sensibilidad")
        frame_resultados.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # ScrolledText para mostrar resultados en formato tabular con mejores detalles
        self.texto_resultados = tk.Text(frame_resultados, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(frame_resultados, command=self.texto_resultados.yview)
        self.texto_resultados.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
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
            
            # Guardar resultados para uso posterior
            self.resultados_calculados = {
                "variable": variable,
                "resultados": resultados,
                "valor_base": {
                    "costos_fijos": costos_fijos,
                    "precio_venta": precio_venta,
                    "costo_variable": costo_variable
                }
            }
            
            # Mostrar resultados en la tabla
            self.mostrar_tabla_resultados(variable, resultados)
            
            # Mostrar gráfico detallado en ventana separada
            self.mostrar_grafico_detallado()
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
            return False
    
    def mostrar_tabla_resultados(self, variable, resultados):
        """
        Muestra los resultados del análisis en formato de tabla con interpretación detallada.
        
        Args:
            variable (str): Nombre de la variable analizada
            resultados (list): Lista de diccionarios con los resultados
        """
        # Limpiar contenido previo
        self.texto_resultados.delete(1.0, tk.END)
        
        if not resultados:
            self.texto_resultados.insert(tk.END, "No hay resultados válidos para mostrar.\n"
                                       "Esto puede ocurrir si los cambios en las variables generan situaciones inviables,\n"
                                       "como un precio de venta menor al costo variable.")
            return
        
        # Cabecera con título
        titulo = f"ANÁLISIS DE SENSIBILIDAD: IMPACTO DE CAMBIOS EN {variable.upper()}\n"
        self.texto_resultados.insert(tk.END, titulo, "titulo")
        self.texto_resultados.insert(tk.END, "=" * 80 + "\n\n")
        
        # Resumen de datos base
        base_info = (
            f"DATOS BASE DEL ANÁLISIS:\n"
            f"- Costos Fijos: ${self.controlador.modelo['costos_fijos']:.2f}\n"
            f"- Precio de Venta: ${self.controlador.modelo['precio_venta']:.2f}\n"
            f"- Costo Variable Unitario: ${self.controlador.modelo['costo_variable']:.2f}\n"
            f"- Punto de Equilibrio Base: {self.controlador.modelo['resultados']['pe_unidades']:.2f} unidades "
            f"(${self.controlador.modelo['resultados']['pe_valor']:.2f})\n\n"
        )
        self.texto_resultados.insert(tk.END, base_info)
        
        # Crear encabezado según la variable
        self.texto_resultados.insert(tk.END, "RESULTADOS DEL ANÁLISIS:\n")
        if variable == "Costos Fijos":
            encabezado = f"{'% Cambio':<10} | {'Costos Fijos':<15} | {'PE Unidades':<15} | {'PE Valor':<15} | {'Var. PE %':<10}\n"
        elif variable == "Precio de Venta":
            encabezado = f"{'% Cambio':<10} | {'Precio Venta':<15} | {'PE Unidades':<15} | {'PE Valor':<15} | {'Var. PE %':<10}\n"
        else:  # Costo Variable Unitario
            encabezado = f"{'% Cambio':<10} | {'Costo Var.':<15} | {'PE Unidades':<15} | {'PE Valor':<15} | {'Var. PE %':<10}\n"
        
        self.texto_resultados.insert(tk.END, encabezado)
        self.texto_resultados.insert(tk.END, "-" * 80 + "\n")
        
        # Obtener PE base para calcular variaciones porcentuales
        pe_base = self.controlador.modelo['resultados']['pe_unidades']
        
        # Insertar cada fila de resultados
        for r in resultados:
            # Calcular variación porcentual del PE respecto al base
            var_pe_pct = ((r['pe_unidades'] - pe_base) / pe_base) * 100
            
            fila = f"{r['porcentaje']:+6.1f}% | "
            fila += f"${r['variable_ajustada']:<14.2f} | "
            fila += f"{r['pe_unidades']:<14.2f} | "
            fila += f"${r['pe_valor']:<14.2f} | "
            fila += f"{var_pe_pct:+8.2f}%\n"
            
            self.texto_resultados.insert(tk.END, fila)
        
        # Añadir interpretación
        self.texto_resultados.insert(tk.END, "\nINTERPRETACIÓN DEL ANÁLISIS:\n")
        self.texto_resultados.insert(tk.END, "-" * 80 + "\n")
        
        # Calcular elasticidad (sensibilidad promedio)
        if len(resultados) > 1:
            # Buscar resultados para cambios de +10% y -10% para calcular elasticidad
            r_mas10 = next((r for r in resultados if abs(r['porcentaje'] - 10) < 0.001), None)
            r_menos10 = next((r for r in resultados if abs(r['porcentaje'] + 10) < 0.001), None)
            
            if r_mas10 and r_menos10:
                # Calcular elasticidad como la proporción del cambio en PE dividido por el cambio en la variable
                var_pe_mas = (r_mas10['pe_unidades'] - pe_base) / pe_base * 100
                var_pe_menos = (r_menos10['pe_unidades'] - pe_base) / pe_base * 100
                elasticidad_mas = var_pe_mas / 10  # El cambio fue de 10%
                elasticidad_menos = var_pe_menos / -10  # El cambio fue de -10%
                elasticidad_promedio = (abs(elasticidad_mas) + abs(elasticidad_menos)) / 2
                
                interpretacion = (
                    f"El análisis muestra la sensibilidad del punto de equilibrio ante cambios en {variable.lower()}.\n\n"
                    f"La elasticidad promedio es aproximadamente {elasticidad_promedio:.2f}, lo que significa que "
                    f"por cada 1% de cambio en {variable.lower()}, el punto de equilibrio cambia aproximadamente "
                    f"en un {elasticidad_promedio:.2f}%.\n\n"
                )
                
                # Añadir interpretación según la variable
                if variable == "Costos Fijos":
                    interpretacion += (
                        f"Un aumento del 10% en los costos fijos incrementa el punto de equilibrio "
                        f"en un {var_pe_mas:.2f}% (a {r_mas10['pe_unidades']:.2f} unidades).\n\n"
                        f"Una reducción del 10% en los costos fijos disminuye el punto de equilibrio "
                        f"en un {abs(var_pe_menos):.2f}% (a {r_menos10['pe_unidades']:.2f} unidades).\n\n"
                        f"{'→ Recomendación: ' if abs(elasticidad_promedio) > 0.8 else ''}"
                        f"{'Este análisis indica que el punto de equilibrio es altamente sensible a cambios en los costos fijos. ' if abs(elasticidad_promedio) > 0.8 else ''}"
                        f"{'Se recomienda explorar estrategias para reducir los costos fijos o convertirlos en variables.' if abs(elasticidad_promedio) > 0.8 else ''}"
                    )
                elif variable == "Precio de Venta":
                    interpretacion += (
                        f"Un aumento del 10% en el precio de venta reduce el punto de equilibrio "
                        f"en un {abs(var_pe_mas):.2f}% (a {r_mas10['pe_unidades']:.2f} unidades).\n\n"
                        f"Una reducción del 10% en el precio de venta aumenta el punto de equilibrio "
                        f"en un {var_pe_menos:.2f}% (a {r_menos10['pe_unidades']:.2f} unidades).\n\n"
                        f"{'→ Recomendación: ' if abs(elasticidad_promedio) > 0.8 else ''}"
                        f"{'Este análisis indica que el punto de equilibrio es altamente sensible a cambios en el precio de venta. ' if abs(elasticidad_promedio) > 0.8 else ''}"
                        f"{'Se recomienda evaluar cuidadosamente la estrategia de precios y el impacto en la demanda antes de modificarlos.' if abs(elasticidad_promedio) > 0.8 else ''}"
                    )
                else:  # Costo Variable
                    interpretacion += (
                        f"Un aumento del 10% en el costo variable aumenta el punto de equilibrio "
                        f"en un {var_pe_mas:.2f}% (a {r_mas10['pe_unidades']:.2f} unidades).\n\n"
                        f"Una reducción del 10% en el costo variable disminuye el punto de equilibrio "
                        f"en un {abs(var_pe_menos):.2f}% (a {r_menos10['pe_unidades']:.2f} unidades).\n\n"
                        f"{'→ Recomendación: ' if abs(elasticidad_promedio) > 0.8 else ''}"
                        f"{'Este análisis indica que el punto de equilibrio es altamente sensible a cambios en los costos variables. ' if abs(elasticidad_promedio) > 0.8 else ''}"
                        f"{'Se recomienda buscar eficiencias en la producción o negociar mejores condiciones con proveedores.' if abs(elasticidad_promedio) > 0.8 else ''}"
                    )
            else:
                interpretacion = (
                    f"El análisis muestra cómo el punto de equilibrio cambia cuando se modifica {variable.lower()}.\n\n"
                    f"Para una interpretación más detallada, se recomienda utilizar incrementos que incluyan +/-10%."
                )
        else:
            interpretacion = (
                f"No hay suficientes datos para realizar un análisis completo de sensibilidad.\n"
                f"Se recomienda ajustar los parámetros para obtener más puntos de análisis."
            )
        
        self.texto_resultados.insert(tk.END, interpretacion)
        
        # Configurar estilos de texto si es posible
        try:
            self.texto_resultados.tag_configure("titulo", font=("Arial", 12, "bold"))
        except:
            pass  # Ignorar si falla la configuración de tags
    
    def mostrar_grafico_detallado(self):
        """Muestra el gráfico de resultados en una ventana separada con más detalle."""
        if not self.resultados_calculados:
            messagebox.showinfo(
                "Información", 
                "Primero debe calcular el análisis de sensibilidad."
            )
            return
        
        # Crear una nueva ventana para el gráfico detallado
        ventana_grafico = tk.Toplevel(self.master)
        ventana_grafico.title("Gráfico Detallado - Análisis de Sensibilidad")
        ventana_grafico.geometry("900x700")
        ventana_grafico.minsize(800, 600)
        
        # Crear frame contenedor
        frame_principal = ttk.Frame(ventana_grafico, padding=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        variable = self.resultados_calculados["variable"]
        ttk.Label(
            frame_principal, 
            text=f"Análisis de Sensibilidad: Impacto de Cambios en {variable}",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 20))
        
        # Crear frame para el gráfico
        frame_grafico = ttk.Frame(frame_principal)
        frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear gráfico detallado
        self.crear_grafico_detallado(frame_grafico)
        
        # Botón para cerrar
        ttk.Button(
            frame_principal, 
            text="Cerrar", 
            command=ventana_grafico.destroy
        ).pack(pady=10)
        
        # Centrar la ventana
        ventana_grafico.update_idletasks()
        ancho = ventana_grafico.winfo_width()
        alto = ventana_grafico.winfo_height()
        x = (ventana_grafico.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana_grafico.winfo_screenheight() // 2) - (alto // 2)
        ventana_grafico.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def crear_grafico_detallado(self, frame_contenedor):
        """
        Crea un gráfico detallado para mostrar en la ventana separada.
        
        Args:
            frame_contenedor: Frame donde se mostrará el gráfico
        """
        datos = self.resultados_calculados
        variable = datos["variable"]
        resultados = datos["resultados"]
        valores_base = datos["valor_base"]
        
        if not resultados:
            # Si no hay resultados válidos, mostrar mensaje
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No hay datos válidos para graficar.\nVerifique los parámetros del análisis.", 
                    ha='center', va='center', fontsize=14)
            ax.set_xticks([])
            ax.set_yticks([])
            
            canvas = FigureCanvasTkAgg(fig, frame_contenedor)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            return
        
        # Crear figura con dos subplots
        fig = plt.figure(figsize=(12, 9))
        
        # Extraer datos para graficar
        porcentajes = [r["porcentaje"] for r in resultados]
        pe_unidades = [r["pe_unidades"] for r in resultados]
        pe_valor = [r["pe_valor"] for r in resultados]
        valores_ajustados = [r["variable_ajustada"] for r in resultados]
        
        # Obtener PE base para referencia
        pe_base_unidades = self.controlador.modelo['resultados']['pe_unidades']
        pe_base_valor = self.controlador.modelo['resultados']['pe_valor']
        
        # Primer subplot: PE Unidades vs Porcentaje de cambio
        ax1 = fig.add_subplot(2, 1, 1)
        
        # Graficar línea de PE Unidades
        line_unidades = ax1.plot(porcentajes, pe_unidades, marker='o', color='blue', 
                                label='PE Unidades', linewidth=2)
        
        # Línea horizontal en el valor base
        ax1.axhline(y=pe_base_unidades, color='blue', linestyle='--', alpha=0.5, 
                   label=f'PE Base: {pe_base_unidades:.2f} unidades')
        
        # Línea vertical en 0% (sin cambio)
        ax1.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
        
        # Etiquetas y leyenda
        ax1.set_xlabel('Cambio Porcentual (%)', fontsize=12)
        ax1.set_ylabel('Punto de Equilibrio (Unidades)', color='blue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='blue')
        
        # Configurar grid
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        # Segundo eje Y para mostrar los valores de la variable
        ax1_twin = ax1.twinx()
        
        # Etiqueta según la variable
        if variable == "Costos Fijos":
            var_label = "Costos Fijos ($)"
            base_value = valores_base["costos_fijos"]
        elif variable == "Precio de Venta":
            var_label = "Precio de Venta ($)"
            base_value = valores_base["precio_venta"]
        else:  # Costo Variable
            var_label = "Costo Variable ($)"
            base_value = valores_base["costo_variable"]
        
        # Graficar línea de valor variable
        line_variable = ax1_twin.plot(porcentajes, valores_ajustados, marker='s', 
                                     color='green', label=var_label, linestyle='--', linewidth=1.5)
        
        # Línea horizontal en el valor base de la variable
        ax1_twin.axhline(y=base_value, color='green', linestyle='--', alpha=0.5, 
                        label=f'{var_label} Base: ${base_value:.2f}')
        
        ax1_twin.set_ylabel(var_label, color='green', fontsize=12)
        ax1_twin.tick_params(axis='y', labelcolor='green')
        
        # Combinar leyendas
        lines1 = line_unidades + line_variable
        labels1 = [l.get_label() for l in lines1]
        ax1.legend(lines1, labels1, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
                  ncol=2, fontsize=10)
        
        # Añadir título
        ax1.set_title(f'Impacto de Cambios en {variable} sobre el Punto de Equilibrio (Unidades)', 
                     fontsize=14, pad=10)
        
        # Segundo subplot: PE Valor vs Porcentaje de cambio
        ax2 = fig.add_subplot(2, 1, 2)
        
        # Graficar línea de PE Valor
        ax2.plot(porcentajes, pe_valor, marker='o', color='red', 
                label='PE Valor ($)', linewidth=2)
        
        # Línea horizontal en el valor base
        ax2.axhline(y=pe_base_valor, color='red', linestyle='--', alpha=0.5,