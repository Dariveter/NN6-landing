from pathlib import Path
from html import escape as e
import re, json

W=Path(__file__).parent
O=W.parent/'готовое'
A=O/'assets'
R=W/'v3-research'
bank=W.parents[1]/'07 Банк отзывов и доказательств.md'

def section(html, sid, replacement):
    pattern=r'<section\b[^>]*\bid="'+sid+r'"[^>]*>.*?</section>'
    result,n=re.subn(pattern,lambda m:replacement,html,count=1,flags=re.S)
    assert n==1,sid
    return result

def heading(number,question,answer='',extra=''):
    return f'<div class="question-head"><div><span class="section-index">{number}</span><h2>{question}</h2>{f"<p class=section-answer>{answer}</p>" if answer else ""}</div>{extra}</div>'

def icon(kind,cls=''):
    paths={
      'camp':'<path d="M12 16h26v34H12zM38 16h26v34H38M18 25h12m-12 8h12m16-8h12m-12 8h12"/><path d="m30 55 8 7 8-7"/>',
      'practice':'<path d="m18 23 18-9 18 9-18 10zM18 23v23l18 11 18-11V23M36 33v24"/><path d="m53 52 7 7 13-17"/>',
      'strategy':'<circle cx="38" cy="37" r="25"/><path d="m48 23-5 20-19 8 8-21zM38 5v7m0 50v7M6 37h7m49 0h7"/>',
      'podcast':'<rect x="28" y="10" width="20" height="34" rx="10"/><path d="M19 31v5a19 19 0 0 0 38 0v-5M38 55v11M26 66h24M4 24v18m68-18v18"/>',
      'workshop':'<path d="m14 55 32-32m-8-8 8-8 19 19-8 8zM10 49l12 12-10 8-10-10zM50 51l16 16M55 46l-9 9"/><path d="M17 9v14M10 16h14"/>',
      'case':'<path d="M9 19h25l7 8h28v34H9zM9 19v-6h20l7 6"/><path d="m24 44 9 8 18-18"/>',
      'order':'<path d="M13 12h46v47H13zM22 24h27M22 33h18"/><path d="m43 42 24 8-11 5-6 13z"/>',
      'master':'<path d="M8 12h60v39H8zM27 65l11-14 11 14M21 24h16m-16 9h28"/><circle cx="58" cy="57" r="9"/>',
      'video':'<path d="M10 15h42v45H10zM52 29l18-10v37L52 46"/><path d="m25 27 14 10-14 10z"/>'
    }
    return f'<svg class="drawn-icon {cls}" viewBox="0 0 78 78" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[kind]}</svg>'

# Product-native diagrams keep labels and numbers accessible; these are teaching examples.
def papers(labels,after=False):
    if after:
        visual='<div class="tiny-chart"><i></i><i></i><i></i><i></i><i></i></div>'
        if labels[0]=='План публикаций':
            visual='<div class="tiny-posts"><i><b>ПН</b><span></span></i><i><b>СР</b><span></span></i><i><b>ПТ</b><span></span></i></div>'
        elif labels[0]=='Мой дайджест':
            visual='<div class="tiny-digest"><i><b>01</b><span>Обзор рынка</span></i><i><b>02</b><span>Полезный приём</span></i><i><b>03</b><span>Что попробовать</span></i></div>'
        return '<div class="report-sheet"><div class="sheet-title">'+labels[0]+'</div><div class="sheet-rule"></div>'+visual+'<div class="sheet-check">✓ '+labels[1]+'</div><div class="sheet-check">✓ '+labels[2]+'</div></div><span class="diagram-stamp">ПРОВЕРЯЮ<br>РЕЗУЛЬТАТ</span>'
    return '<div class="paper-stack">'+''.join(f'<div class="paper paper-{i}"><span>{label}</span><i></i><i></i><i></i></div>' for i,label in enumerate(labels))+'</div><span class="diagram-scribble" aria-hidden="true">↝ ↝ ↝</span>'

