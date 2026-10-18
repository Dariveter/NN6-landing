from pathlib import Path
from html import escape
import re,runpy,json
W=Path(__file__).parent;O=W.parent/'готовое'
runpy.run_path(str(W/'build_v4_5.py'))
origin='https://nii-field-winter-v3.vercel.app'
for fn in ['index.html','alumni.html','reviews.html']:
 s=(O/fn).read_text().replace('v4-5','v4-6').replace('assets/johanna-v4-6.webp','assets/johanna-v4-5.webp').replace('CEO NII NeuroCity','CEO НИИ Нейросетей')
 title=re.search(r'<title>(.*?)</title>',s)[1]
 description=('Для выпускников кэмпов НИИ: зимний интенсив и сообщество FIELD. Ноябрь 2026 — январь 2027. 175 евро или 17,5 тысячи рублей.' if fn=='alumni.html' else '29 историй, отзывов и видео участников НИИ Нейросетей: рабочие задачи, решения с ИИ и опыт сообщества FIELD.' if fn=='reviews.html' else 'Зимний интенсив НИИ Нейросетей: ноябрь 2026 — январь 2027. Кэмп, практика, стратегия и сообщество FIELD. 350 евро или 35 тысяч рублей за весь сезон.')
 s=re.sub(r'<meta name="description"[^>]*>','',s)
 url=origin+('/' if fn=='index.html' else '/'+fn)
 metadata='<meta name="description" content="'+escape(description,quote=True)+'"><link rel="canonical" href="'+url+'">'
 for prop,value in [('og:type','website'),('og:site_name','НИИ Нейросетей · FIELD'),('og:locale','ru_RU'),('og:title',title),('og:description',description),('og:url',url),('og:image',origin+'/assets/hero-v4.webp'),('og:image:width','1536'),('og:image:height','1024'),('og:image:alt','Учёба, практика и стратегия в FIELD')]:
  metadata+='<meta property="'+prop+'" content="'+escape(value,quote=True)+'">'
 metadata+='<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+escape(title,quote=True)+'"><meta name="twitter:description" content="'+escape(description,quote=True)+'"><meta name="twitter:image" content="'+origin+'/assets/hero-v4.webp">'
 s=s.replace('</head>',metadata+'</head>')
 if fn=='reviews.html':
  s=s.replace('reviews-v3.js','reviews-v4-6.js')
 else:
  s=s.replace('<a href="#program">Программа</a>','<a href="#program">Кэмп</a><a href="#calendar">Расписание</a><a href="#people">Команда</a>')
  s=s.replace('<a href="alumni.html">Выпускникам</a></nav>','<a href="#faq">Вопросы и ответы</a><a href="alumni.html">Выпускникам</a></nav>')
  s=s.replace('class="track-poster track-practice" href="#calendar"','class="track-poster track-practice" href="#calendar" data-calendar-track="Практика"')
  s=s.replace('class="track-poster track-strategy" href="#calendar"','class="track-poster track-strategy" href="#calendar" data-calendar-track="Стратегия"')
  s=s.replace('Для руководителей, предпринимателей, специалистов и всех любопытных. Приходите с любым уровнем подготовки и своими задачами.','Для руководителей, предпринимателей, специалистов и всех любопытных — с любым уровнем подготовки и своими задачами.')
  s=re.sub(r'(<p class="season-date">.*?)(</p>)',r'\1<span class="hero-start">Старт 9 ноября · онлайн</span>\2',s,count=1,flags=re.S)
  actions=re.search(r'<div class="hero-actions">.*?</div>',s,re.S)[0]
  price=re.search(r'<div class="hero-price">.*?</p></div>',s,re.S)[0]
  s=s.replace(actions,'',1).replace(price,price+actions,1)
  s=re.sub(r'href="#price"( data-cta="(?:hero|header|mobile-dock|closing)")',r'href="#participation"\1',s)
  s=s.replace('href="#price" class="button" data-cta="final"','href="#participation" class="button" data-cta="final"')
  s=s.replace('<div class="season-ticket price-card">','<div class="season-ticket price-card" id="participation">',1)
  benefits=re.search(r'<ul class="included">.*?</ul><p class="price-perspective">.*?</p>',s,re.S)[0]
  s=s.replace(benefits+'</div>','</div><div class="price-benefits">'+benefits+'</div>',1)
  s=s.replace('15 встреч практики и 4 — стратегии','15 событий практики и 4 — стратегии')
  start=s.index('<section class="section" id="stories">');end=s.index('</section>',start)
  block=s[start:end]
  controls='<div class="review-rail-controls js-only"><button type="button" data-story-prev aria-label="Предыдущая история" aria-controls="stories-rail">←</button><span class="review-rail-status" aria-live="polite">6 историй</span><button type="button" data-story-next aria-label="Следующая история" aria-controls="stories-rail">→</button></div>'
  block=block.replace('<div class="review-grid">',controls+'<div class="review-grid" id="stories-rail" tabindex="0" role="region" aria-label="Истории участников: листайте или используйте стрелки">')
  s=s[:start]+block+s[end:]
  # The original description remains complete, but Yuri's role is no longer printed twice.
  s=re.sub(r'(<article class="person" id="expert-yuri".*?<div class="person-bio"><p>.*?) В НИИ Нейросетей специализируется на работе с данными\.(</p>)',r'\1\2',s,count=1,flags=re.S)
 (O/fn).write_text(s)
