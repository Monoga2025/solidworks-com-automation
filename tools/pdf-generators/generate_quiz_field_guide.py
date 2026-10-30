from pathlib import Path
from math import pi, atan, tan, degrees
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from PIL import Image as PILImage

ROOT = Path(__file__).parent
OUT = ROOT / "GUIA_DEFINITIVA_3_QUIZ_SOLIDWORKS_STUDENT_C.pdf"

pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Consolas", r"C:\Windows\Fonts\consola.ttf"))

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#246B9E")
TEAL = colors.HexColor("#167D7F")
GOLD = colors.HexColor("#D99B2B")
RED = colors.HexColor("#A63D40")
INK = colors.HexColor("#19232D")
MUTED = colors.HexColor("#566573")
PALE = colors.HexColor("#F3F6F8")
PALE_BLUE = colors.HexColor("#EAF3F8")
PALE_GOLD = colors.HexColor("#FFF7E3")
PALE_RED = colors.HexColor("#FDEDED")
GRID = colors.HexColor("#C8D2DA")

styles = getSampleStyleSheet()
TITLE = ParagraphStyle("Title", fontName="Arial-Bold", fontSize=21, leading=25, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8)
SUBTITLE = ParagraphStyle("Subtitle", fontName="Arial", fontSize=10.5, leading=14, textColor=BLUE, alignment=TA_CENTER, spaceAfter=10)
H1 = ParagraphStyle("H1", fontName="Arial-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=8, spaceAfter=7, keepWithNext=True)
H2 = ParagraphStyle("H2", fontName="Arial-Bold", fontSize=11.5, leading=15, textColor=BLUE, spaceBefore=7, spaceAfter=5, keepWithNext=True)
BODY = ParagraphStyle("Body", fontName="Arial", fontSize=8.7, leading=12.2, textColor=INK, spaceAfter=5)
SMALL = ParagraphStyle("Small", fontName="Arial", fontSize=7.5, leading=10.2, textColor=MUTED, spaceAfter=3)
CODE = ParagraphStyle("Code", fontName="Consolas", fontSize=7.5, leading=10.5, textColor=colors.HexColor("#173F5F"), leftIndent=5, rightIndent=5, spaceAfter=3)
STEP = ParagraphStyle("Step", fontName="Arial-Bold", fontSize=9, leading=12, textColor=NAVY)
WHITE = ParagraphStyle("White", fontName="Arial-Bold", fontSize=8, leading=10, textColor=colors.white)
CENTER = ParagraphStyle("Center", parent=SMALL, alignment=TA_CENTER)


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("Arial-Bold", 7.5)
        canvas.setFillColor(NAVY)
        canvas.drawString(18*mm, 287*mm, "GUÍA DE CAMPO · 3 QUIZ SOLIDWORKS · STUDENT C")
        canvas.setStrokeColor(GRID)
        canvas.line(18*mm, 284*mm, 192*mm, 284*mm)
    canvas.setStrokeColor(GRID)
    canvas.line(18*mm, 13*mm, 192*mm, 13*mm)
    canvas.setFont("Arial", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18*mm, 8*mm, "Fuentes: clase 69:21 + video unión 3:26 + PDF/Excel/TXT del profesor")
    canvas.drawRightString(192*mm, 8*mm, f"Página {doc.page}")
    canvas.restoreState()


def fit_image(path, max_w=174*mm, max_h=82*mm):
    path = Path(path)
    with PILImage.open(path) as im:
        w, h = im.size
    scale = min(max_w / w, max_h / h)
    return Image(str(path), width=w*scale, height=h*scale)


def callout(title, text, kind="info"):
    bg, border = {
        "info": (PALE_BLUE, BLUE), "warn": (PALE_GOLD, GOLD), "danger": (PALE_RED, RED), "ok": (colors.HexColor("#EAF7F2"), TEAL)
    }[kind]
    table = Table([[Paragraph(f"<b>{title}</b><br/>{text}", BODY)]], colWidths=[174*mm])
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("BOX",(0,0),(-1,-1),1,border),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    return table


def data_table(headers, rows, widths=None, font=7.6):
    data = [[Paragraph(f"<b>{h}</b>", WHITE) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(v), ParagraphStyle("cell", parent=BODY, fontSize=font, leading=font+3)) for v in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),0.4,GRID),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE]),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)
    ]))
    return t


