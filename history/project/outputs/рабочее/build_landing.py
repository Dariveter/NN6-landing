from pathlib import Path
from html import escape as e
import re, shutil, json
from PIL import Image

BASE = Path(__file__).resolve().parents[2]
OUT = BASE / "outputs" / "готовое"
ASSETS = OUT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)
BRAND = Path("/Users/bigd/Obsidian Vault/Маркетинг и бренд/Дизайн-система НИИ")
FONTS = BRAND / "nii-brand-guidelines/assets/fonts"
for name, source in {
    "machina.otf": FONTS / "PPNeueMachina/PPNeueMachina-Ultrabold.otf",
    "onest.ttf": FONTS / "Onest/Onest-Regular.ttf",
    "onest-semibold.ttf": FONTS / "Onest/Onest-SemiBold.ttf",
}.items():
    shutil.copy2(source, ASSETS / name)
shutil.copy2(Path("/Users/bigd/Obsidian Vault/Маркетинг и бренд/03_Маркетинг/Брендинг НИИ/варианты лого НИИ Нейросетей/NII_logo_white_eye.png"), ASSETS / "logo.png")
download = Path("/var/folders/dd/_c2y4k4s6f31hr52hzv1zsl80000gn/T/browser-use/assets/fc51ef0f-90c3-4363-a5f7-af39c9c8cd30")
photos = {"dmitry": "d335e54c69ade221", "denis": "ef086afccd43f93b", "sergey": "8c7a6bd691fc45ed"}
for name, source in photos.items():
    img = Image.open(download / (source + ".png")).convert("RGB")
    img.thumbnail((560, 640))
    img.save(ASSETS / (name + ".webp"), quality=83)
pdf = next((BASE / "raw").glob("FIELD*.pdf"))
shutil.copy2(pdf, OUT / "program-v8.pdf")

source = (BASE / "02 Программа Зима в FIELD v8 — источник истины.md").read_text()
community = source.split("## Практика и Стратегия — по месяцам")[1].split("## Форматы событий")[0]
events = []
month = ""
for line in community.splitlines():
    if line.startswith("### Ноябрь"): month = "nov"
    if line.startswith("### Декабрь"): month = "dec"
    if line.startswith("### Январь"): month = "jan"
    if line.startswith("- **"):
        title, host = line.removeprefix("- **").split("** — ", 1)
        day, track, rest = title.split(" · ", 2)
        fmt, title = rest.split(": ", 1)
        events.append({"month": month, "date": day, "track": track, "format": fmt,
                       "title": title, "host": host.strip() if host.strip() != "—" else "Эксперт определяется по задаче"})
assert len(events) == 19
assert sum(x["track"] == "Практика" for x in events) == 15

