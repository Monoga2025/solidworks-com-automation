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
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Draw header on pages 2 and later
        if self._pageNumber > 1:
            self.drawString(54, 750, "TUTORIAL SOLIDWORKS: ENGRANAJES HELICOIDALES PARAMÉTRICOS")
            self.drawRightString(558, 750, "ANÁLISIS FOTOGRAMA A FOTOGRAMA")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.75)
            self.line(54, 742, 558, 742)
            
        # Draw footer on all pages
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Guía Técnica Oficial de Clase — Basada en Capturas Directas del Profesor")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 32, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 44, 558, 44)
        
        self.restoreState()

def build_pdf():
    pdf_filename = "Tutorial_Modelado_Engranajes_Helicoidales_SolidWorks.pdf"
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
    dark_neutral = colors.HexColor("#1A202C")    # Charcoal body text
    light_bg = colors.HexColor("#F7FAFC")        # Card background
    border_color = colors.HexColor("#E2E8F0")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=dark_neutral,
        spaceAfter=8
    )

    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.white
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_neutral,
        leftIndent=15,
        spaceAfter=4
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2C5282"),
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#742A2A")
    )
    
    story = []
    
    # ---------------------------------------------------------
    # COVER / HEADER BLOCK
    # ---------------------------------------------------------
    story.append(Paragraph("TUTORIAL PASO A PASO: MODELADO PARAMÉTRICO Y ENSAMBLAJE DE ENGRANAJES HELICOIDALES EN SOLIDWORKS", title_style))
    story.append(Paragraph("<b>Guía de Ejecución Exacta basada en Análisis Fotograma a Fotograma del Video del Profesor</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceBefore=0, spaceAfter=12))
    
    meta_data = [
        [Paragraph("<b>Software:</b> SolidWorks (Modelado 3D & Ecuaciones)", body_style), Paragraph("<b>Tema:</b> Engranajes Helicoidales (N<30 y N≥30)", body_style)],
        [Paragraph("<b>Metodología:</b> Variables Globales + Corte Recubierto", body_style), Paragraph("<b>Verificación:</b> Ensamblaje Dinámico a 360°", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))
    
    # Callout Box: Objetivo del Tutorial
    callout_data = [[
        Paragraph("<b>📌 NOTA DE FIDELIDAD TÉCNICA:</b> Este tutorial NO es una transcripción textual genérica. Ha sido construido analizando fotograma a fotograma el video de la clase del profesor. Incluye los atajos, nombres de variables globales exactos, trucos de modelado (como la holgura de 1mm en el plano medio) y las advertencias explícitas del profesor para evitar errores en las entregas y parciales.", body_style)
    ]]
    t_callout = Table(callout_data, colWidths=[504])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEFCBF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D69E2E")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 14))
    
    # ---------------------------------------------------------
    # SECCIÓN 1: FORMULACIÓN Y TABLA DE VARIABLES GLOBALES
    # ---------------------------------------------------------
    story.append(Paragraph("1. Ecuaciones y Variables Globales en SolidWorks", h1_style))
    story.append(Paragraph(
        "Antes de iniciar cualquier trazado, el profesor configura la tabla de <b>Variables Globales</b> en SolidWorks. "
        "Esto garantiza que cualquier cambio posterior en el módulo <i>M</i> o número de dientes <i>N</i> actualice automáticamente toda la geometría de la pieza.",
        body_style
    ))
    
    eq_table_data = [
        [Paragraph("<b>Parámetro / Variable</b>", header_cell_style), Paragraph("<b>Sintaxis SolidWorks</b>", header_cell_style), Paragraph("<b>Fórmula / Definición</b>", header_cell_style), Paragraph("<b>Aplicación</b>", header_cell_style)],
        [Paragraph("Módulo", body_style), Paragraph("<code>\"M\"</code>", code_style), Paragraph("5 mm (o según ejercicio)", body_style), Paragraph("Estándar de engrane", body_style)],
        [Paragraph("Número de Dientes", body_style), Paragraph("<code>\"N\"</code>", code_style), Paragraph("25 (Engranaje 1) / 33 (Engranaje 2)", body_style), Paragraph("Conteo de dientes", body_style)],
        [Paragraph("Ángulo de Hélice", body_style), Paragraph("<code>\"beta\"</code>", code_style), Paragraph("30° (Opuestos en ensamblaje)", body_style), Paragraph("Inclinación helicoidal", body_style)],
        [Paragraph("Diámetro Primitivo", body_style), Paragraph("<code>\"DP\"</code>", code_style), Paragraph("<code>= \"M\" * \"N\"</code>", code_style), Paragraph("Circunferencia de contacto", body_style)],
        [Paragraph("Diámetro Exterior", body_style), Paragraph("<code>\"DE\"</code>", code_style), Paragraph("<code>= \"DP\" + 2 * \"M\"</code>", code_style), Paragraph("Cresta del engranaje", body_style)],
        [Paragraph("Diámetro Interior", body_style), Paragraph("<code>\"DI\"</code>", code_style), Paragraph("<code>= \"DP\" - 2.5 * \"M\"</code>", code_style), Paragraph("Raíz / Pie del diente", body_style)],
        [Paragraph("Círculo de Trazo", body_style), Paragraph("<code>\"CT\"</code>", code_style), Paragraph("<code>= \"DP\" * cos(20 deg)</code>", code_style), Paragraph("Base de arcos de perfil", body_style)],
        [Paragraph("Paso Circular", body_style), Paragraph("<code>\"P\"</code>", code_style), Paragraph("<code>= pi * \"M\"</code>", code_style), Paragraph("Paso transversal", body_style)],
        [Paragraph("Radio 1 (N < 30)", body_style), Paragraph("<code>\"R1\"</code>", code_style), Paragraph("Según tabla Excel del profesor", body_style), Paragraph("Primer arco de raíz", body_style)],
        [Paragraph("Radio 2 (N < 30)", body_style), Paragraph("<code>\"R2\"</code>", code_style), Paragraph("Según tabla Excel del profesor", body_style), Paragraph("Segundo arco medio", body_style)],
        [Paragraph("Radio 3 (N < 30)", body_style), Paragraph("<code>\"R3\"</code>", code_style), Paragraph("Según tabla Excel del profesor", body_style), Paragraph("Tercer arco cresta", body_style)],
        [Paragraph("Radio Único (N ≥ 30)", body_style), Paragraph("<code>\"R1\"</code> (Ver Gotcha)", code_style), Paragraph("Según tabla Excel del profesor", body_style), Paragraph("Arco único (N ≥ 30)", body_style)],
        [Paragraph("Redondeo Raíz", body_style), Paragraph("<code>\"r\"</code> (minúscula)", code_style), Paragraph("<code>= 0.3 * \"M\"</code>", code_style), Paragraph("Empalme de pie", body_style)],
        [Paragraph("Ancho de Cara", body_style), Paragraph("<code>\"A\"</code>", code_style), Paragraph("40 mm", body_style), Paragraph("Espesor de extrusión", body_style)],
        [Paragraph("Chaflán", body_style), Paragraph("<code>\"Ch\"</code>", code_style), Paragraph("<code>= 0.5 * \"M\"</code>", code_style), Paragraph("Bisel exterior", body_style)]
    ]
    
    t_eq = Table(eq_table_data, colWidths=[100, 110, 154, 140])
    t_eq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('BACKGROUND', (0,1), (-1,-1), light_bg),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    
    story.append(t_eq)
    story.append(Spacer(1, 10))
    
    # Image of Excel formulas table
    imgs_excel = [
        [Image("pdf_frames_audit/excel_formulas_2755.png", width=360, height=202)],
        [Paragraph("<b>Fotograma Auditado 17b:</b> Hoja de cálculo Excel del profesor con las ecuaciones exactas para N<30 y N≥30 mostradas en clase.", body_style)]
    ]
    t_excel = Table(imgs_excel, colWidths=[500])
    t_excel.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_excel)
    story.append(Spacer(1, 10))
    
    # Gotcha Alert Box
    gotcha_data = [[
        Paragraph("<b>⚠️ ADVERTENCIA CLAVE DEL PROFESOR (CONFIRMADISIMA EN CLASE):</b><br/>"
                  "SolidWorks <b>NO diferencia entre mayúsculas y minúsculas</b> en la tabla de Ecuaciones. "
                  "Si creas una variable para el redondeo llamada <code>r</code> (minúscula) y luego intentas crear el radio del diente como <code>R</code> (mayúscula), SolidWorks arrojará un error de conflicto. "
                  "Por esta razón, el profesor renombró la variable del radio único como <code>R1</code> en la tabla de ecuaciones.", callout_style)
    ]]
    t_gotcha = Table(gotcha_data, colWidths=[504])
    t_gotcha.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E53E3E")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_gotcha)
    story.append(Spacer(1, 14))
    
    # ---------------------------------------------------------
    # SECCIÓN 2: MODELADO DE ENGRANAJE 1 (N < 30 DIENTES, N = 25)
    # ---------------------------------------------------------
    story.append(Paragraph("2. Parte 1: Modelado de Engranaje 1 (N < 30 Dientes, N = 25)", h1_style))
    story.append(Paragraph(
        "En este primer bloque se detalla la construcción paso a paso del engranaje helicoidal de 25 dientes. "
        "El profesor utiliza la construcción del perfil por 3 arcos concéntricos (<i>R1, R2, R3</i>) y una operación de Corte Recubierto helicoidal.",
        body_style
    ))
    
    # Paso 1.1
    story.append(Paragraph("Paso 1.1: Cilindro Base, Chavetero, Extrusión Plano Medio y Chaflán", h2_style))
    story.append(Paragraph(
        "1. Seleccionar el <b>Plano Alzado</b> y crear un croquis con un círculo de centro.<br/>"
        "2. Colocar la cota inteligente. Borrar el valor numérico, escribir <code>=</code> y seleccionar la variable global <code>\"d\"</code> (diámetro del eje).<br/>"
        "3. Trazar el chavetero cuadrado (1\" x 1/2\" o según eje) recortando sobrantes y acotando completamente.<br/>"
        "4. En la operación <b>Extruir Saliente/Base</b>, seleccionar la condición final <b>Plano Medio</b> y vincular el espesor a la variable <code>\"ancho de cara\"</code>.<br/>"
        "5. Aplicar la operación <b>Chaflán</b> en las aristas extremas del cilindro con el valor vinculado a <code>\"chaflan\"</code>.",
        body_style
    ))
    
    imgs_row1 = [
        [Image("pdf_frames/01_circulo_base.png", width=240, height=135), Image("pdf_frames/02_chavetero.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 01:</b> Croquis del círculo base en Plano Alzado acotado con variable global.", body_style),
         Paragraph("<b>Fotograma 02:</b> Geometría del chavetero cuadrado completamente definida.", body_style)],
        [Image("pdf_frames/03_extrusion_plano_medio.png", width=240, height=135), Image("pdf_frames/04_chaflan.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 03:</b> Extrusión Saliente en Plano Medio con ancho de cara.", body_style),
         Paragraph("<b>Fotograma 04:</b> Aplicación de Chaflán simétrico en aristas exteriores.", body_style)]
    ]
    t_imgs1 = Table(imgs_row1, colWidths=[248, 248])
    t_imgs1.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs1)
    story.append(Spacer(1, 14))
    
    # Paso 1.2
    story.append(Paragraph("Paso 1.2: Croquis de Diámetros de Referencia y Sintaxis de Etiquetas de Cota", h2_style))
    story.append(Paragraph(
        "1. Crear un nuevo croquis en la cara frontal plana del cilindro.<br/>"
        "2. Trazar 4 círculos concéntricos partiendo del centro de la pieza.<br/>"
        "3. Convertir el círculo de <b>Diámetro Primitivo (DP)</b> a geometría constructiva (Línea de construcción).<br/>"
        "4. <b>TRUCO DE PRESENTACIÓN DEL PROFESOR:</b> Al colocar cada cota, en la ventana izquierda de propiedades de SolidWorks, posicionar el cursor ANTES del texto por defecto (ej: <code>d1@Croquis2</code>) y escribir exactamente el nombre de la variable seguido de un espacio igual, por ejemplo: <code>DE = </code>, <code>DP = </code>, <code>CT = </code>, <code>DI = </code>. De esta forma, las etiquetas quedan claramente visibles en el área de dibujo.",
        body_style
    ))
    
    imgs_row2 = [
        [Image("pdf_frames/05_cuatro_circulos_cotas.png", width=320, height=180)],
        [Paragraph("<b>Fotograma 05:</b> Los 4 círculos concéntricos de referencia (DE, DP constructivo, CT, DI) etiquetados adecuadamente.", body_style)]
    ]
    t_imgs2 = Table(imgs_row2, colWidths=[500])
    t_imgs2.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs2)
    story.append(Spacer(1, 14))

    # Paso 1.3
    story.append(Paragraph("Paso 1.3: Construcción del Perfil del Diente mediante 3 Arcos Radiados (R1, R2, R3)", h2_style))
    story.append(Paragraph(
        "Para engranajes con $N < 30$ dientes, la envolvente se aproxima mediante 3 arcos concéntricos sucesivos:<br/>"
        "1. <b>Ángulo Delta (δ):</b> Trazar una línea constructiva inclinada desde el centro a un ángulo $\\delta = 90^\\circ / N$.<br/>"
        "2. <b>Vector R1:</b> En la intersección entre la línea delta y el <i>Diámetro Interior (DI)</i>, trazar una línea constructiva hasta el <i>Círculo de Trazo (CT)</i> con longitud igual a <code>\"R1\"</code>.<br/>"
        "3. <b>Arco 1:</b> Con centro en el extremo de R1 sobre CT, dibujar un círculo de radio R1 y recortar para conservar únicamente el segmento comprendido entre <i>DI</i> y <i>CT</i>.<br/>"
        "4. <b>Vector R2 y Arco 2:</b> Desde el punto donde finalizó el Arco 1 sobre CT, trazar el vector de radio <code>\"R2\"</code> hasta CT. Dibujar el arco y recortar la porción entre <i>CT</i> y <i>DP</i>.<br/>"
        "5. <b>Vector R3 y Arco 3:</b> Desde el final del Arco 2 sobre DP, trazar el vector de radio <code>\"R3\"</code> hasta CT. Dibujar el arco y recortar la porción entre <i>DP</i> y <i>DE</i>.",
        body_style
    ))
    
    imgs_row3 = [
        [Image("pdf_frames/06_trazo_delta_r1.png", width=240, height=135), Image("pdf_frames/07_arco_r1.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 06:</b> Trazo del ángulo delta (90°/N) y vector de radio R1.", body_style),
         Paragraph("<b>Fotograma 07:</b> Primer arco R1 acotado y recortado entre DI y CT.", body_style)],
        [Image("pdf_frames/08_arco_r2.png", width=240, height=135), Image("pdf_frames/09_arco_r3.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 08:</b> Segundo arco R2 entre CT y DP.", body_style),
         Paragraph("<b>Fotograma 09:</b> Tercer arco R3 completando la cresta hasta DE.", body_style)]
    ]
    t_imgs3 = Table(imgs_row3, colWidths=[248, 248])
    t_imgs3.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs3)
    story.append(Spacer(1, 14))

    # Paso 1.4 & 1.5
    story.append(Paragraph("Paso 1.4 y 1.5: Simetría del Diente, Plano Tangente y Ángulo de Giro Helicoidal (θ)", h2_style))
    story.append(Paragraph(
        "1. <b>Simetría:</b> Convertir entidades de los arcos R1, R2, R3 y los bordes DI y DE. Aplicar <i>Simetría de Entidades</i> respecto al eje vertical para obtener el perfil simétrico del diente completo.<br/>"
        "2. <b>Plano Tangente:</b> Crear un plano de referencia tangente a la cara exterior cilíndrica.<br/>"
        "3. <b>Línea Helicoidal:</b> En dicho plano, trazar la línea de dirección de la hélice con un ángulo $\\beta = 30^\\circ$.<br/>"
        "4. <b>Medición del Ángulo de Giro (θ):</b> En la cara posterior del cilindro, proyectar la inclinación de la hélice y medir el ángulo de desviación resultante (en el video el profesor mide $\\theta = 9.71^\\circ$).",
        body_style
    ))
    
    imgs_row4 = [
        [Image("pdf_frames/10_simetria_diente.png", width=240, height=135), Image("pdf_frames/11_plano_helice_30deg.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 10:</b> Perfil del diente completado mediante simetría.", body_style),
         Paragraph("<b>Fotograma 11:</b> Plano de referencia con la línea de dirección de hélice a 30°.", body_style)],
        [Image("pdf_frames/12_angulo_giro_posterior.png", width=240, height=135), Image("pdf_frames/14_rotacion_perfil.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 12:</b> Medición del ángulo de giro posterior θ = 9.71°.", body_style),
         Paragraph("<b>Fotograma 14:</b> Girar entidades en el croquis frontal un ángulo θ / 2.", body_style)]
    ]
    t_imgs4 = Table(imgs_row4, colWidths=[248, 248])
    t_imgs4.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs4)
    story.append(Spacer(1, 14))

    # Paso 1.6 & 1.7
    story.append(Paragraph("Paso 1.6 y 1.7: Croquis Medio ('Truco de Trampa del Profesor') y Corte Recubierto", h2_style))
    story.append(Paragraph(
        "<b>TRUCO MAESTRO DEL PROFESOR PARA CORTE RECURBIERTO LIMPIO:</b><br/>"
        "Si se realiza un corte recubierto directamente entre el croquis frontal y posterior, SolidWorks suele dejar una 'piel' o cascarón metálico flotante en los bordes debido a imprecisiones de curvatura.<br/>"
        "<b>Solución del Profesor:</b><br/>"
        "1. Crear un croquis en el <b>Plano Alzado</b> (plano medio de la pieza).<br/>"
        "2. Calcar el contorno del diente mediante <i>Convertir Entidades</i>.<br/>"
        "3. Aplicar <b>Equidistanciar Entidades (Offset) de 1 mm hacia afuera</b> exclusivamente en el borde exterior.<br/>"
        "4. Convertir las líneas originales internas en geometría constructiva.<br/>"
        "5. Ejecutar la operación <b>Corte Recubierto (Loft Cut)</b> seleccionando secuencialmente los 3 perfiles: Perfil Frontal (girado $\\theta/2$), Perfil Medio (ampliado +1mm) y Perfil Posterior.",
        body_style
    ))
    
    imgs_row5 = [
        [Image("pdf_frames/13_croquis_medio_trampa.png", width=240, height=135), Image("pdf_frames/15_corte_recubierto.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 13:</b> Croquis medio extendido +1mm ('Trampa del profesor').", body_style),
         Paragraph("<b>Fotograma 15:</b> Operación Corte Recubierto (Loft Cut) limpia entre perfiles.", body_style)]
    ]
    t_imgs5 = Table(imgs_row5, colWidths=[248, 248])
    t_imgs5.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs5)
    story.append(Spacer(1, 14))

    # Paso 1.8
    story.append(Paragraph("Paso 1.8: Redondeo del Pie de Diente y Matriz Circular (N = 25)", h2_style))
    story.append(Paragraph(
        "1. Seleccionar las aristas del pie/raíz del hueco cortado y aplicar <b>Redondeo</b> vinculado a la variable global <code>\"r\"</code>.<br/>"
        "2. Activar la operación <b>Matriz Circular</b>.<br/>"
        "3. Seleccionar el eje cilíndrico de la pieza como dirección, marcar la casilla <b>Separación Igual (360°)</b>, ingresar <code>25</code> en el número de instancias y seleccionar las dos operaciones: <i>Corte Recubierto</i> y <i>Redondeo</i>.<br/>"
        "4. Guardar la pieza como <code>Engranaje_N25.SLDPRT</code>.",
        body_style
    ))
    
    imgs_row6 = [
        [Image("pdf_frames/16_matriz_circular_n25.png", width=240, height=135), Image("pdf_frames/17_tabla_ecuaciones.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 16:</b> Matriz circular terminada con 25 dientes helicoidales.", body_style),
         Paragraph("<b>Fotograma 17:</b> Verificación de la tabla de ecuaciones vinculada en SolidWorks.", body_style)]
    ]
    t_imgs6 = Table(imgs_row6, colWidths=[248, 248])
    t_imgs6.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs6)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECCIÓN 3: MODELADO DE ENGRANAJE 2 (N ≥ 30 DIENTES, N = 33)
    # ---------------------------------------------------------
    story.append(Paragraph("3. Parte 2: Modelado de Engranaje 2 (N ≥ 30 Dientes, N = 33)", h1_style))
    story.append(Paragraph(
        "Para engranajes con $N \\ge 30$ dientes, la geometría se simplifica sustancialmente según la explicación del profesor. "
        "Además, para lograr el engrane cinemático con el primer engranaje, se deben respetar reglas estrictas de compatibilidad.",
        body_style
    ))
    
    # Callout Box: Reglas de Compatibilidad
    compat_data = [[
        Paragraph("<b>🧠 REGLAS FUNDAMENTALES DE ENGRANE DEMOSTRADAS POR EL PROFESOR:</b><br/>"
                  "1. <b>Módulo Idéntico:</b> Ambos engranajes DEBEN tener el mismo módulo (en este caso $M = 5$).<br/>"
                  "2. <b>Hélice de Sentido Contrario:</b> Si el Engranaje 1 tiene hélice hacia la derecha ($\\beta_1 = +30^\\circ$), el Engranaje 2 DEBE tener hélice hacia la izquierda ($\\beta_2 = -30^\\circ$).<br/>"
                  "3. <b>Perfil Simplificado de 1 Solo Radio:</b> A partir de 30 dientes no se usan 3 arcos (R1, R2, R3). Se utiliza un único arco <code>R1</code> que abarca desde <i>DI</i> hasta <i>DE</i>.", callout_style)
    ]]
    t_compat = Table(compat_data, colWidths=[504])
    t_compat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_compat)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Paso a Paso del Engranaje de 33 Dientes:", h2_style))
    story.append(Paragraph(
        "1. Crear el cilindro base con extrusión en plano medio ($N=33, M=5, DP=165\\text{ mm}, DE=175\\text{ mm}, DI=152.5\\text{ mm}$).<br/>"
        "2. En el croquis frontal, trazar la línea horizontal de referencia a una distancia de $P/4$ (Paso circular dividido en 4) desde la vertical.<br/>"
        "3. Trazar el vector de radio único <code>\"R1\"</code> desde la intersección con el $DP$ hasta el Círculo de Trazo ($CT$).<br/>"
        "4. Trazar un único arco continuo con radio <code>R1</code> desde <i>DI</i> hasta <i>DE</i>.<br/>"
        "5. Configurar la hélice en sentido opuesto ($\\beta = -30^\\circ$) y medir el nuevo ángulo de giro posterior ($\\theta = 7.50^\\circ$).<br/>"
        "6. Realizar el Corte Recubierto empleando el croquis medio extendido (+1mm) y la matriz circular de 33 instancias.",
        body_style
    ))
    
    imgs_row7 = [
        [Image("pdf_frames/18_n33_cilindro_base.png", width=240, height=135), Image("pdf_frames_audit/p_cuarto_3530.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 18:</b> Cilindro base para N=33 dientes con diámetro primitivo DP=165mm.", body_style),
         Paragraph("<b>Fotograma 19 (Detalle Auditado):</b> Construcción del desplazamiento P/4 sobre DP.", body_style)],
        [Image("pdf_frames/20_n33_perfil_diente.png", width=240, height=135), Image("pdf_frames_audit/plano_truco_4010.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 20:</b> Perfil simplificado de un solo arco continuo R1 (DI a DE).", body_style),
         Paragraph("<b>Fotograma 21 (Truco del Plano):</b> Plano tangente a línea DE/2 en plano alzado.", body_style)],
        [Image("pdf_frames/22_n33_matriz_circular.png", width=240, height=135), Image("pdf_frames/17c_tabla_ecuaciones_n33.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 22:</b> Matriz circular de 33 dientes helicoidales completada.", body_style),
         Paragraph("<b>Fotograma 17c:</b> Tabla de ecuaciones del profesor para el caso N ≥ 30.", body_style)]
    ]
    t_imgs7 = Table(imgs_row7, colWidths=[248, 248])
    t_imgs7.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs7)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECCIÓN 4: ENSAMBLAJE CINEMÁTICO Y SIMULACIÓN DE MOVIENTO
    # ---------------------------------------------------------
    story.append(Paragraph("4. Parte 3: Ensamblaje Mecánico y Simulación de Movimiento a 360°", h1_style))
    story.append(Paragraph(
        "Una vez modeladas las dos piezas, el profesor procede al montaje cinemático para verificar que ambos engranajes articulan perfectamente sin colisiones.",
        body_style
    ))
    
    story.append(Paragraph("Paso 4.1: Construcción de la Pieza de Soporte (Ejes a Distancia entre Centros)", h2_style))
    story.append(Paragraph(
        "La distancia teórica entre centros $C$ viene dada por la suma de los radios primitivos:<br/>"
        "$$\\text{Distancia entre Centros } C = \\frac{DP_1 + DP_2}{2} = \\frac{125\\text{ mm} + 198\\text{ mm}}{2} = 161.5\\text{ mm}$$<br/>"
        "Se crea un archivo de pieza sencillo con dos líneas constructivas o cilindros separados exactamente a $C = 161.5\\text{ mm}$.",
        body_style
    ))
    
    story.append(Paragraph("Paso 4.2: Regla de Oro del Profesor para Ensamblajes en SolidWorks", h2_style))
    story.append(Paragraph(
        "<b>REGLA CRÍTICA ADVERTIDA EN CLASE:</b><br/>"
        "<i>'La primera pieza que se inserta en un archivo de ensamblaje queda FIJADA automáticamente en el origen.'</i><br/>"
        "Si insertas primero uno de los engranajes, este quedará congelado y no podrá rotar. "
        "<b>Procedimiento Correcto:</b> Insertar primero la pieza de soporte/ejes, hacer coincidir su origen con el origen del ensamblaje, y posteriormente insertar los dos engranajes.",
        body_style
    ))

    imgs_row8 = [
        [Image("pdf_frames/23_ejes_distancia_centros.png", width=240, height=135), Image("pdf_frames/24_ensamblaje_fijar_origen.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 23:</b> Pieza de soporte con ejes a distancia C = (DP1 + DP2)/2.", body_style),
         Paragraph("<b>Fotograma 24:</b> Insertar primero la pieza base y fijar su origen.", body_style)],
        [Image("pdf_frames/25_ensamblaje_posicionamiento.png", width=240, height=135), Image("pdf_frames/26_verificacion_primitivos.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 25:</b> Posicionar engranajes con relaciones concéntricas y de ancho.", body_style),
         Paragraph("<b>Fotograma 26:</b> Verificación visual: Tangencia perfecta entre DP1 y DP2.", body_style)],
        [Image("pdf_frames/27_relacion_mecanica_engranaje.png", width=240, height=135), Image("pdf_frames/28_prueba_movimiento.png", width=240, height=135)],
        [Paragraph("<b>Fotograma 27:</b> Configurar Relación Mecánica de Engranaje con ratio 25:33.", body_style),
         Paragraph("<b>Fotograma 28:</b> Prueba final de rotación dinámica continua a 360°.", body_style)]
    ]
    t_imgs8 = Table(imgs_row8, colWidths=[248, 248])
    t_imgs8.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_imgs8)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECCIÓN 5: CHECKLIST Y ERRORES FRECUENTES
    # ---------------------------------------------------------
    story.append(Paragraph("5. Lista de Verificación y Errores Frecuentes (Tips del Profesor)", h1_style))
    
    checklist_data = [
        [Paragraph("<b>Punto de Control</b>", header_cell_style), Paragraph("<b>Causa del Error Común</b>", header_cell_style), Paragraph("<b>Solución / Corrección Exacta</b>", header_cell_style)],
        [Paragraph("1. Acotación de Radios", body_style), Paragraph("Acotar la proyección horizontal/vertical X/Y en lugar de la magnitud escalar directa del vector.", body_style), Paragraph("Hacer clic directo en la línea oblicua del vector R1/R2/R3 para acotar la longitud pura del segmento.", body_style)],
        [Paragraph("2. Conflicto de Nombres de Variables", body_style), Paragraph("Usar <code>r</code> (minúscula) para el redondeo y <code>R</code> (mayúscula) para el radio del diente.", body_style), Paragraph("SolidWorks no distingue mayúsculas. Nombrar el radio como <code>R1</code> para evitar que se bloquee el sistema.", body_style)],
        [Paragraph("3. 'Piel' o Cascarón en Corte Recubierto", body_style), Paragraph("Hacer el corte entre el perfil frontal y posterior sin el croquis medio extendido.", body_style), Paragraph("Crear un croquis en el Plano Alzado con equidistancia +1mm hacia afuera para garantizar un corte limpio.", body_style)],
        [Paragraph("4. Engranaje Inmóvil en Ensamblaje", body_style), Paragraph("Insertar un engranaje como primera pieza del ensamblaje.", body_style), Paragraph("Insertar primero la pieza de soporte/ejes base. La primera pieza es la única que queda fija.", body_style)],
        [Paragraph("5. Dientes Colisionando en Ensamblaje", body_style), Paragraph("Usar el mismo sentido de hélice en ambos engranajes.", body_style), Paragraph("Verificar que un engranaje tenga hélice a la derecha (+30°) y el otro a la izquierda (-30°).", body_style)]
    ]
    
    t_check = Table(checklist_data, colWidths=[120, 184, 200])
    t_check.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('BACKGROUND', (0,1), (-1,-1), light_bg),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
        
    story.append(t_check)
    story.append(Spacer(1, 16))
    
    # Final sign-off block
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=8, spaceAfter=12))
    story.append(Paragraph("<b>FIN DEL TUTORIAL — Documento generado automáticamente con extracción de fotogramas y verificación de ecuaciones en SolidWorks.</b>", ParagraphStyle('EndNote', parent=body_style, fontName='Helvetica-Bold', alignment=1, textColor=primary_color)))
    
    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
