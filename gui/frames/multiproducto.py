"""
Módulo que define el frame para el análisis de punto de equilibrio multiproducto.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Importar la funcionalidad de cálculo multiproducto
from core.equilibrio import calcular_punto_equilibrio_multiproducto


class FrameMultiProducto(ttk.Frame):
    """
    Frame para realizar análisis de punto de equilibrio con múltiples productos.
    """
    
    def __init__(self, parent, controlador):
        """
        Inicializa el frame de análisis multiproducto.
        
        Args:
            parent: El widget padre (normalmente un Notebook)
            controlador: Instancia de la clase principal de la aplicación
        """
        super().__init__(parent)
        self.controlador = controlador
        
        # Configurar el frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        # Lista para almacenar los productos
        self.productos = []
        
        # Variables para los gráficos
        self.figure = None
        self.canvas = None
        self.resultados_calculados = None
        
        # Crear widgets
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crea los widgets del frame."""
        # Título
        ttk.Label(self, text="Análisis Multiproducto", 
                 style="Heading.TLabel").grid(row=0, column=0, pady=20, sticky="n")
        
        # Frame para la gestión de productos
        frame_productos = ttk.LabelFrame(self, text="Gestión de Productos")
        frame_productos.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Frame para añadir un producto
        frame_agregar = ttk.Frame(frame_productos)
        frame_agregar.pack(fill=tk.X, padx=10, pady=10)
        
        # Campos para un nuevo producto
        ttk.Label(frame_agregar, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nombre_var = tk.StringVar()
        ttk.Entry(frame_agregar, textvariable=self.nombre_var, width=15).grid(
            row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(frame_agregar, text="Precio Venta:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.precio_var = tk.StringVar()
        ttk.Entry(frame_agregar, textvariable=self.precio_var, width=10).grid(
            row=0, column=3, padx=5, pady=5, sticky="w")
        
        ttk.Label(frame_agregar, text="Costo Variable:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.costo_var = tk.StringVar()
        ttk.Entry(frame_agregar, textvariable=self.costo_var, width=10).grid(
            row=0, column=5, padx=5, pady=5, sticky="w")
        
        ttk.Label(frame_agregar, text="Mix (%):").grid(row=0, column=6, padx=5, pady=5, sticky="w")
        self.mix_var = tk.StringVar()
        ttk.Entry(frame_agregar, textvariable=self.mix_var, width=10).grid(
            row=0, column=7, padx=5, pady=5, sticky="w")
        
        # Botón para agregar producto
        ttk.Button(frame_agregar, text="Agregar Producto", command=self.agregar_producto).grid(
            row=0, column=8, padx=10, pady=5, sticky="e")
        
        # Frame para lista de productos
        frame_lista = ttk.Frame(frame_productos)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Crear tabla para mostrar productos
        columns = ('nombre', 'precio', 'costo', 'mix')
        self.tabla_productos = ttk.Treeview(
            frame_lista, columns=columns, show='headings', height=5)
        
        # Definir encabezados
        self.tabla_productos.heading('nombre', text='Nombre')
        self.tabla_productos.heading('precio', text='Precio Venta')
        self.tabla_productos.heading('costo', text='Costo Variable')
        self.tabla_productos.heading('mix', text='Mix (%)')
        
        # Definir anchos de columna
        self.tabla_productos.column('nombre', width=150)
        self.tabla_productos.column('precio', width=100)
        self.tabla_productos.column('costo', width=100)
        self.tabla_productos.column('mix', width=80)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(
            frame_lista, orient=tk.VERTICAL, command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscroll=scrollbar.set)
        
        # Colocar tabla y scrollbar
        self.tabla_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones de acción sobre productos
        frame_acciones = ttk.Frame(frame_productos)
        frame_acciones.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Botones de acción
        ttk.Button(frame_acciones, text="Eliminar Seleccionado", 
                  command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_acciones, text="Limpiar Lista", 
                  command=self.limpiar_lista).pack(side=tk.LEFT, padx=5)
        
        # Parámetros adicionales
        frame_parametros = ttk.Frame(frame_productos)
        frame_parametros.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(frame_parametros, text="Costos Fijos Totales:").pack(side=tk.LEFT, padx=5)
        self.costos_fijos_var = tk.StringVar()
        ttk.Entry(frame_parametros, textvariable=self.costos_fijos_var, width=15).pack(side=tk.LEFT, padx=5)
        
        # Botón para calcular
        ttk.Button(frame_parametros, text="Calcular Punto de Equilibrio", 
                  command=self.calcular_multiproducto).pack(side=tk.LEFT, padx=30)
        
        # Botón para ver gráfico detallado
        ttk.Button(frame_parametros, text="Ver Gráfico Detallado", 
                  command=self.mostrar_grafico_detallado).pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados de texto completo (sin gráfico en este frame)
        frame_resultados = ttk.LabelFrame(self, text="Resultados Multiproducto")
        frame_resultados.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Área para texto de resultados que ocupa todo el ancho
        self.texto_resultados = tk.Text(frame_resultados, width=80, height=20)
        scrollbar_resultados = ttk.Scrollbar(
            frame_resultados, orient=tk.VERTICAL, command=self.texto_resultados.yview)
        self.texto_resultados.configure(yscroll=scrollbar_resultados.set)
        
        scrollbar_resultados.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def agregar_producto(self):
        """Agrega un nuevo producto a la lista."""
        try:
            # Obtener y validar datos
            nombre = self.nombre_var.get().strip()
            precio = float(self.precio_var.get())
            costo = float(self.costo_var.get())
            mix = float(self.mix_var.get())
            
            # Validaciones
            if not nombre:
                raise ValueError("El nombre del producto no puede estar vacío.")
            
            if precio <= 0:
                raise ValueError("El precio de venta debe ser mayor que cero.")
            
            if costo <= 0:
                raise ValueError("El costo variable debe ser mayor que cero.")
            
            if mix <= 0 or mix > 100:
                raise ValueError("El mix debe estar entre 0 y 100%.")
            
            if precio <= costo:
                raise ValueError("El precio de venta debe ser mayor que el costo variable.")
            
            # Convertir mix a decimal
            mix_decimal = mix / 100
            
            # Verificar que la suma de los mix no exceda 1 (100%)
            suma_mix = sum(producto["mix"] for producto in self.productos) + mix_decimal
            if suma_mix > 1:
                raise ValueError(f"La suma de los porcentajes de mix no puede exceder el 100%. Actual: {suma_mix * 100:.1f}%")
            
            # Crear diccionario con los datos del producto
            producto = {
                "nombre": nombre,
                "precio_venta": precio,
                "costo_variable": costo,
                "mix": mix_decimal
            }
            
            # Agregar a la lista y a la tabla
            self.productos.append(producto)
            self.tabla_productos.insert('', 'end', values=(
                nombre, f"${precio:.2f}", f"${costo:.2f}", f"{mix:.1f}%"))
            
            # Limpiar campos
            self.nombre_var.set("")
            self.precio_var.set("")
            self.costo_var.set("")
            self.mix_var.set("")
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
            return False
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado de la lista."""
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Seleccione un producto para eliminar.")
            return
        
        # Obtener el índice del elemento seleccionado
        indice = self.tabla_productos.index(seleccion[0])
        
        # Eliminar de la lista y de la tabla
        if 0 <= indice < len(self.productos):
            self.productos.pop(indice)
            self.tabla_productos.delete(seleccion[0])
    
    def limpiar_lista(self):
        """Elimina todos los productos de la lista."""
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar todos los productos?"):
            self.productos = []
            for item in self.tabla_productos.get_children():
                self.tabla_productos.delete(item)
    
    def calcular_multiproducto(self):
        """Calcula el punto de equilibrio multiproducto."""
        try:
            # Validar que haya productos
            if not self.productos:
                raise ValueError("Debe agregar al menos un producto.")
            
            # Validar que la suma de los mix sea 1 (100%)
            suma_mix = sum(producto["mix"] for producto in self.productos)
            if abs(suma_mix - 1) > 0.01:  # Permitir un pequeño error de redondeo
                raise ValueError(f"La suma de los porcentajes de mix debe ser 100%. Actual: {suma_mix * 100:.1f}%")
            
            # Obtener costos fijos totales
            try:
                costos_fijos = float(costos_fijos_texto)
            except ValueError:
                raise ValueError("El valor de Costos Fijos Totales debe ser un número válido.")

            if costos_fijos <= 0:
                raise ValueError("Los costos fijos deben ser mayores que cero.")
            
            # Agregar costos fijos a los productos (asumiendo distribución igual)
            productos_con_cf = self.productos.copy()
            for producto in productos_con_cf:
                producto["costos_fijos"] = costos_fijos * producto["mix"]
            
            # Calcular punto de equilibrio
            resultados = calcular_punto_equilibrio_multiproducto(productos_con_cf)
            
            # Guardar resultados para uso posterior
            self.resultados_calculados = resultados
            
            # Mostrar resultados
            self.mostrar_resultados_multiproducto(resultados)
            
            # Mostrar gráfico detallado en una ventana separada
            self.mostrar_grafico_detallado()
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
            return False
    
    def mostrar_resultados_multiproducto(self, resultados):
        """
        Muestra los resultados del análisis multiproducto.
        
        Args:
            resultados (dict): Diccionario con los resultados del análisis
        """
        # Limpiar el área de resultados
        self.texto_resultados.delete(1.0, tk.END)
        
        # Mostrar resultado general
        texto = "PUNTO DE EQUILIBRIO MULTIPRODUCTO\n"
        texto += "=" * 40 + "\n\n"
        texto += f"Punto de Equilibrio Total: {resultados['pe_unidades_total']:.2f} unidades\n"
        texto += f"Valor de Ventas en PE: ${resultados['pe_valor_total']:.2f}\n\n"
        
        # Tabla de resultados por producto
        texto += "DETALLE POR PRODUCTO\n"
        texto += "=" * 40 + "\n\n"
        texto += f"{'Producto':<20} {'PE Unid.':<15} {'PE Valor':<15} {'% del Total':<15}\n"
        texto += "-" * 65 + "\n"
        
        for producto in resultados['productos']:
            nombre = producto['nombre']
            if len(nombre) > 19:
                nombre = nombre[:16] + "..."
            
            unidades = producto['pe_unidades']
            valor = producto['pe_valor']
            porcentaje_valor = (valor / resultados['pe_valor_total']) * 100
            
            texto += f"{nombre:<20} {unidades:<15.2f} ${valor:<14.2f} {porcentaje_valor:<14.2f}%\n"
        
        # Añadir análisis adicional
        texto += "\n\nANÁLISIS ADICIONAL\n"
        texto += "=" * 40 + "\n\n"
        
        # Calcular márgenes de contribución
        texto += "MÁRGENES DE CONTRIBUCIÓN\n"
        texto += "-" * 40 + "\n"
        
        for producto in self.productos:
            nombre = producto['nombre']
            if len(nombre) > 19:
                nombre = nombre[:16] + "..."
            
            margen = producto['precio_venta'] - producto['costo_variable']
            porcentaje = (margen / producto['precio_venta']) * 100
            
            texto += f"{nombre:<20} ${margen:<15.2f} ({porcentaje:<5.2f}% del precio)\n"
        
        # Insertar texto en el widget
        self.texto_resultados.insert(tk.END, texto)
    
    def mostrar_grafico_detallado(self):
        """Muestra el gráfico de resultados en una ventana separada con más detalle."""
        if not self.resultados_calculados:
            messagebox.showinfo(
                "Información", 
                "Primero debe calcular el punto de equilibrio multiproducto."
            )
            return
        
        # Crear una nueva ventana para el gráfico detallado
        ventana_grafico = tk.Toplevel(self.master)
        ventana_grafico.title("Gráfico Detallado - Punto de Equilibrio Multiproducto")
        ventana_grafico.geometry("900x600")
        ventana_grafico.minsize(800, 600)
        
        # Crear frame contenedor
        frame_principal = ttk.Frame(ventana_grafico, padding=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            frame_principal, 
            text="Análisis Gráfico del Punto de Equilibrio Multiproducto",
            font=("Arial", 11, "bold")
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
        resultados = self.resultados_calculados
        
        # Crear figura con dos subplots
        fig = plt.figure(figsize=(12, 8))
        
        # Primer subplot: gráfico de barras de PE por producto
        ax1 = fig.add_subplot(2, 1, 1)
        
        # Preparar datos para el gráfico
        nombres = [p['nombre'] for p in resultados['productos']]
        valores = [p['pe_valor'] for p in resultados['productos']]
        unidades = [p['pe_unidades'] for p in resultados['productos']]
        
        # Acortar nombres muy largos
        nombres = [n[:10] + "..." if len(n) > 10 else n for n in nombres]
        
        # Crear un gráfico de barras para valores
        x = np.arange(len(nombres))
        width = 0.35
        
        ax1.bar(x - width/2, valores, width, label='Valor de Ventas ($)', color='steelblue')
        
        # Crear un segundo eje Y para las unidades
        ax2 = ax1.twinx()
        ax2.bar(x + width/2, unidades, width, color='orange', label='Unidades')
        
        # Configurar etiquetas y leyenda
        ax1.set_title('Punto de Equilibrio por Producto', fontsize=14)
        ax1.set_xlabel('Productos', fontsize=12)
        ax1.set_xticks(x)
        ax1.set_xticklabels(nombres, rotation=45, ha='right')
        ax1.set_ylabel('Valor de Ventas ($)', fontsize=12, color='steelblue')
        ax2.set_ylabel('Unidades', fontsize=12, color='orange')
        
        # Añadir valores encima de las barras
        for i, v in enumerate(valores):
            ax1.text(i - width/2, v + 0.01 * max(valores), f"${v:.0f}", 
                    ha='center', va='bottom', fontsize=9, color='black', fontweight='bold')
        
        for i, u in enumerate(unidades):
            ax2.text(i + width/2, u + 0.01 * max(unidades), f"{u:.1f}", 
                    ha='center', va='bottom', fontsize=9, color='black', fontweight='bold')
        
        # Combinar leyendas
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # Segundo subplot: gráfico de pastel para la distribución del valor total
        ax3 = fig.add_subplot(2, 1, 2)
        
        # Preparar datos para el gráfico de pastel
        etiquetas = [p['nombre'] for p in resultados['productos']]
        valores_pastel = [p['pe_valor'] for p in resultados['productos']]
        
        # Acortar nombres muy largos
        etiquetas = [n[:15] + "..." if len(n) > 15 else n for n in etiquetas]
        
        # Crear colores para cada porción
        colores = plt.cm.viridis(np.linspace(0, 0.9, len(etiquetas)))
        
        # Calcular porcentajes para mostrar en las etiquetas
        total = sum(valores_pastel)
        porcentajes = [100 * v / total for v in valores_pastel]
        
        # Crear etiquetas con porcentajes
        etiquetas_con_pct = [f"{e} ({p:.1f}%)" for e, p in zip(etiquetas, porcentajes)]
        
        # Crear gráfico de pastel
        wedges, texts, autotexts = ax3.pie(
            valores_pastel, 
            labels=etiquetas_con_pct, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colores,
            wedgeprops={'width': 0.5, 'edgecolor': 'w'},
            textprops={'fontsize': 10}
        )
        
        # Configurar título
        ax3.set_title('Distribución del Valor de Ventas en Punto de Equilibrio', fontsize=12)
        
        # Añadir leyenda
        ax3.legend(wedges, etiquetas_con_pct, title="Productos", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        # Ajustar layout
        plt.tight_layout()
        
        # Crear canvas para mostrar la figura
        canvas = FigureCanvasTkAgg(fig, frame_contenedor)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Añadir barra de herramientas de navegación
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, frame_contenedor)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)