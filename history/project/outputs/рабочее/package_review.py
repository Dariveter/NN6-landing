from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit, quote
from collections import Counter
import re, json, gzip, zipfile

OUT = Path(__file__).resolve().parents[1] / 'готовое'

class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []
    def text(self):
        if self.attrs.get('aria-hidden') == 'true' or 'avatar-letter' in self.attrs.get('class','').split() or self.tag in ('svg', 'canvas', 'script', 'style'):
            return ''
        text = re.sub(r'\s+', ' ', ' '.join(c if isinstance(c,str) else (' ' if c.tag == 'br' else c.text()) for c in self.children)).strip()
        return re.sub(r'\s+([,.;:!?])',r'\1',text)
    def find(self, predicate):
        found = [self] if predicate(self) else []
        for c in self.children:
            if isinstance(c, Node): found.extend(c.find(predicate))
        return found

class Tree(HTMLParser):
    voids = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, source):
        super().__init__(); self.root = Node('root'); self.stack = [self.root]; self.feed(source)
    def handle_starttag(self, tag, attrs):
        n = Node(tag,attrs); self.stack[-1].children.append(n)
        if tag not in self.voids: self.stack.append(n)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]; break
    def handle_data(self, data): self.stack[-1].children.append(data)

def inline(text):
    s=escape(text)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m:'<a href="'+m[2]+'">'+m[1]+'</a>', s)
    s=re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s=re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s

def markdown(md):
    lines=md.splitlines(); out=[]; toc=[]; i=0; h=0
    while i<len(lines):
        s=lines[i].strip()
        if not s: i+=1; continue
        heading=re.match(r'^(#{1,4}) (.+)$',s)
        if heading:
            level=len(heading[1]); h+=1; aid='part-'+str(h)
            out.append(f'<h{level} id="{aid}">{inline(heading[2])}</h{level}>')
            if level==2: toc.append((aid,heading[2]))
            i+=1; continue
        if s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*:?[-]+:?\s*',c) for c in row): rows.append([c.strip() for c in row])
                i+=1
            out.append('<div class="table-scroll"><table>')
            for n,row in enumerate(rows):
                tag='th' if n==0 else 'td'
                out.append('<tr>'+''.join(f'<{tag}>{inline(c)}</{tag}>' for c in row)+'</tr>')
            out.append('</table></div>'); continue
        if re.match(r'^(- |\d+\. )',s):
            ordered=bool(re.match(r'^\d+\. ',s)); tag='ol' if ordered else 'ul'
            out.append('<'+tag+'>')
            while i<len(lines) and re.match(r'^(- |\d+\. )',lines[i].strip()):
                out.append('<li>'+inline(re.sub(r'^(- |\d+\. )','',lines[i].strip()))+'</li>'); i+=1
            out.append('</'+tag+'>'); continue
        para=[s]; i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||- |\d+\. )',lines[i].strip()):
            para.append(lines[i].strip()); i+=1
        out.append('<p>'+inline(' '.join(para))+'</p>')
    return '\n'.join(out), toc

