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
OUT=BASE/'01_Manual'/'APENDICE_UNION_ROSCADA_METODO_PROFESOR.pdf'
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
 s += [Spacer(1,10*mm),Paragraph('UNIÓN ROSCADA · MÉTODO DEL PROFESOR',TITLE),Paragraph('Tornillo · Tuerca · Contratuerca · Tuerca redonda · Arandela',ParagraphStyle('sub',parent=BODY,fontSize=11,textColor=BLUE)),HRFlowable(width='100%',thickness=2,color=NAVY,spaceAfter=10)]
 s.append(box('Regla de uso','Los números visibles pertenecen al ejemplo 1”-8 UNC clase 1A. En el quiz tenés que sustituirlos por la fila asignada completa: diámetro nominal, TPI, serie UNC/UNF, clase, longitud del vástago y longitud roscada. No basta con cambiar el diámetro.',GOLD,colors.HexColor('#FFF7E3')))
 s.append(Spacer(1,4*mm)); s.append(table(['Configuración inicial','Valor'],[['Unidades','MMGS; podés escribir pulgadas con comillas, p. ej. 1"'],['Precisión','4 decimales'],['Material','AISI 1020 para todos los elementos'],['Paso de rosca','25.4/TPI mm, o 1/TPI pulgadas'],['Archivos','tornillo, tuerca, contratuerca, tuerca redonda, arandela']],[70*mm,104*mm]))
 s.append(pic('01_unidades','00:00–00:52 · Propiedades del documento: trabajar con cuatro decimales para evitar que el paso redondeado haga intersectar la rosca.'))
 s.append(PageBreak())

 s.append(Paragraph('1. Tornillo · vástago y cabeza',H1))
 s.append(steps([(1,'Plano Alzado → círculo del <b>diámetro nominal</b>. Para el ejemplo: 1" = 25.4 mm.','Círculo centrado en el origen.','Escribí las pulgadas con comillas para que SolidWorks convierta.'),(2,'Saliente/Base con la <b>longitud total del vástago</b>. Ejemplo: 4".','Cilindro recto.','No confundas longitud total con longitud roscada.'),(3,'En la cara posterior, segundo saliente cilíndrico con diámetro igual a la distancia entre aristas de la cabeza. Ejemplo: 49.02 mm; altura 22.606 mm.','Cabeza cilíndrica lista para recortar.','Tomá ambos valores de la fila del manual de casillas.'),(4,'Redondeo frontal de cabeza igual al espesor de arandela. Ejemplo: 4 mm.','Borde frontal suavizado.','El profesor corrige “4 pulgadas”: son 4 mm.')]))
 s.append(pic('02_vastago','01:05–01:41 · Vástago nominal y longitud total.')); s.append(pic('04_medidas_cabeza','01:46–02:34 · La tabla define distancia entre aristas y altura de cabeza.'))
 s.append(PageBreak())

 s.append(Paragraph('2. Cabeza hexagonal',H1))
 s.append(steps([(5,'En la cara de la cabeza, croquis de <b>polígono de 6 lados</b>, centrado y con vértice/contorno coincidente según el ejemplo.','Hexágono concéntrico.','No lo dibujes a ojo; usá relaciones coincidentes.'),(6,'Extruir corte → Por todo → <b>Invertir lado a cortar</b>. Debe retirarse el exterior y conservarse el hexágono.','Cabeza hexagonal sólida.','Si desaparece el centro, invertiste mal el lado.'),(7,'Redondeo en la base de la cabeza = mitad del redondeo frontal. Ejemplo: 2 mm. Chaflán final con el mismo valor.','Cabeza acabada.','Aplicá operaciones después del corte hexagonal.')]))
 s.append(pic('05_corte_hexagonal','02:59–04:02 · El corte hexagonal exige “Invertir lado a cortar” para conservar la cabeza.'))
 s.append(PageBreak())

 s.append(Paragraph('3. Hélice de la rosca',H1))
 s.append(steps([(8,'En la cara frontal del vástago, croquis de círculo con el mismo diámetro nominal.','Círculo coincidente con el vástago.','No uses el diámetro menor de la rosca.'),(9,'Operaciones → Curvas → Hélice/Espiral. Definición: <b>Altura y paso</b>. Altura = longitud roscada; paso = 1/TPI pulgadas o 25.4/TPI mm.','Ejemplo: altura 3" y paso 1/8".','No escribas 8 como paso.'),(10,'Activá <b>Invertir dirección</b> para que la hélice entre al cilindro. Ángulo inicial = 0° para enganchar el perfil desde Plano Planta.','Hélice dentro del vástago.','90°, 180° y 270° cambian el plano de arranque.')]))
 s.append(pic('06_croquis_helice','04:02–04:32 · Croquis circular que origina la hélice.')); s.append(pic('08_direccion_angulo_helice','04:32–06:04 · Altura/paso, dirección invertida y ángulo inicial 0°.'))
 s.append(PageBreak())

 s.append(Paragraph('4. Perfil de rosca y corte barrido',H1))
 s.append(steps([(11,'En Plano Planta, dibujá el negativo del perfil: triángulo isósceles con ángulo incluido <b>55°</b> para la rosca Whitworth mostrada.','Punta orientada hacia el cilindro.','Usá el perfil/ángulo de la norma asignada si cambia.'),(12,'La anchura del perfil corresponde al paso. Volvé la base línea constructiva y redondeá cresta/raíz con <b>0.1373·P</b>.','Perfil suave y cerrado.','Hacer el redondeo en el croquis evita que la operación falle después.'),(13,'Cerrá el perfil sin superar el paso; hacelo sobresalir aproximadamente 2 mm para retirar toda la “cáscara”.','Contorno único cerrado.','Si excede una vuelta, se auto-intersecta.'),(14,'Relación perforar/enganchar entre un punto cercano a la punta del perfil y el inicio de la hélice.','Perfil ligado a la trayectoria.','No enganches exactamente la punta si bloquea la relación.'),(15,'Operaciones → Corte barrido. Perfil = croquis triangular; trayectoria = hélice.','Rosca tallada completa.','Si falla: 4 decimales, perfil cerrado, paso exacto, sin solape.')]))
 s.append(pic('09_perfil_rosca','06:04–07:16 · Perfil negativo de 55°; la tabla de roscas es la autoridad.')); s.append(pic('11_cierre_perfil','07:16–10:40 · Redondeos, cierre y sobresaliente para evitar cascarón.')); s.append(pic('12_corte_barrido','10:40–11:46 · Corte barrido: perfil + hélice.'))
 s.append(PageBreak())

 s.append(Paragraph('5. Terminación del tornillo',H1))
 s.append(steps([(16,'En la cara final, convertí el contorno y aplicá Extruir corte → Por todo para limpiar el inicio/fin de la hélice.','Rosca termina con cara limpia.','No dejes media vuelta sobresaliendo.'),(17,'Asigná material <b>AISI 1020</b>. Guardá como <b>tornillo.SLDPRT</b>.','Tornillo completo y reconstruido.','Abrilo otra vez antes de reutilizarlo.')]))
 s.append(pic('13_corte_final_rosca','11:46–12:24 · Corte final para limpiar la salida de rosca.')); s.append(pic('14_tornillo_terminado','12:24–12:48 · Tornillo terminado antes de iniciar las tuercas.'))
 s.append(PageBreak())

 s.append(Paragraph('6. Tuerca',H1))
 s.append(steps([(18,'Nueva pieza; cuatro decimales. Saliente cilíndrico con distancia entre aristas correspondiente y altura de tuerca. Ejemplo: 49.02 × 25.65 mm, <b>Plano medio</b>.','Blank simétrico.','Usá la columna exacta de tuerca.'),(19,'Redondeo frontal igual al usado en la cabeza. Luego corte hexagonal Por todo e Invertir lado a cortar.','Tuerca exterior terminada.','Conservá el centro para el taladro.'),(20,'Asistente para taladro → Tapón recto → Pulgadas → Taladro roscado → designación asignada.','Ejemplo visible: 1”-8 UNC.','No elijas UNF si tu fila dice UNC.'),(21,'Activá clase de rosca. Tornillo 1A corresponde a agujero 1B; 2A→2B; 3A→3B. Desactivá avellanado si aparece.','Clase interna correcta.','A = externa; B = interna.'),(22,'Posiciones: cara frontal, punto concéntrico con origen. Aceptá y guardá como <b>tuerca.SLDPRT</b>.','Agujero centrado.','Revisá que profundidad y metadatos correspondan a esta pieza.')]))
 s.append(pic('15_tuerca_cilindro','12:48–13:49 · Cilindro base de tuerca, Plano medio.')); s.append(pic('16_asistente_taladro','15:25–16:51 · Asistente para taladro roscado: estándar, tamaño y clase.'))
 s.append(PageBreak())

 s.append(Paragraph('7. Contratuerca y tuerca redonda',H1))
 s.append(steps([(23,'Sin cerrar la tuerca, Guardar como <b>contratuerca</b>. Cambiá altura por la columna de contratuerca y redondeá ambos lados.','Contratuerca más delgada.','Guardar como antes de editar; no sobrescribas tuerca.'),(24,'Desde la contratuerca, Guardar como <b>tuerca redonda</b>. Eliminá el corte hexagonal y cambiá el diámetro inicial por el valor de tuerca redonda.','Exterior cilíndrico con agujero roscado.','Comprobá que el Taladro roscado siga válido.'),(25,'Abrí nuevamente tuerca, contratuerca y tuerca redonda para confirmar que cada archivo conserva su geometría.','Tres archivos distintos.','El error clásico es guardar el último estado sobre todos.')]))
 s.append(pic('18_contratuerca','16:51–17:28 · Contratuerca: altura propia y redondeo en ambos lados.')); s.append(pic('19_tuerca_redonda','17:28–18:26 · Tuerca redonda: eliminar corte hexagonal y usar diámetro de su columna.'))
 s.append(PageBreak())

 s.append(Paragraph('8. Arandela',H1))
 s.append(steps([(26,'Nueva pieza. Plano Alzado → dos círculos concéntricos. Interior = diámetro nominal/libre indicado; exterior = columna Arandela.','Región anular única.','No agregues geometría de rosca.'),(27,'Saliente/Base → <b>Plano medio</b> → espesor de arandela. Ejemplo: 4 mm.','Una sola operación.','El profesor exige una arandela simple.'),(28,'Guardar como <b>arandela.SLDPRT</b>.','Árbol sin Rosca ni Taladro roscado.','Roscar la arandela fue señalado como error grave.')]))
 s.append(pic('20_arandela_dos_circulos','18:35–19:06 · Dos círculos: nominal interior y diámetro exterior de tabla.')); s.append(pic('21_arandela_final','19:06–19:18 · Arandela final: una extrusión, sin rosca.'))
 s.append(PageBreak())

 s.append(Paragraph('9. Errores que el profesor revisa primero',H1))
 s.append(table(['Error','Por qué ocurre','Prevención'],[['Paso redondeado','Documento con 2 decimales hace que vueltas/perfil se monten','Configurar 4 decimales antes de dibujar.'],['Cambiar solo diámetro','La geometría parece nueva pero rosca, clase, profundidad y metadatos siguen viejos','Modelar desde cero o actualizar cada operación.'],['Sobrescribir piezas','Se usa Guardar en vez de Guardar como al derivar tuercas','Guardar como antes de cada cambio y reabrir archivos.'],['Arandela roscada','Se copia Taladro roscado a la arandela','Crearla nueva con dos círculos y una extrusión.'],['ZIP incorrecto/vacío','Se comprime una carpeta anterior o sin archivos','Subir, descargar de la plataforma y abrir lo descargado.']],[45*mm,62*mm,67*mm]))
 s.append(pic('22_error_guardar_como','19:18–20:03 · Abrir cada archivo detecta si tuerca/contratuerca quedaron sobrescritas.')); s.append(pic('23_error_cambiar_solo_diametro','20:03–21:28 · No cambiar únicamente el diámetro de un modelo anterior.'))
 s.append(PageBreak())

 s.append(Paragraph('10. Checklist de entrega',H1))
 for line in ['□ Documento con 4 decimales.','□ Tornillo: diámetro, longitud total, longitud roscada, TPI, serie y clase correctos.','□ Rosca creada por hélice + perfil + corte barrido; extremos limpios.','□ Tuerca: altura propia, taladro roscado interno clase B.','□ Contratuerca: archivo independiente, altura propia y redondeo en ambos lados.','□ Tuerca redonda: sin corte hexagonal; diámetro de su columna.','□ Arandela: dos círculos, Plano medio, sin rosca.','□ Material AISI 1020 en las cinco piezas.','□ Cinco archivos con nombres correctos en primerapellido-primernombre-ID.','□ ZIP descargado de la plataforma y abierto para comprobar contenido.']:
  s.append(Paragraph(line,ParagraphStyle('ck',parent=BODY,fontSize=10,leading=15,spaceAfter=5)))
 s.append(box('Dato pendiente para Student C','La captura disponible no muestra la fila de STUDENT_C en la tabla de unión roscada. Antes de modelar necesitás confirmar: designación completa (diámetro–TPI–UNC/UNF–clase), longitud del vástago y longitud roscada. El procedimiento de este apéndice queda listo para cualquier fila.',GOLD,colors.HexColor('#FFF7E3')))
 s.append(pic('24_verificar_zip','22:00–23:43 · Verificación final: descargar la entrega y abrir el ZIP enviado.'))
 doc.build(s); print(OUT)

if __name__=='__main__': build()
