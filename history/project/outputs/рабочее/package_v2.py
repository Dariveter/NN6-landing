from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit, quote
from collections import Counter
import ast, json, re, zipfile

W = Path(__file__).resolve().parent
O = W.parent / 'готовое'
# Reuse renderer definitions without running any v1 packaging actions.
source = ast.parse((W / 'package_review.py').read_text())
names = {'Node', 'Tree', 'inline', 'markdown', 'shell', 'export'}
definitions = [n for n in source.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
exec(compile(ast.Module(body=definitions, type_ignores=[]), 'local-review-renderer', 'exec'))

strategy = O / '01 — Стратегия лендинга и путь к продажам.md'
s = strategy.read_text()
s = s.replace('Три ведущих кэмпа: реальная фотография, имя, роль в этой программе. Дополнительные эксперты перечислены рядом с календарём.',
'''В v2 представлены 11 человек: ведущие кэмпа, приглашённые практики и команда сообщества. Десять настоящих фотографий; для Иоганны пока инициалы. Каждая карточка объясняет роль и раскрывается по плюсу. Источники — в реестре изображений v2.''')
visual = '''## 7. Визуальный язык

Текущая редакция — светлая v2: тёплый белый фон, тёмный читаемый текст, фирменные PP Neue Machina и Onest, оригинальный логотип НИИ с тёмными буквами. Три цветные поверхности помогают различать основу, практику и стратегию.

Для страницы созданы пять иллюстраций: рабочие материалы и результат в hero, НИИшка с книгой и три предметные метафоры направлений. Изображение ментора — иллюстрация; рядом объясняется устройство ИИ-репетитора. Настоящие фотографии команды и проверенные логотипы компаний добавляют конкретность.

Подробный разбор изменений и следующих маркетинговых шагов: [Визуальная редакция v2](Визуальная-v2.html). Происхождение изображений: [Реестр](Изображения-v2.html).

## 8. Анимация и скорость

Один декоративный WebGL-canvas связывает страницу тонкими линиями по краям. Движение зависит от прокрутки; отдельно плавно двигаются иллюстрации, появляются блоки и меняются карточки при наведении. Текст остаётся обычным HTML.

Частота отрисовки ограничена 30 кадрами в секунду на широком экране и 24 на узком, плотность пикселей — 1,5 и 1 соответственно. При скрытии вкладки отрисовка прекращается. Есть ручная пауза и системный режим уменьшения движения. При недоступности графики остаются тексты, иллюстрации и функции страницы.

Изображения сохранены локально в WebP, у hero есть уменьшенная мобильная версия, остальные изображения загружаются отложенно. Нет внешней 3D-библиотеки, видеозаставки и автоматически загружаемого PDF.

Цели для опубликованной страницы: LCP ≤ 2,5 с, INP ≤ 200 мс, CLS ≤ 0,1 на 75-м перцентиле реальных посещений. Это ориентиры, а не результаты замера прототипа. [Google Web Vitals](https://web.dev/articles/vitals).

Проверенные размеры файлов и ограничения испытаний приведены в [Проверке v2](Проверка-v2.html). Подключение Tilda, счётчиков и оплаты требует повторного измерения. Расход батареи и мобильная сеть на физических устройствах пока не измерены.

Технические опоры: [MDN: WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices), [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion).

'''
s = re.sub(r'## 7\. Визуальный язык.*?(?=## 9\.)', visual, s, flags=re.S)
s = s.replace('выбор валюты, мобильная навигация и WebGL с резервным отображением', 'одинаковое отображение EUR и RUB, мобильная навигация и распределённая WebGL-анимация')
strategy.write_text(s)

launch = O / '03 — Перенос в Tilda и запуск.md'
s = launch.read_text()
s = s.replace('| Графика | Смысл «задача в центре», тихое движение, пауза | Небольшой T123 / собственный компонент; SVG как резерв |',
'''| Графика | Рабочие материалы → результат, пять иллюстраций, тихое движение, пауза | Локальные WebP и один WebGL-canvas; основное содержимое доступно независимо от графики |''')
s = s.replace('\u0060currency_select\u0060, ', '').replace(', валюта, accordion', ', отображение обеих валют, accordion')
s = s.replace('WebGL используется только в одном декоративном блоке.', 'Один WebGL-canvas создаёт лёгкие линии вдоль всей страницы.')
s = s.replace('движение останавливается за пределами экрана и при скрытой вкладке. При \u0060prefers-reduced-motion\u0060, режиме экономии данных или недоступном WebGL остаётся статичная графика.', 'отрисовка останавливается при скрытой вкладке. При системном уменьшении движения или недоступном WebGL остаются иллюстрации и весь текст страницы.')
s = s.replace('08.10.2026. Статус:', '08.10.2026. Обновлено для светлой v2. Статус:')
if '## Файлы текущей версии' not in s:
    s = s.replace('## Карта переноса', '''## Файлы текущей версии

Основные страницы: index.html и alumni.html. Стили и взаимодействия: assets/style-v2.css, assets/app-v2.js, assets/motion-v2.js. Реестр изображений и актуальная проверка находятся в документах v2. Старые style.css / app.js / field-gl.js сохранены в рабочей папке как история; новые страницы их не подключают.

## Карта переноса''')
launch.write_text(s)

v1qa = O / '05 — Проверка качества.md'
s = v1qa.read_text()
if 'АРХИВ V1' not in s:
    s = s.replace('\n\n', '\n\n**АРХИВ V1.** Этот документ фиксирует прежнюю версию. Текущие результаты находятся в [Проверке v2](Проверка-v2.html).\n\n', 1)
v1qa.write_text(s)

oldcopy = (O / '04 — Тексты лендинга.md').read_text()
copy = ['# FIELD × НН-6 — тексты светлого лендинга v2', '', '08.10.2026. Экспорт актуального HTML. Все раскрытия включены; демонстрационное окно оплаты не включено.', '']
root = Tree((O / 'index.html').read_text()).root
export(root.find(lambda n: n.tag == 'main')[0])
if '## Дополнительные состояния примеров' in oldcopy:
    extra = '## Дополнительные состояния примеров' + oldcopy.split('## Дополнительные состояния примеров', 1)[1]
    copy.append(extra.replace('175 € или 17 500 ₽', '175 евро или 17,5 тысячи рублей'))
(O / '04 — Тексты лендинга.md').write_text('\n'.join(copy))

checks = []
for page in ['index.html', 'alumni.html']:
    root = Tree((O / page).read_text()).root
    nodes = root.find(lambda n: True)
    ids = [n.attrs['id'] for n in nodes if 'id' in n.attrs]
    duplicates = [x for x, count in Counter(ids).items() if count > 1]
    broken = []
    for n in nodes:
        for attr in ('href', 'src'):
            value = n.attrs.get(attr, '')
            parts = urlsplit(value)
            if not value or parts.scheme or value.startswith('//'): continue
            if not parts.path and parts.fragment and parts.fragment not in ids: broken.append(value)
            if parts.path and not (O / unquote(parts.path)).is_file(): broken.append(value)
    assert not duplicates and not broken, (page, duplicates, broken)
    cls = lambda c: root.find(lambda n: c in n.attrs.get('class', '').split())
    assert len(root.find(lambda n: n.tag == 'h1')) == 1
    assert len(cls('week')) == 7
    assert len(cls('event')) == 19 and all(n.tag == 'details' for n in cls('event'))
    assert len(cls('person-details')) == 11
    assert len(cls('company-logo')) == 7
    checks.append(dict(page=page, broken_local_links=broken, duplicate_ids=duplicates, weeks=7, expandable_events=19, people=11, company_logos=7))

events = json.loads((O / 'assets/calendar-v2.json').read_text())
assert Counter(x['month'] for x in events) == {'nov':5, 'dec':7, 'jan':7}
assert Counter(x['track'] for x in events) == {'Практика':15, 'Стратегия':4}
assert all(x['agenda'] for x in events)
browser = json.loads((O / 'проверка/qa-v2.json').read_text())
assert all(x['width'] == x['scrollWidth'] for x in browser['responsive'])
base = ['index.html','assets/style-v2.css','assets/app-v2.js','assets/motion-v2.js','assets/machina.otf','assets/onest.ttf','assets/onest-semibold.ttf','assets/nii-logo-light.webp','assets/favicon.svg']
size = lambda names: sum((O / n).stat().st_size for n in names)
sizes = {'desktop_core_uncompressed_bytes':size(base+['assets/hero-v2.webp']),
         'mobile_core_uncompressed_bytes':size(base+['assets/hero-v2-small.webp']),
         'javascript_uncompressed_bytes':size(['assets/app-v2.js','assets/motion-v2.js']),
         'hero_desktop_bytes':size(['assets/hero-v2.webp']),
         'hero_mobile_bytes':size(['assets/hero-v2-small.webp']),
         'pdf_bytes':(O / 'program-v8.pdf').stat().st_size}
(O / 'проверка/static-v2.json').write_text(json.dumps({'checks':checks,'sizes':sizes},ensure_ascii=False,indent=2))

qa = f'''# FIELD v2 — проверка страницы

8 октября 2026. Проверен локальный сайт в Chromium браузера Codex. Изменения не опубликованы.

## Проверено

| Что | Результат |
|---|---|
| 320 / 360 / 390 / 768 / 1024 / 1280 / 1440 px | Горизонтального переполнения нет |
| Выпускники, 320 px | Переполнения нет, обе суммы имеют одинаковый размер и вес |
| Мобильное меню | Открывается; переход к программе закрывает меню |
| Календарь | Названия трёх месяцев без цифр; декабрь — 7 событий; январь + стратегия — 2 |
| Раскрытия | Событие календаря, неделя, карточка команды и пояснение ментора открываются |
| Цена | EUR и RUB одновременно, внутри блока одинаковые шрифт, размер и вес |
| Окно участия | Открывается и закрывается; явно обозначена неподключённая оплата |
| Фотографии | Все десять портретов загрузились |
| WebGL | Работает; ручная пауза прекращает движение иллюстраций и отрисовку |
| Уменьшенное движение | Canvas скрыт, движение отключено, текст виден |
| Потеря контекста WebGL | Принудительно проверена: canvas скрыт, заголовок и страница остаются |
| JavaScript отключён | Доступны текст, цена и все 19 событий |
| Ошибки браузера | В журнале ошибок после проверок не обнаружены |
| Структура | Один h1, семь недель, 19 раскрываемых событий, 11 карточек людей на страницу |
| Ссылки внутри пакета | Отсутствующих файлов, повторов id и сломанных якорей нет |

Все временные режимы проверки восстановлены. В режиме без JavaScript проверялись содержимое и доступность событий, отдельный клик по нативному раскрытию без JavaScript не заявляется проверенным.

## Размеры файлов

| Набор | Без сжатия |
|---|---:|
| HTML, CSS, два сценария, три шрифта, логотип, favicon и desktop hero | {sizes['desktop_core_uncompressed_bytes']/1024:.1f} КиБ |
| Тот же набор с мобильным hero | {sizes['mobile_core_uncompressed_bytes']/1024:.1f} КиБ |
| Два JavaScript-файла | {sizes['javascript_uncompressed_bytes']/1024:.1f} КиБ |
| Иллюстрация hero: desktop / mobile | {sizes['hero_desktop_bytes']/1024:.1f} / {sizes['hero_mobile_bytes']/1024:.1f} КиБ |
| Исходная PDF-программа, только по ссылке | {sizes['pdf_bytes']/1024/1024:.2f} МиБ |

Это сумма размеров файлов, не измерение сетевой загрузки. В первый набор не включены отложенные портреты, логотипы компаний и нижние иллюстрации: браузер может начать загружать часть из них заранее, поэтому фактический сетевой объём зависит от экрана. Документы разбора и снимки не подгружаются лендингом.

## Исправлено при проверке

На ширине 320 px заголовок FAQ увеличивал ширину страницы: исправлены переносы и ограничение ширины. Проверены переносы hero на промежуточных размерах. У выпускников убрана повторная ссылка на ту же страницу внутри тарифной карточки.

## Чего не проверяли

Реальную оплату, письмо, доступ в Telegram, внешнюю аналитику, физические iPhone / Android, мобильную сеть, батарею, полный WCAG-аудит и экранный диктор. Lighthouse и реальные LCP / INP / CLS не измерялись. Конверсия не измерена.

## Материалы

- проверка/desktop-v2.jpg и mobile-v2.jpg — первый экран.
- проверка/tracks-v2.jpg — цветные направления.
- проверка/calendar-v2.jpg — раскрытое событие.
- проверка/team-v2.jpg — начало команды.
- проверка/price-v2.jpg — оформление обеих валют.
- проверка/qa-v2.json — наблюдения браузера.
- проверка/static-v2.json — проверка файлов и размеры.

Актуальные ограничения и маркетинговые предложения — в [Разборе v2](Визуальная-v2.html).
'''
(O / '09 — Проверка v2.md').write_text(qa)

readme = '''# FIELD — светлая версия v2

Готовый локальный макет и подробный маркетинговый разбор. 08.10.2026.

Откройте Обзор.html: он объединяет страницу, разбор, тексты и результаты проверки. Для самого лендинга откройте index.html; для выпускников — alumni.html. Все файлы в папке готовы к локальному просмотру, установка программ не нужна.

## Главное

- Светлая верстка, правильный логотип, пять новых иллюстраций, мягкое движение по всей странице.
- Три понятных месяца, раскрываемые события, единый формат цены.
- 11 человек в команде, 10 настоящих фотографий, 7 оригинальных логотипов компаний.
- Проверены семь ширин от 320 до 1440 px, основной сценарий и режимы без анимации / JavaScript.

## Документы

- Визуальная-v2.html — изменения и дополнительные предложения для продаж.
- Изображения-v2.html — источники фотографий, знаков и иллюстраций.
- Проверка-v2.html — фактически выполненные проверки и ограничения.
- Стратегия.html — полный анализ продукта и пути к участию.
- Запуск.html — что потребуется для переноса и публикации.
- Тексты.html — все тексты актуальной страницы.

## Осталось определить

Настоящий портрет Иоганны; точная идентификация Лиги и окончательный список компаний; необходимые подписки и нагрузка; финальная оплата и выдача доступа.

Оплата в макете демонстрационная. Живой сайт и подключённые сервисы не менялись. Исходная программа v8 сохранена, её старые внешние платёжные ссылки не проверялись для нового сценария.
'''
(O / '00 — Начать здесь.md').write_text(readme)

css = (O / 'assets/review.css').read_text().replace('url(assets/onest.ttf)','url(onest.ttf)').replace('url(assets/machina.otf)','url(machina.otf)')
if '/* Light review v2 */' not in css:
    css += '\n/* Light review v2 */\nheader{background:#fafbf8;color:#162a2c;border-bottom:1px solid #dce5e1}header a{color:#21675f}body{background:#fafbf8}.button{background:#244a48}.report img{max-width:100%;height:auto;border-radius:12px}.button.primary{background:#c7e9dc;color:#162a2c}\n'
(O / 'assets/review.css').write_text(css)

docs = [
('01 — Стратегия лендинга и путь к продажам.md','Стратегия.html'),
('02 — Правки текущего лендинга A.md','Правки-A.html'),
('03 — Перенос в Tilda и запуск.md','Запуск.html'),
('04 — Тексты лендинга.md','Тексты.html'),
('05 — Проверка качества.md','Проверка.html'),
('product-marketing-field.md','Контекст.html'),
('07 — Визуальная редакция v2 и маркетинговый разбор.md','Визуальная-v2.html'),
('08 — Источники изображений v2.md','Изображения-v2.html'),
('09 — Проверка v2.md','Проверка-v2.html')]
for src,dest in docs:
    md = (O / src).read_text()
    content,toc = markdown(md)
    sidebar = '<aside aria-label="Содержание">'+''.join('<a href="#'+aid+'">'+escape(title)+'</a>' for aid,title in toc)+'</aside>'
    if dest == 'Визуальная-v2.html':
        content += '<h2>Визуальное направление</h2><img src="проверка/desktop-v2.jpg" alt="Первый экран светлой версии"><p></p><img src="проверка/tracks-v2.jpg" alt="Цветовые направления">'
    (O / dest).write_text(shell(md.splitlines()[0].lstrip('# '),'<div class="report">'+sidebar+'<main>'+content+'<p><a href="'+quote(src)+'">Исходный документ Markdown</a></p></main></div>'))

hub = '''<main class="hub"><p class="tag">СВЕТЛАЯ ВЕРСИЯ V2 · 08.10.2026</p><h1>ИИ для работы.<br>Люди для практики.</h1><p class="lead">Новая визуальная редакция лендинга: понятный первый экран, фирменные иллюстрации, цветные разделы, настоящая команда и лёгкое движение по всей странице.</p><div class="actions"><a class="button primary" href="index.html">Открыть лендинг ↗</a><a class="button" href="Визуальная-v2.html">Изменения и маркетинговый разбор</a><a class="button" href="alumni.html">Версия для выпускников</a></div><p class="note">Локальный макет. Оплата и выдача доступа не подключены; публичный сайт не менялся.</p><div class="shots"><a href="index.html"><img src="проверка/desktop-v2.jpg" alt="Первый экран на компьютере"></a><a href="index.html"><img src="проверка/mobile-v2.jpg" alt="Первый экран на телефоне"></a></div><div class="cards"><article class="panel"><h3>Что стало лучше</h3><p>Айдентика, изображения, цвет, взаимодействия, команда и доказательства. Восемь следующих шагов для продаж.</p><a href="Визуальная-v2.html">Разбор v2 →</a></article><article class="panel"><h3>Откуда взяты изображения</h3><p>Пять сгенерированных иллюстраций, десять реальных портретов, семь фирменных логотипов.</p><a href="Изображения-v2.html">Источники →</a></article><article class="panel"><h3>Что проверено</h3><p>Семь размеров от 320 до 1440 px, обе валюты, раскрытия, фильтры и резервное отображение.</p><a href="Проверка-v2.html">Проверка v2 →</a></article><article class="panel"><h3>Путь к покупке и участию</h3><p>Продукт, аудитория, порядок разделов, возражения, гипотезы и измерение результата.</p><a href="Стратегия.html">Полная стратегия →</a></article><article class="panel"><h3>Как запустить</h3><p>Текущие файлы, перенос в Tilda, платёжный маршрут, приглашение и приёмка.</p><a href="Запуск.html">Инструкция →</a></article><article class="panel"><h3>Все тексты</h3><p>Раскрытые недели, события, карточки команды, FAQ и состояния примеров.</p><a href="Тексты.html">Редакционный экспорт →</a></article></div><section class="panel"><h2>Что ещё нужно для публичной версии</h2><p>Настоящий портрет Иоганны, точный список компаний и нужные версии знаков, длительность занятий и подписки, реальная оплата и приглашение. Визуальная версия готова к обсуждению; рост конверсии ещё не измерен.</p></section></main>'''
(O / 'Обзор.html').write_text(shell('FIELD — светлый лендинг v2',hub))

for p in O.glob('*.html'):
    root = Tree(p.read_text()).root
    for n in root.find(lambda n: True):
        for attr in ('href','src'):
            value = n.attrs.get(attr,''); parts = urlsplit(value)
            if not value or parts.scheme or value.startswith('//') or not parts.path: continue
            assert (O / unquote(parts.path)).is_file(), (p.name,value)
print(json.dumps({'pages':checks,'sizes':sizes,'reports':len(docs)},ensure_ascii=False,indent=2))
