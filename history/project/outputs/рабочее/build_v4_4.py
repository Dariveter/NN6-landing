from pathlib import Path
from html import escape
import re,runpy,json
W=Path(__file__).parent;O=W.parent/'готовое'
runpy.run_path(str(W/'build_v4_3.py'))
logos=json.loads((W/'partner-sources-v4-4.json').read_text())
series=[
 ('memory','Моя вторая память','event-nov-02','event-nov-04','12 ноября','19 ноября'),
 ('website','Вайбкодим сайт','event-dec-06','event-dec-07','1 декабря','8 декабря'),
 ('customer','ИИ и путь клиента','event-jan-15','event-jan-18','19 января','26 января')
]
for fn in ['index.html','alumni.html','reviews.html']:
 s=(O/fn).read_text()
 s=s.replace('style-v4-3.css','style-v4-4.css').replace('app-v4-3.js','app-v4-4.js')
 s=s.replace('neuroniy-v4-3.js','neuroniy-v4-4.js').replace('neuroniy-engine-v4-3.js','neuroniy-engine-v4-4.js')
 if fn!='reviews.html':
  assert 'Что хочется<br> упростить?' in s
  s=s.replace('Что хочется<br> упростить?','Что вам хочется<br> отдать ИИ?')
  s=s.replace('И того, что хочется упростить.','И того, что вам хочется отдать ИИ.')
  s=s.replace('Что получилось у участников?','Что уже получилось<br> у наших участников')
  s=s.replace('<em>— 6</em>','<em><span class="camp-number-dash" aria-hidden="true">—</span><span class="camp-number">6</span></em>')
  old=re.search(r'<div class="company-grid">(.*?)</div></div></section>',s,re.S)
  assert old
  cards=''.join('<a class="company-logo logo-'+x['key']+'" href="'+x['site']+'" target="_blank" rel="noopener" aria-label="'+escape(x['name'],quote=True)+' — сайт компании"><img src="'+x['file']+'" alt="'+escape(x['name'],quote=True)+'" loading="lazy" decoding="async" width="190" height="80"><span>'+escape(x['name'])+'</span></a>' for x in logos)
  controls='<div class="company-browser-controls"><p>Листайте компании <span aria-hidden="true">↔</span></p><button type="button" data-company-prev aria-label="Предыдущие компании" aria-controls="company-grid" disabled>←</button><button type="button" data-company-next aria-label="Следующие компании" aria-controls="company-grid">→</button></div>'
  grid='<div class="company-grid" id="company-grid" role="region" aria-label="Компании и организации, с которыми мы учимся, работаем и сотрудничаем" tabindex="0">'+cards+old[1]+'</div>'+controls+'</div></section>'
  s=s[:old.start()]+grid+s[old.end():]
  s=s.replace('<p>Для C-level и бизнес-команд.</p>','<p>Для C-level и бизнес-команд.<small>Обучение и сотрудничество с компаниями и организациями из разных стран.</small></p>')
  for kind,title,first,second,date1,date2 in series:
   for part,eid,other,otherdate in [(1,first,second,date2),(2,second,first,date1)]:
    m=re.search(r'<details id="'+eid+r'".*?</details>',s,re.S);assert m
    event=m[0].replace('class="event event-practice"','class="event event-practice event-series series-'+kind+'" data-series="'+kind+'" data-series-part="'+str(part)+'"')
    ribbon='<div class="series-ribbon"><span class="series-name"><i class="series-chain" aria-hidden="true"></i>Серия «'+title+'»</span><span class="series-progress" role="img" aria-label="Часть '+str(part)+' из 2"><span class="series-node'+(' is-current' if part==1 else '')+'">01</span><span class="series-line" aria-hidden="true"></span><span class="series-node'+(' is-current' if part==2 else '')+'">02</span></span></div>'
    event=event.replace('<summary>','<summary>'+ribbon,1)
    targetname='Перейти ко второй части' if part==1 else 'Вернуться к первой части'
    jump='<a class="series-jump" href="#'+other+'" data-series-link><span>'+targetname+'<small>'+otherdate+' · '+title+'</small></span><span aria-hidden="true">'+('→' if part==1 else '←')+'</span></a>'
    event=event.replace('</div></details>',jump+'</div></details>')
    s=s[:m.start()]+event+s[m.end():]
  assert s.count('data-series-part=')==6
  assert s.count('class="company-logo ')==19
 (O/fn).write_text(s)
(O/'assets/style-v4-4.css').write_text((O/'assets/style-v4-3.css').read_text()+'\n'+(W/'v4-4-overrides.css').read_text())
(O/'assets/app-v4-4.js').write_text((O/'assets/app-v4-3.js').read_text().replace('field-winter-v4.3','field-winter-v4.4')+'\n'+(W/'partners-v4-4.js').read_text())
runpy.run_path(str(W/'build_neuroniy_knowledge_v4_3.py'))
kb=json.loads((O/'assets/neuroniy-knowledge-v4-3.json').read_text());kb['version']='FIELD-winter-v4.4'
(O/'assets/neuroniy-knowledge-v4-4.json').write_text(json.dumps(kb,ensure_ascii=False,indent=2)+'\n')
for name in ['neuroniy-v4-3.js','neuroniy-engine-v4-3.js']:
 (O/'assets'/name.replace('v4-3','v4-4')).write_text((W/name).read_text().replace('v4-3','v4-4').replace('v4.3','v4.4'))
(O/'api/neuroniy.js').write_text((W/'neuroniy-api-v4-3.js').read_text().replace('v4-3','v4-4').replace('v4.3','v4.4'))
print('v4.4: 6 original partner logos, new headlines, clear numeral 6, 3 linked series.')

