from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
from PIL import Image as PILImage

BASE=Path(__file__).resolve().parents[1]
FRAMES=BASE/'04_Fotogramas'/'Union_Roscada'
OUT=BASE/'01_Manual'/'QUIZ_1_UNION_ROSCADA_STUDENT_A_PASO_A_PASO.pdf'
pdfmetrics.registerFont(TTFont('Arial',r'C:\Windows\Fonts\arial.ttf')); pdfmetrics.registerFont(TTFont('Arial-Bold',r'C:\Windows\Fonts\arialbd.ttf'))
NAVY=colors.HexColor('#17324D'); BLUE=colors.HexColor('#246B9E'); GOLD=colors.HexColor('#D99B2B'); RED=colors.HexColor('#A63D40'); PALE=colors.HexColor('#F3F6F8'); GRID=colors.HexColor('#C8D2DA'); INK=colors.HexColor('#19232D')
TITLE=ParagraphStyle('t',fontName='Arial-Bold',fontSize=20,leading=24,textColor=NAVY,spaceAfter=8)
H1=ParagraphStyle('h1',fontName='Arial-Bold',fontSize=15,leading=19,textColor=NAVY,spaceAfter=7,spaceBefore=5,keepWithNext=True)
H2=ParagraphStyle('h2',fontName='Arial-Bold',fontSize=11,leading=14,textColor=BLUE,spaceAfter=4,keepWithNext=True)
BODY=ParagraphStyle('b',fontName='Arial',fontSize=8.8,leading=12.2,textColor=INK,spaceAfter=4)
SMALL=ParagraphStyle('s',fontName='Arial',fontSize=7.5,leading=10,textColor=colors.HexColor('#566573'))
WHITE=ParagraphStyle('w',fontName='Arial-Bold',fontSize=8,leading=10,textColor=colors.white)
STEP=ParagraphStyle('st',fontName='Arial-Bold',fontSize=9,leading=12,textColor=NAVY)

def hf(canvas,doc):
 canvas.saveState(); canvas.setStrokeColor(GRID); canvas.line(18*mm,13*mm,192*mm,13*mm); canvas.setFont('Arial',7); canvas.setFillColor(colors.HexColor('#566573')); canvas.drawString(18*mm,8*mm,'Video de clase 23:44 · Transcripción local con timestamps'); canvas.drawRightString(192*mm,8*mm,f'Página {doc.page}'); canvas.restoreState()

def image(prefix,maxh=75*mm):
 p=next(FRAMES.glob(prefix+'*.jpg')); im=PILImage.open(p); w,h=im.size; scale=min(174*mm/w,maxh/h); return Image(str(p),width=w*scale,height=h*scale)

def pic(prefix,cap): return KeepTogether([image(prefix),Spacer(1,2*mm),Paragraph(cap,SMALL),Spacer(1,3*mm)])

def box(title,text,color=BLUE,bg=colors.HexColor('#EAF3F8')):
 t=Table([[Paragraph(f'<b>{title}</b><br/>{text}',BODY)]],colWidths=[174*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1,color),('PADDING',(0,0),(-1,-1),7)])); return t

def steps(rows):
 data=[]
 for n,a,v,r in rows:data.append([Paragraph(str(n),STEP),Paragraph(a,BODY),Paragraph(v,SMALL),Paragraph(r,SMALL)])
 t=Table(data,colWidths=[10*mm,80*mm,42*mm,42*mm]); t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.35,GRID),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#EAF3F8')),('PADDING',(0,0),(-1,-1),4)])); return t

def table(headers,rows,widths):
 data=[[Paragraph(f'<b>{x}</b>',WHITE) for x in headers]]+[[Paragraph(str(x),BODY) for x in r] for r in rows]
 t=Table(data,colWidths=widths,repeatRows=1); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('GRID',(0,0),(-1,-1),.4,GRID),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('PADDING',(0,0),(-1,-1),4)])); return t

