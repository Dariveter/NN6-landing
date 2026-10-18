from pathlib import Path
from html import escape
import re,runpy,json
W=Path(__file__).parent;O=W.parent/'готовое'
runpy.run_path(str(W/'build_v4_4.py'))
source=(W/'experts-source-v4-5.md').read_text()
bios={name.replace('Раппопорт','Рапопорт'):body.strip().replace('превратить ее','превратить её') for name,body in re.findall(r'^## \[([^\]]+)\].*?\n\n(.*?)(?=\n## |\Z)',source,re.S|re.M)}
assert len(bios)==10
keys={'Дмитрий Эйгенсон':'dmitry','Юрий Рапопорт':'yuri','Денис Домрачев':'denis','Сергей Долгов':'sergey','Иоганна Алексанян':'johanna','Александр Ярыгин':'alexander','Юлия Кветна':'yulia','Андрей Смирнов':'andrey','Валентин Васин':'valentin','Сергей Васильев':'vasilyev'}
people={}
dialog='''<dialog id="expert-dialog" class="expert-dialog" aria-labelledby="expert-dialog-name"><form method="dialog" class="expert-dialog-closebar"><button type="submit" aria-label="Закрыть описание эксперта" autofocus>×</button></form><div class="expert-dialog-content"><div class="expert-dialog-header"><img id="expert-dialog-photo" alt="" width="160" height="180"><div><p class="eyebrow">КОМАНДА И ЭКСПЕРТЫ FIELD</p><h2 id="expert-dialog-name"></h2><p id="expert-dialog-expertise"></p></div></div><div id="expert-dialog-body"></div></div></dialog>'''
for fn in ['index.html','alumni.html','reviews.html']:
 s=(O/fn).read_text()
 s=s.replace('style-v4-4.css','style-v4-5.css').replace('app-v4-4.js','app-v4-5.js')
 s=s.replace('neuroniy-v4-4.js','neuroniy-v4-5.js').replace('neuroniy-engine-v4-4.js','neuroniy-engine-v4-5.js')
 s=s.replace('Выпускникам кэмпов НИИ — −50%','Выпускникам кэмпов НИИ: скидка 50%')
 if fn!='reviews.html':
  cards=re.findall(r'<article class="person">.*?</article>',s,re.S);assert len(cards)==9
  yuri='<article class="person"><img src="assets/yuri.webp" alt="Юрий Рапопорт" width="400" height="460" loading="lazy" decoding="async"><div class="person-copy"><h3>Юрий Рапопорт</h3><p class="person-expertise">CEO NII NeuroCity</p><details class="person-details"><summary>Как поможет в FIELD<span class="plus" aria-hidden="true">+</span></summary><p>В НИИ Нейросетей специализируется на работе с данными.</p></details></div></article>'
  s=s.replace(cards[0],cards[0]+yuri,1)
  def card(m):
   c=m[0];name=re.search(r'<h3>(.*?)</h3>',c)[1];key=keys[name]
   expertise=re.search(r'<p class="person-expertise">(.*?)</p>',c)[1]
   role=re.search(r'<details class="person-details">.*?</summary><p>(.*?)</p>',c,re.S)[1]
   if key=='johanna':
    c=re.sub(r'<div class="portrait-initials".*?</div>','<img src="assets/johanna-v4-5.webp" alt="Иоганна Алексанян" width="400" height="460" loading="lazy" decoding="async">',c,flags=re.S)
   img=re.search(r'<img .*?>',c)[0]
   c=c.replace('<article class="person">','<article class="person" id="expert-'+key+'" data-expert="'+key+'">',1)
   label=escape('Об эксперте: '+name,quote=True)
   c=c.replace(img,'<button type="button" class="person-photo-button" data-expert-open aria-haspopup="dialog" aria-controls="expert-dialog" aria-label="'+label+'">'+img+'<span class="person-photo-hint">Об эксперте <span aria-hidden="true">↗</span></span></button>',1)
   c=c.replace('<h3>'+name+'</h3>','<h3><button type="button" class="person-name-button" data-expert-open aria-haspopup="dialog" aria-controls="expert-dialog">'+name+'</button></h3>')
   bio=escape(bios[name])
   body='<div class="person-bio"><p>'+bio+'</p><h4>В FIELD</h4><p>'+role+'</p></div>'
   c=re.sub(r'<details class="person-details">.*?</details>','<details class="person-details"><summary aria-haspopup="dialog">Об эксперте<span class="plus" aria-hidden="true">+</span></summary>'+body+'</details>',c,flags=re.S)
   people[name]={'key':key,'expertise':expertise,'bio':bios[name],'role':role}
   return c
  s=re.sub(r'<article class="person">.*?</article>',card,s,flags=re.S)
  s=s.replace('<p class="team-explainer">Разбираем ваши задачи, делимся опытом и помогаем довести решения до результата.</p>','<p class="team-explainer">Разбираем ваши задачи, делимся опытом и помогаем довести решения до результата.</p><p class="team-card-hint">Нажмите на имя или фотографию, чтобы познакомиться с экспертом.</p>')
  s=s.replace('</body>',dialog+'</body>')
  assert len(re.findall('data-expert="',s))==10
 (O/fn).write_text(s)
(O/'assets/style-v4-5.css').write_text((O/'assets/style-v4-4.css').read_text()+'\n'+(W/'v4-5-overrides.css').read_text())
(O/'assets/app-v4-5.js').write_text((O/'assets/app-v4-4.js').read_text().replace('field-winter-v4.4','field-winter-v4.5')+'\n'+(W/'experts-v4-5.js').read_text())
runpy.run_path(str(W/'build_neuroniy_knowledge_v4_3.py'))
kb=json.loads((O/'assets/neuroniy-knowledge-v4-3.json').read_text());kb['version']='FIELD-winter-v4.5'
for d in kb['documents']:
 if d['kind']=='person':
  p=people[d['title']]
  d['guide_text']=d['title']+'\n'+p['expertise']+'.\n\n'+p['bio']+'\n\nВ FIELD: '+p['role']
  d['href']='index.html#expert-'+p['key']
assert len([x for x in kb['documents'] if x['kind']=='person'])==10
(O/'assets/neuroniy-knowledge-v4-5.json').write_text(json.dumps(kb,ensure_ascii=False,indent=2)+'\n')
for name in ['neuroniy-v4-4.js','neuroniy-engine-v4-4.js']:
 (O/'assets'/name.replace('v4-4','v4-5')).write_text((O/'assets'/name).read_text().replace('v4-4','v4-5').replace('v4.4','v4.5'))
(O/'api/neuroniy.js').write_text((O/'api/neuroniy.js').read_text().replace('v4-4','v4-5').replace('v4.4','v4.5'))
(W/'experts-content-v4-5.json').write_text(json.dumps(people,ensure_ascii=False,indent=2)+'\n')
print('v4.5: 10 clickable expert biographies, Yuri CEO NII NeuroCity, Johanna portrait, clear alumni discount.')