weeks = [
    ("01", "9–15 ноября", "Рабочее место для ИИ и первая задача", "Запуск системы",
     "Соберёте папку с материалами и правилами работы, познакомитесь с ИИ-ментором и выберете три задачи из своей рутины.",
     "9 ноября — быстрый старт. 13 ноября — выбираем первую задачу и разбираем сложности с настройками.",
     "Дмитрий Эйгенсон"),
    ("02", "16–22 ноября", "ИИ понимает ваши задачи и ограничения", "Управление и безопасность",
     "Настроите инструкции, проекты и память ChatGPT. Разберётесь, какие данные можно передавать ИИ и какие действия требуют вашего подтверждения.",
     "16 ноября — настройки. 18 ноября — мастер-класс Сергея Долгова по безопасности. 20 ноября — сравниваем работу до и после настройки.",
     "Дмитрий Эйгенсон, Сергей Долгов"),
    ("03", "23–29 ноября", "Первое поручение по расписанию", "Поручения",
     "Запустите повторяющуюся задачу: например, сборку отчёта или подборку материалов. Проверите, что происходит без вашего постоянного участия.",
     "23 ноября — постановка поручений. 27 ноября — запускаем сценарии участников и разбираем ошибки.",
     "Дмитрий Эйгенсон"),
    ("04", "30 ноября — 6 декабря", "Визуалы для вашей реальной задачи", "Визуал",
     "Соберёте серию изображений в своём стиле. Научитесь работать с референсами и исправлять отдельные части картинки.",
     "30 ноября — ИИ-дизайнер и арт-директор. 4 декабря — выставка и разбор работ участников.",
     "Денис Домрачев"),
    ("05", "7–13 декабря", "Документы и таблицы в одном процессе", "Документы и таблицы",
     "Выберете свой процесс с отчётами, таблицами или презентациями и соберёте цепочку от исходных материалов до результата, который можно проверить.",
     "7 декабря — документы, таблицы и презентации. 11 декабря — разбираем ваши цепочки и дорабатываем их.",
     "Дмитрий Эйгенсон"),
    ("06", "14–20 декабря", "Система под вашу работу", "Система целиком",
     "Соедините базу знаний, поручения и ассистентов. Подготовите проект, проверите границы автоматизации и сохраните свои материалы.",
     "14 декабря — сборка системы. 18 декабря — предзащита: показываете проект и получаете вопросы для доработки.",
     "Дмитрий Эйгенсон"),
    ("07", "21 декабря", "Показываете, что получилось", "Защита проекта",
     "Представите свой рабочий процесс и результаты его проверки. После финала кэмпа продолжите практику в FIELD.",
     "21 декабря — защита проектов. С 28 декабря по 10 января — каникулы. Программа FIELD продолжается с 11 января.",
     "Дмитрий Эйгенсон"),
]
week_html = "\n".join(f"""<details class="week" {'open' if i == 0 else ''}>
  <summary><span class="week-n">{n}</span><span class="week-title"><small>{date}</small>{title}</span><span class="plus" aria-hidden="true">+</span></summary>
  <div class="week-body"><p>{description}</p><p class="small">{agenda}</p><span class="host">Ведёт: {host}</span></div>
</details>""" for i, (n, date, title, theme, description, agenda, host) in enumerate(weeks))
event_html = "\n".join(f"""<article class="event" data-month="{x['month']}" data-track="{e(x['track'])}">
  <time>{e(x['date'])}</time><div><span class="event-type {'strategy-tag' if x['track']=='Стратегия' else ''}">{e(x['track'])} · {e(x['format'])}</span>
  <h3>{e(x['title'])}</h3><p>{e(x['host'])}</p></div><span class="event-arrow" aria-hidden="true">↗</span></article>""" for x in events)

faq = [
 ("Я только начинаю. Смогу разобраться?", "Да. Маршрут кэмпа начинается с рабочего места, базовых настроек и выбора первой задачи. Технический опыт и навыки программирования не требуются. Между встречами вы пробуете подход на своих материалах."),
 ("Нужно быть на всех 33 встречах?", "Нет. Основной маршрут новичка — занятие в понедельник, практика в течение недели и совместная работа в пятницу. Остальные события выбирайте под свои задачи. Записи всех эфиров входят в участие."),
 ("Сколько времени нужно выделять?", "Заложите два основных эфира в неделю и время, чтобы попробовать задания на своей работе. Эфиры начинаются в 19:00 по Москве, зимой это 18:00 в Израиле и 17:00 CET. Объём самостоятельной работы зависит от вашей задачи; точную длительность встреч можно уточнить у Юрия."),
 ("Какие инструменты и подписки понадобятся?", "В основе кэмпа — работа с ChatGPT; отдельные задачи могут использовать другие сервисы. Для встреч и общения нужны Zoom и Telegram. Возможности ИИ зависят от тарифа и региона. До оплаты уточните у Юрия нужные доступы и возможные дополнительные расходы."),
 ("Что будет, если я пропущу занятие?", "Можно посмотреть запись и применить материал в своём темпе. Записи и материалы доступны, пока вы в сообществе. При выходе доступ закрывается; перед этим материалы можно скачать."),
 ("Кто поможет, если что-то не получается?", "На первом занятии вы получите базовый скилл ИИ-ментора-репетитора. Вопросы по заданиям разбираются на Let's Work, в сообществе есть техподдержка по инструментам. «Стол заказов» посвящён задаче, выбранной из заявок участников. Индивидуальная разработка под ключ в этот формат не входит."),
 ("Когда заканчивается кэмп и что будет потом?", "Финальная защита кэмпа — 21 декабря. Зимний цикл FIELD идёт с ноября 2026 по январь 2027. С 28 декабря по 10 января — каникулы; затем продолжаются практика и экспертные встречи. Условия участия после зимнего цикла уточняйте у команды."),
 ("Есть ли условия для выпускников?", "Да. Для выпускников предыдущих кэмпов НИИ действует скидка 50%: 175 € или 17 500 ₽ за тот же зимний цикл. Участие включает кэмп, практику, стратегию, записи и сообщество."),
 ("Как я получу доступ после оплаты?", "Приглашение в сообщество придёт на email, указанный при оплате. Для оплаты в рублях предусмотрено автоматическое письмо, через Allpay — письмо от команды. Если приглашения нет, проверьте «Спам» и напишите Юрию Рапопорту."),
 ("Как уточнить условия возврата?", "До оплаты ознакомьтесь с офертой. Если условия для вашей ситуации непонятны, обсудите их с Юрием Рапопортом. Он также поможет с выбором валюты, доступами и участием команды."),
]
faq_html = "\n".join(f'<details class="faq-item"><summary>{q}<span class="plus" aria-hidden="true">+</span></summary><p>{a}</p></details>' for q,a in faq)