def build():
 doc=BaseDocTemplate(str(OUT),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=18*mm); doc.addPageTemplates(PageTemplate(id='p',frames=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id='f'),onPage=hf)); s=[]
 s += [Spacer(1,7*mm),Paragraph('QUIZ 1 · UNIÓN ROSCADA',TITLE),Paragraph('Student A · 1 1/2”-6 UNC-2A',ParagraphStyle('sub',parent=BODY,fontSize=12,textColor=BLUE)),Paragraph('Tornillo · Tuerca · Contratuerca · Tuerca redonda · Arandela',ParagraphStyle('sub2',parent=BODY,fontSize=10,textColor=NAVY)),HRFlowable(width='100%',thickness=2,color=NAVY,spaceAfter=8)]
 s.append(box('Tus datos confirmados','Diámetro nominal <b>1 1/2” = 38.1000 mm</b> · 6 TPI · UNC · clase externa 2A / interna 2B · vástago <b>3” = 76.2000 mm</b> · rosca <b>2.5” = 63.5000 mm</b> · paso <b>1/6” = 4.2333 mm</b>.',BLUE,colors.HexColor('#EAF3F8')))
 s.append(Spacer(1,3*mm)); s.append(table(['Dimensión de tu fila','Valor'],[['Altura cabeza','33.78 mm'],['Altura tuerca','38.61 mm'],['Altura contratuerca','29 mm'],['Entre caras / entre aristas','61.20 / 70.61 mm'],['Tuerca redonda','Ø61.20 × 29 mm'],['Arandela','Ø interior 38.10 · Ø exterior 78 · espesor 6 mm'],['Documento / material','MMGS · 4 decimales · AISI 1020']],[82*mm,92*mm]))
 s.append(pic('01_unidades','00:00–00:52 · Propiedades del documento: trabajar con cuatro decimales para evitar que el paso redondeado haga intersectar la rosca.'))
 s.append(PageBreak())

 s.append(Paragraph('1. Tornillo · vástago y cabeza',H1))
 s.append(steps([(1,'Plano Alzado → Croquis → círculo centrado. Cota <b>1.5”</b> o <b>38.1000 mm</b>.','Un círculo negro centrado en el origen.','Si no convierte pulgadas, escribí 1.5in.'),(2,'Operaciones → Saliente/Base. Longitud <b>3” = 76.2000 mm</b>.','Cilindro recto del vástago.','No uses 63.5: esa es solo la parte roscada.'),(3,'Seleccioná la cara posterior → Croquis → círculo Ø<b>70.61 mm</b> → Saliente/Base <b>33.78 mm</b>.','Segundo cilindro unido al vástago.','70.61 es entre aristas; 33.78 es altura de cabeza.'),(4,'Seleccioná la arista frontal de la cabeza → Redondeo <b>6 mm</b>.','Borde frontal suavizado.','6 mm viene del espesor de tu arandela.')]))
 s.append(pic('02_vastago','01:05–01:41 · Vástago nominal y longitud total.')); s.append(pic('04_medidas_cabeza','01:46–02:34 · La tabla define distancia entre aristas y altura de cabeza.'))
 s.append(PageBreak())

 s.append(Paragraph('2. Cabeza hexagonal',H1))
 s.append(steps([(5,'Cara frontal de cabeza → Croquis → Polígono de <b>6 lados</b>, centrado. Acotá la distancia entre caras a <b>61.20 mm</b>.','Hexágono concéntrico dentro del círculo Ø70.61.','No acotes entre vértices: el valor 61.20 es entre caras.'),(6,'Operaciones → Extruir corte → Por todo → <b>Invertir lado a cortar</b>.','Se elimina el anillo exterior y queda la cabeza hexagonal.','Si desaparece el hexágono, cancelá e invertí el lado.'),(7,'Redondeo en la unión cabeza-vástago <b>3 mm</b>. Chaflán frontal <b>3 mm</b>.','Cabeza acabada sin aristas agresivas.','3 mm es la mitad del redondeo frontal de 6 mm.')]))
 s.append(pic('05_corte_hexagonal','02:59–04:02 · El corte hexagonal exige “Invertir lado a cortar” para conservar la cabeza.'))
 s.append(PageBreak())

 s.append(Paragraph('3. Hélice de la rosca',H1))
 s.append(steps([(8,'En la cara frontal libre del vástago → Croquis → Convertir entidades sobre el borde Ø38.10.','Círculo coincidente con el vástago.','No uses diámetro exterior de la cabeza.'),(9,'Operaciones → Curvas → Hélice/Espiral → <b>Altura y paso</b>. Altura <b>2.5” = 63.5000 mm</b>; paso <b>1/6” = 4.2333 mm</b>.','La hélice ocupa solo 63.5 mm del vástago.','No escribas 6 como paso: 6 es TPI.'),(10,'Activá <b>Invertir dirección</b> para que la hélice avance hacia la cabeza. Ángulo inicial <b>0°</b>.','Hélice dentro del cilindro, arrancando sobre Plano Planta.','Si sale hacia afuera, invertí dirección antes de aceptar.')]))
 s.append(pic('06_croquis_helice','04:02–04:32 · Croquis circular que origina la hélice.')); s.append(pic('08_direccion_angulo_helice','04:32–06:04 · Altura/paso, dirección invertida y ángulo inicial 0°.'))
 s.append(PageBreak())

 s.append(Paragraph('4. Perfil de rosca y corte barrido',H1))
 s.append(steps([(11,'Plano Planta → Croquis. Dibujá el perfil negativo triangular mostrado por el profesor, ángulo incluido <b>55°</b>, punta hacia el cilindro.','Triángulo alineado con el inicio de hélice.','Aunque la designación es UNC, para este quiz seguí el perfil de 55° mostrado en clase.'),(12,'Acotá el paso del perfil <b>4.2333 mm</b>. Base como construcción. Redondeos de cresta/raíz: <b>0.1373×P = 0.5812 mm</b>.','Perfil suave y cerrado.','Trabajá con 4 decimales para evitar solape.'),(13,'Cerrá el perfil sin superar los 4.2333 mm y hacelo sobresalir aproximadamente 2 mm.','Un solo contorno cerrado.','Si supera una vuelta, el corte se auto-intersecta.'),(14,'Relación Perforar entre un punto cercano a la punta del perfil y el inicio de la hélice.','Perfil enganchado y sin grados de libertad críticos.','No elijas la punta exacta si la relación falla.'),(15,'Operaciones → Corte barrido. Perfil = croquis; trayectoria = hélice.','Rosca tallada durante 63.5 mm.','Si falla: 4 decimales, 4.2333 exacto, perfil cerrado y sin solape.')]))
 s.append(pic('09_perfil_rosca','06:04–07:16 · Perfil negativo de 55°; la tabla de roscas es la autoridad.')); s.append(pic('11_cierre_perfil','07:16–10:40 · Redondeos, cierre y sobresaliente para evitar cascarón.')); s.append(pic('12_corte_barrido','10:40–11:46 · Corte barrido: perfil + hélice.'))
 s.append(PageBreak())

 s.append(Paragraph('5. Terminación del tornillo',H1))
 s.append(steps([(16,'En la cara final, convertí el contorno y aplicá Extruir corte → Por todo para limpiar el inicio/fin de la hélice.','Rosca termina con cara limpia.','No dejes media vuelta sobresaliendo.'),(17,'Asigná material <b>AISI 1020</b>. Guardá como <b>tornillo.SLDPRT</b>.','Tornillo completo y reconstruido.','Abrilo otra vez antes de reutilizarlo.')]))
 s.append(pic('13_corte_final_rosca','11:46–12:24 · Corte final para limpiar la salida de rosca.')); s.append(pic('14_tornillo_terminado','12:24–12:48 · Tornillo terminado antes de iniciar las tuercas.'))
 s.append(PageBreak())

 s.append(Paragraph('6. Tuerca',H1))
 s.append(steps([(18,'Nueva pieza; MMGS y 4 decimales. Plano Alzado → círculo Ø<b>70.61 mm</b> → Saliente/Base <b>38.61 mm</b>, condición <b>Plano medio</b>.','Cilindro simétrico.','No uses 33.78: esa es la cabeza del tornillo.'),(19,'Redondeo frontal <b>6 mm</b>. En la cara, hexágono entre caras <b>61.20 mm</b> → Corte Por todo → Invertir lado a cortar.','Exterior hexagonal terminado.','Debe conservarse el centro para el agujero.'),(20,'Operaciones → Asistente para taladro → Tapón recto → Pulgadas → Taladro roscado → <b>1 1/2”-6 UNC</b> → Por todo.','Designación exacta de Student A.','No elijas UNF ni otro TPI.'),(21,'Activá clase de rosca interna <b>2B</b>. Desactivá opciones de avellanado.','Clase interna compatible con tornillo 2A.','A es externa; B es interna.'),(22,'Posiciones → cara frontal → punto coincidente con el origen. Aceptá y guardá como <b>tuerca.SLDPRT</b>.','Agujero centrado y árbol sin errores.','Abrí Información de rosca y confirmá 1 1/2”-6 UNC-2B.')]))
 s.append(pic('15_tuerca_cilindro','12:48–13:49 · Cilindro base de tuerca, Plano medio.')); s.append(pic('16_asistente_taladro','15:25–16:51 · Asistente para taladro roscado: estándar, tamaño y clase.'))
 s.append(PageBreak())

 s.append(Paragraph('7. Contratuerca y tuerca redonda',H1))
 s.append(steps([(23,'Con la tuerca abierta: Guardar como <b>contratuerca.SLDPRT</b>. Después cambiá la extrusión de 38.61 a <b>29 mm</b> y redondeá ambos lados.','Contratuerca de 29 mm, archivo independiente.','Guardar como tiene que ocurrir antes de modificar.'),(24,'Guardar como <b>tuerca_redonda.SLDPRT</b>. Eliminá el corte hexagonal y cambiá el croquis inicial a Ø<b>61.20 mm</b>; conservá altura 29 mm y taladro 1 1/2”-6 UNC-2B.','Cilindro roscado Ø61.20 × 29.','Si se vuelve hexagonal, no eliminaste/suprimiste el corte.'),(25,'Cerrá y reabrí tuerca, contratuerca y tuerca redonda.','Tres geometrías diferentes.','Si dos se ven iguales, probablemente sobrescribiste una pieza.')]))
 s.append(pic('18_contratuerca','16:51–17:28 · Contratuerca: altura propia y redondeo en ambos lados.')); s.append(pic('19_tuerca_redonda','17:28–18:26 · Tuerca redonda: eliminar corte hexagonal y usar diámetro de su columna.'))
 s.append(PageBreak())

 s.append(Paragraph('8. Arandela',H1))
 s.append(steps([(26,'Nueva pieza. Plano Alzado → dos círculos concéntricos: interior Ø<b>38.10 mm</b>; exterior Ø<b>78 mm</b>.','Una región anular centrada.','No uses 61.20: ese es el diámetro de la tuerca redonda.'),(27,'Saliente/Base → <b>Plano medio</b> → espesor <b>6 mm</b>.','Una arandela simple.','Solo debe existir una extrusión.'),(28,'Guardar como <b>arandela.SLDPRT</b>. <b>No aplicar ninguna rosca.</b>','Árbol sin Rosca ni Taladro roscado.','Roscar la arandela fue señalado como error grave.')]))
 s.append(pic('20_arandela_dos_circulos','18:35–19:06 · Dos círculos: nominal interior y diámetro exterior de tabla.')); s.append(pic('21_arandela_final','19:06–19:18 · Arandela final: una extrusión, sin rosca.'))
 s.append(PageBreak())

 s.append(Paragraph('9. Errores que el profesor revisa primero',H1))
 s.append(table(['Error','Por qué ocurre','Prevención'],[['Paso redondeado','Documento con 2 decimales hace que vueltas/perfil se monten','Configurar 4 decimales antes de dibujar.'],['Cambiar solo diámetro','La geometría parece nueva pero rosca, clase, profundidad y metadatos siguen viejos','Modelar desde cero o actualizar cada operación.'],['Sobrescribir piezas','Se usa Guardar en vez de Guardar como al derivar tuercas','Guardar como antes de cada cambio y reabrir archivos.'],['Arandela roscada','Se copia Taladro roscado a la arandela','Crearla nueva con dos círculos y una extrusión.'],['ZIP incorrecto/vacío','Se comprime una carpeta anterior o sin archivos','Subir, descargar de la plataforma y abrir lo descargado.']],[45*mm,62*mm,67*mm]))
 s.append(pic('22_error_guardar_como','19:18–20:03 · Abrir cada archivo detecta si tuerca/contratuerca quedaron sobrescritas.')); s.append(pic('23_error_cambiar_solo_diametro','20:03–21:28 · No cambiar únicamente el diámetro de un modelo anterior.'))
 s.append(PageBreak())

 s.append(Paragraph('10. Checklist de entrega',H1))
 for line in ['□ Documento con 4 decimales.','□ Tornillo: diámetro, longitud total, longitud roscada, TPI, serie y clase correctos.','□ Rosca creada por hélice + perfil + corte barrido; extremos limpios.','□ Tuerca: altura propia, taladro roscado interno clase B.','□ Contratuerca: archivo independiente, altura propia y redondeo en ambos lados.','□ Tuerca redonda: sin corte hexagonal; diámetro de su columna.','□ Arandela: dos círculos, Plano medio, sin rosca.','□ Material AISI 1020 en las cinco piezas.','□ Cinco archivos con nombres correctos en primerapellido-primernombre-ID.','□ ZIP descargado de la plataforma y abierto para comprobar contenido.']:
  s.append(Paragraph(line,ParagraphStyle('ck',parent=BODY,fontSize=10,leading=15,spaceAfter=5)))
 s.append(box('Control final de Student A','La fila quedó confirmada: <b>Student A · 1 1/2”-6 UNC-2A · vástago 3” · rosca 2.5”</b>. Antes de comprimir, verificá que las tres piezas con rosca interna indiquen <b>1 1/2”-6 UNC-2B</b> y que la arandela no tenga rosca.',BLUE,colors.HexColor('#EAF3F8')))
 s.append(pic('24_verificar_zip','22:00–23:43 · Verificación final: descargar la entrega y abrir el ZIP enviado.'))
 doc.build(s); print(OUT)

if __name__=='__main__': build()