STYLE='''@font-face{font-family:Onest;src:url(assets/onest.ttf)}@font-face{font-family:Machina;src:url(assets/machina.otf);font-weight:800}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:#17212d;background:#f4f5f6;font:16px/1.65 Onest,system-ui,sans-serif}a{color:#176253;text-underline-offset:4px}header{background:#0b1220;color:#f5f7f8;padding:22px max(24px,calc((100vw - 1260px)/2));display:flex;gap:24px;align-items:center;flex-wrap:wrap}header a{color:#d3ece6;text-decoration:none;font-size:14px}.logo{font:800 22px Machina,system-ui}.report{max-width:1260px;margin:auto;display:grid;grid-template-columns:240px minmax(0,1fr);gap:48px;padding:52px 24px 100px}.report aside{position:sticky;top:24px;align-self:start;max-height:90vh;overflow:auto;font-size:13px}.report aside a{display:block;margin:0 0 10px;text-decoration:none}.report main{min-width:0;max-width:900px}h1,h2,h3{line-height:1.25;letter-spacing:-.035em}h1{font:800 clamp(30px,4vw,46px)/1.12 Machina,system-ui;letter-spacing:-.05em;margin-top:0}h2{font-size:27px;margin:54px 0 20px;scroll-margin-top:24px}h3{font-size:21px;margin:32px 0 14px}p{margin:16px 0}li{margin:9px 0}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.5}th{background:#deebe5;text-align:left}td,th{padding:13px 15px;border:1px solid #d4dcda;vertical-align:top}td{min-width:125px}tr:nth-child(2n) td{background:#fff}.table-scroll{overflow:auto}code{font:13px ui-monospace,monospace;background:#e6e9e8;padding:2px 5px;border-radius:3px;overflow-wrap:anywhere}.hub{max-width:1180px;margin:64px auto;padding:0 24px 80px}.hub h1{max-width:800px}.lead{font-size:21px;max-width:850px}.tag{font-size:12px;letter-spacing:.12em;color:#3a7162}.actions{display:flex;flex-wrap:wrap;gap:14px;margin:32px 0}.button{display:inline-block;background:#0b1220;color:white;border-radius:10px;padding:15px 22px;text-decoration:none}.button.primary{background:#7dd4c8;color:#0b1220;font-weight:bold}.panel{background:white;border:1px solid #dbe2df;border-radius:16px;padding:28px;margin:24px 0}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.cards .panel{margin:0}.cards h3{margin-top:0}.shots{display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:24px;align-items:start;margin:32px 0}.shots img{width:100%;border-radius:12px;box-shadow:0 10px 35px #0b122015}.note{border-left:4px solid #7dd4c8;padding-left:20px;color:#52605c}footer{padding:24px;text-align:center;font-size:13px;color:#5d6965}:focus-visible{outline:3px solid #d16b49;outline-offset:4px}@media(max-width:850px){.report{display:block;padding-top:32px}.report aside{position:static;max-height:none;margin-bottom:40px;border-bottom:1px solid #ccc;padding-bottom:20px}.cards{grid-template-columns:1fr}.shots{grid-template-columns:1fr}.shots img:last-child{max-width:320px}.hub{margin-top:38px}header{padding:20px 24px;gap:16px}.lead{font-size:18px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{header,aside,.actions{display:none!important}.report{display:block;padding:0}body{background:#fff;font-size:11pt}h2{page-break-after:avoid}table{font-size:9pt}tr{break-inside:avoid}a{color:inherit}}'''
(OUT/'assets/review.css').write_text(STYLE)

def shell(title, body):
    return '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+escape(title)+'</title><link rel="stylesheet" href="assets/review.css"></head><body><header><a class="logo" href="Обзор.html">FIELD / НИИ</a><a href="index.html">Лендинг для новых участников ↗</a><a href="alumni.html">Выпускникам ↗</a><a href="Стратегия.html">Стратегия</a></header>'+body+'<footer>8 октября 2026 · Локальные материалы для обсуждения</footer></body></html>'

# Copy export: all default text plus every expanded week and calendar entry.
tree=Tree((OUT/'index.html').read_text()).root
main=tree.find(lambda n:n.tag=='main')[0]
copy=['# FIELD × НН-6 — тексты предлагаемого лендинга','', '08.10.2026. Редакционный экспорт из прототипа. Все недели и месяцы раскрыты. Техническое окно демонстрационной оплаты сюда не включено.','']
def export(n):
    if n.attrs.get('aria-hidden')=='true' or n.tag in ('svg','canvas','script','style','img'): return
    cls=n.attrs.get('class','').split()
    if 'hero-art' in cls: return
    text=n.text()
    if not text: return
    if n.tag in ('h1','h2','h3'): copy.extend(['#'*int(n.tag[1])+' '+text,'']); return
    if n.tag=='summary': copy.extend(['#### '+text,'']); return
    if n.tag in ('p','li','time','footer'):
        copy.extend([('- ' if n.tag=='li' else '')+text,'']); return
    if n.tag=='a':
        href=n.attrs.get('href','')
        if href.startswith('#'): href='index.html'+href
        copy.extend(['['+text+']('+href+')','']); return
    if any(c in cls for c in ('hero-facts','track-top','track-filter-label','price-top','main-price','host','task-file','flow-line','event-type','time-note')):
        copy.extend([text,'']); return
    if n.tag=='button': copy.extend(['Кнопка: '+text,'']); return
    for c in n.children:
        if isinstance(c,Node): export(c)
