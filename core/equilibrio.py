"""
Módulo para el cálculo del punto de equilibrio y análisis relacionados.

Este módulo proporciona funciones para calcular el punto de equilibrio en unidades y en
valor monetario, así como otros indicadores relacionados con el análisis de costos,
volumen y utilidad (CVP).
"""

import numpy as np
import pandas as pd


class AnalizadorEquilibrio:
    """
    Clase para realizar análisis de punto de equilibrio.
    """
    
    def __init__(self, costos_fijos, precio_venta, costo_variable_unitario):
        """
        Inicializa el analizador con los parámetros básicos.
        
        Args:
            costos_fijos (float): Total de costos fijos
            precio_venta (float): Precio de venta unitario
            costo_variable_unitario (float): Costo variable por unidad
        """
        self.costos_fijos = costos_fijos
        self.precio_venta = precio_venta
        self.costo_variable_unitario = costo_variable_unitario
        self.margen_contribucion = self.precio_venta - self.costo_variable_unitario
        
        # Validar que el margen de contribución no sea cero o negativo
        if self.margen_contribucion <= 0:
            raise ValueError("El margen de contribución debe ser positivo. "
                            "El precio de venta debe ser mayor que el costo variable unitario.")
    
    def punto_equilibrio_unidades(self):
        """
        Calcula el punto de equilibrio en unidades.
        
        Returns:
            float: Cantidad de unidades en el punto de equilibrio
        """
        return self.costos_fijos / self.margen_contribucion
    
    def punto_equilibrio_valor(self):
        """
        Calcula el punto de equilibrio en valor monetario.
        
        Returns:
            float: Valor monetario de ventas en el punto de equilibrio
        """
        return self.punto_equilibrio_unidades() * self.precio_venta
    
    def ratio_margen_contribucion(self):
        """
        Calcula el ratio de margen de contribución.
        
        Returns:
            float: Ratio del margen de contribución (entre 0 y 1)
        """
        return self.margen_contribucion / self.precio_venta
    
    def margen_seguridad(self, ventas_esperadas):
        """
        Calcula el margen de seguridad basado en las ventas esperadas.
        
        Args:
            ventas_esperadas (float): Ventas esperadas en unidades
            
        Returns:
            dict: Diccionario con el margen de seguridad en unidades, valor y porcentaje
        """
        pe_unidades = self.punto_equilibrio_unidades()
        
        # Validar que las ventas esperadas no sean menores al punto de equilibrio
        if ventas_esperadas < pe_unidades:
            raise ValueError("Las ventas esperadas son menores al punto de equilibrio, "
                            "lo que resultaría en un margen de seguridad negativo.")
        
        margen_unidades = ventas_esperadas - pe_unidades
        margen_valor = margen_unidades * self.precio_venta
        margen_porcentaje = (margen_unidades / ventas_esperadas) * 100
        
        return {
            "unidades": margen_unidades,
            "valor": margen_valor,
            "porcentaje": margen_porcentaje
        }
    
    def utilidad_estimada(self, unidades_vendidas):
        """
        Calcula la utilidad estimada para un determinado nivel de ventas.
        
        Args:
            unidades_vendidas (float): Cantidad de unidades vendidas
            
        Returns:
            float: Utilidad estimada
        """
        ingresos = unidades_vendidas * self.precio_venta
        costos_variables_totales = unidades_vendidas * self.costo_variable_unitario
        utilidad = ingresos - costos_variables_totales - self.costos_fijos
        
        return utilidad
    
    def grado_apalancamiento_operativo(self, unidades_vendidas):
        """
        Calcula el grado de apalancamiento operativo.
        
        Args:
            unidades_vendidas (float): Cantidad de unidades vendidas
            
        Returns:
            float: Grado de apalancamiento operativo
        """
        # Validar que las unidades vendidas no sean iguales al punto de equilibrio
        pe_unidades = self.punto_equilibrio_unidades()
        if unidades_vendidas == pe_unidades:
            raise ValueError("El grado de apalancamiento operativo no está definido en el punto de equilibrio.")
        
        margen_contribucion_total = unidades_vendidas * self.margen_contribucion
        utilidad = margen_contribucion_total - self.costos_fijos
        
        # Fórmula para el grado de apalancamiento operativo (GAO)
        gao = margen_contribucion_total / utilidad
        
        return gao
    
    def generar_datos_grafico(self, unidades_min=0, unidades_max=None):
        """
        Genera los datos para graficar el punto de equilibrio.
        
        Args:
            unidades_min (float, optional): Unidades mínimas para el gráfico. Default es 0.
            unidades_max (float, optional): Unidades máximas para el gráfico. 
                Si es None, se calcula automáticamente como 2 veces el punto de equilibrio.
                
        Returns:
            pandas.DataFrame: DataFrame con los datos para graficar
        """
        pe_unidades = self.punto_equilibrio_unidades()
        
        if unidades_max is None:
            unidades_max = pe_unidades * 2
        
        # Crear un rango de unidades
        unidades = np.linspace(unidades_min, unidades_max, 100)
        
        # Calcular costos e ingresos para cada punto
        costos_fijos = np.full_like(unidades, self.costos_fijos)
        costos_variables = unidades * self.costo_variable_unitario
        costos_totales = costos_fijos + costos_variables
        ingresos = unidades * self.precio_venta
        utilidades = ingresos - costos_totales
        
        # Crear DataFrame con los resultados
        datos = pd.DataFrame({
            'unidades': unidades,
            'costos_fijos': costos_fijos,
            'costos_variables': costos_variables,
            'costos_totales': costos_totales,
            'ingresos': ingresos,
            'utilidades': utilidades
        })
        
        return datos
    
    def calcular_unidades_para_utilidad_objetivo(self, utilidad_objetivo):
        """
        Calcula las unidades que deben venderse para alcanzar una utilidad objetivo.
        
        Args:
            utilidad_objetivo (float): Utilidad objetivo deseada
            
        Returns:
            float: Unidades necesarias para alcanzar la utilidad objetivo
        """
        return (self.costos_fijos + utilidad_objetivo) / self.margen_contribucion


