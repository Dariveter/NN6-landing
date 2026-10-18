from pathlib import Path
from html import escape
import re, runpy, json
W=Path(__file__).parent; O=W.parent/'готовое'
runpy.run_path(str(W/'build_v4_2.py'))

def once(s, pattern, replacement):
    s,n=re.subn(pattern,lambda m:replacement(m) if callable(replacement) else replacement,s,count=1,flags=re.S)
    assert n==1,pattern
    return s

events={
'event-nov-01':('Мир без работы',[
'Кто я, если моя работа больше не нужна?',
'Что реально меняется на рынке образования и труда — без паники и без розовых очков.',
'Гости: психолог, HR-специалист и предприниматель нового времени Валентин Васин.'],
'Иоганна Алексанян · Валентин Васин и приглашённые эксперты'),
'event-nov-02':('Моя вторая память. Личная база знаний с ИИ',[
'Собираем заметки, книги и документы в Obsidian или Notion и подключаем ИИ.',
'ИИ находит нужное в этой библиотеке и готовит по ней тексты и планы.',
'На выходе: личная база знаний, доступная для работы нескольким нейросетям и агентам.'],None),
'event-nov-03':('Будни юриста с ИИ',[
'Договоры или оферты по шаблону — проверка на ошибки, противоречия и риски.',
'Что можно отдавать ИИ в юридической работе, а что нет.',
'Практические кейсы применения ИИ в юридической практике.'],None),
'event-nov-04':('Моя вторая память. Применяем базу знаний в работе',[
'Собираем услуги, цены и опыт прошлых проектов. ИИ готовит персонализированное предложение клиенту.',
'Клиент меняет бюджет или сроки — с ИИ пересобираем предложение и план.',
'На выходе: система знаний о моей работе, которая позволяет экономить часы и значительно облегчает аналитику.'],None),
'event-nov-05':('Стол заказов: разбираем ваши задачи',[
'Задачи из «Стола заказов» за октябрь и ноябрь.',
'Эксперт разбирает несколько задач участников в прямом эфире: от постановки до работающего решения.',
'Задачи выбираем заранее по заявкам из «Стола заказов».'],None),
'event-dec-08':('ИИ делает нас глупее?',[
'Что происходит с нашей способностью рассуждать, когда за нас думает ИИ?',
'Чему и как учиться самим и учить детей в мире с ИИ?',
'Где ИИ помогает сформировать своё мнение, а где начинает выбирать за нас?'],None),
'event-dec-10':('Стол заказов: разбираем ваши задачи',[
'Задачи из «Стола заказов» за ноябрь и декабрь.',
'Эксперт разбирает несколько задач участников в прямом эфире: от постановки до работающего решения.',
'Задачи выбираем заранее по заявкам из «Стола заказов».'],None),
'event-dec-11':('ИИ для SMM: реальная практика',[
'Поиск tone of voice бренда и устранение «следов ИИ» в тексте.',
'Создание серии постов и их рассылка — управляем голосом.',
'Визуал без дизайнера.',
'Разбор отзывов и переписок с клиентами, выявление болей и превращение их в контент.'],None),
}
flows=[
('reports','case','Отчёты собираются вручную','Из файлов — в понятную сводку',
'Вы сводите таблицы, документы и заметки, а потом ещё раз проверяете цифры.',
'Соберёте цепочку от исходных материалов до сводки, выводов и презентации. Проверка результата остаётся за вами.',
'Кэмп · неделя 5','week-05','Как в FIELD научиться делать отчёты и работать с таблицами?'),
('offers','masterclass','Каждое предложение — с нуля','КП под задачу и бюджет клиента',
'Услуги, цены и опыт лежат в разных местах. Клиент меняет условия — вы начинаете заново.',
'Соберёте знания о своей работе. На их основе ИИ помогает готовить и пересобирать персональное предложение и план.',
'Вторая память · 19 ноября','event-nov-04','Как готовить коммерческие предложения клиентам с ИИ?'),
('knowledge','memory','Нужное теряется в заметках','База знаний, с которой работает ИИ',
'Материалов много, а найти нужный фрагмент и применить его в работе трудно.',
'Объедините заметки, книги и документы в Obsidian или Notion. Подключите ИИ для поиска, текстов и планов по своим материалам.',
'Вторая память · 12 ноября','event-nov-02','Как сделать личную базу знаний в Obsidian или Notion?'),
('content','podcast','Контент забирает всё время','Тексты и визуалы в голосе бренда',
'Нужно придумывать посты, писать, рисовать и отвечать клиентам — часто всё сразу.',
'Попробуете выпускать серии постов и визуалов, а отзывы и переписки превращать в темы, которые волнуют ваших клиентов.',
'SMM · 17 декабря','event-dec-11','Я занимаюсь маркетингом и контентом. Что мне подойдёт?'),
('website','masterclass','Есть идея, а своего сайта нет','От задачи — к опубликованному сайту',
'Идея остаётся в заметках: неясно, с чего начать и как довести прототип до рабочего варианта.',
'Пройдёте путь от задачи и референсов до публикации. Разберёте формы, сервисы и доработку сайта на примерах участников.',
'Вайбкодинг · 1 и 8 декабря','event-dec-06','Можно ли сделать свой сайт без навыков программирования?'),
('automation','orders','Одни действия повторяются снова','Поручения и связь между сервисами',
'Переносите данные, собираете подборки и запускаете одни и те же действия вручную.',
'В кэмпе запустите первое поручение по расписанию. На практике познакомитесь с n8n и связками таблиц, мессенджеров и почты.',
'Кэмп + n8n · 10 декабря','event-dec-09','Хочу автоматизировать повторяющуюся работу. С чего начать?')
]
workflow='<section class="section workflow-section" id="workflows"><div class="wrap"><div class="workflow-heading"><div><p class="eyebrow">НАЧИНАЕМ С ВАШЕЙ РАБОТЫ</p><h2>Что хочется<br> упростить?</h2></div><p>Выберите знакомую задачу.<br> Посмотрите, что можно собрать с ИИ<br> и где этому учиться в FIELD.</p></div><div class="workflow-grid">'
for i,(id,art,pain,title,before,after,label,target,question) in enumerate(flows):
 workflow+=f'<details class="workflow-card workflow-tone-{i%3}" id="workflow-{id}"><summary><img src="assets/format-{art}-v4-2.webp" alt="" width="140" height="140" loading="lazy" decoding="async"><span class="workflow-pain">{escape(pain)}</span><h3>{escape(title)}</h3><span class="workflow-open">Как это работает<span class="plus" aria-hidden="true">+</span></span></summary><div class="workflow-body"><p><span class="workflow-before">Сейчас</span>{escape(before)}</p><p><span class="workflow-after">С ИИ</span>{escape(after)}</p><a class="workflow-route" href="#{target}">{escape(label)} <span aria-hidden="true">↗</span></a><button class="text-link" type="button" data-ask-neuroniy="{escape(question,quote=True)}">Спросить Нейрония</button></div></details>'