export(main)
copy.extend(['## Дополнительные состояния примеров','','### Контент и визуал','','Подготовить серию материалов в своём стиле. На каждый пост снова собираете тезисы, ищете референсы и объясняете, как должен выглядеть результат.','','Бриф + примеры вашего стиля → задаёте тему, аудиторию и стиль → ИИ готовит тексты и варианты визуала → вы проверяете смысл и редактируете.','','### Повторяющаяся рутина','','Получать подборку нужных материалов. Повторяете один и тот же поиск, открываете источники и вручную выбираете, что пригодится в работе.','','Источники + правила отбора → описываете поручение и расписание → ИИ собирает материалы по правилам → вы проверяете источники и отбор.','','## Вход для выпускника','','Вернитесь в практику. Зима в FIELD.','','Три месяца новых задач, живой практики и экспертных разборов. Для выпускников кэмпов НИИ — тот же зимний цикл за половину стоимости.','','175 € или 17 500 ₽ · за три месяца.','','Впервые в НИИ? Условия для новых участников.',''])
(OUT/'04 — Тексты лендинга.md').write_text('\n'.join(copy))

# Narrow, meaningful static validation of the actual two-page artifact.
checks=[]
for page in ('index.html','alumni.html'):
    root=Tree((OUT/page).read_text()).root
    nodes=root.find(lambda n:True)
    ids=[n.attrs['id'] for n in nodes if 'id' in n.attrs]
    duplicates=[x for x,count in Counter(ids).items() if count>1]
    broken=[]
    for n in nodes:
        for attr in ('href','src'):
            value=n.attrs.get(attr,''); parts=urlsplit(value)
            if not value or parts.scheme or value.startswith('//'): continue
            if not parts.path and parts.fragment and parts.fragment not in ids: broken.append(value)
            if parts.path and not (OUT/unquote(parts.path)).is_file(): broken.append(value)
    assert not duplicates, (page,duplicates)
    assert not broken, (page,broken)
    assert len(root.find(lambda n:n.tag=='h1'))==1
    assert len(root.find(lambda n:'week' in n.attrs.get('class','').split()))==7
    assert len(root.find(lambda n:'event' in n.attrs.get('class','').split()))==19
    checks.append({'page':page,'unique_ids':len(ids),'broken_local_links':broken,'duplicate_ids':duplicates,'weeks':7,'community_events':19})
events=json.loads((OUT/'assets/calendar-source.json').read_text())
assert Counter(x['month'] for x in events)=={'nov':5,'dec':7,'jan':7}
assert Counter(x['track'] for x in events)=={'Практика':15,'Стратегия':4}

assets=[p for p in (OUT/'assets').iterdir() if p.name!='review.css']
initial=['index.html','assets/style.css','assets/app.js','assets/field-gl.js','assets/machina.otf','assets/onest.ttf','assets/onest-semibold.ttf','assets/logo.png','assets/favicon.svg']
weight=sum((OUT/p).stat().st_size for p in initial)
allweight=weight+sum((OUT/'assets'/p).stat().st_size for p in ['dmitry.webp','denis.webp','sergey.webp'])
jsweight=sum((OUT/'assets'/p).stat().st_size for p in ['app.js','field-gl.js'])
size={'core_uncompressed_bytes':weight,'with_all_portraits_uncompressed_bytes':allweight,'javascript_uncompressed_bytes':jsweight,'pdf_bytes':(OUT/'program-v8.pdf').stat().st_size,'core_files':{p:(OUT/p).stat().st_size for p in initial}}
(OUT/'проверка/static-checks.json').write_text(json.dumps({'checks':checks,'sizes':size},ensure_ascii=False,indent=2))
responsive=json.loads((OUT/'проверка/responsive.json').read_text())
assert all(x['width']==x['scrollWidth'] for x in responsive)