def page(alumni=False):
    heading = 'Вернитесь в практику.<br><em>Зима в FIELD.</em>' if alumni else 'Сделайте ИИ<br>частью<br><em>своей работы.</em>'
    intro = 'Три месяца новых задач, живой практики и экспертных разборов. Для выпускников кэмпов НИИ — тот же зимний цикл за половину стоимости.' if alumni else 'Научитесь поручать ИИ свою рутину и соберите рабочий процесс на собственных задачах — с преподавателями и сообществом ИИ-практиков FIELD.'
    price = "175" if alumni else "350"
    rub = "17 500" if alumni else "35 000"
    hero_label = 'ДЛЯ ВЫПУСКНИКОВ КЭМПОВ НИИ' if alumni else 'КЭМП «НАЧАЛЬНИК НЕЙРОСЕТЕЙ — 6» В FIELD'
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="robots" content="noindex,nofollow">
<title>{'Зима в FIELD — выпускникам' if alumni else 'НН-6 и Зима в FIELD'} · НИИ Нейросетей</title>
<meta name="description" content="С 9 ноября: кэмп Начальник нейросетей — 6 и три месяца в сообществе ИИ-практиков FIELD. Свои задачи, живая практика, записи и экспертные встречи.">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/machina.otf" as="font" type="font/otf" crossorigin>
<link rel="preload" href="assets/onest.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<script src="assets/app.js" defer></script>
</head>
<body data-audience="{'alumni' if alumni else 'new'}">
<a class="skip" href="#main">Перейти к содержанию</a>
<header class="header"><div class="wrap header-inner">
 <a class="brand" href="{'alumni.html' if alumni else 'index.html'}" aria-label="FIELD — НИИ Нейросетей"><img src="assets/logo.png" alt="НИИ Нейросетей" width="132" height="39"><span class="brand-divider"></span><span>FIELD<span class="brand-dot">●</span></span></a>
 <nav class="desktop-nav" aria-label="Навигация"><a href="#how">Как устроено</a><a href="#program">Программа</a><a href="#stories">Отзывы</a><a href="#price">Стоимость</a></nav>
 <a class="button button-small header-cta" href="#price" data-cta="header">Участвовать <span aria-hidden="true">↗</span></a>
 <button class="menu-button js-only" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Открыть меню"><span></span><span></span></button>
