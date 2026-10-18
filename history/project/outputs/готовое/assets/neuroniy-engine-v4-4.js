(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.FieldKnowledge=api;})(typeof window!=='undefined'?window:this,function(){
'use strict';
const clean=s=>String(s||'').toLowerCase().replace(/ё/g,'е').replace(/[^a-zа-я0-9\s]/g,' ').replace(/\s+/g,' ').trim();
const stop=new Set('как что это для или мне меня есть кто все какие будет такое вас можно нужно чем про ваш хочу сколько этого пожалуйста узнать расскажи подробнее там будет будем делать уметь такое этого которой чтобы который научиться помогите подскажи ваш ваши если очень вопрос расскажите'.split(' '));
const tokens=s=>[...new Set(clean(s).split(' ').filter(x=>x.length>2&&!stop.has(x)).map(x=>x.length>5?x.slice(0,-2):x))];
const handoff='Этот ответ пока живёт у Юры, а не в моей нейронной голове 🙂 В материалах сайта его нет, поэтому не буду придумывать. Можно уточнить у Юры в Telegram.';
function links(kb,ids){return [...new Set(ids)].map(id=>kb.answers.find(x=>x.id===id)||kb.documents.find(x=>x.id===id)).filter(Boolean).slice(0,2).map(d=>({label:d.question||d.title,href:d.source||d.href}));}
function guide(question,kb,history=[]){
 const original=clean(question);let q=original;
 const previous=Array.isArray(history)?history.filter(x=>x&&x.role==='user'&&typeof x.content==='string').slice(-1)[0]?.content:'';
 const followup=previous&&/^(а )?(кто ведет|кто будет вести|когда это|а когда|во сколько|что на выходе|какой результат|расскажи подробнее|а подробнее|что будем делать|а как|сколько длится|а что там|кто эксперт)/.test(original);
 if(followup)q=clean(previous+' '+question);
 const answer=(text,sourceLinks=[],human=false,extra={})=>({answer:text,links:sourceLinks,needs_human:human,mode:'guide',...extra});
 const human=(text=handoff,sources=[])=>answer(text,[...sources.slice(0,1),{label:'Уточнить у Юры в Telegram ↗',href:kb.contact.url}],true);
 const rows=ids=>{const a=[...new Set(ids)].map(id=>kb.answers.find(x=>x.id===id)).filter(Boolean).slice(0,2);return answer(a.map(x=>x.answer).join('\n\n'),links(kb,a.map(x=>x.id)));};
 const docResult=(d,lead='')=>answer(lead+(d.guide_text||d.text),[...(d.route?[d.route]:[]),{label:d.title,href:d.href}].slice(0,2),false,{source_ids:[d.id]});
 const docs=kb.documents;
 if(/(?:позови|свяжи|передай|написать|связаться|поговорить|дай контакт).*(?:юр|юри|человек|менеджер)|^(?:юра|юрий|живой человек|человек)$/.test(q))
  return human('Зову человеческий интеллект на помощь 🙂 Кнопка откроет Telegram Юры. Сообщение сможете отправить сами.');
 if(/возврат|вернут.*деньг|вернете/.test(q)&&/оплатил|оплатила|мой|моей|мне|хочу|если/.test(q))
  return human('Условия возврата изложены в оферте для выбранного способа оплаты. Применение к вашей ситуации лучше уточнить у Юры: я не вижу платежей и не принимаю решения о возврате.',links(kb,['legal']));
 if(/где.*оферт|условия возврат|юридическ.*(?:документ|соглашен)|политик.*конфиденц|обработк.*данн|договор с вами|terms|privacy/.test(q))return rows(['legal',/\bvip\b|вип/.test(q)?'vip':/оплат/.test(q)?'payment':null]);
 if(/(?:оплатил|заплатил|оплатила|списал|платеж прошел|письмо не пришло|нет приглашения|не пришл.*приглаш|не получил.*доступ)/.test(q))
  return human(kb.answers.find(x=>x.id==='invitation').answer,links(kb,['invitation']));
 if(/скидк/.test(q)&&/\d/.test(q)&&!/50/.test(q))
  return human('На сайте указана только скидка 50% для выпускников предыдущих кэмпов НИИ. Другие скидки не заявлены; индивидуальные условия может подтвердить Юра.',links(kb,['price-alumni']));
 if(/(?:возврат|вернут.*деньг|рассроч|промокод|ндс|реквизит|счет для|договор с вами|остат.*мест|мест осталось|гаранти.*(?:доход|результат)|вернете)/.test(q))
  return human('Для этого вопроса важны конкретные условия. На сайте нет готового ответа по вашей ситуации. Не буду заменять договор фантазией 🙂 До оплаты посмотрите оферту, а детали уточните у Юры.',links(kb,['section-price']));
 if(/после январ|после зим|феврал|навсегда|пожизнен|вечно/.test(q))
  return human('Записи доступны, пока вы в сообществе; перед выходом их можно скачать. Условия продления после зимнего цикла на сайте не опубликованы, пожизненный доступ не обещается. Это уточнит Юра.',links(kb,['recordings']));
 // Direct dates take priority over generic terms such as "работа" or "память".
 const monthNames={nov:'ноябр',dec:'декабр',jan:'январ'};
 let month=Object.keys(monthNames).find(k=>q.includes(monthNames[k]));
 const date=month&&q.match(new RegExp('(\\d{1,2})\\s*'+monthNames[month]));
 if(date){
  const event=docs.find(d=>d.kind==='event'&&d.month===month&&new RegExp('(?:^|\\s)'+date[1]+'\\s').test(d.date));
  if(event)return docResult(event);
  const week=docs.find(d=>d.kind==='week'&&new RegExp('(?:^|\\s)'+date[1]+'\\s+'+monthNames[month]).test(clean(d.text)));
  if(week)return docResult(week);
  return answer('Отдельное событие на '+date[1]+' '+({nov:'ноября',dec:'декабря',jan:'января'})[month]+' в расписании не нашлось. Посмотрите календарь: в нём можно выбрать месяц и направление.',links(kb,['section-calendar']));
 }
 if(month&&/(расписан|событи|встреч|программ|что будет|что.*пройдет|покажи|план на|что в)/.test(q)){
  const events=docs.filter(d=>d.kind==='event'&&d.month===month);
  return answer('Кроме основного кэмпа, в этом месяце:\n\n'+events.map(d=>'• '+d.date.replace(/^\S+ /,'')+' — '+d.title+'.').join('\n')+'\n\nНачало: 19:00 Москва · 18:00 Израиль · 17:00 CET.',links(kb,['section-calendar']));
 }
 // Named event series and named experts have their own context instead of a generic FAQ answer.
 if(/втор.*памят/.test(q)&&/(когда|даты|ведет|встреч|расписан)/.test(q)){
  const ev=docs.filter(d=>['event-nov-02','event-nov-04'].includes(d.id));
  return answer('«Моя вторая память» — два воркшопа Александра Ярыгина:\n\n'+ev.map(d=>'• '+d.date.replace(/^\S+ /,'')+' — '+d.title+'.').join('\n')+'\n\n19:00 Москва · 18:00 Израиль · 17:00 CET.',links(kb,ev.map(d=>d.id)));
 }
 const named=docs.find(d=>d.kind==='person'&&(clean(d.title).split(' ').some(n=>n.length>4&&q.includes(n.slice(0,-1)))||(/дима|дмитри/.test(q)&&/эйгенсон/.test(clean(d.title)))));
 if(named&&!/стои|тариф/.test(q)){
  const ev=docs.filter(d=>d.kind==='event'&&clean(d.host).includes(clean(named.title).split(' ').pop()));
  let text=named.guide_text;
  if(/ведет|ведут|встреч|тем|заняти|эфир/.test(q)&&ev.length)text+='\n\nСобытия в расписании:\n'+ev.map(d=>'• '+d.date.replace(/^\S+ /,'')+' — '+d.title+'.').join('\n');
  return answer(text,[{label:named.title,href:named.href},...(ev.length?[{label:'События с экспертом',href:ev[0].href}]:[])],false,{source_ids:[named.id]});
 }
 const explicitEvent=docs.filter(d=>d.kind==='event').map(d=>({d,title:clean(d.title)})).find(({title})=>
  (title.length>8&&q.includes(title))||
  (/мир без работ/.test(q)&&/мир без работ/.test(title))||
  (/глуп|разуч.*дум|самостоятельно мысл/.test(q)&&/глуп/.test(title))||
  (/будни юрист|юридич|договор|оферт/.test(q)&&/юрист/.test(title))||
  (/смм|smm|голос бренда|tone of voice/.test(q)&&/smm/.test(title))||
  (/apple|эппл/.test(q)&&/apple/.test(title))||
  (/ии прогноз|прогноз 2027/.test(q)&&/прогноз/.test(title))||
  (/центр.*компетенц/.test(q)&&/центр/.test(title)));
 if(explicitEvent)return docResult(explicitEvent.d);
 if(/кто (?:ведет|преподает|эксперт|преподавател)|какие эксперт|кто в команде|команда field/.test(q)&&!previous){
  const people=docs.filter(d=>d.kind==='person');
  return answer('С вами работают преподаватели и практики:\n\n'+people.map(d=>'• '+d.guide_text.split('\n').slice(0,2).join(' — ')).join('\n'),links(kb,['section-people']));
 }
 let picked=[];
 const pick=id=>{if(!picked.includes(id))picked.push(id);};
 if(/архив|прошл.*(?:эфир|программ)|творческ.*мастерск|библиотек.*запис|старые.*запис/.test(q))pick('archive');
 if(/корпорат|бизнес команд|командой|команду|команды|для сотрудник/.test(q)&&/услов|стои|тариф|цен|участ|обуч|прийти|привести|оплат/.test(q))
  return human(kb.answers.find(x=>x.id==='team').answer,links(kb,['team']));
 if(/\bvip\b|вип|индивидуальн.*участ/.test(q))
  return rows(['vip']);
 if(/выпуск|уже учил|раньше учил|прошел кэмп|скидк/.test(q))pick('price-alumni');
 if(/цен|стои|евро|рубл|тариф|350|35000/.test(q)&&!/инструмент|подписк|сервис|шекел/.test(q))pick(picked.includes('price-alumni')?'price-alumni':'price-new');
 if(/как оплат|оплатить|оплат[аыу]|платеж|картой|allpay|robokass|шекел|валют/.test(q))pick('payment');
 if(/как вступ|как присоед|как записат|как купить|хочу участ|вступление|приглашен|письмо/.test(q))pick('join');
 if(/инструмент|chatgpt|чат ?гпт|подписк|какие сервис|какие нейросет|claude|zoom|telegram|где.*(?:проход|встреч)|очно|онлайн/.test(q)&&!/настро|памят|инструкц|проект/.test(q))pick('tools');
 if(/нович|с нуля|не пробовал|не умею|уров|не пользовал|нет опыт/.test(q))pick('beginner');
 if(/для кого|кому подход|руководител|предпринимател|любопытн/.test(q)&&!/задач|отчет|контент/.test(q))pick('audience');
 if(/совмещ|нагруз|обязательн|успев|работаю|нет времени|не хват.*времен|как проход.*недел|ритм/.test(q))pick('rhythm');
 if(/сколько.*(?:час|времен)|длительн|длится эфир|длится занят|длится встреч|90 минут/.test(q))pick('duration');
 if(/входит|включен|включает|состав участ|что получу|чем.*занимат/.test(q)&&!picked.length)pick('included');
 if(/запис|пропущ|пропуст|скачат/.test(q)&&!picked.includes('archive'))pick('recordings');
 if(/начало|старт|когда начина|когда законч|длится программ|каникул|срок|даты программ/.test(q))pick('dates');
 if(/москв|израил|cet|часов.*нач|во сколько|время эфир|время встреч/.test(q))pick('times');
 if(/поддержк|застря|не получается|кто поможет|техпомощ/.test(q))pick('support');
 if(/ментор/.test(q))pick('mentor');
 if(/стол.*заказ|задач.*участник|профориент/.test(q))pick('orders');
 if(/гост.*будущ|подкаст/.test(q))pick('podcast');
 if(/стратег|теория/.test(q))pick('strategy');
 if(/основной кэмп|что такое кэмп|начальник нейросет|кэмп.*устроен/.test(q))pick('camp');
 if(/что такое практик|сколько практик/.test(q))pick('practice');
 if(/отзыв|истори.*участник|результат.*участник|кейс.*участник/.test(q))pick('stories');
 if(/сертификат|диплом|защита проект/.test(q))pick('certificates');
 if(/какие.*задач|что.*(?:смогу|научусь)|что можно сделать|помоги выбрат|с чего нач|важно знать перед|разобраться в участ/.test(q)&&!picked.length)pick('tasks');
 if(picked.length)return rows(picked);
 if(/^(привет|здравств|добрый|кто ты|что умеешь|спасибо)/.test(q))
  return answer('Я Нейроний, ваш помощник FIELD 🙂 Помогаю разобраться в программе, рабочих задачах, расписании и оплате. С какой задачей вы хотите прийти?',links(kb,['tasks']));
 // Retrieval over public site chunks, with small, explicit Russian task synonyms.
 const taskRules=[
  ['workflow-offers',/коммерческ|предложени.*клиент|\bкп\b|оффер|смет|бюджет.*клиент/],
  ['workflow-knowledge',/баз.*знан|втор.*памят|obsidian|notion|заметк|найти.*документ/],
  ['workflow-reports',/отчет|таблиц|сводк|excel|аналитик|документ|презентаци/],
  ['workflow-content',/контент|посты|постов|постинг|маркетинг|маркетолог|визуал|рассылк|соцсет|бренд/],
  ['workflow-website',/сайт|лендинг|вайбкод|прототип|программиров|кодинг/],
  ['workflow-automation',/автоматиз|повторя|рутин|n8n|связать.*сервис|интеграц|бот|поручен/]
 ];
 const task=taskRules.find(([,re])=>re.test(q));
 if(task)return docResult(docs.find(d=>d.id===task[0]));
 const tt=tokens(q);
 const ranked=docs.filter(d=>['event','week','person','faq','review'].includes(d.kind)).map(d=>{
  const h=tokens(d.title),body=clean(d.text);let score=0,hits=0;
  for(const t of tt){if(h.some(x=>x.startsWith(t)||t.startsWith(x))){score+=5;hits++;}else if(body.includes(t)){score+=.7;hits++;}}
  return {d,score,coverage:tt.length?hits/tt.length:0};
 }).sort((a,b)=>b.score-a.score);
 const top=ranked[0];
 if(top&&top.score>=5&&top.coverage>=.55)return docResult(top.d,'По программе это связано со следующим:\n\n');
 if(tt.length<2||/^(расскажи|подробнее|не знаю|помоги|интересно|как это|о чем)/.test(original))
  return answer('Помогу сузить выбор 🙂 Что сейчас важнее: отчёты и документы, клиенты и предложения, база знаний, контент, сайт или автоматизация? Можно также спросить о стоимости, датах и вступлении.',links(kb,['tasks','included']));
 return human();
}
return {guide,links,clean,tokens,handoff};
});

