from pathlib import Path
import runpy,re
W=Path(__file__).parent;O=W.parent/'готовое'
runpy.run_path(str(W/'build_v4.py'))

def move_after(s,section_id,after_id):
    pattern=lambda key:r'<section\b[^>]*\bid="'+key+r'"[^>]*>.*?</section>'
    m=re.search(pattern(section_id),s,re.S);assert m,section_id
    block=m.group();s=s[:m.start()]+s[m.end():]
    anchor=re.search(pattern(after_id),s,re.S);assert anchor,after_id
    return s[:anchor.end()]+'\n'+block+s[anchor.end():]

def polish(s):
    # Space survives when the responsive stylesheet hides a line break.
    s=re.sub(r'(<br\b[^>]*>)(?!\s)',r'\1 ',s)
    s=re.sub(r'\b(?:НН|NN)[‑–-]?6\b','«Начальник нейросетей — 6»',s)
    s=s.replace('Программа примерная: возможны изменения, но не существенные.','В программе возможны несущественные изменения.')
    s=s.replace('Бренд-бук в ИИ','Брендбук в ИИ')
    s=s.replace('Ведёт: Дмитрий Эйгенсон, Сергей Долгов','Ведут: Дмитрий Эйгенсон, Сергей Долгов')
    s=s.replace('На первом занятии вы получите базовый скилл ИИ-ментора-репетитора. Вопросы по заданиям разбираются на Let\'s Work,','На первом занятии вы получите базовые инструкции для ИИ-ментора. Вопросы по заданиям разбираются на совместных встречах по пятницам,')
    s=s.replace('инструкции на email','инструкции по электронной почте')
    s=s.replace('Приглашение в сообщество придёт на email, указанный при оплате. Для оплаты в рублях предусмотрено автоматическое письмо, через Allpay — письмо от команды.','Приглашение в сообщество придёт на адрес электронной почты, указанный при оплате.')
    return s

wordmark='<div class="camp-wordmark" aria-label="Кэмп «Начальник нейросетей — 6»"><span class="camp-tag">КЭМП</span><b>Начальник<br> нейросетей</b><em>— 6</em></div>'
for fn in ['index.html','alumni.html']:
    s=(O/fn).read_text()
    s=s.replace('assets/style-v4.css','assets/style-v4-1.css')
    if fn=='index.html':
        s=re.sub(r'<p class="hero-audience">.*?</p>','<p class="hero-audience">Для руководителей, предпринимателей, специалистов и всех любопытных. Приходите с любым уровнем подготовки и своими задачами. <strong>Вместе создаём систему навыков.</strong></p>',s,count=1,flags=re.S)
    s=re.sub(r'<div class="camp-wordmark".*?</div>',lambda _:wordmark,s,count=1,flags=re.S)
    s=s.replace('<strong>19:00 Москва</strong><span>18:00 Израиль · 17:00 CET</span>','<span>19:00 Москва</span><span>18:00 Израиль</span><span>17:00 CET</span>')
    for kind in ['camp','practice','strategy']:
        pat=r'(<a class="track-poster track-'+kind+r'".*?<div class="poster-visual">)<svg class="route-art".*?</svg>'
        image=f'<img class="route-art route-photo" src="assets/route-{kind}-v4-1.webp" alt="" width="560" height="560" loading="lazy" decoding="async">'
        s,n=re.subn(pat,lambda m:m[1]+image,s,count=1,flags=re.S);assert n==1,kind
    s=move_after(s,'how','top');s=move_after(s,'tasks','stories')
    for sid,num in [('how','01'),('rhythm','02'),('program','03'),('calendar','04'),('people','05'),('stories','06'),('tasks','07'),('price','08'),('join','09')]:
        pat=r'(<section\b[^>]*id="'+sid+r'".*?<span class="section-index">)\d+'
        s,n=re.subn(pat,lambda m:m[1]+num,s,count=1,flags=re.S);assert n==1,(sid,n)
    s=polish(s)
    (O/fn).write_text(s)

s=polish((O/'reviews.html').read_text().replace('assets/style-v4.css','assets/style-v4-1.css'))
(O/'reviews.html').write_text(s)
(O/'assets/style-v4-1.css').write_text((O/'assets/style-v4.css').read_text()+'\n'+(W/'v4-1-overrides.css').read_text())
print('v4.1: audience, section order, full camp name, generated route objects, whitespace and equal time zones')
