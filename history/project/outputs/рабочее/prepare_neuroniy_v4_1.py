from pathlib import Path
from html.parser import HTMLParser
import json,re

W=Path(__file__).parent
O=W.parent/'готовое'
R=Path('/Users/bigd/Obsidian Vault/Сообщество/Артефакты/FIELD-дизайн-v4/готовое')

class Node:
    def __init__(self,tag='',attrs=()):self.tag=tag;self.attrs=dict(attrs);self.children=[]
    def text(self):
        if 'plus' in self.attrs.get('class','').split():return ''
        return ' '.join(' '.join(x if isinstance(x,str) else x.text() for x in self.children).split())
    def find(self,predicate):
        result=[self] if predicate(self) else []
        for c in self.children:
            if isinstance(c,Node):result+=c.find(predicate)
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

p=Tree();p.feed((O/'index.html').read_text())
faq=[]
for i,n in enumerate(p.root.find(lambda x:'faq-item' in x.attrs.get('class','').split()),1):
    faq.append({'id':f'faq-{i:02d}','question':n.find(lambda x:x.tag=='summary')[0].text(),'answer':' '.join(x.text() for x in n.find(lambda x:x.tag=='p')),'source':'index.html#faq','status':'from_current_landing'})
facts=[
 {'id':'audience','question':'Для кого программа? Можно начать с любого уровня?','answer':'Для руководителей, предпринимателей, специалистов и всех любопытных. Можно прийти с любым уровнем подготовки и своими задачами. Вместе создаём систему навыков.','source':'index.html#top'},
 {'id':'included','question':'Что входит в участие?','answer':'Три направления: основной Кэмп «Начальник нейросетей — 6» — 14 событий, практика — 15 мероприятий, стратегия — 4 мероприятия. Всего 33 события. Также входят записи, материалы, сообщество в Telegram и помощь по инструментам.','source':'index.html#how'},
 {'id':'price-new','question':'350 евро — только за Кэмп? Сколько стоит вся программа?','answer':'350 евро или 35 тысяч рублей — стоимость всей трёхмесячной программы, включая Кэмп, практику, стратегию, записи и сообщество.','source':'index.html#price'},
 {'id':'price-alumni','question':'Какая цена для выпускника?','answer':'Для выпускников предыдущих кэмпов НИИ — 175 евро или 17,5 тысячи рублей за тот же зимний цикл.','source':'alumni.html#price'},
 {'id':'season','question':'Когда начинается программа и сколько длится?','answer':'Зимний цикл FIELD проходит с ноября 2026 по январь 2027. Основной Кэмп начинается 9 ноября, финальная защита — 21 декабря. Каникулы — с 28 декабря по 10 января.','source':'index.html#program'},
 {'id':'timezones','question':'В какое время эфиры в Москве, Израиле и CET?','answer':'19:00 Москва, 18:00 Израиль, 17:00 CET. Это зимнее время для программы ноября 2026 — января 2027.','source':'index.html#rhythm'},
 {'id':'own-task','question':'Можно заниматься со своей задачей?','answer':'Да. Приходите со своей задачей: документы и отчёты, контент и коммуникации, визуальные материалы или повторяющийся рабочий процесс. Задача помогает выбрать подходящие темы и применить подход на практике.','source':'index.html#tasks'},
 {'id':'team','question':'Можно прийти командой?','answer':'Условия участия вашей команды можно обсудить с Юрием. Отдельная цена для команды на странице не указана.','source':'index.html#price'},
 {'id':'join','question':'Как присоединиться?','answer':'Напишите Юрию: уточните условия и подходящую валюту, получите ссылку на оплату. После оплаты команда пришлёт приглашение и инструкции по электронной почте.','source':'index.html#join'}
]
data={
 'schema_version':1,'content_version':'FIELD-winter-v4.1','prepared_at':'2026-10-08',
 'status':'prepared_not_connected','source_status':'current_landing_review_version',
 'valid_for':{'season':'Ноябрь 2026 — январь 2027','starts':'2026-11-09','camp_final':'2026-12-21','break_start':'2026-12-28','break_end':'2027-01-10'},
 'fixed_prices':{'new_member':{'EUR':350,'RUB':35000,'display':'350 евро или 35 тысяч рублей','scope':'Вся трёхмесячная программа FIELD'},'alumni':{'EUR':175,'RUB':17500,'display':'175 евро или 17,5 тысячи рублей','scope':'Тот же зимний цикл для выпускников предыдущих кэмпов НИИ'}},
 'contact':{'name':'Юрий Рапопорт','url':'https://t.me/stonerized','purpose':'Условия участия, оплата, доступ, участие команды'},
 'answers':facts+faq,
 'unknowns_requiring_team':['Точные условия возврата','Рассрочка','Цена для команды','Участие после января 2027','Точная длительность каждого эфира','Индивидуальные договорённости','Актуальная стоимость подписок сторонних ИИ-сервисов'],
 'response_contract':{'answer_length':'2–4 предложения, если вопрос не требует подробностей','sources_required':True,'actions':'Не больше двух подходящих ссылок','when_unknown':'Сказать, каких сведений нет, и предложить уточнить у Юрия','no_automatic_messages':True,'no_private_vault_access':True},
 'note':'Подготовленная база для будущего помощника. Не является подключённым RAG или работающим чатом. При запуске команда проверяет актуальность сведений.'
}
(R/'field-public-knowledge-v4-1.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
assert len(faq)==10,len(faq)
print(json.dumps({'answers':len(data['answers']),'faq':len(faq),'status':data['status']},ensure_ascii=False))