</div>
<nav id="mobile-nav" class="mobile-nav" aria-label="Мобильная навигация" hidden><a href="#how">Как устроено</a><a href="#program">Программа</a><a href="#stories">Отзывы</a><a href="#price">Стоимость</a><a href="alumni.html">Выпускникам</a></nav></header>
<main id="main">
<section class="hero" id="top">
 <div class="wrap hero-grid">
  <div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> {hero_label}</p>
   <h1>{heading}</h1>
   <p class="hero-intro">{intro}</p>
   <div class="hero-facts"><span>Старт <strong>9 ноября</strong></span><span>Онлайн</span><span>{'Для выпускников НИИ' if alumni else 'Подходит новичкам'}</span></div>
   <div class="hero-actions"><a class="button" href="#price" data-cta="hero">Выбрать участие <span aria-hidden="true">↗</span></a><a class="text-link" href="#how">Как всё устроено <span aria-hidden="true">↓</span></a></div>
   <p class="hero-price"><strong>{price} €</strong> <span>или {rub} ₽ · за три месяца</span></p>
   <a class="alumni-link" href="{'index.html' if alumni else 'alumni.html'}">{'Впервые в НИИ? Условия для новых участников' if alumni else 'Уже были на кэмпе НИИ? Для вас −50%'} <span aria-hidden="true">↗</span></a>
  </div>
  <div class="hero-art" aria-label="Учёба, практика и поддержка вокруг вашей задачи">
   <div class="art-topline"><span>ВАША ЗАДАЧА — В ЦЕНТРЕ</span><span>01 / FIELD</span></div>
   <svg class="field-fallback" viewBox="0 0 600 580" aria-hidden="true"><defs><radialGradient id="orb"><stop stop-color="#7DD4C8" stop-opacity=".32"/><stop offset="1" stop-color="#7DD4C8" stop-opacity="0"/></radialGradient></defs><circle cx="300" cy="284" r="235" fill="url(#orb)"/><g fill="none" stroke="#7DD4C8" stroke-opacity=".38"><ellipse cx="300" cy="280" rx="227" ry="104" transform="rotate(-30 300 280)"/><ellipse cx="300" cy="280" rx="214" ry="151" transform="rotate(35 300 280)"/><ellipse cx="300" cy="280" rx="211" ry="186" transform="rotate(70 300 280)"/></g></svg>
   <canvas id="field-canvas" aria-hidden="true"></canvas>
   <div class="art-core"><span>ВАШ</span><strong>рабочий<br>процесс</strong><span class="core-plus">+</span></div>
   <div class="orbit-label orbit-a"><i></i> Учёба</div><div class="orbit-label orbit-b"><i></i> Практика</div><div class="orbit-label orbit-c"><i></i> Поддержка</div>
   <div class="art-bottom"><span>Идея → проба → результат</span><button id="motion-toggle" class="motion-button js-only" type="button" aria-pressed="false" aria-label="Приостановить анимацию">Ⅱ</button></div>
  </div>
 </div>
 <div class="wrap hero-bottom"><p><strong>7 недель</strong> кэмпа НН-6</p><span aria-hidden="true">в</span><p><strong>3 месяцах</strong> участия в FIELD</p><p class="hero-bottom-note">Ноябрь 2026 — январь 2027<br>Выбирайте события под свои задачи</p></div>
</section>

<section class="proof-band" aria-labelledby="proof-title"><div class="wrap proof-grid">
 <div><span class="eyebrow">ИЗ ОПЫТА УЧАСТНИКОВ</span><h2 id="proof-title">Рутина может занимать<br>меньше места в жизни.</h2></div>
 <blockquote><p>«Я автоматизировала подготовку еженедельного международного бюллетеня, на который раньше уходило примерно 3–4 часа в неделю. Практически ноль ручного труда, только корректировка».</p><footer><span class="avatar-letter">А</span><span><strong>Анжела</strong><small>Организация по защите прав музыкальных исполнителей · НН-4</small></span></footer></blockquote>
</div><div class="wrap"><p class="proof-note">Опыт участницы прошлого кэмпа. Ваш результат зависит от задачи, практики и возможностей инструментов.</p></div></section>

<section class="section light" id="tasks"><div class="wrap">
 <div class="section-heading"><div><p class="eyebrow">01 / С ЧЕГО НАЧНЁМ</p><h2>С вашей работы.<br>И того, что хочется упростить.</h2></div><p>Одна повторяющаяся задача — хорошая точка входа. Учимся передавать ИИ материалы, задавать правила и проверять результат.</p></div>
 <div class="task-tabs js-only" role="group" aria-label="Выберите пример задачи"><button type="button" data-task="documents" aria-pressed="true">Документы и отчёты</button><button type="button" data-task="content" aria-pressed="false">Контент и визуал</button><button type="button" data-task="routine" aria-pressed="false">Повторяющаяся рутина</button></div>
 <div class="task-demo" aria-live="polite"><div class="task-start"><span class="label">ВАША ЗАДАЧА</span><h3 id="task-title">Собрать отчёт из нескольких файлов</h3><p id="task-problem">Каждую неделю открываете таблицы, сводите цифры и заново оформляете выводы.</p><span class="task-file" id="task-file">↳ Таблицы + шаблон отчёта</span></div>
 <div class="task-flow"><div class="flow-line"><b>1</b><span id="task-step1">Передаёте материалы и правила</span></div><div class="flow-line"><b>2</b><span id="task-step2">ИИ собирает черновик по шаблону</span></div><div class="flow-line"><b>3</b><span id="task-step3">Вы проверяете цифры и выводы</span></div><p class="small">Пример учебного сценария. Возможность автоматизации проверяем на ваших данных.</p></div></div>