tasks_data=[
 ('documents','Документы и отчёты','Собрать отчёт из нескольких файлов',
  ['Продажи','Расходы','План'],['Сводный отчёт','Цифры на месте','Выводы проверены'],
  'Открываю файлы, свожу цифры, переношу данные в отчёт.',
  'Передаю материалы и шаблон. ИИ собирает черновик, я проверяю цифры и выводы.'),
 ('content','Контент и визуал','Подготовить серию материалов в своём стиле',
  ['Тезисы','Референсы','Правки'],['План публикаций','Мой стиль','Моя редактура'],
  'Для каждой публикации заново собираю идеи, тексты и примеры оформления.',
  'Задаю аудиторию и стиль. Получаю варианты текста и визуала, выбираю и редактирую.'),
 ('routine','Повторяющаяся рутина','Получать подборку нужных материалов',
  ['Источники','Ссылки','Заметки'],['Мой дайджест','Ссылки сохранены','Факты проверены'],
  'Повторяю поиск, открываю источники и вручную собираю полезное.',
  'Описываю поручение и правила отбора. ИИ собирает подборку, я проверяю источники.')
]
task_buttons=''.join(f'<button type="button" data-demo="{k}" aria-pressed="{str(i==0).lower()}" aria-controls="demo-{k}">{label}</button>' for i,(k,label,*_) in enumerate(tasks_data))
task_panels=''
for k,label,title,before,after,btxt,atxt in tasks_data:
    task_panels+=f'''<article class="comparison-panel" id="demo-{k}" data-demo-panel="{k}"><h3>{title}</h3><div class="comparison"><div class="compare-side before"><p class="compare-label"><span>ДО</span> Без ИИ</p><div class="work-diagram" role="img" aria-label="Разрозненные материалы: {', '.join(before)}">{papers(before)}</div><p>{btxt}</p></div><div class="compare-side after"><p class="compare-label"><span>ПОСЛЕ</span> С ИИ</p><div class="work-diagram" role="img" aria-label="{after[0]} с проверкой человеком">{papers(after,True)}</div><p>{atxt}</p></div></div></article>'''
tasks='<section class="section" id="tasks"><div class="wrap">'+heading('01','С чего начнём?','С вашей работы.<br>И того, что хочется упростить.')+f'<div class="task-tabs js-only" aria-label="Выберите пример задачи">{task_buttons}</div>{task_panels}<p class="example-note">Учебные примеры. Начинаем с одной своей задачи; результат всегда проверяет человек.</p></div></section>'

track_data=[
 ('camp','Кэмп НН-6','14','событий','Основа для новичка','Последовательный маршрут от настройки ИИ до собственного рабочего процесса.','9 ноября — 21 декабря','#program'),
 ('practice','Практика','15','мероприятий','Выбирайте свои темы','Базы знаний, сайты, документы, контент и автоматизация для вашей работы.','Ноябрь — январь','#calendar'),
 ('strategy','Стратегия','4','мероприятия','Понимание пути компании и собственной карьеры','Обсуждаем с экспертами, как ИИ меняет работу, решения и нас самих.','Ноябрь — январь','#calendar')]
track_cards=''
for k,name,count,unit,benefit,desc,period,target in track_data:
    track_cards+=f'''<a class="track-poster track-{k}" href="{target}" data-cta="track-{k}"><div class="poster-top"><span>{name}</span><span class="poster-arrow" aria-hidden="true">↗</span></div><div class="poster-visual">{icon(k)}<div class="event-count"><strong>{count}</strong><span>{unit}</span></div></div><h3>{benefit}</h3><p>{desc}</p><footer>{period}<span>Входит в участие</span></footer></a>'''
tracks='<section class="section" id="how"><div class="wrap">'+heading('02','Что входит в участие?','Кэмп, практика и стратегия.<br>Три направления — одна программа.')+f'<div class="track-grid">{track_cards}</div><p class="choice-note"><strong>Все 33 события доступны вам.</strong> Новичкам достаточно идти по маршруту кэмпа. Остальные встречи выбирайте под свои задачи; записи входят в участие.</p></div></section>'

