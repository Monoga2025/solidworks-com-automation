import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D"))
        
        # Header on pages 2 and later
        if self._pageNumber > 1:
            self.drawString(54, 750, "MANUAL MAESTRO DE MODELADO SOLIDWORKS: ENGRANAJES HELICOIDALES")
            self.drawRightString(558, 750, "GUÍA ATÓMICA Y EJERCICIO PRÁCTICO REAL")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.75)
            self.line(54, 742, 558, 742)
            
        # Footer on all pages
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        self.drawString(54, 32, "Procedimiento Exacto del Profesor — Secuencia de 44 Fotogramas + Cuaderno de Trabajo")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 32, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 44, 558, 44)
        
        self.restoreState()

def build_pdf():
    pdf_filename = "Manual_Maestro_Engranajes_Helicoidales_SolidWorks.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1A365D")   # Deep navy
    secondary_color = colors.HexColor("#2B6CB0") # Medium blue
    accent_color = colors.HexColor("#D69E2E")    # Warm gold/amber
    dark_neutral = colors.HexColor("#1A202C")    # Dark charcoal for maximum legibility
    light_bg = colors.HexColor("#F7FAFC")        # Card background
    border_color = colors.HexColor("#CBD5E0")
    highlight_bg = colors.HexColor("#EDF2F7")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=dark_neutral,
        spaceAfter=6
    )

    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12,
        textColor=colors.white
    )
    
    step_num_style = ParagraphStyle(
        'StepNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=primary_color
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#2C5282")
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#742A2A")
    )
    
    story = []
    
    # ---------------------------------------------------------
    # COVER / HEADER BLOCK
    # ---------------------------------------------------------
    story.append(Paragraph("MANUAL MAESTRO ATÓMICO: MODELADO 3D Y ENSAMBLAJE DE ENGRANAJES HELICOIDALES EN SOLIDWORKS", title_style))
    story.append(Paragraph("<b>Guía de Ejecución Recetario Paso a Paso (44 Fotogramas) + Ejercicio Práctico Real de Autoevaluación</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceBefore=0, spaceAfter=10))
    
    meta_data = [
        [Paragraph("<b>Propósito:</b> Permitir el modelado autónomo leyendo el PDF sin consultar el video.", body_style),
         Paragraph("<b>Metodología:</b> Instrucciones atómicas + Secuencia de 44 Fotogramas", body_style)],
        [Paragraph("<b>Incluye:</b> Ejercicio práctico real con solucionario para autoevaluación.", body_style),
         Paragraph("<b>Software:</b> SolidWorks (Ecuaciones + Operaciones Avanzadas)", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), highlight_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    # ---------------------------------------------------------
    # SECCIÓN 1: FORMULACIÓN Y TABLA DE ECUACIONES
    # ---------------------------------------------------------
    story.append(Paragraph("1. Tabla de Ecuaciones y Variables Globales en SolidWorks", h1_style))
    story.append(Paragraph(
        "Antes de trazar cualquier elemento en SolidWorks, debes abrir la ventana de <b>Ecuaciones</b> "
        "(Menú <code>Herramientas</code> &gt; <code>Ecuaciones...</code> o clic derecho en la carpeta <i>Ecuaciones</i> en el árbol FeatureManager). "
        "Ingresa la siguiente tabla de variables entre comillas exactas:",
        body_style
    ))
    
    eq_table_data = [
        [Paragraph("<b>Variable Global</b>", header_cell_style), Paragraph("<b>Sintaxis Exacta SolidWorks</b>", header_cell_style), Paragraph("<b>Fórmula / Expresión</b>", header_cell_style), Paragraph("<b>Descripción Técnica</b>", header_cell_style)],
        [Paragraph("Módulo", body_style), Paragraph("<code>\"M\"</code>", code_style), Paragraph("<code>5</code> (mm)", body_style), Paragraph("Tamaño del diente", body_style)],
        [Paragraph("Número de Dientes", body_style), Paragraph("<code>\"N\"</code>", code_style), Paragraph("<code>25</code> (o <code>33</code>)", body_style), Paragraph("Cantidad de dientes", body_style)],
        [Paragraph("Ángulo de Hélice", body_style), Paragraph("<code>\"beta\"</code>", code_style), Paragraph("<code>30</code> (deg)", body_style), Paragraph("Inclinación helicoidal", body_style)],
        [Paragraph("Diámetro Primitivo", body_style), Paragraph("<code>\"DP\"</code>", code_style), Paragraph("<code>= \"M\" * \"N\"</code>", code_style), Paragraph("Línea neutra de engrane", body_style)],
        [Paragraph("Diámetro Exterior", body_style), Paragraph("<code>\"DE\"</code>", code_style), Paragraph("<code>= \"DP\" + 2 * \"M\"</code>", code_style), Paragraph("Cresta del engranaje", body_style)],
        [Paragraph("Diámetro Interior", body_style), Paragraph("<code>\"DI\"</code>", code_style), Paragraph("<code>= \"DP\" - 2.5 * \"M\"</code>", code_style), Paragraph("Pie / Raíz del diente", body_style)],
        [Paragraph("Círculo de Trazo", body_style), Paragraph("<code>\"CT\"</code>", code_style), Paragraph("<code>= \"DP\" * cos(20 deg)</code>", code_style), Paragraph("Base de arcos de perfil", body_style)],
        [Paragraph("Paso Circular", body_style), Paragraph("<code>\"P\"</code>", code_style), Paragraph("<code>= pi * \"M\"</code>", code_style), Paragraph("Paso transversal", body_style)],
        [Paragraph("Radio 1 (N < 30)", body_style), Paragraph("<code>\"R1\"</code>", code_style), Paragraph("Valor según tabla Excel", body_style), Paragraph("Primer arco de raíz", body_style)],
        [Paragraph("Radio 2 (N < 30)", body_style), Paragraph("<code>\"R2\"</code>", code_style), Paragraph("Valor según tabla Excel", body_style), Paragraph("Segundo arco medio", body_style)],
        [Paragraph("Radio 3 (N < 30)", body_style), Paragraph("<code>\"R3\"</code>", code_style), Paragraph("Valor según tabla Excel", body_style), Paragraph("Tercer arco cresta", body_style)],
        [Paragraph("Radio Único (N ≥ 30)", body_style), Paragraph("<code>\"R1\"</code> (Ver Gotcha)", code_style), Paragraph("Valor según tabla Excel", body_style), Paragraph("Arco único (N ≥ 30)", body_style)],
        [Paragraph("Redondeo Raíz", body_style), Paragraph("<code>\"r\"</code> (minúscula)", code_style), Paragraph("<code>= 0.3 * \"M\"</code>", code_style), Paragraph("Empalme de pie", body_style)],
        [Paragraph("Ancho de Cara", body_style), Paragraph("<code>\"A\"</code>", code_style), Paragraph("<code>40</code> (mm)", body_style), Paragraph("Espesor de extrusión", body_style)],
        [Paragraph("Chaflán", body_style), Paragraph("<code>\"Ch\"</code>", code_style), Paragraph("<code>= 0.5 * \"M\"</code>", code_style), Paragraph("Bisel exterior", body_style)]
    ]
    
    t_eq = Table(eq_table_data, colWidths=[90, 110, 154, 150])
    t_eq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('BACKGROUND', (0,1), (-1,-1), light_bg),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_eq)
    story.append(Spacer(1, 8))

    imgs_s01 = [
        [Image("pdf_frames_dense/s01_menu_ecuaciones.png", width=240, height=135), Image("pdf_frames_audit/excel_formulas_2755.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 01:</b> Menú de administración de Ecuaciones en SolidWorks.", body_style),
         Paragraph("<b>Fotograma 02:</b> Tabla de fórmulas Excel del profesor para R1, R2, R3.", body_style)]
    ]
    t_s01 = Table(imgs_s01, colWidths=[248, 248])
    t_s01.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 3)]))
    story.append(t_s01)
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECCIÓN 2: GUÍA ATÓMICA DE MODELADO (N < 30 DIENTES, N = 25)
    # ---------------------------------------------------------
    story.append(Paragraph("2. Guía Atómica Paso a Paso: Modelado de Engranaje 1 (N < 30 Dientes, N = 25)", h1_style))
    story.append(Paragraph(
        "Sigue en orden estricto cada una de las siguientes instrucciones numeradas para completar la pieza en SolidWorks:",
        body_style
    ))
    
    steps_p1 = [
        ("Paso 1", "Crear nuevo documento: Clic en <b>Nuevo</b> &gt; <b>Pieza</b> &gt; <b>Aceptar</b>."),
        ("Paso 2", "En el árbol de diseño (FeatureManager), haz clic en <b>Plano Alzado</b> y presiona el icono <b>Croquis</b>."),
        ("Paso 3", "En la pestaña Croquis, haz clic en <b>Círculo</b> (Círculo de centro). Haz clic en el origen <code>(0,0)</code>, abre el círculo y haz clic para fijarlo."),
        ("Paso 4", "Haz clic en <b>Cota Inteligente</b>. Selecciona la circunferencia. En el cuadro emergente, borra el número, escribe <code>=</code> y selecciona la Variable Global <code>\"d\"</code> (diámetro del eje). Presiona la tilde verde."),
        ("Paso 5", "Dibuja el chavetero: Clic en <b>Rectángulo</b> desde el centro superior del círculo (o líneas). Acota el ancho a 1\" y la altura a 1/2\"."),
        ("Paso 6", "Clic en <b>Recortar Entidades</b> (Recorte inteligente). Arrastra el cursor sobre la línea del círculo dentro del chavetero para abrir la geometría."),
        ("Paso 7", "Sal del croquis. Ve a la pestaña <b>Operaciones</b> &gt; haz clic en <b>Extruir Saliente/Base</b>."),
        ("Paso 8", "En `Dirección 1`, cambia la condición final a <b>Plano Medio</b>. En el cuadro de profundidad, borra el valor, escribe <code>=</code> y selecciona <code>\"ancho de cara\"</code>. Haz clic en <b>Aceptar</b>."),
        ("Paso 9", "Clic en <b>Chaflán</b> (desplegable de Redondeo). Selecciona las 2 aristas circulares externas (frontal y posterior). Escribe <code>= \"chaflan\"</code> y acepta.")
    ]
    
    t_steps1_data = []
    for num, desc in steps_p1:
        t_steps1_data.append([Paragraph(f"<b>{num}</b>", step_num_style), Paragraph(desc, body_style)])
    
    t_steps1 = Table(t_steps1_data, colWidths=[54, 450])
    t_steps1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, border_color)
    ]))
    story.append(t_steps1)
    story.append(Spacer(1, 8))

    imgs_p1_1 = [
        [Image("pdf_frames_dense/s02_circulo_base_origen.png", width=160, height=90),
         Image("pdf_frames_dense/s04_rectangulo_chavetero.png", width=160, height=90),
         Image("pdf_frames_dense/s06_extrusion_plano_medio.png", width=160, height=90)],
        [Paragraph("<b>Pasos 3-4:</b> Círculo base acotado con variable d.", body_style),
         Paragraph("<b>Pasos 5-6:</b> Chavetero recortado.", body_style),
         Paragraph("<b>Pasos 7-8:</b> Extrusión Plano Medio.", body_style)]
    ]
    t_imgs_p1_1 = Table(imgs_p1_1, colWidths=[166, 166, 166])
    t_imgs_p1_1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 2)]))
    story.append(t_imgs_p1_1)
    story.append(Spacer(1, 10))

    # Pasos 10 a 21: Croquis de 4 círculos y trazado del diente
    steps_p1_2 = [
        ("Paso 10", "Haz clic en la cara frontal plana del cilindro y presiona el icono <b>Croquis</b>."),
        ("Paso 11", "Trazar 4 círculos concéntricos desde el origen."),
        ("Paso 12", "Selecciona el segundo círculo (DP). En el PropertyManager a la izquierda, marca la casilla <b>Geometría de Construcción</b>."),
        ("Paso 13", "Acotar los 4 círculos con <b>Cota Inteligente</b> escribiendo las etiquetas exactas antes del valor:<br/>"
                   "• Círculo 1 (Exterior): En PropertyManager escribir <code>DE = </code> &gt; valor <code>= \"DE\"</code>.<br/>"
                   "• Círculo 2 (Constructivo): En PropertyManager escribir <code>DP = </code> &gt; valor <code>= \"DP\"</code>.<br/>"
                   "• Círculo 3 (Trazo): En PropertyManager escribir <code>CT = </code> &gt; valor <code>= \"CT\"</code>.<br/>"
                   "• Círculo 4 (Interior): En PropertyManager escribir <code>DI = </code> &gt; valor <code>= \"DI\"</code>."),
        ("Paso 14", "Trazar línea constructiva vertical desde el origen hacia arriba. Trazar segunda línea constructiva inclinada hacia la derecha. Acotar el ángulo entre ambas como <code>= 90 / \"N\"</code> (Ángulo Delta)."),
        ("Paso 15", "Clic en <b>Línea Constructiva</b>. Haz clic en la intersección entre la línea delta y el círculo <code>DI</code>. Arrastra la línea hasta tocar el círculo <code>CT</code>. Acota la longitud pura de la línea oblicua como <code>= \"R1\"</code>."),
        ("Paso 16", "Clic en <b>Arco Centro-Extremos</b>. Haz centro en el extremo final de R1 sobre <code>CT</code>. Abre el arco pasando por el punto inicial sobre <code>DI</code> hasta <code>CT</code>. Usa <i>Recortar Entidades</i> para dejar SOLO el tramo entre <code>DI</code> y <code>CT</code>."),
        ("Paso 17", "Desde el extremo superior de este arco sobre <code>CT</code>, traza una nueva línea constructiva hasta <code>CT</code> de longitud <code>= \"R2\"</code>. Dibuja el arco recortando el tramo entre <code>CT</code> y <code>DP</code>."),
        ("Paso 18", "Desde el extremo superior del segundo arco sobre <code>DP</code>, traza una nueva línea constructiva hasta <code>CT</code> de longitud <code>= \"R3\"</code>. Dibuja el arco recortando el tramo entre <code>DP</code> y <code>DE</code>."),
        ("Paso 19", "Clic en <b>Convertir Entidades</b>. Selecciona los círculos <code>DI</code>, <code>DE</code> y los 3 arcos (R1, R2, R3)."),
        ("Paso 20", "Clic en <b>Simetría de Entidades</b>. Selecciona los 3 arcos y en `Con respecto a` selecciona la línea vertical central. Haz clic en Aceptar."),
        ("Paso 21", "Usa <b>Recortar Entidades</b> para limpiar las curvas sobrantes exterior e interior, dejando únicamente el perfil del diente cerrado.")
    ]

    t_steps2_data = []
    for num, desc in steps_p1_2:
        t_steps2_data.append([Paragraph(f"<b>{num}</b>", step_num_style), Paragraph(desc, body_style)])
    
    t_steps2 = Table(t_steps2_data, colWidths=[54, 450])
    t_steps2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, border_color)
    ]))
    story.append(t_steps2)
    story.append(Spacer(1, 8))

    imgs_p1_2 = [
        [Image("pdf_frames_dense/s08_cuatro_circulos_frontales.png", width=160, height=90),
         Image("pdf_frames_dense/s12_vector_r1_ct.png", width=160, height=90),
         Image("pdf_frames_dense/s17_arco_r3_recorte.png", width=160, height=90)],
        [Paragraph("<b>Pasos 11-13:</b> 4 Círculos etiquetados.", body_style),
         Paragraph("<b>Pasos 14-15:</b> Ángulo delta y vector R1.", body_style),
         Paragraph("<b>Pasos 16-18:</b> Perfil de 3 arcos concéntricos.", body_style)]
    ]
    t_imgs_p1_2 = Table(imgs_p1_2, colWidths=[166, 166, 166])
    t_imgs_p1_2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 2)]))
    story.append(t_imgs_p1_2)
    story.append(Spacer(1, 10))

    # Pasos 22 a 31: Hélice, Corte Recubierto y Matriz
    steps_p1_3 = [
        ("Paso 22", "Oculta el croquis frontal haciendo clic en el ojo."),
        ("Paso 23", "Ve a <b>Geometría de Referencia</b> &gt; <b>Plano</b>. Selecciona la superficie cilíndrica exterior (tangente) y el plano de planta/alzado. Crea el Plano 1."),
        ("Paso 24", "En el Plano 1, abre un croquis. Dibuja una línea de adelante hacia atrás sobre el cilindro y acota el ángulo respecto al eje como <code>= \"beta\"</code> (30°)."),
        ("Paso 25", "En la cara posterior, mide el ángulo de desviación resultante (medir $\\theta = 9.71^\\circ$)."),
        ("Paso 26", "<b>TRUCO MAESTRO DEL PROFESOR (CROQUIS MEDIO EXTENDIDO):</b><br/>"
                   "1. Haz clic en el <b>Plano Alzado</b> (mitad de la pieza) &gt; presiona <b>Croquis</b>.<br/>"
                   "2. Haz clic en <b>Convertir Entidades</b> y calca el perfil del diente del Croquis 1.<br/>"
                   "3. Clic en <b>Equidistanciar Entidades (Offset)</b> &gt; distancia <b>1 mm</b> hacia AFUERA en el contorno exterior.<br/>"
                   "4. Selecciona las líneas internas originales y marca <b>Para construcción</b>. Esto garantiza que el perfil medio sea 1mm más grande, eliminando cascarones residuales en el corte."),
        ("Paso 27", "Vuelve al Croquis 1 (cara frontal). Haz clic en <b>Girar Entidades</b>. Selecciona el perfil del diente. Centro de rotación: el origen. Ángulo: <code>9.71 / 2</code> ($4.855^\\circ$) hacia la izquierda. Acepta."),
        ("Paso 28", "Ve a <b>Operaciones</b> &gt; haz clic en <b>Corte Recubierto (Loft Cut)</b>.<br/>"
                   "En la caja <i>Perfiles</i>, selecciona secuencialmente:<br/>"
                   "1. Perfil Frontal (Croquis 1, girado $4.855^\\circ$).<br/>"
                   "2. Perfil Medio (Plano Alzado, extendido $+1\\text{ mm}$).<br/>"
                   "3. Perfil Posterior (girado $-4.855^\\circ$). Haz clic en Aceptar."),
        ("Paso 29", "Clic en <b>Redondeo</b>. Selecciona las 2 aristas del pie del hueco cortado. Radio: escribe <code>= \"r\"</code>. Acepta."),
        ("Paso 30", "Clic en <b>Matriz Circular</b> (desplegable de Matriz Lineal). Selecciona la cara cilíndrica como eje. Marca <b>Separación Igual (360°)</b>. Número de instancias: <code>25</code> (o vincular a <code>\"N\"</code>). Selecciona las operaciones <i>Corte Recubierto</i> y <i>Redondeo</i>. Haz clic en Aceptar."),
        ("Paso 31", "Guarda la pieza como <code>Engranaje_N25.SLDPRT</code>.")
    ]

    t_steps3_data = []
    for num, desc in steps_p1_3:
        t_steps3_data.append([Paragraph(f"<b>{num}</b>", step_num_style), Paragraph(desc, body_style)])
    
    t_steps3 = Table(t_steps3_data, colWidths=[54, 450])
    t_steps3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, border_color)
    ]))
    story.append(t_steps3)
    story.append(Spacer(1, 8))

    imgs_p1_3 = [
        [Image("pdf_frames_dense/s24_equidistanciar_1mm_trampa.png", width=160, height=90),
         Image("pdf_frames_dense/s27_corte_recubierto_seleccion.png", width=160, height=90),
         Image("pdf_frames_dense/s29_matriz_circular_25.png", width=160, height=90)],
        [Paragraph("<b>Paso 26:</b> Croquis medio extendido +1mm.", body_style),
         Paragraph("<b>Paso 28:</b> Selección de perfiles para Loft Cut.", body_style),
         Paragraph("<b>Paso 30:</b> Matriz circular de 25 dientes.", body_style)]
    ]
    t_imgs_p1_3 = Table(imgs_p1_3, colWidths=[166, 166, 166])
    t_imgs_p1_3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 2)]))
    story.append(t_imgs_p1_3)
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # SECCIÓN 3: GUÍA ATÓMICA DE MODELADO (N ≥ 30 DIENTES, N = 33)
    # ---------------------------------------------------------
    story.append(Paragraph("3. Guía Atómica Paso a Paso: Modelado de Engranaje 2 (N ≥ 30 Dientes, N = 33)", h1_style))
    story.append(Paragraph(
        "Para engranajes con $N \\ge 30$ dientes, la geometría cambia según el método simplificado del profesor:",
        body_style
    ))
    
    steps_p2 = [
        ("Paso 1", "Crear cilindro base con extrusión en Plano Medio ($N=33, M=5, DP=165\\text{ mm}, DE=175\\text{ mm}, DI=152.5\\text{ mm}$)."),
        ("Paso 2", "<b>Construcción del Desplazamiento P/4:</b> En el croquis frontal, trazar una línea horizontal de construcción desde la línea vertical central a una distancia igual a <code>= \"P\" / 4</code>."),
        ("Paso 3", "Desde el extremo final de esta horizontal sobre $DP$, trazar una línea constructiva hasta el Círculo de Trazo ($CT$) con longitud <code>= \"R1\"</code>."),
        ("Paso 4", "<b>Perfil Simplificado de 1 Solo Arco:</b> Trazar un arco continuo con centro en el extremo de R1 sobre $CT$ que va directamente desde $DI$ hasta $DE$ (sin arcos intermedios R2 ni R3)."),
        ("Paso 5", "<b>Hélice Invertida:</b> Crear la línea directriz de hélice en el plano tangente con ángulo opuesto <code>beta = -30 deg</code>. Mide el ángulo de giro posterior ($\\theta = 7.50^\\circ$)."),
        ("Paso 6", "Ejecutar el croquis medio extendido (+1mm), realizar el <b>Corte Recubierto</b>, aplicar el redondeo de pie <code>= \"r\"</code> y la <b>Matriz Circular</b> de 33 instancias. Guardar como <code>Engranaje_N33.SLDPRT</code>.")
    ]

    t_steps_p2_data = []
    for num, desc in steps_p2:
        t_steps_p2_data.append([Paragraph(f"<b>{num}</b>", step_num_style), Paragraph(desc, body_style)])
    
    t_steps_p2 = Table(t_steps_p2_data, colWidths=[54, 450])
    t_steps_p2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, border_color)
    ]))
    story.append(t_steps_p2)
    story.append(Spacer(1, 8))

    imgs_p2 = [
        [Image("pdf_frames_dense/s32_n33_horizontal_p_cuarto.png", width=160, height=90),
         Image("pdf_frames_dense/s34_n33_arco_unico_r1.png", width=160, height=90),
         Image("pdf_frames_dense/s38_n33_matriz_circular_33.png", width=160, height=90)],
        [Paragraph("<b>Paso 2:</b> Desplazamiento horizontal P/4.", body_style),
         Paragraph("<b>Paso 4:</b> Arco único R1 de DI a DE.", body_style),
         Paragraph("<b>Paso 6:</b> Engranaje de 33 dientes terminado.", body_style)]
    ]
    t_imgs_p2 = Table(imgs_p2, colWidths=[166, 166, 166])
    t_imgs_p2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 2)]))
    story.append(t_imgs_p2)
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # SECCIÓN 4: GUÍA ATÓMICA DE ENSAMBLAJE CINEMÁTICO
    # ---------------------------------------------------------
    story.append(Paragraph("4. Guía Atómica Paso a Paso: Ensamblaje Mecánico y Simulación Dinámica", h1_style))
    story.append(Paragraph(
        "Sigue estas instrucciones para ensamblar los dos engranajes y ponerlos a rotar suavemente a 360°:",
        body_style
    ))

    steps_p3 = [
        ("Paso 1", "<b>Pieza Base de Soporte:</b> Crear un nuevo archivo de pieza. Dibujar una base plana con dos ejes verticales separados exactamente a la Distancia entre Centros Teórica:<br/>"
                   "$$\\text{Distancia entre Centros } C = \\frac{DP_1 + DP_2}{2} = \\frac{125 + 198}{2} = 161.5\\text{ mm}$$<br/>"
                   "Guardar como <code>Base_Soporte.SLDPRT</code>."),
        ("Paso 2", "<b>Regla de Oro del Profesor:</b> Abre un archivo de <b>Nuevo Ensamblaje</b>. Inserta PRIMERO la pieza <code>Base_Soporte.SLDPRT</code> y haz coincidir su origen con el origen del ensamblaje. (Esta pieza quedará FIJA)."),
        ("Paso 3", "Inserta los archivos <code>Engranaje_N25.SLDPRT</code> y <code>Engranaje_N33.SLDPRT</code>."),
        ("Paso 4", "<b>Relaciones Concéntricas:</b> Clic en <b>Relación de Posición</b>. Selecciona el agujero central de N25 y el primer eje de la base. Aplica relación <i>Concéntrica</i>. Repite para N33 en el segundo eje."),
        ("Paso 5", "<b>Relación de Ancho / Coincidencia:</b> Aplica relación de coincidencia entre las caras frontales de los engranajes para que queden perfectamente alineados en el mismo plano."),
        ("Paso 6", "<b>Verificación de Tangencia:</b> Haz visibles los croquis con los círculos de $DP_1$ y $DP_2$. Verifica visualmente que ambos círculos se toquen en un punto sin cruzarse."),
        ("Paso 7", "<b>Relación Mecánica de Engranaje:</b> Ve a <i>Relaciones de Posición</i> &gt; despliega <b>Relaciones Mecánicas</b> &gt; clic en <b>Engranaje</b>. Selecciona las superficies cilíndricas de ambos engranajes. En los cuadros de relación, ingresa <code>25</code> para N25 y <code>33</code> para N33. Haz clic en Aceptar."),
        ("Paso 8", "<b>Prueba Dinámica:</b> Con el mouse, haz clic en uno de los dientes y arrastra en círculo. Los dos engranajes deben rotar suavemente en sentido opuesto a 360° sin colisionar.")
    ]

    t_steps_p3_data = []
    for num, desc in steps_p3:
        t_steps_p3_data.append([Paragraph(f"<b>{num}</b>", step_num_style), Paragraph(desc, body_style)])
    
    t_steps_p3 = Table(t_steps_p3_data, colWidths=[54, 450])
    t_steps_p3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, border_color)
    ]))
    story.append(t_steps_p3)
    story.append(Spacer(1, 8))

    imgs_p3 = [
        [Image("pdf_frames_dense/s39_soporte_distancia_centros.png", width=160, height=90),
         Image("pdf_frames_dense/s42_verificacion_tangencia_dp.png", width=160, height=90),
         Image("pdf_frames_dense/s44_prueba_movimiento_360.png", width=160, height=90)],
        [Paragraph("<b>Paso 1:</b> Pieza base con distancia C = 161.5mm.", body_style),
         Paragraph("<b>Paso 6:</b> Tangencia perfecta entre DP1 y DP2.", body_style),
         Paragraph("<b>Paso 8:</b> Rotación dinámica a 360° en ensamblaje.", body_style)]
    ]
    t_imgs_p3 = Table(imgs_p3, colWidths=[166, 166, 166])
    t_imgs_p3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('PADDING', (0,0), (-1,-1), 2)]))
    story.append(t_imgs_p3)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECCIÓN 5: EJERCICIO PRÁCTICO REAL CON SOLUCIONARIO (WORKBOOK)
    # ---------------------------------------------------------
    story.append(Paragraph("5. Cuaderno de Trabajo: Ejercicio Práctico Real de Autoevaluación", h1_style))
    story.append(Paragraph(
        "Para comprobar si has dominado la técnica y puedes modelar cualquier par de engranajes helicoidales por tu cuenta, "
        "resuelve el siguiente ejercicio real completo. Al final se incluye el solucionario con todas las respuestas numéricas para verificar tu modelo.",
        body_style
    ))

    ex_card_data = [[
        Paragraph("<b>📝 ENUNCIADO DEL EJERCICIO PRÁCTICO REAL:</b><br/>"
                  "Se requiere diseñar un juego de engranajes helicoidales para un reductor de velocidad en SolidWorks con los siguientes datos:<br/>"
                  "• <b>Módulo Estándar:</b> $M = 4\\text{ mm}$<br/>"
                  "• <b>Piñón (Engranaje A - N &lt; 30):</b> $N_A = 20$ dientes | Diámetro de eje $d_A = 25\\text{ mm}$ (Chavetero $8\\text{ mm} \\times 4\\text{ mm}$)<br/>"
                  "• <b>Rueda (Engranaje B - N ≥ 30):</b> $N_B = 36$ dientes | Diámetro de eje $d_B = 40\\text{ mm}$ (Chavetero $12\\text{ mm} \\times 5\\text{ mm}$)<br/>"
                  "• <b>Ángulo de Hélice:</b> $\\beta = 25^\\circ$ (Piñón hélice derecha $+25^\\circ$, Rueda hélice izquierda $-25^\\circ$)<br/>"
                  "• <b>Ancho de Cara:</b> $A = 35\\text{ mm}$", body_style)
    ]]
    t_ex_card = Table(ex_card_data, colWidths=[504])
    t_ex_card.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ex_card)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>📊 SOLUCIONARIO CON RESPUESTAS ESPERADAS (PARA VERIFICAR TU MODELO):</b>", h2_style))

    sol_table_data = [
        [Paragraph("<b>Parámetro Calculado</b>", header_cell_style), Paragraph("<b>Fórmula Aplicada</b>", header_cell_style), Paragraph("<b>Resultado Piñón (NA=20)</b>", header_cell_style), Paragraph("<b>Resultado Rueda (NB=36)</b>", header_cell_style)],
        [Paragraph("Diámetro Primitivo (DP)", body_style), Paragraph("<code>DP = M * N</code>", code_style), Paragraph("<b>80.00 mm</b>", body_style), Paragraph("<b>144.00 mm</b>", body_style)],
        [Paragraph("Diámetro Exterior (DE)", body_style), Paragraph("<code>DE = DP + 2*M</code>", code_style), Paragraph("<b>88.00 mm</b>", body_style), Paragraph("<b>152.00 mm</b>", body_style)],
        [Paragraph("Diámetro Interior (DI)", body_style), Paragraph("<code>DI = DP - 2.5*M</code>", code_style), Paragraph("<b>70.00 mm</b>", body_style), Paragraph("<b>134.00 mm</b>", body_style)],
        [Paragraph("Círculo de Trazo (CT)", body_style), Paragraph("<code>CT = DP * cos(20 deg)</code>", code_style), Paragraph("<b>75.175 mm</b>", body_style), Paragraph("<b>135.315 mm</b>", body_style)],
        [Paragraph("Paso Circular (P)", body_style), Paragraph("<code>P = pi * M</code>", code_style), Paragraph("<b>12.566 mm</b>", body_style), Paragraph("<b>12.566 mm</b>", body_style)],
        [Paragraph("Desplazamiento P/4", body_style), Paragraph("<code>P / 4</code>", code_style), Paragraph("N/A (Usa 3 arcos)", body_style), Paragraph("<b>3.1415 mm</b>", body_style)],
        [Paragraph("Ángulo Delta (δ)", body_style), Paragraph("<code>90 deg / N</code>", code_style), Paragraph("<b>4.50°</b>", body_style), Paragraph("N/A", body_style)],
        [Paragraph("Redondeo Raíz (r)", body_style), Paragraph("<code>r = 0.3 * M</code>", code_style), Paragraph("<b>1.20 mm</b>", body_style), Paragraph("<b>1.20 mm</b>", body_style)],
        [Paragraph("Chaflán (Ch)", body_style), Paragraph("<code>Ch = 0.5 * M</code>", code_style), Paragraph("<b>2.00 mm</b>", body_style), Paragraph("<b>2.00 mm</b>", body_style)],
        [Paragraph("Distancia entre Centros (C)", body_style), Paragraph("<code>C = (DP_A + DP_B) / 2</code>", code_style), Paragraph("<b>112.00 mm</b> (Distancia exacta de soporte)", body_style), Paragraph("<b>112.00 mm</b>", body_style)]
    ]

    t_sol = Table(sol_table_data, colWidths=[130, 154, 110, 110])
    t_sol.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('BACKGROUND', (0,1), (-1,-1), light_bg),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))

    story.append(t_sol)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>✅ LISTA DE COMPROBACIÓN FINAL (CHECKLIST DE AUTOEVALUACIÓN):</b>", h2_style))
    
    check_items = [
        "1. ¿Configuraste las Ecuaciones en SolidWorks y verificaste que los diámetros DP, DE, DI y CT cambian automáticamente al editar M o N?",
        "2. ¿En el Piñón (N=20) acotaste la longitud escalar pura de las líneas constructivas R1, R2 y R3 sin confundir con sus componentes X/Y?",
        "3. ¿En el Croquis Medio (Plano Alzado) aplicaste la equidistancia de +1mm hacia afuera para asegurar un corte recubierto 100% limpio?",
        "4. ¿En la Rueda (N=36) usaste el desplazamiento P/4 = 3.1415mm y trazaste un único arco R1 desde DI hasta DE?",
        "5. ¿Configuraste el ángulo de hélice en sentido opuesto en la rueda (beta = -25°)?",
        "6. ¿En el ensamblaje fijaste primero la pieza base de soporte con ejes separados exactamente a C = 112.00mm?",
        "7. ¿Al activar la Relación Mecánica de Engranaje con ratio 20:36 ambos engranajes rotan suavemente a 360° sin colisionar?"
    ]

    t_chk_data = []
    for item in check_items:
        t_chk_data.append([Paragraph("<b>[  ]</b>", step_num_style), Paragraph(item, body_style)])

    t_chk = Table(t_chk_data, colWidths=[30, 474])
    t_chk.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_chk)
    story.append(Spacer(1, 14))

    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph("<b>FIN DEL MANUAL MAESTRO — Preparado con secuencia atómica de 44 fotogramas y cuaderno de trabajo para aprendizaje 100% autónomo.</b>", ParagraphStyle('EndNote', parent=body_style, fontName='Helvetica-Bold', alignment=1, textColor=primary_color)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master PDF successfully generated: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