</div></section>

<section class="section light" id="how"><div class="wrap">
 <div class="section-heading"><div><p class="eyebrow">02 / ОДНО УЧАСТИЕ — ТРИ НАПРАВЛЕНИЯ</p><h2>Освойте основу.<br>Оставайтесь в практике.</h2></div><p>FIELD — сообщество ИИ-практиков. В зимний цикл входит кэмп НН-6, работа над прикладными задачами и встречи с экспертами.</p></div>
 <div class="track-grid">
  <article class="track-card track-camp"><div class="track-top"><span>01</span><span>14 событий</span></div><span class="track-symbol" aria-hidden="true">↗</span><h3>Кэмп НН-6</h3><p>Последовательный маршрут от настройки ИИ до собственного рабочего процесса.</p><footer>9 ноября — 21 декабря<br><strong>Основа для новичка</strong></footer></article>
  <article class="track-card track-practice"><div class="track-top"><span>02</span><span>15 событий</span></div><span class="track-symbol" aria-hidden="true">✳</span><h3>Практика</h3><p>Базы знаний, сайты, документы, контент и автоматизация. Пробуете то, что нужно в вашей работе.</p><footer>Ноябрь — январь<br><strong>Выбираете свои темы</strong></footer></article>
  <article class="track-card track-strategy"><div class="track-top"><span>03</span><span>4 события</span></div><span class="track-symbol" aria-hidden="true">◎</span><h3>Стратегия</h3><p>Разговоры с экспертами о работе, человеке и компаниях рядом с ИИ. Чтобы понимать, куда двигаться.</p><footer>Ноябрь — январь<br><strong>Взгляд шире инструментов</strong></footer></article>
 </div>
 <div class="calm-note"><span class="note-symbol" aria-hidden="true">↳</span><p><strong>33 живых события — это выбор.</strong> Новичкам достаточно идти по маршруту кэмпа. Дополнительные встречи выбирайте по интересу; записи входят в участие.</p></div>
</div></section>

<section class="section dark" id="rhythm"><div class="wrap">
 <div class="section-heading"><div><p class="eyebrow">03 / РИТМ, В КОТОРОМ ЕСТЬ ВРЕМЯ СДЕЛАТЬ</p><h2>Разобрались вместе.<br>Попробовали у себя.<br><em>Вернулись с вопросами.</em></h2></div><div><p>Два основных эфира в неделю и практика между ними. Для заданий вы берёте свои документы, процессы и идеи.</p><p class="time-note">19:00 Москва · 18:00 Израиль<br><span>17:00 CET · зимнее время</span></p></div></div>
 <div class="rhythm-grid"><article><span>ПН</span><h3>Разбираем подход</h3><p>Ведущий показывает рабочий процесс целиком. Вы понимаете, как повторить его на своей задаче.</p></article><article><span>ВТ — ЧТ</span><h3>Пробуете на практике</h3><p>Переносите подход на свои материалы. ИИ-ментор помогает разбираться и двигаться по программе.</p></article><article><span>ПТ</span><h3>Дорабатываем вместе</h3><p>На Let's Work смотрим работы участников, отвечаем на вопросы и разбираем то, что не получилось.</p></article></div>
 <div class="mentor-row"><div class="mentor-sign" aria-hidden="true"><span></span><span></span></div><div><h3>ИИ-ментор — с первого занятия</h3><p>Вы получите базовый скилл — набор инструкций для ИИ-репетитора. Он помогает учиться, находить ориентиры в сообществе и собирать персональную базу знаний.</p></div></div>
</div></section>

