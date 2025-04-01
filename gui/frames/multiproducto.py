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
        
        # Frame para resultados y gráficos
        frame_resultados = ttk.LabelFrame(self, text="Resultados Multiproducto")
        frame_resultados.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Dividir en dos áreas: tabla de resultados y gráfico
        frame_resultados.columnconfigure(0, weight=4)
        frame_resultados.columnconfigure(1, weight=6)
        frame_resultados.rowconfigure(0, weight=1)
        
        # Área para tabla de resultados
        frame_tabla_resultados = ttk.Frame(frame_resultados)
        frame_tabla_resultados.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Crear tabla para mostrar resultados
        self.texto_resultados = tk.Text(frame_tabla_resultados, width=40, height=20)
        scrollbar_resultados = ttk.Scrollbar(
            frame_tabla_resultados, orient=tk.VERTICAL, command=self.texto_resultados.yview)
        self.texto_resultados.configure(yscroll=scrollbar_resultados.set)
        
        self.texto_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_resultados.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área para gráfico
        frame_grafico = ttk.Frame(frame_resultados)
        frame_grafico.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Inicializar el gráfico
        self.figure, self.ax = plt.subplots(figsize=(6, 5), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.figure, frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Mostrar mensaje inicial en el gráfico
        self.ax.text(
            0.5, 0.5, 
            "Agregue productos y calcule el\npunto de equilibrio multiproducto", 
            ha='center', va='center', 
            fontsize=12
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
    
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
            costos_fijos = float(self.costos_fijos_var.get())
            if costos_fijos <= 0:
                raise ValueError("Los costos fijos deben ser mayores que cero.")
            
            # Agregar costos fijos a los productos (asumiendo distribución igual)
            productos_con_cf = self.productos.copy()
            for producto in productos_con_cf:
                producto["costos_fijos"] = costos_fijos * producto["mix"]
            
            # Calcular punto de equilibrio
            resultados = calcular_punto_equilibrio_multiproducto(productos_con_cf)
            
            # Mostrar resultados
            self.mostrar_resultados_multiproducto(resultados)
            
            # Graficar resultados
            self.graficar_resultados_multiproducto(resultados)
            
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
        texto += f"{'Producto':<15} {'PE Unid.':<10} {'PE Valor':<15}\n"
        texto += "-" * 40 + "\n"
        
        for producto in resultados['productos']:
            nombre = producto['nombre']
            if len(nombre) > 14:
                nombre = nombre[:11] + "..."
            
            texto += f"{nombre:<15} {producto['pe_unidades']:<10.2f} ${producto['pe_valor']:<14.2f}\n"
        
        # Insertar texto en el widget
        self.texto_resultados.insert(tk.END, texto)
    
    def graficar_resultados_multiproducto(self, resultados):
        """
        Genera gráficos para visualizar los resultados del análisis multiproducto.
        
        Args:
            resultados (dict): Diccionario con los resultados del análisis
        """
        # Limpiar el gráfico anterior
        self.ax.clear()
        
        # Preparar datos para el gráfico
        nombres = [p['nombre'] for p in resultados['productos']]
        valores = [p['pe_valor'] for p in resultados['productos']]
        unidades = [p['pe_unidades'] for p in resultados['productos']]
        
        # Acortar nombres muy largos
        nombres = [n[:10] + "..." if len(n) > 10 else n for n in nombres]
        
        # Crear un gráfico de barras para valores
        x = np.arange(len(nombres))
        width = 0.35
        
        self.ax.bar(x - width/2, valores, width, label='Valor de Ventas ($)')
        
        # Crear un segundo eje Y para las unidades
        ax2 = self.ax.twinx()
        ax2.bar(x + width/2, unidades, width, color='orange', label='Unidades')
        
        # Configurar etiquetas y leyenda
        self.ax.set_title('Punto de Equilibrio por Producto')
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(nombres, rotation=45, ha='right')
        self.ax.set_ylabel('Valor de Ventas ($)')
        ax2.set_ylabel('Unidades')
        
        # Combinar leyendas
        lines1, labels1 = self.ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        self.ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # Ajustar diseño
        plt.tight_layout()
        
        # Actualizar el canvas
        self.canvas.draw()