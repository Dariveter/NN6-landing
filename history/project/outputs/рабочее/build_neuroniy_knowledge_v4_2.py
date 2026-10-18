from pathlib import Path
from html.parser import HTMLParser
import json,re
W=Path(__file__).parent;O=W.parent/'готовое'
class Node:
 def __init__(self,tag='',attrs=()):self.tag=tag;self.attrs=dict(attrs);self.children=[]
 def has(self,c):return c in self.attrs.get('class','').split()
 def text(self,skip=()):
  if self.tag in ['script','style','svg'] or self.has('plus') or any(self.has(c) for c in skip):return ''
  return ' '.join(' '.join(x if isinstance(x,str) else x.text(skip) for x in self.children).split())
 def find(self,p):
  result=[self] if p(self) else []
  for c in self.children:
   if isinstance(c,Node):result+=c.find(p)
  return result
class Tree(HTMLParser):
 def __init__(self):super().__init__();self.root=Node('root');self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].children.append(d)
def tree(fn):
 p=Tree();p.feed((O/fn).read_text());return p.root
def heading(n):
 h=n.find(lambda x:x.tag in ['h1','h2','h3','summary'])
 return h[0].text() if h else ''
root=tree('index.html');documents=[]
for s in root.find(lambda x:x.tag=='section' and bool(x.attrs.get('id'))):
 sid=s.attrs['id'];documents.append({'id':'section-'+sid,'title':heading(s) or sid,'text':s.text(['event','faq-item','person','review-card']),'href':'index.html#'+sid})
for i,n in enumerate(root.find(lambda x:x.has('event')),1):
 title=n.find(lambda x:x.tag=='h3')[0].text()
 date=n.find(lambda x:x.tag=='time')[0].text()
 host=n.find(lambda x:x.has('event-host'))[0].text()
 timing=n.find(lambda x:x.has('event-time'))[0].text()
 topics=[x.text() if x.text().endswith(('.', '!', '?')) else x.text().rstrip(';')+'.' for x in n.find(lambda x:x.tag=='li')]
 guide=f'«{title}» — {date}.\nУчастник эфира: {host}.\n\n'+'\n'.join('• '+x for x in topics)+f'\n\n{timing}.'
 documents.append({'id':n.attrs['id'],'title':title,'text':n.text(),'guide_text':guide,'href':'index.html#'+n.attrs['id']})
for i,n in enumerate(root.find(lambda x:x.has('person')),1):
 documents.append({'id':f'person-{i}','title':heading(n),'text':n.text(),'href':'index.html#people'})
for i,n in enumerate(root.find(lambda x:x.has('faq-item')),1):
 documents.append({'id':f'faq-{i}','title':heading(n),'text':n.text(),'href':'index.html#faq'})
reviews=tree('reviews.html')
for i,n in enumerate(reviews.find(lambda x:x.has('review-card')),1):
 documents.append({'id':f'review-{i}','title':heading(n),'text':n.text(),'href':'reviews.html'+('#'+n.attrs['id'] if n.attrs.get('id') else '')})
alumni=tree('alumni.html').find(lambda x:x.attrs.get('id')=='price')[0]
documents.append({'id':'alumni-price','title':'Участие выпускников','text':alumni.text(),'href':'alumni.html#price'})
answers=[
 {'id':'price-new','question':'Сколько стоит участие?','answer':'350 евро или 35 тысяч рублей — за всю программу с ноября по январь. В эту сумму входят Кэмп «Начальник нейросетей — 6», практика, стратегия, записи и сообщество.','source':'index.html#price'},
 {'id':'price-alumni','question':'Условия для выпускников','answer':'Если вы выпускник предыдущего кэмпа НИИ, стоимость того же зимнего цикла — 175 евро или 17,5 тысячи рублей. Это скидка 50%.','source':'alumni.html#price'},
 {'id':'tools','question':'Инструменты и подписки','answer':'В основе Кэмпа — ChatGPT; для отдельных задач могут понадобиться другие сервисы. Встречаемся в Zoom и общаемся в Telegram. Включённые платные подписки на ИИ-сервисы на сайте не заявлены: нужные доступы и дополнительные расходы стоит уточнить у Юры до оплаты.','source':'index.html#faq'},
 {'id':'beginner','question':'Можно ли начать с нуля?','answer':'Да, можно прийти с любым уровнем подготовки. Начинаем с рабочего места, настроек и первой собственной задачи. Программировать заранее не нужно: вместе разберём ChatGPT, скиллы, агентов и соберём систему навыков для вашей работы.','source':'index.html#how'},
 {'id':'rhythm','question':'Как совмещать с работой?','answer':'Основной ритм Кэмпа: в понедельник разбираем подход, со вторника по четверг пробуете его на своих задачах, в пятницу дорабатываем вместе. Дополнительные события выбираете по интересу — посещать все 33 не обязательно. Точную длительность эфиров можно уточнить у Юры.','source':'index.html#rhythm'},
 {'id':'included','question':'Что входит в участие?','answer':'Три направления и 33 события: 14 событий Кэмпа «Начальник нейросетей — 6», 15 событий практики и 4 события стратегии. Плюс записи, материалы, сообщество и помощь по инструментам.','source':'index.html#how'},
 {'id':'recordings','question':'Записи и пропущенные эфиры','answer':'Все эфиры можно посмотреть в записи и применить материал в своём темпе. Записи и материалы доступны, пока вы в сообществе. Перед выходом их можно скачать; после выхода доступ закрывается.','source':'index.html#faq'},
 {'id':'dates','question':'Сроки зимней программы','answer':'Зимний цикл — ноябрь 2026 — январь 2027. Кэмп начинается 9 ноября, финальная защита — 21 декабря. С 28 декабря по 10 января — каникулы, с 11 января продолжается программа FIELD.','source':'index.html#program'},
 {'id':'times','question':'Время эфиров','answer':'19:00 Москва · 18:00 Израиль · 17:00 CET. Это зимнее время эфиров программы ноября 2026 — января 2027.','source':'index.html#rhythm'},
 {'id':'team','question':'Участие бизнес-команды','answer':'С НИИ учатся и работают C-level и бизнес-команды. Условия для вашей команды обсудите с Юрой: готового корпоративного тарифа на странице нет.','source':'index.html#companies'},
 {'id':'join','question':'Как присоединиться?','answer':'Напишите Юре: он поможет с условиями, валютой и ссылкой на оплату. После оплаты получите приглашение в сообщество и инструкции по электронной почте.','source':'index.html#join'}
]
kb={'version':'FIELD-winter-v4.2','updated':'2026-10-08','scope':'Только публичное содержимое текущих страниц index.html, alumni.html, reviews.html. PDF не индексирован.','season':'Ноябрь 2026 — январь 2027','contact':{'name':'Юрий Рапопорт','url':'https://t.me/stonerized'},'answers':answers,'documents':documents}
assert len(documents)>=70,len(documents)
assert all('мероприяти' not in x['text'].lower() for x in documents)
assert len({x['id'] for x in documents})==len(documents)
(O/'assets/neuroniy-knowledge-v4-2.json').write_text(json.dumps(kb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'documents':len(documents),'prepared_answers':len(answers),'characters':sum(len(x['text']) for x in documents)},ensure_ascii=False))