<section class="section light" id="program"><div class="wrap program-grid">
 <div class="program-intro"><p class="eyebrow">04 / КЭМП НН-6</p><h2>Каждая неделя<br>добавляет<br>часть системы.</h2><p>Шесть учебных недель и финальная защита. Начинаем 9 ноября, проект показываете 21 декабря.</p><a class="text-link" href="program-v8.pdf" target="_blank" rel="noopener" data-cta="program-pdf">Полная программа в PDF <span aria-hidden="true">↗</span></a><div class="program-price"><strong>{price} € / {rub} ₽</strong><small>Кэмп и три месяца FIELD — вместе</small><a href="#price" class="text-link">К условиям участия →</a></div></div>
 <div class="week-list">{week_html}<p class="small program-disclaimer">Программа примерная: возможны изменения, но не существенные.</p></div>
</div></section>

<section class="section light calendar-section" id="calendar"><div class="wrap">
 <div class="section-heading"><div><p class="eyebrow">05 / ПРАКТИКА И СТРАТЕГИЯ</p><h2>За пределами кэмпа —<br>ещё 19 встреч.</h2></div><p>Можно собрать свою траекторию: личная база знаний, сайт, автоматизация, бренд или работа с клиентами.</p></div>
 <div class="calendar-toolbar js-only"><div class="month-tabs" role="group" aria-label="Месяц событий"><button type="button" data-month-filter="nov" aria-pressed="true">Ноябрь <span>5</span></button><button type="button" data-month-filter="dec" aria-pressed="false">Декабрь <span>7</span></button><button type="button" data-month-filter="jan" aria-pressed="false">Январь <span>7</span></button></div><label class="track-filter-label">Направление <select id="track-filter"><option value="all">Все</option><option value="Практика">Практика</option><option value="Стратегия">Стратегия</option></select></label></div>
 <p id="calendar-status" class="sr-only" aria-live="polite"></p><div class="event-list">{event_html}</div>
 <div class="calendar-footer"><p>Каникулы: 28 декабря — 10 января.<br>Программа примерная: возможны изменения, но не существенные.</p><a class="text-link" href="#price">Всё входит в участие <span aria-hidden="true">↗</span></a></div>
</div></section>

<section class="section dark" id="people"><div class="wrap">
 <div class="section-heading"><div><p class="eyebrow">06 / С КЕМ ВЫ БУДЕТЕ РАБОТАТЬ</p><h2>Люди, у которых<br>можно спросить «как».</h2></div><p>Преподаватели показывают процессы на экране, а на совместных встречах разбирают работы участников.</p></div>
 <div class="people-grid">
 <article class="person person-lead"><img src="assets/dmitry.webp" alt="Дмитрий Эйгенсон" width="400" height="440" loading="lazy"><div><span class="eyebrow">ОСНОВАТЕЛЬ НИИ · ИЗРАИЛЬ</span><h3>Дмитрий Эйгенсон</h3><p>Ведёт основной маршрут кэмпа: от первой задачи и настроек ИИ до поручений, документов и сборки своей системы.</p></div></article>
 <article class="person"><img src="assets/denis.webp" alt="Денис Домрачев" width="400" height="440" loading="lazy"><div><span class="eyebrow">ВИЗУАЛ И МАРКЕТИНГ · АРГЕНТИНА</span><h3>Денис Домрачев</h3><p>Визуальные материалы, бренд-бук и работа с клиентами. Ведёт визуальную неделю кэмпа и практику в FIELD.</p></div></article>
 <article class="person"><img src="assets/sergey.webp" alt="Сергей Долгов" width="400" height="440" loading="lazy"><div><span class="eyebrow">БЕЗОПАСНОСТЬ · ПОРТУГАЛИЯ</span><h3>Сергей Долгов</h3><p>Правила работы с данными и границы самостоятельных действий ИИ. Мастер-класс 18 ноября.</p></div></article>
 </div>
 <p class="experts-line">В программе FIELD также: Иоганна Алексанян · Александр Ярыгин · Юлия Кветна · Андрей Смирнов · Валентин Васин · Сергей Васильев.</p>
</div></section>