workflow+='</div><p class="workflow-note">Не нужно внедрять всё сразу. Возьмите одну свою задачу, соберите решение и доработайте его вместе с сообществом.</p></div></section>'
archive='''<aside class="archive-pass" id="archive" aria-labelledby="archive-title"><img src="assets/format-memory-v4-2.webp" alt="" width="220" height="220" loading="lazy" decoding="async"><div><p class="eyebrow">ЕЩЁ БОЛЬШЕ ПРАКТИКИ ВНУТРИ</p><h3 id="archive-title">Вступаете в FIELD.<br> Открываете целую библиотеку.</h3><p>С первого дня в сообществе — записи всех прошлых полезных эфиров и программ FIELD и курс «Творческая мастерская».</p><div class="archive-tags"><span>Эфиры сообщества</span><span>Прошлые программы</span><span>«Творческая мастерская»</span></div><small>Входит в участие. Выбирайте материалы под свою задачу и возвращайтесь к ним, пока вы в сообществе.</small></div></aside>'''
expertise={
'Дмитрий Эйгенсон':('Личная эффективность с ИИ, агенты и рабочие процессы','Ведёт основной маршрут «Начальник нейросетей — 6»: от первой задачи и настройки ИИ до поручений, документов и своей рабочей системы.'),
'Денис Домрачев':('Визуальная коммуникация, маркетинг и путь клиента',None),
'Сергей Долгов':('Безопасность ИИ, работа с данными и границы автоматизации',None),
'Иоганна Алексанян':('коммьюнити-менеджер Field','Развивает сообщество, соединяет участников и экспертов. Продюсер и ведущая ежемесячного эфира «Гости из будущего» — о человеке и жизни рядом с ИИ.'),
'Александр Ярыгин':('Базы знаний в Obsidian и Notion, работа с нейросетями и агентами','Ведёт два воркшопа «Моя вторая память». Вместе собираете личную базу знаний и применяете её к предложениям клиентам, планированию и аналитике.'),
'Юлия Кветна':('Вайбкодинг: сайты и решения для рабочих задач',None),
'Андрей Смирнов':('Автоматизация в n8n и интеграции между сервисами',None),
'Валентин Васин':('Предпринимательство, SMM и контент с ИИ','11 ноября участвует в «Гостях из будущего» как предприниматель нового времени. 17 декабря разбирает тексты, рассылки, визуал и обратную связь клиентов.'),
'Сергей Васильев':('Речь, коммуникации и презентации',None)
}
def faq(s,question,text):
 pattern=r'(<details class="faq-item"><summary>'+re.escape(question)+r'<span.*?</summary>)<p>.*?</p>(</details>)'
 return once(s,pattern,lambda m:m[1]+'<p>'+text+'</p>'+m[2])
