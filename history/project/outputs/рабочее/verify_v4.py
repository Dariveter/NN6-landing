from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
O=Path(__file__).parent.parent/'готовое'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.ids=[];self.h1=0;self.classes=[];self.words=[]
    def handle_starttag(self,t,a):
        a=dict(a)
        if 'id' in a:self.ids.append(a['id'])
        if t=='h1':self.h1+=1
        self.classes.extend(a.get('class','').split())
        for k in ['src','href','srcset']:
            if a.get(k):self.refs.append(a[k])
    def handle_data(self,d):self.words.append(d)
checks=[];files=set(['index.html','alumni.html','reviews.html','assets/app-v4.js','assets/motion-v4.js','assets/style-v4.css','assets/reviews-v3.js'])
for fn in ['index.html','alumni.html','reviews.html']:
    text=(O/fn).read_text();p=Page();p.feed(text);broken=[]
    for ref in p.refs:
        if urlsplit(ref).scheme or ref.startswith('//'):continue
        path=unquote(urlsplit(ref).path)
        if not path:
            if ref.startswith('#') and ref[1:] not in p.ids:broken.append(ref)
        elif not (O/path).exists():broken.append(ref)
        else:files.add(path)
    checks.append(dict(page=fn,broken_local_links=broken,duplicate_ids=sorted({x for x in p.ids if p.ids.count(x)>1}),h1=p.h1,events=p.classes.count('event'),team=p.classes.count('person'),review_materials=p.classes.count('review-card')))
    assert not broken and len(set(p.ids))==len(p.ids) and p.h1==1,checks[-1]
    if fn!='reviews.html':
        assert p.classes.count('event')==19 and p.classes.count('person')==9
        assert 'Гульнара' not in text and 'На текущих программах' not in text and '· НН-4' not in text
        plain=' '.join(' '.join(p.words).split())
        assert all(x in plain for x in ['19:00 Москва','18:00 Израиль','Ноябрь','Декабрь','Январь','Обсудить условия для вашей команды']),fn
for name in re.findall(r'url\([\"\']?([^\)\"\']+)',(O/'assets/style-v4.css').read_text()):
    if not name.startswith(('data:','#','%23')):
        file='assets/'+name;assert (O/file).is_file(),file;files.add(file)
files.update(['assets/hero-v4.webp','assets/hero-v4-small.webp'])
(O/'site-v4-files.txt').write_text('\n'.join(sorted(files))+'\n')
core=['index.html','assets/style-v4.css','assets/app-v4.js','assets/motion-v4.js','assets/machina.otf','assets/onest.ttf','assets/onest-semibold.ttf','assets/nii-logo-white.webp','assets/hero-v4.webp']
sizes={f:(O/f).stat().st_size for f in core}
result={'checks':checks,'core_files_bytes':sizes,'desktop_core_uncompressed_bytes':sum(sizes.values()),'mobile_hero_bytes':(O/'assets/hero-v4-small.webp').stat().st_size,'public_file_count':len(files),'note':'File sizes, not a network speed or Core Web Vitals measurement.'}
(O/'проверка/static-v4.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