<section class="section light" id="stories"><div class="wrap">
 <div class="section-heading"><div><p class="eyebrow">07 / ОПЫТ УЧАСТНИКОВ</p><h2>У каждого —<br>своя первая победа.</h2></div><p>Эти отзывы — о предыдущих кэмпах и программах НИИ. Они показывают разные задачи и опыт участников.</p></div>
 <div class="quotes-grid">
 <blockquote class="quote-card"><span class="quote-mark" aria-hidden="true">“</span><p>«Ты как будто взял достаточно опытного сотрудника и дальше только донастраиваешь его, добавляешь знаний».</p><footer><strong>Анастасия</strong><span>Руководитель отдела закупок · НН-4</span></footer></blockquote>
 <blockquote class="quote-card"><span class="quote-mark" aria-hidden="true">“</span><p>«Я после прошлого тренинга, умея прежде только складывать ячейки в Икселе, сделала с ГПТ таблицу мониторинга финансового портфеля».</p><footer><strong>Анастасия</strong><span>Участница программ НИИ Нейросетей</span></footer></blockquote>
 <blockquote class="quote-card"><span class="quote-mark" aria-hidden="true">“</span><p>«Я так вдохновлена тем, что обычный человек может что-то сделать».</p><footer><strong>Елена</strong><span>Digital-обучение и Customer Success · НН-4</span></footer></blockquote>
 </div>
 <a class="video-link" href="https://www.youtube.com/watch?v=HfpWO6Y4aPo" target="_blank" rel="noopener" data-cta="video"><span class="play-icon" aria-hidden="true">▶</span><span><strong>Как это было у DDX Fitness</strong><small>Видеоотзыв о НИИ Нейросетей · Анна Глумакова</small></span><span aria-hidden="true">↗</span></a>
</div></section>

<section class="section price-section" id="price"><div class="wrap price-grid">
 <div class="price-intro"><p class="eyebrow">08 / ЗИМА В FIELD</p><h2>Один вход.<br>Три месяца<br><em>в практике.</em></h2><p>Ноябрь 2026 — январь 2027.<br>Кэмп НН-6 начинается 9 ноября.</p><ul class="included"><li>Все 14 событий кэмпа НН-6</li><li>15 встреч практики и 4 — стратегии</li><li>Записи эфиров и материалы</li><li>Сообщество в Telegram и техпомощь</li><li>ИИ-ментор с первого занятия</li></ul></div>
 <div class="price-card">
  <div class="price-top"><span class="label">УЧАСТНИК</span><span class="price-period">Зимний цикл · 3 месяца</span></div>
  <fieldset class="currency-switch js-only"><legend class="sr-only">Валюта отображения</legend><label><input type="radio" name="currency" value="EUR" checked><span>EUR €</span></label><label><input type="radio" name="currency" value="RUB"><span>RUB ₽</span></label></fieldset>
  <div class="main-price"><strong id="price-value">{price} €</strong><span>за весь цикл</span></div><p id="price-alternative" class="price-alternative">или {rub} ₽</p>
  <a class="button price-button" href="#join" data-checkout data-cta="pricing">Выбрать участие <span aria-hidden="true">↗</span></a>
  <div class="alumni-price"><strong>Выпускникам кэмпов НИИ — −50%</strong><p>175 € или 17 500 ₽ за тот же состав участия.</p><a href="alumni.html" class="text-link">Условия для выпускников →</a></div>
  <p class="billing-note">По оплате в шекелях и необходимым подпискам на ИИ-сервисы — уточните у Юрия до оплаты.</p>
  <a class="contact-link" href="https://t.me/stonerized" target="_blank" rel="noopener" data-cta="contact-price"><span class="contact-dot"></span> Задать вопрос Юрию <span aria-hidden="true">↗</span></a>
 </div>
 <div class="access-note"><span aria-hidden="true">↳</span><p><strong>Записи доступны, пока вы в сообществе.</strong> Перед выходом материалы можно скачать. Условия продолжения после зимнего цикла уточняйте у команды.</p></div>
</div></section>