# Funciones de utilidad para análisis adicionales

def calcular_punto_equilibrio_multiproducto(productos):
    """
    Calcula el punto de equilibrio para múltiples productos.
    
    Args:
        productos (list): Lista de diccionarios con la información de cada producto
            Cada diccionario debe contener:
            - 'nombre': Nombre del producto
            - 'precio_venta': Precio de venta unitario
            - 'costo_variable': Costo variable unitario
            - 'mix': Porcentaje del mix de ventas (en decimal, debe sumar 1)
            
    Returns:
        dict: Diccionario con los resultados del análisis
    """
    # Validar que la suma de porcentajes del mix sea 1
    suma_mix = sum(producto['mix'] for producto in productos)
    if abs(suma_mix - 1) > 0.0001:  # Permitir un pequeño error de redondeo
        raise ValueError("La suma de los porcentajes del mix debe ser 1.")
    
    # Calcular el margen de contribución ponderado
    margen_ponderado = 0
    for producto in productos:
        margen_unitario = producto['precio_venta'] - producto['costo_variable']
        margen_ponderado += margen_unitario * producto['mix']
    
    # Calcular el punto de equilibrio en unidades totales
    costos_fijos_totales = sum(producto.get('costos_fijos', 0) for producto in productos)
    
    if margen_ponderado <= 0:
        raise ValueError("El margen de contribución ponderado debe ser positivo.")
    
    pe_unidades_total = costos_fijos_totales / margen_ponderado
    
    # Calcular el punto de equilibrio para cada producto
    resultados = {
        'pe_unidades_total': pe_unidades_total,
        'productos': []
    }
    
    valor_total = 0
    for producto in productos:
        pe_producto = pe_unidades_total * producto['mix']
        valor_producto = pe_producto * producto['precio_venta']
        valor_total += valor_producto
        
        resultados['productos'].append({
            'nombre': producto['nombre'],
            'pe_unidades': pe_producto,
            'pe_valor': valor_producto
        })
    
    resultados['pe_valor_total'] = valor_total
    
    return resultados