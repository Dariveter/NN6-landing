from pathlib import Path
import re

W=Path(__file__).parent
O=W.parent/'готовое'
base=(O/'assets/style-v2.css').read_text()+'\n'+(O/'assets/style-v3.css').read_text().replace('@import url("style-v2.css");','')
(O/'assets/style-v4.css').write_text(base+'\n'+(W/'v4-overrides.css').read_text())
def section(s,key,markup):
    s,n=re.subn(r'<section\b[^>]*\bid="'+key+r'"[^>]*>.*?</section>',lambda _:markup,s,count=1,flags=re.S)
    assert n==1,key
    return s

def hero(alumni=False):
    title='Зимний<br>интенсив<span class="hero-org">НИИ Нейросетей</span>'
    intro='Три месяца учёбы, практики и стратегии<br class="desktop-break"> в сообществе <strong>FIELD.</strong>'
    foot='Для руководителей, предпринимателей и специалистов. Начать можно с нуля — и со своей рабочей задачи.'
    if alumni: foot='Для выпускников кэмпов НИИ. Возвращайтесь за новыми задачами, практикой и своим следующим шагом.'
    price='175 евро</span><span class="price-or">или</span><span>17,5 тысячи рублей' if alumni else '350 евро</span><span class="price-or">или</span><span>35 тысяч рублей'
    link='<a class="alumni-link" href="index.html">Условия для новых участников ↗</a>' if alumni else '<a class="alumni-link" href="alumni.html">Выпускникам кэмпов НИИ — скидка 50% ↗</a>'
    return f'''<section class="hero hero-winter" id="top">
<canvas id="hero-canvas" aria-hidden="true"></canvas><div class="hero-grain" aria-hidden="true"></div>
<div class="wrap hero-grid"><div class="hero-copy">
<p class="season-date"><span class="status-dot"></span> НОЯБРЬ 2026 — ЯНВАРЬ 2027</p>
<h1>{title}</h1><p class="hero-intro">{intro}</p><p class="hero-audience">{foot}</p>
<div class="hero-actions"><a class="button" href="#price" data-cta="hero">Выбрать участие <span aria-hidden="true">↗</span></a><a class="text-link" href="#how">Что внутри <span aria-hidden="true">↓</span></a></div>
<div class="hero-price"><small>Весь зимний сезон</small><p class="price-pair"><span>{price}</span></p></div>{link}
</div><div class="hero-art"><div class="scene-orbit orbit-one" aria-hidden="true"></div><div class="scene-orbit orbit-two" aria-hidden="true"></div>
<div class="hero-image-wrap"><picture><source media="(max-width: 700px)" srcset="assets/hero-v4-small.webp"><img class="hero-image" src="assets/hero-v4.webp" alt="Мятный маршрут учёбы, коралловый маршрут практики и синий маршрут стратегии соединяются в одном рабочем пространстве" width="1536" height="1024" fetchpriority="high" decoding="async"></picture></div>
<span class="scene-label scene-learn"><i></i> Учёба</span><span class="scene-label scene-work"><i></i> Практика</span><span class="scene-label scene-plan"><i></i> Стратегия</span>
<div class="scene-caption"><span class="scene-cross" aria-hidden="true">+</span><span>Своя задача.<br>Новый способ работать.</span></div>
</div></div>
<div class="wrap season-strip"><div class="season-start"><span>ВСТРЕЧАЕМСЯ ОНЛАЙН</span><strong>9 ноября — старт</strong></div><div><span class="strip-no">01</span><p>Учёба<small>Разобраться и настроить</small></p></div><div><span class="strip-no">02</span><p>Практика<small>Применить в своей работе</small></p></div><div><span class="strip-no">03</span><p>Стратегия<small>Увидеть следующий шаг</small></p></div></div>
</section>'''

def price(alumni=False):
    amount='175 евро</span><span class="price-or">или</span><span>17,5 тысячи рублей' if alumni else '350 евро</span><span class="price-or">или</span><span>35 тысяч рублей'
    note='<strong>Ваша скидка выпускника — 50%</strong><p>Тот же состав участия. Включая кэмп, практику и стратегию.</p><a href="index.html" class="text-link">Условия для новых участников →</a>' if alumni else '<strong>Выпускникам кэмпов НИИ — −50%</strong><p>175 евро или 17,5 тысячи рублей за тот же состав участия.</p><a href="alumni.html" class="text-link">Условия для выпускников →</a>'
    return f'''<section class="section price-section" id="price"><div class="wrap price-grid">
<div class="price-intro"><span class="section-index">08</span><h2>Сколько стоит<br>весь сезон?</h2><p class="section-answer">Один абонемент.<br>Все три направления.</p><p>С ноября 2026 по январь 2027.<br>Первое занятие кэмпа — 9 ноября.</p>
<ul class="included"><li>14 событий кэмпа НН-6</li><li>15 встреч практики и 4 — стратегии</li><li>Записи эфиров и материалы</li><li>Сообщество в Telegram и техпомощь</li><li>ИИ-ментор с первого занятия</li></ul><p class="price-perspective">В своём темпе: основной маршрут — в кэмпе, остальные встречи выбираете под свои задачи.</p></div>
<div class="season-ticket price-card"><div class="ticket-top"><span class="ticket-brand">FIELD<span>●</span></span><span class="ticket-season">ЗИМНИЙ СЕЗОН<br>2026 / 2027</span></div><div class="ticket-title"><h3>Ваш пропуск<br>в практику.</h3><div class="ticket-duration"><b>3</b><span>месяца<br>вместе</span></div></div><div class="ticket-tracks"><span>Кэмп НН-6</span><span>Практика</span><span>Стратегия</span></div>
<div class="ticket-tear" aria-hidden="true"></div><div class="ticket-body"><p class="ticket-price-label">ЗА ВСЮ ПРОГРАММУ</p><div class="main-price"><p class="price-pair"><span>{amount}</span></p></div>
<a class="button price-button" href="https://t.me/stonerized" target="_blank" rel="noopener" data-checkout data-cta="pricing">Обсудить участие <span aria-hidden="true">↗</span></a><p class="ticket-next">Юрий поможет с оплатой и доступом в сообщество.</p><div class="alumni-price">{note}</div><a class="vip-link" href="https://t.me/stonerized" target="_blank" rel="noopener" data-cta="vip">VIP-участие — обсудить с Юрием ↗</a><p class="billing-note">Оплату в шекелях и необходимые подписки на ИИ-сервисы уточните у Юрия до оплаты.</p></div></div>
<div class="access-note"><span aria-hidden="true">↳</span><p><strong>Записи доступны, пока вы в сообществе.</strong> Перед выходом материалы можно скачать. Условия продолжения после зимнего цикла уточняйте у команды.</p></div></div></section>'''