for fn in ['index.html','alumni.html','reviews.html']:
 s=(O/fn).read_text()
 s=s.replace('assets/style-v4-2.css','assets/style-v4-3.css').replace('assets/app-v4-2.js','assets/app-v4-3.js')
 s=s.replace('assets/neuroniy-v4-2.js','assets/neuroniy-v4-3.js').replace('assets/neuroniy-engine.js','assets/neuroniy-engine-v4-3.js')
 s=s.replace('Организация по защите прав музыкальных исполнителей','Юрист по защите прав музыкальных исполнителей, участница сообщества FIELD')
 s=s.replace('<span>Интересуется автоматизацией</span>','<span>Участник сообщества FIELD</span>')
 s=s.replace('<strong>Иван</strong><span>Участник программ НИИ</span>','<strong>Иван</strong><span>Участник сообщества FIELD</span>')
 s=s.replace('Голубой океан применён к своему продукту / ERRC-сетка готова / Три группы не-клиентов определены','Голубой океан применён к своему продукту: ERRC-сетка готова, три группы неклиентов определены')
 # No third-party chat is required to get an answer already present on the site.
 s=s.replace('<a href="https://t.me/stonerized" target="_blank" rel="noopener">Сразу к Юре ↗</a>','')
 s=s.replace('При включённых ИИ-ответах ваш вопрос и несколько предыдущих реплик передаются сервису модели через Vercel. Не присылайте пароли и конфиденциальные документы. Сайт не сохраняет историю после закрытия страницы.','Справочный режим ищет ответы в публичных материалах этого сайта прямо в вашем браузере. История не сохраняется после перезагрузки. Если команда включит разговорную ИИ-модель, вопрос и несколько реплик будут передаваться ей через Vercel; режим будет указан здесь.')
 s=s.replace('Я Нейроний, ваш помощник FIELD. Помогу разобраться в программе и условиях. Что хотите узнать?','Я Нейроний, ваш помощник FIELD. Знаю программу, расписание, экспертов и условия. Расскажите о своей задаче — помогу найти подходящие темы. Если ответа на сайте нет, подскажу, что уточнить у Юры.')
 s=s.replace('data-neuroniy-question="Как совмещать программу с работой и сколько времени нужно?">Сколько времени нужно?','data-neuroniy-question="Какие рабочие задачи я смогу решать с ИИ?">Что можно сделать?')
 if fn!='reviews.html':
  for eid,(title,topics,host) in events.items():
   def patch_event(m):
    e=once(m[0],r'<h3>.*?</h3>','<h3>'+title+'</h3>')
    e=once(e,r'<ul>.*?</ul>','<ul>'+''.join('<li>'+escape(t)+'</li>' for t in topics)+'</ul>')
    if host:e=once(e,r'<p class="event-host">.*?</p>','<p class="event-host">'+host+'</p>')
    return e
   s=once(s,r'<details id="'+eid+r'".*?</details>',patch_event)
  s=s.replace('Как довести прототип до рабочего, а не бросить на второй неделе','Как довести прототип до рабочего варианта, а не бросить на второй неделе')
  # This separate expert podcast is on 28 January; the 20 January forecast keeps its date/topic.
  s=s.replace('<h3>Центр ИИ-компетенций вашей компании</h3>','<h3>Центры ИИ-компетенций в вашей компании</h3>')
  s=s.replace('<p class="event-format">Подкаст<span>Разговор с экспертом</span></p>','<p class="event-format">«Гости из будущего» · подкаст<span>Разговор с экспертами</span></p>')
  s=once(s,r'<section class="proof-band".*?</section>',workflow)
  s=once(s,r'(<section class="section" id="how">.*?)(</div></section>)',lambda m:m[1]+archive+m[2])
  def person(m):
   card=m[0];name=re.search(r'<h3>(.*?)</h3>',card)[1];ex,role=expertise[name]
   card=once(card,r'<span class="person-role">.*?</span>','')
   card=once(card,r'(<h3>.*?</h3>)<p>.*?</p>',lambda x:x[1]+'<p class="person-expertise">'+ex+'</p>')
   card=card.replace('<summary>Подробнее','<summary>Как поможет в FIELD')
   if role:card=once(card,r'(<details class="person-details">.*?</summary>)<p>.*?</p>',lambda x:x[1]+'<p>'+role+'</p>')
   return card
  s=re.sub(r'<article class="person">.*?</article>',person,s,flags=re.S)
  s=s.replace('<p class="team-explainer">Преподаватели и практики, которые будут вести занятия, разборы и встречи этой зимой.</p>','<p class="team-explainer">Разбираем ваши задачи, делимся опытом и помогаем довести решения до результата.</p>')
  week=[0]
  def week_id(m):week[0]+=1;return '<details id="week-'+str(week[0]).zfill(2)+'" class="week"'
  s=re.sub(r'<details class="week"',week_id,s)
  s=once(s,r'<a class="text-link" href="program-v8.pdf".*?</a>','<a class="text-link" href="#calendar" data-cta="program-calendar">Посмотреть другие события ↓</a>')
  s=s.replace('<li>Записи эфиров и материалы</li>','<li>Записи эфиров и материалы</li><li>Архив программ FIELD и курс «Творческая мастерская»</li>')
  alumni=fn=='alumni.html'; eur='175 евро' if alumni else '350 евро';rub='17,5 тысячи рублей' if alumni else '35 тысяч рублей'
  rub_url='https://auth.robokassa.ru/merchant/Invoice/'+('zsvU4K-XrU6vDPws1PCE7Q' if alumni else 'vGIdNYbfc0OC9iYIDn4ChA')
  eur_url='https://allpay.to/~eygenson/'+('0e132bee51' if alumni else 'e105254657')
  s=once(s,r'<a class="button price-button".*?</a>','<p class="ticket-plan">Участник'+(' · выпускник кэмпа' if alumni else '')+'</p><a class="button price-button" href="'+rub_url+'" target="_blank" rel="noopener" data-checkout data-cta="pricing">Оплатить участие <span aria-hidden="true">↗</span></a>')
  s=once(s,r'<p class="ticket-next">.*?</p>','<p class="ticket-next">Выберите валюту → оплатите картой → получите приглашение на почту.</p>')
  s=once(s,r'<p class="billing-note">.*?</p>','<p class="billing-note">Оплата картой через Robokassa или Allpay. Подписки на ИИ-сервисы в составе участия не заявлены.</p>')
  dialog=f'''<dialog id="checkout-dialog" aria-labelledby="checkout-title"><div class="dialog-inner"><button class="dialog-close" type="button" aria-label="Закрыть окно">×</button><p class="eyebrow">УЧАСТНИК{' · ДЛЯ ВЫПУСКНИКОВ КЭМПА' if alumni else ''}</p><h2 id="checkout-title">Три месяца в FIELD.<br> Выберите валюту.</h2><p class="checkout-included">Кэмп «Начальник нейросетей — 6», практика, стратегия, сообщество, архив программ и «Творческая мастерская».</p><div class="payment-options"><a href="{rub_url}" target="_blank" rel="noopener" class="payment-option payment-rub" data-cta="pay-rub"><span>Оплата в рублях <span aria-hidden="true">↗</span></span><strong>{rub}</strong><small>Банковская карта · Robokassa</small></a><a href="{eur_url}" target="_blank" rel="noopener" class="payment-option payment-eur" data-cta="pay-eur"><span>Оплата в евро <span aria-hidden="true">↗</span></span><strong>{eur}</strong><small>Банковская карта · Allpay</small></a></div><p class="payment-currency-note">Allpay показывает эквивалент суммы в шекелях перед оплатой.</p><div class="payment-next"><span aria-hidden="true">✉</span><p><strong>Приглашение придёт на почту.</strong> Укажите при оплате адрес, которым пользуетесь. На него придут ссылка на сообщество и инструкции.</p></div><p class="checkout-terms">Перед оплатой ознакомьтесь с <a href="https://neuralinstitute.ru/oferta" target="_blank" rel="noopener">офертой</a>. Стоимость — за весь зимний цикл: ноябрь 2026 — январь 2027.</p><button type="button" class="dialog-back">Вернуться к странице</button></div></dialog>'''
  # Preserve the existing legal destination rather than invent a new offer URL.
  offer=re.search(r'<a[^>]+href="([^"]+)"[^>]*>[^<]*[Оо]ферт[^<]*</a>',s)
  assert offer,'offer link missing'
  dialog=dialog.replace('https://neuralinstitute.ru/oferta',offer[1])
  s=once(s,r'<dialog id="checkout-dialog".*?</dialog>',dialog)
  s=s.replace('<h3>Выбираете участие</h3><p>Пишете Юрию. Уточняете условия, подходящую валюту и получаете ссылку на оплату.</p>','<h3>Оплачиваете на сайте</h3><p>Выбираете рубли или евро и оплачиваете участие банковской картой. Указываете свою электронную почту.</p>')
  s=s.replace('<h3>Начинаете со своей задачи</h3><p>9 ноября собираете рабочее место, знакомитесь с ИИ-ментором и выбираете первую задачу.</p>','<h3>Начинаете со своей задачи</h3><p>Сразу после вступления открываете библиотеку записей. 9 ноября начинаете кэмп: собираете рабочее место и выбираете первую задачу.</p>')
  s=once(s,r'<div class="join-contact">.*?</div>','<div class="join-contact"><p>Хотите понять, что подойдёт именно вам? <strong>Спросите Нейрония о своей задаче.</strong></p><button type="button" class="text-link" data-ask-neuroniy="Помоги выбрать, с чего начать в FIELD">Спросить помощника ↗</button></div>')
  for place,label,q in [('faq','Спросить Нейрония ↗','Что важно знать перед вступлением?'),('final','Сначала задать вопрос ↗','Помоги разобраться в участии в FIELD')]:
   s=once(s,r'<a[^>]*data-cta="contact-'+place+r'".*?</a>','<button type="button" class="text-link" data-ask-neuroniy="'+q+'">'+label+'</button>')
  s=faq(s,'Совмещу ли я это с работой?','Заложите два основных эфира в неделю и время, чтобы попробовать задания на своей работе. Эфиры начинаются в 19:00 по Москве, зимой это 18:00 в Израиле и 17:00 CET. Объём самостоятельной работы зависит от вашей задачи. Все дополнительные темы можно выбирать по интересу и смотреть в записи.')
  s=faq(s,'Какие инструменты и подписки понадобятся?','В основе кэмпа — ChatGPT. На отдельных практиках разбираем Obsidian или Notion для базы знаний, n8n для автоматизации и инструменты создания сайтов и визуалов. Встречаемся в Zoom, общаемся в Telegram. Платные подписки на ИИ-сервисы в стоимость участия не заявлены; возможности сервисов зависят от тарифа и региона.')
  s=faq(s,'Кто поможет, если что-то не получается?','На первом занятии вы получите базовые инструкции для ИИ-ментора. По пятницам дорабатываем задачи вместе, в сообществе есть техподдержка по инструментам. На «Столе заказов» эксперт разбирает несколько задач участников — от постановки до работающего решения. Индивидуальная разработка под ключ в этот формат не входит.')
  s=faq(s,'Как уточнить условия возврата?','До оплаты ознакомьтесь с офертой. Если условия для вашей ситуации непонятны, обсудите их с Юрием Рапопортом.')
  newfaq='<details class="faq-item"><summary>Что доступно сразу после вступления?<span class="plus" aria-hidden="true">+</span></summary><p>Записи всех прошлых полезных эфиров и программ сообщества FIELD и курс «Творческая мастерская». Это входит в участие: можно выбрать материал под текущую задачу, не дожидаясь нового эфира. Доступ сохраняется, пока вы в сообществе.</p></details>'
  s=once(s,r'(<details class="faq-item"><summary>Что будет, если я пропущу занятие\?.*?</details>)',lambda m:m[1]+newfaq)
  # A visible explanation also supplies factual context to the assistant.
  s=once(s,r'(<div class="format-guide">.*?</div>)',lambda m:m[1]+'<details class="format-description"><summary>Что такое «Гости из будущего» и «Стол заказов»?<span class="plus" aria-hidden="true">+</span></summary><p><strong>«Гости из будущего»</strong> — ежемесячный эфир Иоганны Алексанян о человеке и жизни рядом с ИИ. Обсуждаем с экспертами и участниками сообщества наши перспективы в новой реальности. В январе также встречаемся с приглашёнными экспертами индустрии на подкасте «Центры ИИ-компетенций в вашей компании».</p><p><strong>«Стол заказов»</strong> — эксперт решает реальные задачи участников в прямом эфире. Выбираем их заранее по заявкам из «Стола заказов».</p></details>')
 (O/fn).write_text(s)
(O/'assets/style-v4-3.css').write_text((O/'assets/style-v4-2.css').read_text()+'\n'+(W/'v4-3-overrides.css').read_text())
app=(O/'assets/app-v4-2.js').read_text().replace('field-winter-v4.2','field-winter-v4.3')
(O/'assets/app-v4-3.js').write_text(app)
for name in ['neuroniy-v4-3.js','neuroniy-engine-v4-3.js']:
 (O/'assets'/name).write_text((W/name).read_text())
(O/'api/neuroniy.js').write_text((W/'neuroniy-api-v4-3.js').read_text())
runpy.run_path(str(W/'build_payments_v4_3.py'))
runpy.run_path(str(W/'build_neuroniy_knowledge_v4_3.py'))
print('v4.3: corrected schedule, task routes, archive, expertise and direct payment.')