def step_table(rows):
    data=[]
    for number, action, verify, recover in rows:
        data.append([
            Paragraph(str(number), STEP),
            Paragraph(action, BODY),
            Paragraph(verify, SMALL),
            Paragraph(recover, SMALL),
        ])
    t=Table(data,colWidths=[10*mm,79*mm,42*mm,43*mm],repeatRows=0)
    t.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.35,GRID),("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(0,-1),PALE_BLUE),
        ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)
    ]))
    return t


def captioned(path, caption, timestamp=None, max_h=78*mm):
    cap = caption if not timestamp else f"<b>{timestamp}</b> · {caption}"
    return KeepTogether([fit_image(ROOT/path, max_h=max_h), Spacer(1,2*mm), Paragraph(cap, CENTER), Spacer(1,3*mm)])


class GuideDoc(BaseDocTemplate):
    pass


def build():
    doc=GuideDoc(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm,title="Guía definitiva 3 quiz SolidWorks - Student C")
    frame=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id="normal")
    doc.addPageTemplates(PageTemplate(id="main",frames=frame,onPage=header_footer))
    story=[]

    # Cover
    story += [Spacer(1,12*mm),Paragraph("GUÍA DEFINITIVA DE CAMPO",TITLE),Paragraph("Tres quiz de SolidWorks · Método del profesor · Caso Student C",TITLE),Paragraph("Cálculo teórico · Dos engranajes helicoidales · Ensamble funcional · Unión roscada",SUBTITLE),HRFlowable(width="100%",thickness=2,color=NAVY,spaceBefore=2,spaceAfter=10)]
    story.append(callout("Ruta rápida", "1) Completá primero la tabla de valores. 2) Modelá Z19 con la rama &lt;30. 3) Modelá Z38 con la rama ≥30 y hélice contraria. 4) Ensamblá verificando tangencia de diámetros primitivos. 5) Para la unión roscada, respetá exactamente la designación asignada y nunca rosques la arandela.","ok"))
    story.append(Spacer(1,5*mm))
    story.append(data_table(["Dato asignado","Valor"],[["Estudiante","STUDENT C"],["Z1","38 dientes"],["Z2","19 dientes"],["M","2 mm"],["Alfa / ataque","20°"],["Ángulo helicoidal","25°; sentidos opuestos entre engranajes"]],[55*mm,119*mm],9))
    story.append(Spacer(1,5*mm))
    story.append(callout("Auditoría de fuentes", "El video largo de clase dura 69:21 y contiene engranajes, ensamble y reglas de evaluación. El ZIP nuevo contiene <b>un solo video</b> de 3:26 sobre arandela y errores de configuración; no contiene los otros dos videos mencionados. La sección de unión roscada marca claramente qué está confirmado y qué depende de la fila asignada que no aparece completa en la captura.","warn"))
    story.append(PageBreak())

    # Quiz map
    story.append(Paragraph("1. Qué te evalúan y en qué orden",H1))
    story.append(data_table(["Quiz","Tiempo dicho en clase","Entrega","Punto de control"],[
        ["1 · Unión roscada","40 min","Tornillo, tuerca, contratuerca, tuerca redonda y arandela","Cada archivo con su nombre; configuración UNC/UNF correcta."],
        ["2 · Teórico","15 min","Resultados pedidos para un engranaje","Elegir rama &lt;30 o ≥30 antes de calcular."],
        ["3 · Engranajes","1 hora","Dos engranajes y ensamblaje funcional","Mismo módulo, mismo |ángulo helicoidal| y sentidos contrarios."],
    ],[24*mm,30*mm,62*mm,58*mm]))
    story.append(Spacer(1,4*mm))
    story.append(captioned("pdf_frames_dense/s44_prueba_movimiento_360.png","El resultado final se prueba girando el conjunto; no basta con que las piezas se vean juntas.","Clase 66:00–68:00"))
    story.append(callout("Regla de nombres", "El enunciado usa <b>N(#dientes)_Q(ángulo de ataque)_M(módulo)_A(ángulo hélice)</b>. Para Student C: <b>N38_Q20_M2_A25</b> y <b>N19_Q20_M2_A25</b>. La carpeta/ensamble se marca con nombre, apellido e ID.","info"))
    story.append(PageBreak())

    # Calculations dashboard
    story.append(Paragraph("2. Valores resueltos para Student C",H1))
    story.append(Paragraph("Usá estos números como control, pero mantené las fórmulas en SolidWorks. Cambiar N, Alfa o M debe reconstruir el modelo.",BODY))
    rows=[
        ["Rama","≥30","<30"],["N","38","19"],["M","2","2"],["Alfa","20°","20°"],["De","80.00","42.00"],["Dp","76.00","38.00"],["Ct","71.42","35.71"],["Di","71.00","33.33"],["Par / Pitch","6.28","6.28"],["Delta","2.37°","4.74°"],["R1","9.50","2.58"],["R2","—","8.13"],["R3","—","12.20"],["r","0.60","0.60"],["Acara","8.00","8.00"],["Chaflán","1.56","0.80"],["P/4","1.57","—"],["Dist_Plan","40.00","—"],
    ]
    story.append(data_table(rows[0],rows[1:],[54*mm,60*mm,60*mm],8.5))
    story.append(Spacer(1,4*mm))
    story.append(callout("Ángulos posteriores calculados", "Con el método geométrico observado: θ = atan[(Acara·tan β)/(De/2)]. Para Z38: θ≈<b>5.33°</b>, por lo que los perfiles frontal/posterior se giran ±<b>2.66°</b>. Para Z19: θ≈<b>10.07°</b>, por lo que se giran ±<b>5.04°</b>. Verificá la medición en tu propio croquis antes del corte recubierto.","info"))
    story.append(PageBreak())

    # Exact equations
    story.append(Paragraph("3. Tabla de ecuaciones: copiar sin renombrar",H1))
    story.append(Paragraph("Para <b>Z19</b> partí de <code>Equations -30.txt</code> y cambiá solo N=19, Alfa=20 y M=2. Para <b>Z38</b> partí de <code>Engranaje +30 (2).txt</code> y cambiá solo N=38, Alfa=20 y M=2.",BODY))
    eq_common=[["De",'ROUND("M"*("N"+2),2)'],["Dp",'ROUND("N"*"M",2)'],["Ct",'ROUND(IF("Alfa"=14,"Dp"*0.96815,IF("Alfa"=15,"Dp"*0.96592,IF("Alfa"=20,"Dp"*0.93969,0))),2)'],["Par",'ROUND("M"*PI,2)'],["Delta",'ROUND(90/"N",2)'],["r",'ROUND("M"*0.3,2)'],["Acara",'ROUND("M"*4,2)'],["Chaflan",'ROUND(("Dp"+"De")/100,2)']]
    story.append(data_table(["Variable","Expresión exacta común"],eq_common,[38*mm,136*mm],7.3))
    story.append(Spacer(1,3*mm))
    story.append(data_table(["Rama <30 · Z19","Expresión"],[["Di",'ROUND("Dp"-(2*("M"*1.167)),2)'],["R1",'ROUND(IF("Alfa"=20,"Dp"*0.068,"Dp"*0.07),2)'],["R2",'ROUND(IF("Alfa"=20,"Dp"*0.214,"Dp"*0.22),2)'],["R3",'ROUND(IF("Alfa"=20,"Dp"*0.321,"Dp"*0.33),2)']],[48*mm,126*mm],7.3))
    story.append(Spacer(1,3*mm))
    story.append(data_table(["Rama ≥30 · Z38","Expresión"],[["Di",'ROUND("Dp"-(2*("M"*1.25)),2)'],["R1",'ROUND("Dp"/8,2)'],["Dist_Plan",'ROUND("De"/2,2)'],["P/4",'ROUND("Par"/4,2)']],[48*mm,126*mm],7.3))
    story.append(callout("Gotcha de nombres", "SolidWorks no diferencia mayúsculas y minúsculas. El profesor conserva <b>R1</b> como radio único de Z≥30 porque <b>r</b> ya identifica el redondeo del pie.","danger"))
    story.append(PageBreak())

    # Common base
    story.append(Paragraph("4. Base común de ambos engranajes",H1))
    steps=[
        (1,"Nuevo documento de <b>Pieza</b>. Antes de dibujar, importá/pegá la tabla correcta en Herramientas → Ecuaciones.","N, Alfa y M aparecen como variables globales.","Si una ecuación queda roja, revisá comillas, separador decimal y nombres duplicados."),
        (2,"Plano Alzado → Croquis. Dibujá círculo del eje y chavetero; vinculá sus cotas a las variables/dimensiones indicadas.","Croquis completamente definido.","No dejes líneas duplicadas ni el círculo atravesando el chavetero."),
        (3,"Saliente/Base extruido → <b>Plano medio</b> → profundidad <b>= Acara</b>.","Z19 y Z38 quedan de 8 mm de ancho.","Si crece solo hacia un lado, no elegiste Plano medio."),
        (4,"Chaflán en las dos aristas externas → <b>= Chaflan</b>.","Z19=0.80 mm; Z38=1.56 mm.","Seleccioná ambas aristas antes de aceptar."),
    ]
    story.append(step_table(steps))
    story.append(Spacer(1,4*mm))
    story.append(captioned("pdf_frames_dense/s06_extrusion_plano_medio.png","Extrusión obligatoriamente en Plano medio y vinculada a Acara.","Clase 01:30–02:30"))
    story.append(captioned("pdf_frames_dense/s07_aplicacion_chaflan.png","Chaflán en ambas caras; el valor proviene de la tabla.","Clase 02:30–03:00"))
    story.append(PageBreak())

    # Z19 tracing
    story.append(Paragraph("5. Engranaje Z19 · rama menor de 30 dientes",H1))
    story.append(callout("Valores de esta pieza", "N=19 · M=2 · Alfa=20° · De=42 · Dp=38 · Ct=35.71 · Di=33.33 · Delta=4.74° · R1=2.58 · R2=8.13 · R3=12.20 · r=0.60 · Acara=8 · hélice 25°.","ok"))
    z19a=[
        (1,"En la cara frontal creá un <b>croquis de trazado separado</b>. Convertí De y dibujá Dp, Ct y Di concéntricos.","Cuatro circunferencias reconocibles y etiquetadas.","El PDF dice que este trazado separado es obligatorio para calificar el proceso."),
        (2,"Convertí Dp a geometría de construcción. Editá el texto de cada cota como DE, DP, CT y DI.","El árbol conserva un croquis solo de construcción.","No confundas Ct con diámetro primitivo."),
        (3,"Desde el centro, línea vertical y línea inclinada. Acotá el ángulo <b>= Delta = 4.74°</b>.","La inclinada corta Di y orienta el flanco.","Si el perfil queda invertido, abriste Delta al lado incorrecto."),
        (4,"Desde intersección Delta–Di trazá vector constructivo hasta Ct y acotá la <b>longitud oblicua</b> = R1.","R1=2.58 sobre el vector completo.","No acotes su componente X: el profesor advierte que arruina todo el perfil."),
        (5,"Con centro en el extremo de R1, creá círculo/arco y dejá solo el tramo <b>Di→Ct</b>.","Primer arco limpio.","Recortá ambos sobrantes; no borres los círculos guía."),
        (6,"Desde el final anterior, vector R2; arco <b>Ct→Dp</b>. Repetí con R3 para <b>Dp→De</b>.","Tres arcos tangenciales de raíz a cresta.","Si no coinciden, revisá que el punto inicial sea el final del arco anterior."),
    ]
    story.append(step_table(z19a))
    story.append(captioned("pdf_frames_dense/s12_vector_r1_ct.png","Acotar la magnitud completa del vector R1, no una proyección.","Clase 06:30–08:00"))
    story.append(captioned("pdf_frames_dense/s17_arco_r3_recorte.png","Orden exacto de arcos: R1 Di→Ct, R2 Ct→Dp, R3 Dp→De.","Clase 08:00–10:30"))
    story.append(PageBreak())

    # Z19 loft
    story.append(Paragraph("6. Z19 · perfil cerrado, hélice y corte recubierto",H1))
    z19b=[
        (7,"Nuevo croquis en cara frontal. Convertí Di, De y los tres arcos; simetría de los arcos respecto de la vertical; recortá hasta obtener <b>un único contorno cerrado</b>.","Solo queda el hueco de un diente.","Ocultá el trazado original; no lo borres."),
        (8,"Plano de referencia tangente a De. En ese plano dibujá línea frontal→posterior y acotá <b>25°</b>.","La directriz muestra el sentido de hélice.","Para la otra pieza el sentido debe ser contrario."),
        (9,"En la cara posterior medí el giro: control aproximado θ=<b>10.07°</b>.","Valor cercano a 10.07°.","Si difiere mucho, revisá Acara=8, De=42 y hélice=25°."),
        (10,"En Plano Alzado (mitad), convertí el perfil y aplicá Equidistanciar <b>1 mm hacia afuera</b>. Convertí la línea original a construcción.","Perfil medio más grande y cerrado.","Sin +1 mm aparece un cascarón residual después del loft."),
        (11,"Girado de perfiles: frontal <b>+5.04°</b>, posterior <b>−5.04°</b>; el medio queda centrado.","Tres perfiles ordenados y simétricos.","No gires 10.07° completo en cada cara."),
        (12,"Operaciones → <b>Corte recubierto</b>. Selección: frontal → medio +1 mm → posterior.","Se elimina un hueco helicoidal continuo.","Si falla: revisar perfiles cerrados, sin dobles líneas y en orden."),
        (13,"Redondeá las dos aristas del pie con <b>r=0.60</b>. Matriz circular, separación igual 360°, <b>19</b> instancias, incluyendo corte y redondeo.","19 espacios uniformes.","Si la matriz falla, seleccioná el eje/cara cilíndrica y ambas operaciones."),
    ]
    story.append(step_table(z19b))
    story.append(captioned("pdf_frames_dense/s24_equidistanciar_1mm_trampa.png","El perfil medio debe sobresalir 1 mm; la línea original queda constructiva.","Clase 15:30–17:30"))
    story.append(captioned("pdf_frames_dense/s27_corte_recubierto_seleccion.png","Orden de selección del Corte recubierto.","Clase 25:30–26:30"))
    story.append(PageBreak())

    # Z38 branch
    story.append(Paragraph("7. Engranaje Z38 · rama de 30 dientes o más",H1))
    story.append(callout("Valores de esta pieza", "N=38 · M=2 · Alfa=20° · De=80 · Dp=76 · Ct=71.42 · Di=71.00 · Delta=2.37° · R1 único=9.50 · P/4=1.57 · r=0.60 · Acara=8 · hélice opuesta −25°.","ok"))
    z38=[
        (1,"Repetí base, agujero/chavetero, Plano medio y chaflán con la tabla ≥30.","Disco De=80, ancho 8.","No reutilices Di de la rama <30: acá usa factor 1.25."),
        (2,"Croquis de trazado separado con De, Dp, Ct y Di. Desde el eje vertical trazá horizontal constructiva <b>P/4=1.57</b>.","La horizontal termina en la referencia indicada por el profesor.","No uses P/2; la clase corrige explícitamente a P/4."),
        (3,"Uní el extremo de P/4 con el centro. En la intersección de esa inclinada con Dp, trazá vector hasta Ct de longitud <b>R1=9.50</b>.","Un único centro de arco.","En cotas puede verse R; en ecuaciones se conserva R1 para evitar conflicto con r."),
        (4,"Generá un solo arco y recortalo para dejar el perfil entre <b>Di y De</b>.","Perfil simplificado de un arco.","Aunque Ct/Dp cambien de orden, el diente siempre se talla entre Di y De."),
        (5,"Convertí De, Di y arco; simetría; contorno cerrado. Plano tangente usando <b>Dist_Plan=40</b>.","Plano realmente tangente a De.","El profesor evita amarrar el plano a una línea que luego deba girarse."),
        (6,"Hélice en sentido contrario: <b>−25°</b>. Giro posterior esperado θ≈<b>5.33°</b>; perfiles ±<b>2.66°</b>.","Dientes opuestos a Z19.","Si ambos van al mismo lado, no engranan correctamente."),
        (7,"Perfil medio +1 mm, Corte recubierto, redondeo r=0.60 y matriz circular de <b>38</b> instancias.","Pieza completa sin cascarón.","Si queda una piel exterior, el perfil medio no era mayor."),
    ]
    story.append(step_table(z38))
    story.append(captioned("pdf_frames_dense/s32_n33_horizontal_p_cuarto.png","La rama ≥30 empieza con el desplazamiento P/4.","Clase 35:00–36:00"))
    story.append(captioned("pdf_frames_dense/s34_n33_arco_unico_r1.png","Un solo R1; no existen R2/R3 en esta rama.","Clase 36:00–37:30"))
    story.append(captioned("pdf_frames_dense/s35_n33_helice_opuesta_30deg.png","La segunda hélice debe ir en sentido contrario.","Clase 40:30–42:30"))
    story.append(PageBreak())

    # Assembly
    story.append(Paragraph("8. Ensamblaje funcional",H1))
    story.append(callout("Distancia exacta entre ejes", "(Dp38/2)+(Dp19/2) = 76/2 + 38/2 = <b>57.00 mm</b>. Esta distancia hace tangentes los círculos primitivos.","ok"))
    assy=[
        (1,"Pieza soporte: croquis con dos líneas/ejes constructivos separados <b>57 mm</b>. Extrusión simétrica mayor que Acara.","Dos referencias limpias para posicionar centros.","No uses De para la distancia; siempre Dp."),
        (2,"Nuevo Ensamblaje. Insertá primero el soporte y hacé coincidir origen con origen; fijalo.","Soporte inmóvil.","La primera pieza queda fijada; si insertás primero un engranaje, después cuesta posicionar todo."),
        (3,"Insertá Z38 y Z19. Relación concéntrica de cada agujero con su eje; relación de ancho/centrado respecto del soporte.","Ambos giran sin trasladarse.","No fijes los engranajes; solo sus ejes/posición axial."),
        (4,"Verificá tangencia visual de Dp=76 y Dp=38. Si no coincide, corregí centros a 57 mm.","Primitivos tangentes.","Que los exteriores se toquen no valida el engrane."),
        (5,"Relación de posición → Mecánicas → Engranaje. Seleccioná caras cilíndricas/ejes y relación <b>38:19 = 2:1</b>.","Al girar Z38, Z19 gira al doble y en sentido contrario.","Si giran como ruedas lisas, falta la relación mecánica de engranaje."),
        (6,"Prueba 360°. Revisá interferencia, sentido de hélice y reconstrucción sin errores.","Movimiento continuo.","Si se cruzan, revisá hélices opuestas y posición axial."),
    ]
    story.append(step_table(assy))
    story.append(captioned("pdf_frames_dense/s39_soporte_distancia_centros.png","Soporte con distancia entre ejes definida desde los diámetros primitivos.","Clase 54:00–56:30"))
    story.append(captioned("pdf_frames_dense/s43_relacion_mecanica_engranaje.png","La relación mecánica convierte el conjunto en engranaje funcional.","Clase 60:30–66:00"))
    story.append(PageBreak())

    # Theory quiz
    story.append(Paragraph("9. Quiz teórico: respuesta sin perder tiempo",H1))
    story.append(Paragraph("El formulario puede pedir un solo engranaje. Identificá N primero y usá la columna correspondiente de la tabla de la página 3.",BODY))
    story.append(data_table(["Si te piden…","Z38","Z19"],[
        ["K / coeficiente Ct (Alfa 20)","0.93969","0.93969"],["Ct","71.42","35.71"],["De","80.00","42.00"],["Dp","76.00","38.00"],["Di","71.00","33.33"],["P / Par","6.28","6.28"],["R1","9.50","2.58"],["R2","No aplica","8.13"],["R3","No aplica","12.20"],["r","0.60","0.60"],["Delta","2.37°","4.74°"],
    ],[70*mm,52*mm,52*mm],8.5))
    story.append(Spacer(1,4*mm))
    story.append(callout("Control lógico", "Los dos engranajes tienen el mismo M y Alfa. Por eso comparten Par/Pitch y r. Z38 tiene Dp exactamente el doble de Z19; la relación cinemática es 2:1.","info"))
    story.append(callout("No mezclar nomenclaturas", "En el archivo del profesor, <b>Ct</b> es el círculo de trazado calculado con coeficiente por Alfa, mientras <b>Par/Pitch</b> es M·π. Copiá los nombres tal como aparecen en la plantilla entregada.","danger"))
    story.append(PageBreak())

    # Threaded union
    story.append(Paragraph("10. Unión roscada: lo confirmado por el video nuevo",H1))
    story.append(callout("Límite de evidencia", "La fila de Student C para la unión roscada no aparece en la captura disponible y el ZIP contiene solo un video de advertencias, no los cinco tutoriales completos. No inventes diámetro, TPI, serie UNC/UNF, clase, longitud de vástago ni longitud roscada: copialos de tu fila asignada.","warn"))
    union=[
        (1,"Arandela: Plano Alzado → dos círculos concéntricos. Interior = diámetro nominal/libre indicado; exterior = valor de tabla.","Dos círculos, una sola región anular.","Si hay más operaciones de las necesarias, simplificá."),
        (2,"Saliente/Base → Plano medio → <b>4 mm</b> en el ejemplo mostrado.","Una sola extrusión.","El profesor la llama cuello/arandela y muestra una única operación."),
        (3,"<b>No aplicar rosca al agujero de la arandela.</b>","Árbol sin Taladro roscado/Rosca en arandela.","Este error fue señalado explícitamente como grave."),
        (4,"Para tornillo/tuercas, calculá paso: <b>paso mm = 25.4 / TPI</b>.","El paso coincide con la designación UNC/UNF.","No confundas TPI con paso en mm."),
        (5,"Si reutilizás una pieza, cambiá no solo el diámetro visible: actualizá designación, estándar, clase, diámetro nominal, profundidad y longitud roscada.","Información del Taladro roscado coincide con la nueva designación.","El video muestra piezas visualmente cambiadas pero con metadatos/rosca anteriores: se califican mal."),
        (6,"Guardar exactamente: tornillo, tuerca, contratuerca, tuerca redonda y arandela; carpeta primerapellido-primernombre-ID.","Cinco archivos separados con nombres correctos.","No comprimas antes de abrir cada archivo y reconstruir."),
    ]
    story.append(step_table(union))
    story.append(captioned("source_media/union_frames/t24.jpg","Arandela: diámetro exterior 55 mm en la configuración mostrada; el interior depende del nominal asignado.","Video unión 00:19–00:34"))
    story.append(captioned("source_media/union_frames/t53.jpg","Resultado de la única operación de extrusión de la arandela.","Video unión 00:48–01:07"))
    story.append(PageBreak())
    story.append(Paragraph("11. Errores de unión roscada que bajan la nota",H1))
    story.append(captioned("source_media/union_frames/t136.jpg","El árbol muestra Taladro roscado: la información debe coincidir con el nominal y la profundidad reales.","Video unión 02:12–02:48"))
    story.append(data_table(["Síntoma","Causa","Corrección"],[
        ["Arandela con rosca","Se aplicó Rosca/Taladro roscado al agujero","Eliminar la operación; la arandela es un anillo liso."],
        ["La pieza parece 3/4 pero propiedades dicen 1 pulgada","Se cambió geometría sin cambiar configuración","Editar la operación y escoger la designación completa correcta."],
        ["Profundidad o longitud roscada incorrecta","Se conservó el valor de otra pieza","Introducir longitud de vástago y longitud roscada de la fila asignada."],
        ["Rosca demasiado gruesa/fina","Se usó TPI como milímetros","Calcular 25.4/TPI y conservar UNC/UNF/clase."],
        ["Archivo correcto pero nombre incorrecto","No se siguió el formato del enunciado","Renombrar pieza y carpeta antes de comprimir."],
    ],[48*mm,58*mm,68*mm],7.7))
    story.append(PageBreak())

    # Recovery matrix
    story.append(Paragraph("12. Matriz de rescate: si te estancás, hacé esto",H1))
    story.append(data_table(["Falla","Diagnóstico rápido","Acción exacta"],[
        ["Ecuación roja","Nombre duplicado o comillas incorrectas","Usar R1 para radio ≥30 y r para redondeo; pegar sintaxis del TXT."],
        ["Croquis no cierra","Entidad doble, sobrante o línea no constructiva","Mostrar relaciones, recortar sobrantes y convertir guías a construcción."],
        ["Corte recubierto falla","Perfil abierto o selección fuera de orden","Comprobar frontal/medio/posterior cerrados; seleccionar en ese orden."],
        ["Queda cascarón","Perfil medio del mismo tamaño","Equidistanciar exactamente 1 mm hacia afuera."],
        ["Matriz circular falla","Eje u operaciones incorrectas","Seleccionar cara/eje cilíndrico; incluir corte recubierto y redondeo."],
        ["Dientes no parecen helicoidales","Perfiles sin giro o mismo signo","Usar ±θ/2; hélices opuestas entre piezas."],
        ["Engranajes no tocan","Centros calculados con De","Cambiar distancia a (Dp1+Dp2)/2 = 57 mm."],
        ["Uno no gira","Pieza fijada o sin mate mecánico","Desfijar engranajes; conservar soporte fijo; crear mate Engranaje 38:19."],
        ["Reconstrucción rompe todo","Se borró una referencia padre","Ocultar croquis/planos en vez de borrarlos."],
    ],[45*mm,58*mm,71*mm],7.4))
    story.append(Spacer(1,5*mm))
    story.append(callout("Regla del profesor", "No hagas pasos por imitación sin entender la referencia. Cada croquis debe mostrar qué variable controla la geometría y cada operación debe conservar sus padres.","danger"))
    story.append(PageBreak())

    # Final checklist
    story.append(Paragraph("13. Lista final antes de comprimir y enviar",H1))
    checks=[
        "□ Z19 usa rama <30 con R1/R2/R3; Z38 usa rama ≥30 con un solo R1.",
        "□ Los croquis de trazado permanecen separados y visibles en el árbol cuando se necesiten para revisión.",
        "□ Ambos engranajes tienen M=2, Alfa=20° y |hélice|=25°, pero sentidos opuestos.",
        "□ Acara=8 mm en ambas piezas y las extrusiones están en Plano medio.",
        "□ Perfiles medios del corte recubierto tienen +1 mm; no hay cascarones.",
        "□ Matrices: 19 y 38 instancias; incluyen corte y redondeo.",
        "□ Distancia entre centros=57 mm y los círculos primitivos son tangentes.",
        "□ Mate mecánico 38:19; prueba manual de giro completa.",
        "□ Arandela sin rosca; cinco componentes roscados guardados por separado.",
        "□ Designación, TPI, UNC/UNF, clase, profundidades y longitudes coinciden con la fila asignada.",
        "□ Nombres de piezas/carpeta cumplen el formato del enunciado.",
        "□ Abriste cada archivo después de guardar y no muestra errores de reconstrucción.",
    ]
    for item in checks:
        story.append(Paragraph(item,ParagraphStyle("check",parent=BODY,fontSize=10,leading=15,leftIndent=5,spaceAfter=5)))
    story.append(Spacer(1,4*mm))
    story.append(callout("Fuente temporal", "Engranajes: clase 00:00–66:30. Reglas del quiz: 66:30–68:00. Unión/arandela: video nuevo 00:00–03:26. Fórmulas: Plantilla_Calculo_Engranajes.xlsx y los dos TXT entregados.","info"))
    story.append(Paragraph("Fin de la guía · Trabajá siempre desde las ecuaciones y verificá cada reconstrucción antes del siguiente paso.",ParagraphStyle("end",parent=SUBTITLE,fontSize=11,spaceBefore=12)))

    doc.build(story)
    print(OUT)

if __name__ == "__main__":
    build()
