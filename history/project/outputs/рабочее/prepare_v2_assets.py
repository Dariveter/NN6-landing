from pathlib import Path
from PIL import Image
import shutil,json
W=Path(__file__).parent
O=W.parent/'готовое'; A=O/'assets'; R=W/'v2-research'
G=Path('/Users/bigd/.codex/generated_images/01a11a49-96d8-77c0-9710-9138004e1bf0')
items={'hero':'exec-ca0ec1df-365d-4045-a832-1a56a530c55b.png','mentor':'exec-b85971d8-bbf0-416f-8eb9-b47747c9625b.png','camp':'exec-ae07d3b9-5aab-49be-b6fe-967d2c7f0be2.png','practice':'exec-854c773a-06e3-484c-a795-86c5d68eecce.png','strategy':'exec-2abcd17d-cb2c-4311-9162-749357979156.png'}
for name,fn in items.items():
 im=Image.open(G/fn); im.thumbnail((1200,900) if name=='hero' else (600,480)); im.save(A/(name+'-v2.webp'),quality=84,method=6)
 if name=='hero':
  im.thumbnail((700,525));im.save(A/'hero-v2-small.webp',quality=81,method=6)
for n in ['alexander','yulia','andrey','valentin','yuri']:
 im=Image.open(R/(n+'.png')).convert('RGB');im.thumbnail((540,600));im.save(A/(n+'.webp'),quality=84,method=6)
im=Image.open('/Users/bigd/Downloads/portrait.jpg');im.thumbnail((540,600));im.save(A/'vasilyev.webp',quality=84,method=6)
logo=Path('/Users/bigd/Obsidian Vault/Маркетинг и бренд/03_Маркетинг/Брендинг НИИ/варианты лого НИИ Нейросетей/NII_logo_black_eye.png')
im=Image.open(logo);im.thumbnail((650,120));im.save(A/'nii-logo-light.webp',quality=95,method=6)
for n,p in {'wrf':'/Users/bigd/Downloads/logo.png','corestone':'/Users/bigd/Obsidian Vault/B2B/13_Обучение компаний/Корстоун/Задача по верстке/Логотип.png','murom':'/Users/bigd/Obsidian Vault/B2B/13_Обучение компаний/ЗАО Муром/murom_logo.jpg'}.items():
 im=Image.open(p);im.thumbnail((530,280));im.save(A/(n+'-logo.webp'),quality=94,method=6)
shutil.copy2('/var/folders/dd/_c2y4k4s6f31hr52hzv1zsl80000gn/T/browser-use/assets/d1a25013-f76c-4206-b7ac-6ce78cb4d6e5/0945528295b86877.svg',A/'askona-logo.svg')
shutil.copy2('/var/folders/dd/_c2y4k4s6f31hr52hzv1zsl80000gn/T/browser-use/assets/d49743cc-f845-4574-b554-61b39aaa0c17/bc10c2b452e6ed59.svg',A/'ddx-logo.svg')
for fn in ['index.html','alumni.html']:
 p=W/('v1-'+fn)
 if not p.exists():shutil.copy2(O/fn,p)
print({p.name:p.stat().st_size for p in A.glob('*v2*')})