rhythm='<section class="section" id="rhythm"><div class="wrap">'+heading('03','Как будет проходить неделя?','Разбираемся вместе. Пробуем у себя.<br>Возвращаемся с вопросами.',
 '<p class="week-time"><strong>19:00 Москва</strong><span>18:00 Израиль · 17:00 CET</span><small>Зимнее время основных эфиров</small></p>')+'''
<div class="week-board" aria-label="Типовая неделя кэмпа"><div class="week-label">ВАША НЕДЕЛЯ В КЭМПЕ <span>Практика встроена в рабочий ритм</span></div><div class="week-days"><b>ПН</b><b>ВТ</b><b>СР</b><b>ЧТ</b><b>ПТ</b><b>СБ</b><b>ВС</b></div><div class="week-schedule"><article class="day-live monday"><span class="day-mobile">ПОНЕДЕЛЬНИК</span><span class="week-kind">ЭФИР</span><h3>Разбираем<br>подход</h3><p>Ведущий показывает процесс на рабочей задаче.</p></article><article class="day-practice"><span class="day-mobile">ВТОРНИК — ЧЕТВЕРГ</span><span class="week-kind">СВОЯ ПРАКТИКА</span><h3>Пробуете<br>на практике</h3><p>Применяете подход к своим материалам. Сохраняете вопросы и находки.</p><div class="practice-path" aria-hidden="true"><span>Проба</span><i>→</i><span>Вопрос</span><i>→</i><span>Решение</span></div></article><article class="day-live friday"><span class="day-mobile">ПЯТНИЦА</span><span class="week-kind">LET’S WORK</span><h3>Дорабатываем<br>вместе</h3><p>Разбор работ, ответы на вопросы, следующий шаг.</p></article><div class="day-rest"><span class="day-mobile">ВЫХОДНЫЕ</span><span>〰</span><p>В своём<br>ритме</p></div></div></div><p class="example-note">Дополнительные мероприятия — по календарю ниже. Посещать все встречи не обязательно.</p>
<div class="mentor-row"><img src="assets/mentor-v3.webp" alt="НИИшка и рука наставника помогают разобрать вопрос на шаги" width="900" height="600" loading="lazy"><div><p class="support-label">ПОДДЕРЖКА МЕЖДУ ЭФИРАМИ</p><h3>Мы рядом, когда вы<br>застряли на задаче.</h3><p>На первом занятии настроите ИИ-ментора. Он поможет разложить задачу на шаги и разобраться в материале. Вопросы по вашей работе принесёте преподавателям и сообществу.</p><details class="mentor-details"><summary>Как устроен ИИ-ментор<span class="plus" aria-hidden="true">+</span></summary><p>Вы получаете инструкции для ИИ-репетитора и используете их в своём ИИ-инструменте. Ответы и решения проверяете вы. Живая поддержка дополняет работу ментора.</p></details></div></div></div></section>'''

logos=[('askona-logo.svg','Askona',''),('ddx-logo.svg','DDX Fitness',''),('wrf-logo.webp','White Rabbit Family','logo-wrf'),('corestone-logo.webp','Corestone',''),('murom-logo.webp','Муром',''),('samolet-logo.svg','Самолёт',''),('b2b-zdravservice.webp','Здравсервис',''),('b2b-samolet-plus.webp','Самолёт Плюс',''),('b2b-polair.webp','POLAIR',''),('b2b-everia.webp','Everia Life',''),('b2b-unicom.png','UNIQOM',''),('b2b-dobrograd.webp','Доброград',''),('b2b-hart.webp','Hart','')]
company='<section class="companies" id="companies"><div class="wrap"><div class="companies-heading"><h2>С нами учились<br>и работали</h2><p>Опыт НИИ — обучение и прикладные программы для команд бизнеса.</p></div><div class="company-grid">'+''.join(f'<div class="company-logo {cls}"><img src="assets/{fn}" alt="{name}" loading="lazy" width="190" height="80"><span>{name}</span></div>' for fn,name,cls in logos)+'''<a class="company-cta" href="https://t.me/stonerized" target="_blank" rel="noopener" data-cta="b2b-logos">Обсудить условия<br>для вашей команды<span aria-hidden="true">↗</span></a></div></div></section>'''

events=json.loads((A/'calendar-v2.json').read_text())
def format_info(fmt):
    if 'Подкаст' in fmt: return 'podcast','Подкаст','Разговор с экспертом'
    if 'Воркшоп' in fmt: return 'workshop','Воркшоп','Делаем вместе'
    if 'Case Study' in fmt: return 'case','Разбор кейса','Реальный опыт'
    if 'Стол заказов' in fmt: return 'order','Стол заказов','Ваша задача в эфире'
    return 'master','Мастер-класс','Приём в действии'