art={
'camp':'<path d="M30 130V46Q73 29 113 52Q157 30 198 46V130Q156 111 113 133Q70 111 30 130Z" fill="#fff9e9"/><path d="M113 53V132M45 62Q75 52 96 63M45 80Q75 70 96 81M45 98Q75 88 96 99M132 64Q160 53 183 64M132 83Q160 72 183 83"/><path d="M14 114Q-3 2 66 18Q108 28 64 58" fill="none" stroke="#267f74" stroke-width="14"/>',
'practice':'<path d="M36 42H130V144H36Z" fill="#ffc2a4" transform="rotate(-12 83 90)"/><path d="M82 22H181V136H82Z" fill="#fff9e9" transform="rotate(7 130 80)"/><path d="M100 51H156M102 66H146M101 114V94H113V114M123 114V80H135V114M145 114V70H157V114"/><path d="m163 115 15 15 27-37" fill="none" stroke="#b93e20" stroke-width="13"/>',
'strategy':'<path d="M25 139V114H57V87H90V61H123V34H157V14H189V139Z" fill="#fff9e9"/><path d="M25 114H57V87H90V61H123V34H157V14" fill="none" stroke="#3567d6" stroke-width="12"/><path d="M52 25C47 55 89 48 105 20M94 18L105 20 101 32" fill="none" stroke="#234997" stroke-width="5"/>'}

for fn in ['index.html','alumni.html']:
    s=(W/('v3-'+fn)).read_text(); alumni=fn=='alumni.html'
    s=s.replace('style-v3.css','style-v4.css').replace('app-v3.js','app-v4.js')
    s=s.replace('<meta name="color-scheme" content="light">','<meta name="color-scheme" content="light"><meta name="theme-color" content="#0b1725">')
    title='Зимний интенсив НИИ Нейросетей · Ноябрь — январь · FIELD'
    if alumni: title='Зимний интенсив FIELD — выпускникам НИИ'
    s=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',s)
    s=s.replace('<canvas id="ambient-canvas" aria-hidden="true"></canvas>','')
    # Only the header uses the white brand asset; footer remains light.
    s=s.replace('src="assets/nii-logo-light.webp"','src="assets/nii-logo-white.webp"',1)
    s=section(s,'top',hero(alumni));s=section(s,'price',price(alumni))
    for kind in ['camp','practice','strategy']:
        pat=r'(<a class="track-poster track-'+kind+r'".*?<div class="poster-visual">)<svg.*?</svg>'
        svg=f'<svg class="route-art" viewBox="0 0 224 166" fill="none" stroke="#0b2432" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{art[kind]}</svg>'
        s,n=re.subn(pat,lambda m:m[1]+svg,s,count=1,flags=re.S);assert n==1,kind
    s=s.replace('<p class="choice-note">','<div class="routes-join" aria-hidden="true"><i></i><i></i><i></i><span>FIELD</span></div><p class="choice-note">')
    s=s.replace('Что будет<br>после оплаты?','Как присоединиться?')
    s=s.replace('Уточняете доступы и условия, выбираете подходящую валюту оплаты.','Пишете Юрию. Уточняете условия, подходящую валюту и получаете ссылку на оплату.')
    s=s.replace('Письмо с доступом придёт на email. При оплате через Allpay его отправляет команда.','После оплаты получаете приглашение в сообщество и инструкции на email.')
    s=s.replace('ЛОКАЛЬНЫЙ ПРОТОТИП','ЗИМНИЙ СЕЗОН FIELD')
    s=s.replace('<strong>Оплата в прототипе не подключена.</strong><p>Здесь будет переход к подтверждённой платёжной форме. Сейчас можно обсудить участие с Юрием.</p>','<strong>Присоединиться через команду.</strong><p>Напишите Юрию: он уточнит условия, пришлёт ссылку на оплату и поможет с доступом.</p>')
    s=s.replace('Участие в зимнем FIELD','Обсудим ваше участие')
    (O/fn).write_text(s)

s=(W/'v3-reviews.html').read_text().replace('style-v3.css','style-v4.css')
s=s.replace('src="assets/nii-logo-light.webp"','src="assets/nii-logo-white.webp"',1)
(O/'reviews.html').write_text(s)
s=(O/'assets/app-v3.js').read_text().replace('field-editorial-v3','field-winter-v4').replace('motion-v3.js','motion-v4.js').replace('checkout_preview_open','join_options_open')
(O/'assets/app-v4.js').write_text(s)
print('v4 pages built; verified program, team and reviews preserved')