app=(O/'assets/app-v4-5.js').read_text().replace('v4.5','v4.6').replace("document.documentElement.classList.contains('motion-paused')","document.body.classList.contains('motion-paused')")
app=app.replace("$('#calendar-status').textContent = 'Показано событий: ' + count;","$('#calendar-status').textContent = ({nov:'Ноябрь',dec:'Декабрь',jan:'Январь'})[month] + (track==='all'?'':' · '+track) + ' · событий: ' + count;")
# A repeated link to the same expert must reopen the card even when the hash has not changed.
app=app.replace("addEventListener('hashchange',revealExpert);addEventListener('load',revealExpert);","addEventListener('hashchange',revealExpert);addEventListener('load',revealExpert);document.addEventListener('field:reveal-expert',revealExpert);")
(O/'assets/app-v4-6.js').write_text(app+'\n'+(W/'ux-v4-6.js').read_text())
(O/'assets/style-v4-6.css').write_text((O/'assets/style-v4-5.css').read_text()+'\n'+(W/'v4-6-overrides.css').read_text())
(O/'assets/reviews-v4-6.js').write_text((W/'reviews-v4-6.js').read_text())
for name in ['neuroniy-v4-5.js','neuroniy-engine-v4-5.js']:
 source=(O/'assets'/name).read_text().replace('v4-5','v4-6').replace('v4.5','v4.6')
 if name=='neuroniy-engine-v4-5.js':
  source=source.replace(".replace(/ё/g,'е')",".replace(/ё/g,'е').replace(/раппопорт/g,'рапопорт')")
  source=source.replace("const named=docs.find", "if(/(?:ceo|генеральн.*директор|гендиректор)/.test(q)&&/(?:нии|нейросет|рапопорт)/.test(q))return docResult(docs.find(d=>d.kind==='person'&&/Рапопорт/.test(d.title)));\n const named=docs.find")
 else:
  source=source.replace("if(new URL(a.href).pathname===location.pathname){setTimeout(revealHash,0);}","if(new URL(a.href).pathname.replace(/index\\.html$/,'')===location.pathname.replace(/index\\.html$/,'')){setTimeout(()=>{revealHash();document.dispatchEvent(new Event('field:reveal-expert'));},0);}")
 (O/'assets'/name.replace('v4-5','v4-6')).write_text(source)
kb=json.loads((O/'assets/neuroniy-knowledge-v4-5.json').read_text().replace('CEO NII NeuroCity','CEO НИИ Нейросетей'))
kb['version']='FIELD-winter-v4.6'
for doc in kb['documents']:
 if doc['kind']=='person' and doc['title']=='Юрий Рапопорт':
  doc['guide_text']=doc['guide_text'].replace(' В НИИ Нейросетей специализируется на работе с данными.','',1)
(O/'assets/neuroniy-knowledge-v4-6.json').write_text(json.dumps(kb,ensure_ascii=False,indent=2)+'\n')
(O/'api/neuroniy.js').write_text((O/'api/neuroniy.js').read_text().replace('v4-5','v4-6').replace('v4.5','v4.6'))
print('v4.6: CEO corrected, targeted calendar links, hero clarity, direct price access, review navigation, readable mobile UI and share metadata.')
