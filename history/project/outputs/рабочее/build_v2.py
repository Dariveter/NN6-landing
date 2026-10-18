from pathlib import Path
from html import escape as e
import re,json
W=Path(__file__).parent; O=W.parent/'готовое'; A=O/'assets'; B=W.parents[1]
source=(B/'02 Программа Зима в FIELD v8 — источник истины.md').read_text()
chunk=source.split('## Практика и Стратегия — по месяцам')[1].split('## Форматы событий')[0]
events=[]; month=''
for line in chunk.splitlines():
 if line.startswith('### Ноябрь'):month='nov'
 if line.startswith('### Декабрь'):month='dec'
 if line.startswith('### Январь'):month='jan'
 if line.startswith('- **'):
  head,host=line[4:].split('** — ',1); date,track,rest=head.split(' · ',2); fmt,title=rest.split(': ',1)
  events.append(dict(month=month,date=date,track=track,format=fmt,title=title,host=host.strip() if host.strip()!='—' else 'Эксперт определяется по задаче',agenda=[]))
 elif line.startswith('  - ') and events:events[-1]['agenda'].append(line[4:])
assert len(events)==19
cards=[]
for x in events:
 agenda=''.join('<li>'+e(t)+'</li>' for t in x['agenda'])
 cards.append(f'''<details class="event" data-month="{x['month']}" data-track="{x['track']}"><summary><time>{e(x['date'])}</time><div><span class="event-type {'strategy-tag' if x['track']=='Стратегия' else ''}">{e(x['track'])} · {e(x['format'])}</span><h3>{e(x['title'])}</h3><p>{e(x['host'])}</p></div><span class="plus" aria-hidden="true">+</span></summary><div class="event-body"><ul>{agenda}</ul><p class="event-time">19:00 Москва · 18:00 Израиль · 17:00 CET</p></div></details>''')