event_cards=''
for x in events:
    k,label,sub=format_info(x['format']);track='strategy' if x['track']=='Стратегия' else 'practice'
    agenda=''.join('<li>'+e(t)+'</li>' for t in x['agenda'])
    extra=' · встреча 1 из 2' if '1 из 2' in x['format'] else (' · встреча 2 из 2' if '2 из 2' in x['format'] else '')
    event_cards+=f'''<details class="event event-{track}" data-month="{x['month']}" data-track="{x['track']}"><summary><div class="event-cover">{icon(k)}<span>{label}</span></div><div class="event-main"><div class="event-meta"><span class="track-label">{x['track']}</span><time>{e(x['date'])}</time></div><h3>{e(x['title'])}</h3><p class="event-format">{label}{extra}<span>{sub}</span></p><p class="event-host">{e(x['host'])}</p></div><span class="plus" aria-hidden="true">+</span></summary><div class="event-body"><ul>{agenda}</ul><p class="event-time">19:00 Москва · 18:00 Израиль · 17:00 CET</p></div></details>'''
calendar='<section class="section" id="calendar"><div class="wrap">'+heading('05','Что ещё в программе?','Кроме основного кэмпа — ещё <strong>19 мероприятий.</strong>')+'''
<div class="format-guide"><span>ФОРМАТЫ</span><span>🎙 Подкаст</span><span>🛠 Воркшоп</span><span>▣ Разбор кейса</span><span>✳ Стол заказов</span><span>↗ Мастер-класс</span></div>
<div class="calendar-tools js-only"><div class="month-tabs" role="group" aria-label="Месяц событий"><button data-month-filter="nov" aria-pressed="true">Ноябрь</button><button data-month-filter="dec" aria-pressed="false">Декабрь</button><button data-month-filter="jan" aria-pressed="false">Январь</button></div><label class="track-filter-label" for="track-filter">Направление <select id="track-filter"><option value="all">Все</option><option value="Практика">Практика</option><option value="Стратегия">Стратегия</option></select></label></div><p id="calendar-status" class="sr-only" aria-live="polite"></p><div class="event-list">'''+event_cards+'''</div><div class="calendar-footer"><p>Каникулы: 28 декабря — 10 января.<br><small>Возможны несущественные изменения программы.</small></p><a class="text-link" href="#price">Всё входит в участие ↗</a></div></div></section>'''