<section class="section light join-section" id="join"><div class="wrap">
 <div class="section-heading"><div><p class="eyebrow">09 / ОТ РЕШЕНИЯ — К ПЕРВОЙ ЗАДАЧЕ</p><h2>Как вы попадёте в FIELD.</h2></div><p>В сообществе есть последовательный маршрут для старта и события, которые вы выбираете сами.</p></div>
 <ol class="join-steps"><li><span>01</span><h3>Выбираете участие</h3><p>Уточняете доступы и условия, выбираете подходящую валюту оплаты.</p></li><li><span>02</span><h3>Получаете приглашение</h3><p>Письмо с доступом придёт на email. При оплате через Allpay его отправляет команда.</p></li><li><span>03</span><h3>Начинаете со своей задачи</h3><p>9 ноября собираете рабочее место, знакомитесь с ИИ-ментором и выбираете первую задачу.</p></li></ol>
 <div class="join-contact"><p>Нужно разобраться перед решением? <strong>Юрий Рапопорт поможет с участием.</strong></p><a href="https://t.me/stonerized" class="text-link" target="_blank" rel="noopener" data-cta="contact-join">Написать Юрию ↗</a></div>
</div></section>

<section class="section light faq-section" id="faq"><div class="wrap faq-grid"><div><p class="eyebrow">10 / ДО ТОГО, КАК РЕШИТЬ</p><h2>Остались<br>вопросы?</h2><a class="text-link" href="https://t.me/stonerized" target="_blank" rel="noopener" data-cta="contact-faq">Обсудить с Юрием ↗</a></div><div>{faq_html}</div></div></section>

<section class="final-section dark"><div class="wrap final-grid"><div><p class="eyebrow">ВАША ПЕРВАЯ ЗАДАЧА УЖЕ ЕСТЬ В ВАШЕЙ РАБОТЕ</p><h2>Начнём с неё.</h2><p>Кэмп НН-6 и сообщество ИИ-практиков FIELD.<br>Старт 9 ноября · три месяца учёбы и практики.</p></div><div><a href="#price" class="button" data-cta="final">Выбрать участие <span aria-hidden="true">↗</span></a><a href="https://t.me/stonerized" class="text-link" target="_blank" rel="noopener" data-cta="contact-final">Сначала задать вопрос ↗</a></div></div></section>
</main>
<footer class="footer dark"><div class="wrap footer-top"><a class="brand" href="#top"><img src="assets/logo.png" alt="НИИ Нейросетей" width="132" height="39"></a><p>FIELD · Сообщество ИИ-практиков</p><a href="https://t.me/stonerized" target="_blank" rel="noopener" data-cta="b2b">Участие команды ↗</a></div><div class="wrap footer-bottom"><span>НИИ Нейросетей · 2026</span><a href="https://ne-institute.com/oferta" target="_blank" rel="noopener">Публичная оферта</a><a href="https://ne-institute.com/privacy" target="_blank" rel="noopener">Конфиденциальность</a><a href="mailto:yuri.rapoport@mail.ru">yuri.rapoport@mail.ru</a></div></footer>
<div class="mobile-dock js-only" hidden><span><strong class="dock-price">{price} €</strong><small>за 3 месяца</small></span><a class="button button-small" href="#price" data-cta="mobile-dock">Участвовать ↗</a></div>
<dialog id="checkout-dialog" aria-labelledby="checkout-title"><div class="dialog-inner"><button class="dialog-close" type="button" aria-label="Закрыть окно">×</button><p class="eyebrow">ЛОКАЛЬНЫЙ ПРОТОТИП</p><h2 id="checkout-title">Участие в зимнем FIELD</h2><p class="dialog-price">{price} €</p><p>Кэмп НН-6, практика, стратегия, записи и сообщество на три месяца.</p><div class="preview-disclosure"><strong>Оплата в прототипе не подключена.</strong><p>Здесь будет переход к подтверждённой платёжной форме. Сейчас можно обсудить участие с Юрием.</p></div><a href="https://t.me/stonerized" class="button" target="_blank" rel="noopener" data-cta="contact-dialog">Написать Юрию ↗</a><button type="button" class="dialog-back">Вернуться к странице</button></div></dialog>
<noscript><style>.js-only{{display:none!important}}.event[hidden]{{display:grid}}</style></noscript>
</body></html>"""

(OUT / "index.html").write_text(page(False))
(OUT / "alumni.html").write_text(page(True))
(ASSETS / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#7DD4C8"/><path d="M20 15h27v8H29v7h15v8H29v13h-9z" fill="#0B1220"/></svg>')
(ASSETS / "calendar-source.json").write_text(json.dumps(events, ensure_ascii=False, indent=2))
print(str(OUT))
print("19 community events; 7 camp weeks; 2 HTML pages")