(A/'calendar-v2.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
people=[
 ('dmitry','Дмитрий Эйгенсон','Основатель НИИ','Личная система и рабочие процессы','Ведёт основной маршрут НН-6: от первой задачи и настройки ИИ до поручений, документов и своей рабочей системы.'),
 ('denis','Денис Домрачев','Визуал и маркетинг','Стиль, контент и путь клиента','Ведёт визуальную неделю кэмпа, бренд-бук и воркшопы по работе с клиентами. Показывает, как применять ИИ в маркетинге.'),
 ('sergey','Сергей Долгов','ИИ и безопасность','Данные и границы автоматизации','Проводит мастер-класс по безопасности 18 ноября. Разбирает правила работы с данными и действия, для которых нужно подтверждение человека.'),
 ('ioganna','Иоганна Алексанян','Сообщество Field','Диалог с экспертами и участниками','Продюсер и ведущая «Гостей из будущего». Помогает выстраивать жизнь сообщества и обсуждать, как ИИ меняет человека и работу.'),
 ('alexander','Александр Ярыгин','Базы знаний','Память для клиентов и проектов','Ведёт две встречи о личной базе знаний: от структуры материалов до карточек клиентов и журнала решений.'),
 ('yulia','Юлия Кветна','Вайбкодинг','От идеи к своему сайту','Проводит «Стол заказов» и воркшопы по созданию сайта. Вместе с участниками проходит путь от задачи и референсов до публикации.'),
 ('andrey','Андрей Смирнов','Автоматизация','n8n и связь между сервисами','Ведёт введение в n8n и мини-курс в записи. Показывает, как связать таблицы, мессенджеры и почту в рабочий процесс.'),
 ('valentin','Валентин Васин','SMM и контент','Реальная практика продвижения','Разбирает тексты, рассылки, визуал и работу с обратной связью клиентов на практических примерах.'),
 ('vasilyev','Сергей Васильев','Презентации и речь','Структура, подача и репетиция','Тренер по речи и коммуникациям. В январе ведёт мастер-класс «Презентуем в стиле Apple»: от идеи и структуры до выступления.'),
 ('gulnara','Гульнара Галеева','Команда НИИ','Обучение команд и партнёрства','Отвечает за корпоративные программы и партнёрства. Помогает подобрать формат обучения для задач команды.'),
 ('yuri','Юрий Рапопорт','Команда НИИ','Участие и работа с данными','Помогает разобраться в составе участия, оплате и доступах. Преподаватель НИИ с экспертизой в работе с данными.'),
]
team=[]
for n,name,role,title,bio in people:
 pic=f'<img src="assets/{n}.webp" alt="{name}" width="400" height="460" loading="lazy" decoding="async">' if n!='ioganna' else '<div class="portrait-initials" role="img" aria-label="Иоганна Алексанян: карточка без фотографии"><span>ИА</span><small>Соединяет людей<br>и новые идеи</small></div>'
 team.append(f'<article class="person">{pic}<div class="person-copy"><span class="person-role">{role}</span><h3>{name}</h3><p>{title}</p><details class="person-details"><summary>Подробнее<span class="plus" aria-hidden="true">+</span></summary><p>{bio}</p></details></div></article>')
team.append('<article class="person person-community"><div class="community-portrait"><span>+</span><h3>И ваш<br>опыт тоже.</h3></div><div class="person-copy"><span class="person-role">СООБЩЕСТВО FIELD</span><h3>Здесь учатся<br>друг у друга</h3><p>Приносите свою задачу, вопросы и находки.</p><a href="#price" class="text-link" data-cta="team-community">Присоединиться →</a></div></article>')
teamhtml='''<section class="section" id="people"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">ЛЮДИ, КОТОРЫЕ РЯДОМ</p><h2>Команда НИИ Нейросетей<br>и сообщество Field</h2></div><p>Преподаватели, практики и команда сообщества. У каждого — своя область, у вас — возможность учиться и задавать вопросы.</p></div><div class="people-grid">'''+''.join(team)+'''</div></div></section>'''
logos=[('askona-logo.svg','Askona',''),('ddx-logo.svg','DDX Fitness',''),('wrf-logo.webp','White Rabbit Family','logo-wrf'),('corestone-logo.webp','Corestone',''),('murom-logo.webp','Муром',''),('samolet-logo.svg','Самолёт',''),('zdravservice-logo.webp','Здравсервис','')]
companyhtml='''<section class="companies" id="companies"><div class="wrap"><div class="companies-heading"><p class="eyebrow">ИИ В РЕАЛЬНОМ БИЗНЕСЕ</p><h2>С нами учатся и работают</h2><p>Компании, для которых НИИ проводит обучение и прикладные программы.</p></div><div class="company-grid">'''+''.join(f'<div class="company-logo {cls}"><img src="assets/{fn}" alt="{name}" loading="lazy" width="190" height="80"><span>{name}</span></div>' for fn,name,cls in logos)+'''</div><div class="company-more"><span>Также в опыте НИИ — компания «Лига».</span></div><div class="company-cohort"><span class="cohort-dot" aria-hidden="true"></span><p>На текущих программах — <strong>White Rabbit Family, Арт-Моторс, Ланцет</strong> и другие команды.</p><a href="https://t.me/stonerized" target="_blank" rel="noopener" class="text-link" data-cta="b2b-logos">Условия для вашей команды ↗</a></div></div></section>'''
heroart='''<div class="hero-art" aria-label="От рабочих материалов к проверяемому результату с помощью ИИ"><span class="art-kicker">ВАША РАБОТА, НА НОВОМ УРОВНЕ</span><div class="hero-image-wrap"><picture><source media="(max-width: 700px)" srcset="assets/hero-v2-small.webp"><img class="hero-image" src="assets/hero-v2.webp" alt="Документы, таблицы и письма складываются в организованный рабочий процесс" width="1200" height="900" fetchpriority="high" decoding="async"></picture><span class="floating-note note-input"><i class="note-dot"></i> Ваши материалы</span><span class="floating-note note-result"><i>✓</i> Результат под контролем</span></div><div class="art-steps"><span><b>01</b> Поручаете</span><span><b>02</b> Пробуете</span><span><b>03</b> Проверяете</span></div></div>'''
mentor='''<div class="mentor-row"><img src="assets/mentor-v2.webp" alt="НИИшка с открытой книгой — иллюстрация ИИ-ментора" width="420" height="280" loading="lazy"><div><p class="eyebrow">ПОДДЕРЖКА МЕЖДУ ЭФИРАМИ</p><h3>Рядом, когда<br>застряли на задаче.</h3><p>На первом занятии настроите ИИ-ментора: он поможет разобрать задачу на шаги и разобраться в материале. А вопросы по вашей работе принесёте на совместную практику.</p><details class="mentor-details"><summary>Как устроен ИИ-ментор<span class="plus" aria-hidden="true">+</span></summary><p>Это набор инструкций для ИИ-репетитора, который вы используете в своём ИИ-инструменте. Он помогает учиться; ответы и решения вы проверяете. Живая поддержка преподавателей и сообщества дополняет его работу.</p></details></div></div>'''
for fn in ['index.html','alumni.html']:
 s=(W/('v1-'+fn)).read_text();alumni=fn=='alumni.html'
 price='175 евро' if alumni else '350 евро'; rub='17,5 тысячи рублей' if alumni else '35 тысяч рублей'; pair=f'<span>{price}</span><span class="price-or">или</span><span>{rub}</span>'
 s=s.replace('content="light dark"','content="light"').replace('assets/style.css','assets/style-v2.css').replace('assets/app.js','assets/app-v2.js').replace('assets/logo.png','assets/nii-logo-light.webp').replace('width="132" height="39"','width="190" height="31"')
 s=s.replace('<a class="skip"', '<canvas id="ambient-canvas" aria-hidden="true"></canvas><div class="scroll-progress" aria-hidden="true"></div><a class="skip"',1)
 s=s.replace('<button class="menu-button', '<button id="motion-toggle" class="motion-button js-only" type="button" aria-pressed="false" aria-label="Приостановить анимацию" title="Приостановить анимацию">Ⅱ</button><button class="menu-button',1)
 if not alumni:
  s=re.sub(r'<h1>.*?</h1>','<h1>Меньше рутины.<br>Больше дела.<br><em>С помощью ИИ.</em></h1>',s,count=1)
  s=re.sub(r'<p class="hero-intro">.*?</p>','<p class="hero-intro">Практический кэмп НН-6 и три месяца в сообществе Field. Для руководителей, предпринимателей и специалистов, которые хотят применять ИИ в своей работе.</p>',s,count=1)
 s=re.sub(r'<div class="hero-art".*?(?=\n </div>\n <div class="wrap hero-bottom")',heroart,s,flags=re.S)
 s=re.sub(r'<p class="hero-price">.*?</p>',f'<div class="hero-price"><p class="price-pair">{pair}</p><small>за весь зимний цикл · кэмп + сообщество</small></div>',s)
 s=s.replace('<strong>7 недель</strong> кэмпа НН-6','<strong>6 недель + финал</strong> основной маршрут кэмпа').replace('<strong>3 месяцах</strong>','<strong>3 месяцах</strong>')
 # Keep the previous verified testimonial block, add company evidence before it.
 idx=s.index('<section class="proof-band')
 s=s[:idx]+companyhtml+'\n'+s[idx:]
 for name,symbol in [('camp','↗'),('practice','✳'),('strategy','◎')]:
  s=s.replace(f'<span class="track-symbol" aria-hidden="true">{symbol}</span>',f'<img class="track-art" src="assets/{name}-v2.webp" alt="" width="340" height="260" loading="lazy">')
 s=re.sub(r'<div class="mentor-row">.*?(?=\n</div></section>)',mentor,s,count=1,flags=re.S)
 s=re.sub(r'<div class="event-list">.*?</div>\n <div class="calendar-footer">','<div class="event-list">'+''.join(cards)+'</div>\n <div class="calendar-footer">',s,flags=re.S)
 s=re.sub(r'(Ноябрь|Декабрь|Январь) <span>[0-9]+</span>',r'\1',s)
 s=re.sub(r'<section class="section dark" id="people">.*?</section>',teamhtml,s,flags=re.S)
 s=re.sub(r'<fieldset class="currency-switch.*?</fieldset>','',s,flags=re.S)
 s=re.sub(r'<div class="main-price">.*?<p id="price-alternative" class="price-alternative">.*?</p>',f'<div class="main-price"><p class="price-pair">{pair}</p><span>за все три месяца</span></div>',s,flags=re.S)
 s=re.sub(r'<div class="program-price"><strong>.*?</strong>',f'<div class="program-price"><p class="price-pair">{pair}</p>',s)
 s=re.sub(r'<strong class="dock-price">.*?</strong>',f'<strong class="dock-price">{price}<br>или {rub}</strong>',s)
 s=re.sub(r'<p class="dialog-price">.*?</p>',f'<p class="dialog-price price-pair">{pair}</p>',s)
 s=s.replace('175 € или 17 500 ₽','175 евро или 17,5 тысячи рублей')
 s=s.replace('Сколько времени нужно выделять?', 'Совмещу ли я это с работой?')
 s=s.replace('class="section dark"','class="section"').replace('class="final-section dark"','class="final-section"').replace('class="footer dark"','class="footer"')
 s=s.replace('НН-6 и Зима в FIELD','НН-6 и Field — ИИ для работы и бизнеса')
 s=s.replace('<span class="label">УЧАСТНИК</span>','<span class="label">'+('ВЫПУСКНИК НИИ · −50%' if alumni else 'УЧАСТНИК')+'</span>')
 s=s.replace('<p class="billing-note">','<a class="vip-link" href="https://t.me/stonerized" target="_blank" rel="noopener" data-cta="vip">VIP-участие — обсудить с Юрием ↗</a><p class="billing-note">')
 s=s.replace('<noscript><style>.js-only{display:none!important}.event[hidden]{display:grid}</style></noscript>','<noscript><style>.js-only{display:none!important}</style></noscript>')
 s=s.replace('<br>','<br> ')
 s=s.replace('<span aria-hidden="true">в</span><p><strong>3 месяцах</strong>', '<span>в</span><p><strong>3 месяцах</strong>')
 if alumni:
  s=s.replace('<div class="alumni-price"><strong>Выпускникам кэмпов НИИ — −50%</strong><p>175 евро или 17,5 тысячи рублей за тот же состав участия.</p><a href="alumni.html" class="text-link">Условия для выпускников →</a></div>', '<div class="alumni-price"><strong>Ваша скидка уже учтена — 50%</strong><p>В стоимость входит весь зимний цикл.</p><a href="index.html" class="text-link">Условия для новых участников →</a></div>')
  s=s.replace('<a href="alumni.html">Выпускникам</a>', '<a href="index.html">Новым участникам</a>')
 (O/fn).write_text(s)
app=(A/'app.js').read_text()
app=app.replace("field-recommended-v1","field-light-v2")
app=app.replace("let currency = 'EUR'","let currency = 'unselected'")
app=re.sub(r"  \$\$\('input\[name=currency\]'\).*?(?=  const dialog)",'',app,flags=re.S)
app=app.replace("    $('.dialog-price').textContent = prices[currency];\n",'')
app=app.replace("$$('.week,.faq-item')","$$('.week,.faq-item,.event,.person-details,.mentor-details')")
app=app.replace("script.src = 'assets/field-gl.js'","script.src = 'assets/motion-v2.js'")
app=app.replace("if (evt.key === 'Escape' && !menu.hidden)","if (evt.key === 'Escape' && !menu.hidden)")
(A/'app-v2.js').write_text(app)
print('v2 HTML ready: 19 expandable events, 11 people + community card, 7 original company logos')