# Source-backed stories: exact quotes and editorial summaries are separate fields.
cases=json.loads((R/'approved-cases.json').read_text())
story_specs=[
 ('Анжела','Анжела Абелян','Организация по защите прав музыкальных исполнителей','Бюллетень, который собирается сам','Раньше — 3–4 часа еженедельного мониторинга. Теперь настроенный процесс собирает выпуск со ссылками на источники; Анжела проверяет и корректирует результат.','Практически ноль ручного труда, только корректировка','routine'),
 ('Снежана','Снежана','Backend-разработчик','Три задачи — в первый день','Собрала для ИИ контекст проекта, правила безопасности и порядок проверки. Из восьми задач, оставленных руководительницей на время отпуска, закрыла три в первый день.','Начальница ушла в отпуск на три недели, оставила мне восемь задач. Я сегодня с помощью этого скилла закончила три','work'),
 ('Анастасия Павлова','Анастасия','Руководитель отдела закупок','Рабочая сводка из нескольких файлов','Передала ИИ файлы и логику консолидации отчётов. Получила сводку, которую осталось проверить и поправить; раньше ручная сборка занимала до двух часов.','Ты как будто взял достаточно опытного сотрудника и дальше только донастраиваешь его, добавляешь знаний','work'),
 ('Елена Серова','Елена Серова','Digital-обучение и Customer Success','Свой центр материалов и выбора тестов','Собрала примерно за день рабочую версию Assessment Hub с подбором тестов, видео и гайдами. Решение встроили в платформу компании.','Я так вдохновлена тем, что обычный человек может что-то сделать','content'),
 ('Ольга Тарасова','Ольга Тарасова','Режиссёр и продюсер','Презентация для реального клиента','По образцу готовой презентации собрала новую с другими данными и продала её клиенту. По её описанию, Claude сэкономил минимум неделю работы.','Чем сильнее режиссёр, тем талантливее работы','content'),
 ('Надежда','Надежда Фоминых','Руководитель аппарата президента холдинга','От экспериментов — к рабочей системе','Настраивает контекст под свои функции и переносит идеи из проектов участников на собственные задачи. Подключает инструменты по необходимости.','Есть те, кто играется, и те, кто работает и внедряет, — они в разных весовых категориях','work'),
 ('Олеся','Олеся Руденко','Финансовый консультант','Экспертиза — человеку. Рутина — ИИ','Сравнивает версии финансовых моделей, проверяет технические ошибки и анализирует данные во время встреч. Методологию и оценку результата оставляет за собой.','Я помогаю сформулировать методологию и подход. А нейросеть уберёт всю рутину, которую вы боитесь','work'),
 ('Галина','Галина','Юрист-консультант','Больше времени на сам анализ','Использует ИИ для предварительной выборки и сопоставления фактов из больших массивов документов. Проверку и профессиональную интерпретацию выполняет сама.','Задачи, на которых мы раньше нарабатывали практику, внимательность, аналитику, скрупулёзность, — они улетают часто на пять минут','work'),
 ('Андрей','Андрей Идиатулин','Владелец компании интерьерных технологий','Из каталога и прайса — в предложение','Собрал шаблон презентации с описанием товаров, характеристиками и сметой, а также опросник для продавца. Инженерные знания стали доступнее команде продаж.','','work'),
 ('Борис','Борис Белкин','ИТ-управление и стартапы','Инструменты соединились в одну воронку','Связал поиск потенциальных клиентов, тексты, автоответчик, лендинг, таблицу и итоговый отчёт. На защите демонстрировал работающую цепочку.','Факт сам по себе достаточно интересный, и он мощный, потому что это работает','routine'),
 ('Лена','Лена Прудникова','Маркетинговые исследования','ИИ на разных этапах исследования','Использует Claude для анализа интервью и больших массивов текста, предварительного сбора рыночной информации и сложных статистических задач.','','content'),
 ('Анастасия Гаспар','Анастасия Гаспар','Консалтинг в фармацевтике','Сайт и материалы для своей практики','Создала сайт, материалы для клиентов, базы контактов и контрактов, печатную инфографику. ИИ встроился в развитие её собственного консалтинга.','Я вообще никогда не была дизайнером. Сейчас уже во всём этом тоже разобралась','content'),
]
stories=[]
for i,(needle,name,role,title,summary,quote,category) in enumerate(story_specs):
    src=next(x for x in cases if needle in Path(x['file']).name)
    text=re.sub(r'\s+',' ',src['text'])
    if quote:
        normalize=lambda t:re.sub(r'\W+','',t).lower()
        assert normalize(quote) in normalize(text),(name,'quote mismatch')
    stories.append(dict(id='story-'+str(i+1),name=name,role=role,title=title,summary=summary,quote=quote,category=category,kind='case',source=src['file']))
extra=[
 ('Иван','Участник программ НИИ','Система для своих целей','К 10 календарному дню обучения понял связки Notebook LM, клода и обсидиана […] А затем используя методологию, связал все в систему управления по сути жизнью через призму достижения целей и баланса работы и отдыха. Да еще и дашборд создал для отслеживания прогресса','work'),
 ('Ирина','Участница программ НИИ','Новый взгляд на свой продукт','Голубой океан применён к своему продукту / ERRC-сетка готова / Три группы не-клиентов определены','work'),
 ('Анастасия','Участница программ НИИ','Порядок в идеях и проектах','AI коуч - крутейший! Сразу все структурировал, убрал хаос, дал идеи для проектов. Спасибо за такое задание и инструмент!','work')]
for name,role,title,quote,cat in extra:
    stories.append(dict(id='story-'+str(len(stories)+1),name=name,role=role,title=title,summary='',quote=quote,category=cat,kind='quote',source=str(bank)))
