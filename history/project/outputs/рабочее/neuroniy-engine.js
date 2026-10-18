(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.FieldKnowledge=api;})(typeof window!=='undefined'?window:this,function(){
'use strict';
const clean=s=>String(s||'').toLowerCase().replace(/ё/g,'е').replace(/[^a-zа-я0-9\s]/g,' ').replace(/\s+/g,' ').trim();
const tokens=s=>clean(s).split(' ').filter(x=>x.length>2&&!['как','что','это','для','или','мне','меня','есть','кто','все','какие','будет','такое','вас','можно','нужно','чем','про','ваш','хочу','сколько','этого','пожалуйста'].includes(x)).map(x=>x.length>5?x.slice(0,-2):x);
const handoff='Кажется, этот ответ пока живёт у Юры, а не в моей нейронной голове 🙂 Не буду фантазировать — у него можно уточнить детали в Telegram.';
function links(kb,ids){return [...new Set(ids)].map(id=>kb.documents.find(x=>x.id===id)||kb.answers.find(x=>x.id===id)).filter(Boolean).slice(0,2).map(d=>({label:d.title||d.question,href:d.href||d.source}));}
function guide(question,kb,history=[]){
 const q=clean(question);let rows=[];
 const select=id=>{const x=kb.answers.find(x=>x.id===id);if(x&&!rows.includes(x))rows.push(x);};
 const unknown=/рассроч|возврат|вернут|гарантир|промокод|скидк.*(?:90|100)|бесплатн.*подписк|после январ|феврал|ндс|инн|реквизит|договор|мест осталось|заплатил|оплатил|где приглашен/.test(q);
 if(unknown)return {answer:handoff,links:[{label:'Написать Юре в Telegram ↗',href:kb.contact.url}],needs_human:true,mode:'guide'};
 if(/цен|стои|евро|рубл|тариф|платить|350|35000/.test(q)&&!/инструмент|подписк|сервис/.test(q))select(/выпуск|уже учил|повторно|раньше учил/.test(q)?'price-alumni':'price-new');
 if(/инструмент|chatgpt|чат ?гпт|подписк|сервис|claude|доступы/.test(q))select('tools');
 if(/нович|с нуля|не пробовал|не умею|уров|не пользовал/.test(q))select('beginner');
 if(/врем|совмещ|часов|нагруз|обязательн|успев/.test(q))select('rhythm');
 if(/входит|включен|состав|чем.*занимат/.test(q)&&!/подписк|инструмент|сервис/.test(q))select('included');
 if(/выпуск|уже учил|повторно|раньше учил/.test(q))select('price-alumni');
 if(/запис|пропущ|пропуст|скачат/.test(q))select('recordings');
 if(/начина|начало|старт|длится|заканч|каникул|даты/.test(q))select('dates');
 if(/москв|израил|cet|часов.*нач|во сколько/.test(q)){rows=rows.filter(x=>x.id!=='rhythm');select('times');}
 if(/команд|c level|сотрудник/.test(q)&&/цен|услов|привести|прийти|групп|обуч|корпорат/.test(q))select('team');
 if(/юра|юри|человек|менеджер|связат|телеграм/.test(q)&&!/инструмент|сервис/.test(q))return {answer:'Зову человеческий интеллект на помощь 🙂 Юра подскажет по участию, оплате и доступу. Нажмите кнопку — откроется его Telegram.',links:[{label:'Написать Юре ↗',href:kb.contact.url}],needs_human:true,mode:'guide'};
 if(/как вступ|как присоед|как запис|как купить|хочу участ/.test(q))select('join');
 if(rows.length)return {answer:rows.slice(0,2).map(x=>x.answer).join('\n\n'),links:links(kb,rows.slice(0,2).map(x=>x.id)),needs_human:false,mode:'guide'};
 const tt=tokens(q);
 const ranked=kb.documents.map(d=>{const h=tokens(d.title),body=clean(d.text);let score=0;for(const t of tt){if(h.some(x=>x.startsWith(t)||t.startsWith(x)))score+=5;else if(body.includes(t))score+=1;}return {d,score};}).sort((a,b)=>b.score-a.score);
 const top=ranked[0];
 if(top&&top.score>=Math.max(5,tt.length*1.1)){
  const source=top.d.guide_text||top.d.text;
  const text=source.length>900?source.slice(0,900).replace(/\s+\S*$/,'')+'…':source;
  return {answer:'Нашёл подходящий раздел программы:\n\n'+text,links:links(kb,[top.d.id]),needs_human:false,mode:'guide'};
 }
 if(/^(привет|здравствуйте|добрый день|кто ты|что умеешь)/.test(q))return {answer:'Я Нейроний, ваш помощник FIELD 🙂 Разбираюсь в программе, стоимости, инструментах и расписании. С какой задачей вы хотите прийти?',links:[],needs_human:false,mode:'guide'};
 return {answer:handoff,links:[{label:'Написать Юре в Telegram ↗',href:kb.contact.url}],needs_human:true,mode:'guide'};
}
return {guide,links,clean,tokens,handoff};
});
