from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json, shutil, re, unicodedata

BASE=Path(__file__).resolve().parents[1]
GEAR=BASE.parent/'Mierda no abrir'/'video.mp4'
UNION=BASE/'source_media'/'union.mp4'  # supply your own recording
OUT=BASE/'04_Fotogramas'/'Secuencias_Densas'
FONT=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',22)
BOLD=ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf',23)

WINDOWS=[
 ('G01','Engranaje · base, extrusión plano medio y chaflán',GEAR,0,195),
 ('G02','Engranaje <30 · ecuaciones y círculos De/Dp/Ct/Di',GEAR,195,360),
 ('G03','Engranaje <30 · Delta, vector R1 y primer arco',GEAR,330,495),
 ('G04','Engranaje <30 · radios R2/R3, recortes y perfil',GEAR,480,650),
 ('G05','Engranaje <30 · simetría y contorno cerrado',GEAR,630,790),
 ('G06','Engranaje <30 · plano tangente y dirección helicoidal',GEAR,780,930),
 ('G07','Engranaje <30 · perfil medio y equidistancia +1 mm',GEAR,920,1040),
 ('G08A','Engranaje <30 · medir el giro posterior',GEAR,1040,1190),
 ('G08B','Engranaje <30 · preparar el perfil frontal',GEAR,1190,1340),
 ('G08C','Engranaje <30 · perfiles frontal y posterior ±θ/2',GEAR,1340,1515),
 ('G09','Engranaje <30 · corte recubierto, redondeo y matriz',GEAR,1510,1660),
 ('G10A','Engranaje ≥30 · elegir ecuaciones',GEAR,1650,1800),
 ('G10B','Engranaje ≥30 · crear la base',GEAR,1800,1950),
 ('G10C','Engranaje ≥30 · preparar círculos de trazado',GEAR,1950,2040),
 ('G11','Engranaje ≥30 · construcción P/4 y arco único R1',GEAR,2040,2260),
 ('G12A','Engranaje ≥30 · crear referencia de plano',GEAR,2250,2400),
 ('G12B','Engranaje ≥30 · plano y hélice contraria',GEAR,2400,2550),
 ('G12C','Engranaje ≥30 · medir y aplicar giro',GEAR,2550,2670),
 ('G13A','Engranaje ≥30 · cerrar perfiles',GEAR,2660,2820),
 ('G13B','Engranaje ≥30 · perfil medio y orientación',GEAR,2820,2980),
 ('G13C','Engranaje ≥30 · corte recubierto',GEAR,2980,3130),
 ('G13D','Engranaje ≥30 · redondeo y matriz',GEAR,3130,3180),
 ('G14A','Ensamblaje · soporte',GEAR,3180,3300),
 ('G14B','Ensamblaje · distancia entre centros',GEAR,3300,3420),
 ('G15A','Ensamblaje · insertar piezas',GEAR,3410,3560),
 ('G15B','Ensamblaje · restringir posición y orientación',GEAR,3560,3720),
 ('G16A','Ensamblaje · relación mecánica',GEAR,3710,3840),
 ('G16B','Ensamblaje · prueba de giro',GEAR,3840,3970),
 ('G17','Quiz teórico · instrucciones y reglas finales',GEAR,3960,4110),
 ('U01','Unión · configuración de 4 decimales y vástago',UNION,0,105),
 ('U02','Unión · cabeza, redondeos y corte hexagonal',UNION,100,245),
 ('U03','Unión · croquis y configuración de hélice',UNION,240,365),
 ('U04','Unión · perfil de rosca de 55 grados',UNION,360,510),
 ('U05','Unión · cierre del perfil y enganche a hélice',UNION,500,650),
 ('U06','Unión · corte barrido y limpieza de extremos',UNION,640,755),
 ('U07','Unión · tuerca y corte exterior',UNION,750,925),
 ('U08','Unión · asistente de taladro y clase interna',UNION,920,1015),
 ('U09','Unión · contratuerca y tuerca redonda',UNION,1005,1105),
 ('U10','Unión · arandela',UNION,1100,1175),
 ('U11','Unión · errores de guardado y reutilización',UNION,1170,1300),
 ('U12','Unión · verificación de archivos y ZIP',UNION,1300,1424),
]

def stamp(sec): return f'{int(sec)//60:02d}:{int(sec)%60:02d}'

def build():
 OUT.mkdir(parents=True,exist_ok=True); manifest=[]
 for ident,title,video,start,end in WINDOWS:
  seq=OUT/ident; seq.mkdir(exist_ok=True)
  # Six exact evidence states: beginning, four interior checkpoints, ending.
  times=[start+(end-start)*i/5 for i in range(6)]
  frames=[]
  for i,t in enumerate(times,1):
   p=seq/f'{ident}_{i:02d}_{stamp(t).replace(":","m")}s.jpg'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',f'{t:.3f}','-i',str(video),'-frames:v','1','-vf','scale=960:-2','-q:v','2',str(p),'-y'],check=True)
   frames.append(p)
  montage=Image.new('RGB',(1920,900),'white'); d=ImageDraw.Draw(montage)
  d.rectangle((0,0,1920,58),fill='#17324D'); d.text((18,15),f'{ident} · {title}',font=BOLD,fill='white')
  for i,(p,t) in enumerate(zip(frames,times)):
   im=Image.open(p).convert('RGB'); im.thumbnail((620,370))
   x=(i%3)*640+10; y=(i//3)*410+70
   montage.paste(im,(x+(620-im.width)//2,y))
   d.text((x,y+372),f'{i+1}/6 · {stamp(t)}',font=FONT,fill='#17324D')
  safe=unicodedata.normalize('NFKD',title).encode('ascii','ignore').decode('ascii')
  safe=re.sub(r'[^A-Za-z0-9_-]+','_',safe).strip('_')
  mp=OUT/f'{ident}_{safe}.jpg'
  montage.save(mp,quality=92)
  manifest.append({'id':ident,'title':title,'source':str(video),'start_seconds':start,'end_seconds':end,'montage':str(mp.relative_to(BASE)),'frames':[str(p.relative_to(BASE)) for p in frames],
  'review_prompt':'Identify the active SolidWorks command; selected plane/face/entities; every visible value; orientation/direction; expected result after Accept; hidden transition between frames; likely novice failure; exact recovery.'})
  print(ident,mp.name)
 (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print('storyboards',len(manifest))
if __name__=='__main__': build()