videos=[
 ('HfpWO6Y4aPo','Анна Глумакова','DDX Fitness','Корпоративное обучение'),
 ('_2A0CNZSMe0','Миха Нешер','Недвижимость в Израиле и Европе','ИИ в работе предпринимателя'),
 ('93-2lGITv08','Роман Янушевский','Участник программ НИИ','Опыт после кэмпа'),
 ('d9TLypIPpiA','Антон','Предприниматель','Впечатления об обучении'),
 ('zcXYXs12mmk','Ольга','Участница программ НИИ','Личная история'),
 ('7RdnUkCqAx0','Участники воркшопа','Лондон','После живого воркшопа'),
 ('agnpxXXyznQ','Участник интенсива','Программы НИИ','После интенсива'),
 ('IS7-BdRhfYk','Участник интенсива','Программы НИИ','Впечатления об интенсиве'),
 ('gPeYRxmDL5M','Участник интенсива','Программы НИИ','Опыт обучения'),
 ('tgsH1L6wj4Q','Участники интенсива','Программы НИИ','Голоса участников'),
 ('Ew4fDEOxebw','Участник программ НИИ','Видеоотзыв','Обучение в НИИ'),
 ('x2G9WeEpvXg','Участник программ НИИ','Видеоотзыв','Личные впечатления'),
 ('Nj040Bt61kU','Участник программ НИИ','Видеоотзыв','Опыт участника'),
 ('sExRNmHIDJk','Участник программ НИИ','Видеоотзыв','О программах НИИ')]
for vid,name,role,title in videos:
    stories.append(dict(id=vid,name=name,role=role,title=title,summary='',quote='',category='video',kind='video',url='https://www.youtube.com/watch?v='+vid,source=str(bank)))
(A/'stories-v3.json').write_text(json.dumps([{k:v for k,v in s.items() if k!='source'} for s in stories],ensure_ascii=False,indent=2))
(R/'review-sources.json').write_text(json.dumps(stories,ensure_ascii=False,indent=2))

def story_card(s,full=False,i=0):
    top=f'<span class="review-kind">{"ВИДЕО" if s["kind"]=="video" else ("ИСТОРИЯ УЧАСТНИКА" if s["kind"]=="case" else "ОТЗЫВ")}</span>'
    person=f'<footer><span class="person-initial">{e(s["name"][0])}</span><div><strong>{e(s["name"])}</strong><span>{e(s["role"])}</span></div></footer>'
    if s['kind']=='video':
        content=f'<a class="video-poster" href="{s["url"]}" target="_blank" rel="noopener" aria-label="Смотреть видео: {e(s["title"])} — {e(s["name"])}"><span class="play-circle" aria-hidden="true">▶</span>{icon("video")}<span>Смотреть на YouTube ↗</span></a><h3>{e(s["title"])}</h3>'
    else:
        content=f'<h3>{e(s["title"])}</h3>'
        if s['summary']:content+=f'<p class="case-summary">{e(s["summary"])}</p>'
        if s['quote']:content+=f'<blockquote>«{e(s["quote"])}»</blockquote>'
    if not full:content+=f'<a class="story-more" href="reviews.html#{s["id"]}">Читать историю ↗</a>'
    return f'<article class="review-card review-tone-{i%3}" id="{s["id"] if full else "preview-"+s["id"]}" data-review-type="{s["kind"]}">{top}{content}{person}</article>'
preview_cards=''.join(story_card(stories[i],i=i) for i in [0,1,2,3,4,5])
reviews_section='<section class="section" id="stories"><div class="wrap">'+heading('07','Что получилось у участников?','Рабочие задачи. Живые люди.<br>Результаты, которые можно объяснить.')+f'<div class="review-grid">{preview_cards}</div><div class="all-reviews"><div><strong>29</strong><span>историй, отзывов<br>и видео в подборке</span></div><a class="button" href="reviews.html" data-cta="all-reviews">Все отзывы и истории <span aria-hidden="true">↗</span></a></div><p class="example-note">Опыт участников предыдущих программ НИИ. Результат зависит от задачи, практики и возможностей инструментов.</p></div></section>'

