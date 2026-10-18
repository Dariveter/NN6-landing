from pathlib import Path
import re,runpy,json
W=Path(__file__).parent;O=W.parent/'готовое'
runpy.run_path(str(W/'build_v4_1.py'))

def terms(s):
    forms={'мероприятие':'событие','мероприятия':'события','мероприятий':'событий','мероприятию':'событию','мероприятием':'событием','мероприятии':'событии','мероприятиях':'событиях','мероприятиями':'событиями','мероприятиям':'событиям'}
    def repl(m):
        v=forms[m.group().lower()]
        return v.capitalize() if m.group()[0].isupper() else v
    return re.sub(r'мероприят(?:иями|иях|иям|ием|ию|ии|ий|ия|ие)',repl,s,flags=re.I)

widget=(W/'neuroniy-widget.html').read_text()
formats={'Подкаст':'podcast','Воркшоп':'memory','Разбор кейса':'case','Мастер-класс':'masterclass','Стол заказов':'orders'}
for fn in ['index.html','alumni.html','reviews.html']:
    s=terms((O/fn).read_text())
    s=s.replace('assets/style-v4-1.css','assets/style-v4-2.css')
    s=s.replace('</head>','<link rel="stylesheet" href="assets/neuroniy-v4-2.css"><script src="assets/neuroniy-engine.js" defer></script><script src="assets/neuroniy-v4-2.js" defer></script></head>')
    if fn!='reviews.html':
        s=s.replace('С нами учились<br> и работали','С нами учатся<br> и работают').replace('Опыт НИИ — обучение и прикладные программы для команд бизнеса.','Для C-level и бизнес-команд.')
        s=s.replace('<h3>Основа для новичка</h3><p>Последовательный маршрут от настройки ИИ до собственного рабочего процесса.</p>','<h3>Всё самое необходимое<br> в 2027 году</h3><ul class="camp-skills"><li>Агенты</li><li>ChatGPT</li><li>Скиллы</li><li>Навыки</li></ul>')
        seq=[0]
        def event(m):
            text=m.group();seq[0]+=1
            label=re.search(r'<div class="event-cover">.*?<span>(.*?)</span></div>',text,re.S).group(1)
            kind=formats[label]
            month=re.search(r'data-month="([^"]+)"',text).group(1)
            text=text.replace('<details ',f'<details id="event-{month}-{seq[0]:02d}" ',1)
            return re.sub(r'(<div class="event-cover">)<svg.*?</svg>',lambda q:q[1]+f'<img class="event-object" src="assets/format-{kind}-v4-2.webp" alt="" width="360" height="360" loading="lazy" decoding="async">',text,count=1,flags=re.S)
        s=re.sub(r'<details class="event .*?</details>',event,s,flags=re.S)
        assert seq[0]==19,seq
        guide='<div class="format-guide"><span>ФОРМАТЫ</span>'+''.join(f'<span><img src="assets/format-{kind}-v4-2.webp" alt="" width="38" height="38" loading="lazy">{label}</span>' for label,kind in formats.items())+'</div>'
        s=re.sub(r'<div class="format-guide">.*?</div>',lambda _:guide,s,count=1,flags=re.S)
        s=s.replace('<div class="companies-heading">','<div class="companies-heading">',1)
        # Small meaningful visual accents reuse the same lightweight image family.
        s=s.replace('<p class="support-label">ПОДДЕРЖКА МЕЖДУ ЭФИРАМИ</p>','<p class="support-label">ПОДДЕРЖКА МЕЖДУ ЭФИРАМИ</p>')
        s=s.replace('<p>Юрий Рапопорт поможет с участием.</p>','<p>Юрий Рапопорт поможет с участием.</p>')
        join=re.search(r'<ol class="join-steps">.*?</ol>',s,re.S)
        assert join
        j=join.group()
        for i,k in enumerate(['route-camp-v4-1','format-memory-v4-2','format-orders-v4-2'],1):
            j=j.replace(f'<li><span>0{i}</span>',f'<li><img class="join-object" src="assets/{k}.webp" alt="" width="120" height="120" loading="lazy"><span>0{i}</span>')
        s=s[:join.start()]+j+s[join.end():]
        # A small research object sits with the participant stories heading.
        s=s.replace('<h2>Что получилось у участников?</h2>','<h2>Что получилось у участников?</h2><img class="stories-object" src="assets/format-case-v4-2.webp" alt="" width="160" height="160" loading="lazy">')
        s=s.replace('assets/app-v4.js','assets/app-v4-2.js')
    s=s.replace('</body>',widget+'\n</body>')
    (O/fn).write_text(s)
(O/'assets/style-v4-2.css').write_text((O/'assets/style-v4-1.css').read_text()+'\n'+(W/'v4-2-overrides.css').read_text())
(O/'assets/app-v4-2.js').write_text(terms((O/'assets/app-v4.js').read_text()).replace("field-winter-v4'","field-winter-v4.2'"))
for name in ['neuroniy-v4-2.css','neuroniy-v4-2.js','neuroniy-engine.js']:
    (O/'assets'/name).write_text((W/name).read_text())
print('v4.2 pages built: events, camp skills, company copy, five illustrated event formats, Neuroniy widget.')