qa=f'''# Проверка прототипа FIELD

Дата: 08.10.2026. Проверен локальный статический сайт в браузере Codex на Chromium. Это не production, не испытание на физических телефонах и не полный аудит WCAG.

## Что прошло

| Проверка | Результат |
|---|---|
| Ширина 320 / 375 / 390 / 768 / 1024 / 1440 px | Горизонтального переполнения нет во всех шести размерах |
| Мобильный первый экран 390×844 | Цена начинается на 507 px; главный CTA расположен до неё, графика ниже |
| Мобильное меню | Открывается; выбор «Стоимость» закрывает меню и ведёт к тарифу |
| EUR → RUB | Основная цена и цена в демонстрационном окне меняются на 35 000 ₽ |
| Выпускники | Заголовок адаптирован; 175 € / 17 500 ₽, цена в окне соответствует |
| Диалог участия | Открывается; закрывается по Escape и кнопке; фокус возвращается на исходную кнопку |
| Примеры задач | «Повторяющаяся рутина» меняет задачу, проблему, материалы и три шага |
| Календарь | Декабрь показывает 7 событий; фильтр стратегии оставляет встречу 9 декабря |
| Программа | Нативный блок третьей недели открывается по клику |
| WebGL | Графика работает; ручная пауза и возобновление меняют состояние |
| Уменьшение движения | При системной настройке остаётся статичная графика; кнопка анимации скрыта |
| Потеря контекста WebGL | Принудительно проверена: включается резервная графика, текст остаётся |
| Без JavaScript | Текст, цена и все 19 событий присутствуют; динамические фильтры скрыты |
| Проверка ошибок браузера | Перед принудительным отключением WebGL ошибок и предупреждений не обнаружено |
| Синтаксис сценариев | Оба JavaScript-файла проходят проверку синтаксиса Node |
| Структура | Один h1 на страницу; 7 недель; 19 событий, из них 15 практики и 4 стратегии |
| Локальные ссылки и якоря | Нет отсутствующих файлов, повторяющихся id и несуществующих внутренних якорей |

При проверке без JavaScript браузерная автоматизация не смогла нажать accordion, поскольку её механизм клика также использует JavaScript. Проверена доступность текста и событий; раскрытие без JavaScript не объявляется отдельно проверенным. Нативный HTML `details` использован в реализации. Отключение сценариев и другие режимы эмуляции после проверки восстановлены.

## Вес ресурсов

| Набор | Без сжатия |
|---|---:|
| Основной HTML, CSS, два сценария, три шрифта, логотип и favicon | {weight/1024:.1f} КиБ |
| Тот же набор и все три фото преподавателей | {allweight/1024:.1f} КиБ |
| Два JavaScript-файла вместе | {jsweight/1024:.1f} КиБ |
| Программа PDF, только по запросу | {(OUT/'program-v8.pdf').stat().st_size/1024/1024:.2f} МиБ |

Это размеры файлов, а не сетевой замер. В сумму страницы не включены аналитические документы, скриншоты и исходный PDF, который не загружается автоматически. На production итог зависит от сжатия, кэширования, платформы, счётчиков и платёжных компонентов. Внешних исполняемых библиотек в прототипе нет.

## Чего эти проверки не доказывают

Не измерены реальные LCP / INP / CLS посетителей, конверсия, загрузка по мобильной сети и расход батареи. Не выполнены Lighthouse, полный аудит контрастов, screen reader и тесты на физическом iPhone / Android. Не проверена настоящая платёжная транзакция, доставка письма и выдача доступа.

Публичные страницы оферты и конфиденциальности доступны при чтении 08.10; применимость текста к зимнему продукту и всем валютам не оценивалась. Переходы в Telegram, отправка сообщений и платежи не выполнялись.

## Что исправлено во время проверки

На ширине 320 px заголовок FAQ создавал горизонтальный сдвиг: исправлены перенос и минимальная ширина. Исправлено размещение подписи внутри декоративной графики. Уточнено отношение сроков: семь недель кэмпа проходят внутри трёх месяцев FIELD.

## Материалы проверки

- `проверка/desktop.png` — первый экран 1280×900.
- `проверка/mobile.png` — первый экран 390×844.
- `проверка/responsive.json` — измерения ширины на шести размерах.
- `проверка/static-checks.json` — состав файлов, точные размеры и структурные проверки.

Для запуска остаётся проверка из документа «03 — Перенос в Tilda и запуск». Рост продаж не измерен; называть прототип доказанно более конверсионным пока нельзя.
'''
(OUT/'05 — Проверка качества.md').write_text(qa)