for fn in ['index.html','alumni.html']:
    s=(W/('v2-'+fn)).read_text();alumni=fn=='alumni.html'
    s=s.replace('style-v2.css','style-v3.css').replace('app-v2.js','app-v3.js')
    s=s.replace('assets/hero-v2-small.webp','assets/hero-v3-small.webp').replace('assets/hero-v2.webp','assets/hero-v3.webp')
    s=s.replace('ВАША РАБОТА, НА НОВОМ УРОВНЕ','ЧЕЛОВЕК РЕШАЕТ. ИИ ПОМОГАЕТ.')
    s=re.sub(r'<span class="floating-note.*?</span><span class="floating-note.*?</span>','',s)
    s=s.replace('<span class="floating-note note-input"><i class="note-dot"></i> Ваши материалы</span>','')
    s=s.replace('<span class="floating-note note-result"><i>✓</i> Результат под контролем</span>','')
    s=s.replace('Документы, таблицы и письма складываются в организованный рабочий процесс','Человек превращает разрозненные материалы в понятный рабочий результат с помощью ИИ')
    s=s.replace('· НН-4','').replace(' · НН4','')
    s=section(s,'companies',company)
    s=section(s,'tasks',tasks)
    s=section(s,'how',tracks)
    s=section(s,'rhythm',rhythm)
    program=re.search(r'<section\b[^>]*id="program".*?</section>',s,re.S)[0]
    weeks=re.search(r'<div class="weeks">.*',program,re.S)
    if not weeks:
        weeks=re.search(r'<div class="week-list">.*',program,re.S)
    assert weeks
    tail=weeks[0]
    program_new='''<section class="section camp-section" id="program"><div class="wrap program-grid"><div class="program-intro"><span class="section-index">04</span><div class="camp-wordmark" aria-label="Кэмп НН-6"><span>КЭМП</span><b>НН<span>6</span></b></div><h2>Как устроен<br>основной кэмп?</h2><p class="section-answer">Шесть учебных недель<br>и финальная защита.</p><p>Начинаем 9 ноября.<br>Проект показываете 21 декабря.</p><div class="camp-included">Входит в трёхмесячную<br>программу FIELD</div><a class="text-link" href="program-v8.pdf" target="_blank" rel="noopener" data-cta="program-pdf">Полная программа в PDF ↗</a></div>'''+tail
    s=section(s,'program',program_new)
    s=section(s,'calendar',calendar)
    people=re.search(r'<section\b[^>]*id="people".*?</section>',s,re.S)[0]
    people=re.sub(r'<article class="person"><img src="assets/(?:gulnara|yuri)\.webp".*?</article>','',people,flags=re.S)
    people=re.sub(r'<article class="person person-community">.*?</article>','',people,flags=re.S)
    people=re.sub(r'<div class="section-heading">.*?(?=<div class="people-grid">)',heading('06','Кто будет с вами?','Команда НИИ Нейросетей<br>и сообщество Field','<p class="team-explainer">Преподаватели и практики, которые будут вести занятия, разборы и встречи этой зимой.</p>'),people,flags=re.S)
    s=section(s,'people',people)
    s=section(s,'stories',reviews_section)
    s=s.replace('<p class="eyebrow">08 / ЗИМА В FIELD</p><h2>Один вход.<br> Три месяца<br> <em>в практике.</em></h2>','<span class="section-index">08</span><h2>Сколько стоит<br>всё участие?</h2>')
    s=s.replace('<p class="eyebrow">09 / ОТ РЕШЕНИЯ — К ПЕРВОЙ ЗАДАЧЕ</p><h2>Как вы попадёте в FIELD.</h2>','<span class="section-index">09</span><h2>Что будет<br>после оплаты?</h2>')
    s=s.replace('<p class="eyebrow">10 / ДО ТОГО, КАК РЕШИТЬ</p><h2>Остались<br> вопросы?</h2>','<span class="section-index">10</span><h2>Что ещё<br>важно знать?</h2>')
    s=s.replace('Зимний цикл · 3 месяца','Вся программа · 3 месяца')
    s=s.replace('<h2>Начнём с неё.</h2>','<h2>С какой задачей<br>придёте вы?</h2>')
    s=s.replace('hero-image"','hero-image"')
    assert 'Гульнара' not in s
    assert 'Лига»' not in s and 'Арт-Моторс' not in s and 'Ланцет' not in s
    assert not re.search(r'350|175|тысяч|евро',re.search(r'<section\b[^>]*id="program".*?</section>',s,re.S)[0])
    (O/fn).write_text(s)

