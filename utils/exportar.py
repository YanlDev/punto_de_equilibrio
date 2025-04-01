import os
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import pandas as pd
import tempfile
from io import BytesIO


def exportar_a_pdf(modelo, ruta_archivo=None, incluir_graficos=True):
    """
    Exporta los resultados del análisis a un archivo PDF.
    
    Args:
        modelo (dict): Diccionario con los datos del modelo
        ruta_archivo (str, optional): Ruta donde guardar el archivo. Si es None,
                                     se guarda en el directorio actual con un nombre por defecto.
        incluir_graficos (bool, optional): Si se incluyen gráficos en el PDF. Default es True.
        
    Returns:
        str: Ruta del archivo generado
    """
    # Definir ruta si no se proporciona
    if ruta_archivo is None:
        fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_archivo = f"punto_equilibrio_{fecha_hora}.pdf"
    
    # Crear el documento
    doc = SimpleDocTemplate(
        ruta_archivo,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Contenedor para los elementos del documento
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    estilo_subtitulo = estilos['Heading2']
    estilo_normal = estilos['Normal']
    
    # Crear estilo para párrafos centrados
    estilo_centrado = ParagraphStyle(
        'Centrado',
        parent=estilos['Normal'],
        alignment=1  # 0=izquierda, 1=centro, 2=derecha
    )
    
    # Título y fecha
    elementos.append(Paragraph("Informe de Análisis de Punto de Equilibrio", estilo_titulo))
    elementos.append(Spacer(1, 0.25 * inch))
    
    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(Paragraph(f"Generado el: {fecha_actual}", estilo_centrado))
    elementos.append(Spacer(1, 0.5 * inch))
    
    # Sección: Parámetros del Análisis
    elementos.append(Paragraph("1. Parámetros del Análisis", estilo_subtitulo))
    elementos.append(Spacer(1, 0.1 * inch))
    
    # Crear tabla con los parámetros
    datos_parametros = [
        ["Parámetro", "Valor"],
        ["Costos Fijos", f"${modelo['costos_fijos']:.2f}"],
        ["Precio de Venta Unitario", f"${modelo['precio_venta']:.2f}"],
        ["Costo Variable Unitario", f"${modelo['costo_variable']:.2f}"],
        ["Margen de Contribución", f"${modelo['precio_venta'] - modelo['costo_variable']:.2f}"]
    ]
    
    # Agregar unidades esperadas si existe
    if modelo.get('unidades_esperadas', 0) > 0:
        datos_parametros.append(["Unidades Esperadas", f"{modelo['unidades_esperadas']:.2f}"])
    
    tabla_parametros = Table(datos_parametros, colWidths=[2.5*inch, 2*inch])
    tabla_parametros.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elementos.append(tabla_parametros)
    elementos.append(Spacer(1, 0.3 * inch))
    
    # Sección: Resultados del Análisis
    if modelo["resultados"]:
        elementos.append(Paragraph("2. Resultados del Análisis", estilo_subtitulo))
        elementos.append(Spacer(1, 0.1 * inch))
        
        resultados = modelo["resultados"]
        margen = resultados["margen_seguridad"]
        
        # Crear tabla con los resultados
        datos_resultados = [
            ["Medida", "Valor"],
            ["Punto de Equilibrio (Unidades)", f"{resultados['pe_unidades']:.2f}"],
            ["Punto de Equilibrio (Valor)", f"${resultados['pe_valor']:.2f}"],
            ["Ratio de Margen de Contribución", f"{resultados['ratio_mc'] * 100:.2f}%"]
        ]
        
        # Agregar margen de seguridad si hay unidades esperadas
        if modelo.get('unidades_esperadas', 0) > 0 and modelo['unidades_esperadas'] > resultados['pe_unidades']:
            datos_resultados.extend([
                ["Margen de Seguridad (Unidades)", f"{margen['unidades']:.2f}"],
                ["Margen de Seguridad (Valor)", f"${margen['valor']:.2f}"],
                ["Margen de Seguridad (%)", f"{margen['porcentaje']:.2f}%"],
                ["Utilidad Estimada", f"${resultados['utilidad_estimada']:.2f}"],
                ["Grado de Apalancamiento Operativo", f"{resultados['gao']:.2f}"]
            ])
        
        tabla_resultados = Table(datos_resultados, colWidths=[2.5*inch, 2*inch])
        tabla_resultados.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elementos.append(tabla_resultados)
        elementos.append(Spacer(1, 0.3 * inch))
    
    # Sección: Gráficos
    if incluir_graficos and modelo["datos_grafico"] is not None:
        elementos.append(Paragraph("3. Representación Gráfica", estilo_subtitulo))
        elementos.append(Spacer(1, 0.1 * inch))
        
        # Crear gráfico de punto de equilibrio
        fig, ax = plt.subplots(figsize=(8, 5))
        
        datos = modelo["datos_grafico"]
        pe_unidades = modelo["resultados"]["pe_unidades"]
        pe_valor = modelo["resultados"]["pe_valor"]
        
        # Graficar costos totales e ingresos
        ax.plot(datos['unidades'], datos['costos_totales'], 
                label='Costos Totales', color='red')
        ax.plot(datos['unidades'], datos['ingresos'], 
                label='Ingresos', color='blue')
        
        # Marcar el punto de equilibrio
        ax.plot([pe_unidades], [pe_valor], 'ro', markersize=8)
        
        # Líneas punteadas para el punto de equilibrio
        ax.axvline(x=pe_unidades, color='gray', linestyle=':', alpha=0.7)
        ax.axhline(y=pe_valor, color='gray', linestyle=':', alpha=0.7)
        
        # Configurar ejes y leyenda
        ax.set_xlabel('Unidades')
        ax.set_ylabel('Valor ($)')
        ax.set_title('Análisis de Punto de Equilibrio')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        
        # Guardar gráfico en memoria en lugar de en un archivo
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        # Devolver el puntero al inicio del buffer
        buffer.seek(0)
        
        # Usar directamente el buffer como fuente de imagen
        elementos.append(Image(buffer, width=6*inch, height=4*inch))
        elementos.append(Spacer(1, 0.2 * inch))
        
        # Añadir leyenda del gráfico
        elementos.append(Paragraph(
            f"El punto de equilibrio se encuentra en {pe_unidades:.2f} unidades, "
            f"con un valor de ventas de ${pe_valor:.2f}.",
            estilo_normal
        ))
    
    # Añadir interpretación
    elementos.append(Spacer(1, 0.3 * inch))
    elementos.append(Paragraph("4. Interpretación de Resultados", estilo_subtitulo))
    elementos.append(Spacer(1, 0.1 * inch))
    
    if modelo["resultados"]:
        resultados = modelo["resultados"]
        pe_unidades = resultados["pe_unidades"]
        pe_valor = resultados["pe_valor"]
        ratio_mc = resultados["ratio_mc"]
        
        interpretacion = (
            f"Con un costo fijo de ${modelo['costos_fijos']:.2f}, un precio de venta de "
            f"${modelo['precio_venta']:.2f} y un costo variable unitario de "
            f"${modelo['costo_variable']:.2f}, el punto de equilibrio se alcanza al "
            f"vender {pe_unidades:.2f} unidades, lo que representa un valor de ventas "
            f"de ${pe_valor:.2f}.\n\n"
            
            f"El ratio de margen de contribución es {ratio_mc * 100:.2f}%, lo que significa "
            f"que por cada peso de ventas, {ratio_mc * 100:.2f} centavos contribuyen a cubrir "
            f"los costos fijos y generar utilidades."
        )
        
        elementos.append(Paragraph(interpretacion, estilo_normal))
        
        # Añadir interpretación del margen de seguridad si corresponde
        if modelo.get('unidades_esperadas', 0) > 0:
            elementos.append(Spacer(1, 0.2 * inch))
            
            unidades_esperadas = modelo['unidades_esperadas']
            margen = resultados["margen_seguridad"]
            
            if unidades_esperadas > pe_unidades:
                interpretacion_margen = (
                    f"Con una proyección de ventas de {unidades_esperadas:.2f} unidades, "
                    f"existe un margen de seguridad de {margen['unidades']:.2f} unidades "
                    f"({margen['porcentaje']:.2f}%), lo que indica que las ventas pueden "
                    f"caer hasta en un {margen['porcentaje']:.2f}% antes de incurrir en pérdidas."
                )
            else:
                interpretacion_margen = (
                    f"La proyección de ventas ({unidades_esperadas:.2f} unidades) es menor "
                    f"que el punto de equilibrio ({pe_unidades:.2f} unidades), lo que indica "
                    f"que con este nivel de ventas se incurrirá en pérdidas."
                )
            
            elementos.append(Paragraph(interpretacion_margen, estilo_normal))
    
    # Añadir pie de página
    elementos.append(Spacer(1, inch))
    elementos.append(Paragraph(
        "Este informe fue generado automáticamente por la aplicación 'Analizador de Punto de Equilibrio'.",
        estilo_centrado
    ))
    
    # Generar el PDF
    doc.build(elementos)
    
    return ruta_archivo


def exportar_a_excel(modelo, ruta_archivo=None):
    """
    Exporta los resultados del análisis a un archivo Excel.
    
    Args:
        modelo (dict): Diccionario con los datos del modelo
        ruta_archivo (str, optional): Ruta donde guardar el archivo. Si es None,
                                     se guarda en el directorio actual con un nombre por defecto.
        
    Returns:
        str: Ruta del archivo generado
    """
    # Definir ruta si no se proporciona
    if ruta_archivo is None:
        fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_archivo = f"punto_equilibrio_{fecha_hora}.xlsx"
    
    # Crear un escritor de Excel con pandas
    with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
        # Hoja 1: Parámetros
        df_parametros = pd.DataFrame({
            'Parámetro': [
                'Costos Fijos',
                'Precio de Venta Unitario',
                'Costo Variable Unitario',
                'Margen de Contribución',
                'Unidades Esperadas'
            ],
            'Valor': [
                modelo['costos_fijos'],
                modelo['precio_venta'],
                modelo['costo_variable'],
                modelo['precio_venta'] - modelo['costo_variable'],
                modelo.get('unidades_esperadas', 0)
            ]
        })
        
        df_parametros.to_excel(writer, sheet_name='Parámetros', index=False)
        
        # Hoja 2: Resultados
        if modelo["resultados"]:
            resultados = modelo["resultados"]
            margen = resultados["margen_seguridad"]
            
            df_resultados = pd.DataFrame({
                'Medida': [
                    'Punto de Equilibrio (Unidades)',
                    'Punto de Equilibrio (Valor)',
                    'Ratio de Margen de Contribución',
                    'Margen de Seguridad (Unidades)',
                    'Margen de Seguridad (Valor)',
                    'Margen de Seguridad (%)',
                    'Utilidad Estimada',
                    'Grado de Apalancamiento Operativo'
                ],
                'Valor': [
                    resultados['pe_unidades'],
                    resultados['pe_valor'],
                    resultados['ratio_mc'],
                    margen['unidades'],
                    margen['valor'],
                    margen['porcentaje'] / 100,  # Convertir a decimal para formato porcentaje
                    resultados['utilidad_estimada'],
                    resultados['gao']
                ]
            })
            
            df_resultados.to_excel(writer, sheet_name='Resultados', index=False)
        
        # Hoja 3: Datos para gráfico
        if modelo["datos_grafico"] is not None:
            # Tomar una muestra de los datos para no sobrecargar el archivo
            datos_muestra = modelo["datos_grafico"].iloc[::5].copy()  # Cada 5 filas
            
            # Añadir columna de utilidad
            datos_muestra['utilidad'] = datos_muestra['ingresos'] - datos_muestra['costos_totales']
            
            datos_muestra.to_excel(writer, sheet_name='Datos_Gráfico', index=False)
        
        # Hoja 4: Análisis de sensibilidad (si existe)
        if modelo.get("analisis_sensibilidad") is not None:
            df_sensibilidad = pd.DataFrame(modelo["analisis_sensibilidad"])
            df_sensibilidad.to_excel(writer, sheet_name='Sensibilidad', index=False)
    
    return ruta_archivo