docs=[('01 — Стратегия лендинга и путь к продажам.md','Стратегия.html'),('02 — Правки текущего лендинга A.md','Правки-A.html'),('03 — Перенос в Tilda и запуск.md','Запуск.html'),('04 — Тексты лендинга.md','Тексты.html'),('05 — Проверка качества.md','Проверка.html'),('product-marketing-field.md','Контекст.html')]
for src,dest in docs:
    md=(OUT/src).read_text(); content,toc=markdown(md)
    sidebar='<aside aria-label="Содержание">'+''.join('<a href="#'+aid+'">'+escape(title)+'</a>' for aid,title in toc)+'</aside>'
    (OUT/dest).write_text(shell(md.splitlines()[0].lstrip('# '),'<div class="report">'+sidebar+'<main>'+content+'<p><a href="'+quote(src)+'">Исходный документ Markdown</a></p></main></div>'))

hub='''<main class="hub"><p class="tag">КОНЦЕПЦИЯ / ТЕКСТ / РАБОЧИЙ ПРОТОТИП · 08.10.2026</p><h1>Понятный вход в FIELD.<br>Через свою рабочую задачу.</h1><p class="lead">Рекомендуемая версия лендинга для новых участников: кэмп НН-6 внутри трёх месяцев сообщества, реальная программа, ясная стоимость и следующий шаг.</p><div class="actions"><a class="button primary" href="index.html">Открыть лендинг ↗</a><a class="button" href="Стратегия.html">Читать подробный разбор</a><a class="button" href="alumni.html">Вход для выпускника</a></div><p class="note">Это локальный прототип. Страница работает, но оплата и выдача доступа не подключены. Живой сайт не изменялся.</p><div class="shots"><a href="index.html"><img src="проверка/desktop.png" alt="Первый экран лендинга на компьютере"></a><a href="index.html"><img src="проверка/mobile.png" alt="Первый экран на телефоне"></a></div><div class="cards"><article class="panel"><h3>Почему именно так</h3><p>Позиционирование, аудит исходной страницы, сегменты, путь к покупке и входу, обоснование каждого блока, A/B-проверка и метрики.</p><a href="Стратегия.html">Стратегия и UX →</a></article><article class="panel"><h3>Что исправить уже сейчас</h3><p>Ошибки даты, продолжительности, главной кнопки, тарифов и выдачи доступа. Отдельный список для текущего aicamp6.</p><a href="Правки-A.html">Правки контроля A →</a></article><article class="panel"><h3>Как довести до запуска</h3><p>Карта блоков Tilda, действия кнопок, требования к оплате, письму и входу, порядок приёмки.</p><a href="Запуск.html">Инструкция запуска →</a></article><article class="panel"><h3>Что проверено</h3><p>Шесть размеров экрана, основные взаимодействия, режим без анимации, резервная графика и вес ресурсов.</p><a href="Проверка.html">Результаты и ограничения →</a></article><article class="panel"><h3>Тексты по блокам</h3><p>Редакционный экспорт: все недели и события раскрыты, дополнительные состояния интерактивных примеров включены.</p><a href="Тексты.html">Открыть текст →</a></article><article class="panel"><h3>Контекст продукта</h3><p>Краткий документ для будущей работы над страницей, объявлениями и письмами. Открытые условия отделены от фактов.</p><a href="Контекст.html">Маркетинговый контекст →</a></article></div><section class="panel"><h2>С чего начать просмотр</h2><ol><li>Откройте лендинг и посмотрите первый экран как человек, впервые пришедший в НИИ.</li><li>Пройдите по программе и цене. Нажмите переключатели и основную кнопку.</li><li>В разборе оцените смысловую конструкцию: своя задача → обучение → практика → участие.</li><li>Перед запуском согласуйте платёжный путь, приглашение, дополнительные подписки и окончательную программу.</li></ol><p>Исходные материалы handoff и каноны Obsidian не изменялись. Файлы можно открывать напрямую в браузере; сборка и установка программ не нужны.</p></section></main>'''
(OUT/'Обзор.html').write_text(shell('FIELD — лендинг и аналитика',hub))
print(json.dumps(size,ensure_ascii=False,indent=2))