review_header='''<header class="header"><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="НИИ Нейросетей — на главную"><img src="assets/nii-logo-light.webp" alt="НИИ Нейросетей" width="190" height="34"><span class="brand-divider"></span><span>FIELD<span class="brand-dot">●</span></span></a><a class="review-back" href="index.html#stories">← К программе</a><a class="button button-small" href="index.html#price">Выбрать участие ↗</a></div></header>'''
review_body=f'''<main id="main"><section class="reviews-intro"><div class="wrap"><span class="editorial-label">ЛЮДИ И ИХ РАБОТА</span><h1>Это уже<br>получилось.</h1><p>Истории, отзывы и видео участников программ НИИ Нейросетей. Посмотрите, с какими задачами они пришли и что изменилось в работе.</p><div class="review-totals"><span><b>12</b> кейсов</span><span><b>3</b> отзыва</span><span><b>14</b> видео</span></div></div></section><section class="section reviews-collection"><div class="wrap"><div class="review-filters js-only" aria-label="Формат материалов"><button data-review-filter="all" aria-pressed="true">Вся подборка</button><button data-review-filter="case" aria-pressed="false">Истории и проекты</button><button data-review-filter="quote" aria-pressed="false">Отзывы</button><button data-review-filter="video" aria-pressed="false">Видео</button></div><p class="review-status" aria-live="polite">29 материалов</p><div class="review-grid">{''.join(story_card(x,True,i) for i,x in enumerate(stories))}</div><p class="example-note">Личный опыт участников прошлых программ. Текст кейсов — редакционный пересказ; прямая речь выделена кавычками. Видео открываются на YouTube.</p></div></section><section class="review-join"><div class="wrap"><h2>Теперь — ваша задача.</h2><a class="button" href="index.html#price">Посмотреть программу и участие ↗</a></div></section></main>'''
review_script='''document.documentElement.classList.add('js');const buttons=[...document.querySelectorAll('[data-review-filter]')];buttons.forEach(b=>b.addEventListener('click',()=>{buttons.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));let n=0;document.querySelectorAll('[data-review-type]').forEach(c=>{c.hidden=b.dataset.reviewFilter!=='all'&&c.dataset.reviewType!==b.dataset.reviewFilter;if(!c.hidden)n++});document.querySelector('.review-status').textContent='Материалов: '+n}));'''
(A/'reviews-v3.js').write_text(review_script)
(O/'reviews.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Истории и отзывы участников — НИИ Нейросетей</title><link rel="icon" href="assets/favicon.svg"><link rel="stylesheet" href="assets/style-v3.css"><script src="assets/reviews-v3.js" defer></script></head><body class="reviews-page"><a class="skip" href="#main">Перейти к содержанию</a>'+review_header+review_body+'<footer class="footer"><div class="wrap"><a href="index.html">НИИ Нейросетей · FIELD</a><a href="index.html#price">Условия участия ↗</a></div></footer></body></html>')

app=(A/'app-v2.js').read_text()
demo_js='''  const demoButtons=$$('[data-demo]'), demoPanels=$$('[data-demo-panel]');
  const selectDemo = (key) => {demoButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.demo===key)));demoPanels.forEach(p=>p.hidden=p.dataset.demoPanel!==key);};
  demoButtons.forEach(b=>b.addEventListener('click',()=>{selectDemo(b.dataset.demo);record('task_example_select',{task:b.dataset.demo});}));
  selectDemo('documents');
'''
app=re.sub(r'  const tasks = \{.*?(?=  let month)',lambda _:demo_js,app,flags=re.S)
app=app.replace('field-light-v2','field-editorial-v3').replace('motion-v2.js','motion-v3.js')
(A/'app-v3.js').write_text(app)
motion=(A/'motion-v2.js').read_text()
motion=motion.replace('vec3(.26,.64,.55),vec3(.87,.49,.31)','vec3(.08,.66,.59),vec3(.93,.38,.17)')
motion=motion.replace('if (!gl) return;', "if (!gl) {canvas.hidden=true;canvas.dataset.renderer='fallback';return;}")
motion=motion.replace('if (!paused && !document.hidden && !reduced.matches && !frame)', 'if (gl && !paused && !document.hidden && !reduced.matches && !frame)')
motion=motion.replace("document.querySelectorAll('.section-heading,.track-card,.person,.quote-card,.join-steps li')","document.querySelectorAll('.question-head,.track-poster,.person,.review-card,.join-steps li')")
(A/'motion-v3.js').write_text(motion)
print('v3: 13 company logos, 9 people, 19 event cards, 29 review materials; no price in camp section')
