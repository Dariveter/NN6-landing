'use strict';
(() => {
 document.documentElement.classList.add('js');
 const pet=document.querySelector('#neuroniy-pet'),dialog=document.querySelector('#neuroniy-dialog');if(!pet||!dialog)return;
 const launch=pet.querySelector('button'),log=dialog.querySelector('.neuroniy-conversation'),form=dialog.querySelector('form'),input=form.querySelector('textarea'),send=form.querySelector('button'),mode=dialog.querySelector('.neuroniy-mode');
 let knowledge,history=[],busy=false,serverMode='guide',previousOverflow='',turn=0;
 const ready=()=>knowledge?Promise.resolve(knowledge):fetch('assets/neuroniy-knowledge-v4-4.json').then(r=>{if(!r.ok)throw Error('knowledge');return r.json();}).then(data=>(knowledge=data));
 const dock=document.querySelector('.mobile-dock');
 const dockPosition=()=>pet.style.setProperty('--pet-bottom',matchMedia('(max-width:620px)').matches&&dock&&!dock.hidden?(Math.ceil(dock.getBoundingClientRect().height)+10)+'px':'16px');
 if(dock)new MutationObserver(dockPosition).observe(dock,{attributes:true,attributeFilter:['hidden']});
 addEventListener('resize',dockPosition);dockPosition();
 const revealHash=()=>{
  const hash=location.hash;if(!/^#(?:event-|week-|workflow-)/.test(hash))return;
  const target=document.getElementById(hash.slice(1));if(!target)return;
  if(hash.startsWith('#week-')||hash.startsWith('#workflow-')){target.open=true;target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth',block:'center'});return;}
  const month=target.dataset.month,button=document.querySelector('[data-month-filter="'+month+'"]'),filter=document.querySelector('#track-filter');
  if(filter){filter.value='all';filter.dispatchEvent(new Event('change'));}
  button?.click();target.open=true;target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth',block:'center'});
 };
 addEventListener('hashchange',revealHash);addEventListener('load',revealHash);
 function close(){dialog.close();}
 launch.addEventListener('click',()=>{
  if(dialog.open)return;previousOverflow=document.body.style.overflow;dialog.showModal();document.body.style.overflow='hidden';launch.setAttribute('aria-expanded','true');pet.classList.add('is-open');ready().catch(()=>{});
  fetch('/api/neuroniy',{headers:{Accept:'application/json'}}).then(r=>r.ok?r.json():null).then(data=>{serverMode=data?.mode==='ai'?'ai':'guide';mode.textContent=serverMode==='ai'?'ИИ-ответы по материалам сайта':'Ответы из программы FIELD';}).catch(()=>{serverMode='guide';});
  if(innerWidth>620)input.focus();else dialog.querySelector('.neuroniy-close').focus();
 });
 dialog.querySelector('.neuroniy-close').addEventListener('click',close);
 dialog.addEventListener('click',e=>{if(e.target===dialog)close();});
 dialog.addEventListener('close',()=>{document.body.style.overflow=previousOverflow;pet.classList.remove('is-open');launch.setAttribute('aria-expanded','false');launch.focus();});
 input.addEventListener('input',()=>{input.style.height='auto';input.style.height=Math.min(input.scrollHeight,112)+'px';});
 input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();form.requestSubmit();}});
 const scroll=()=>{log.scrollTop=log.scrollHeight;};
 function message(text,from='neuroniy',links=[],note=''){
  const el=document.createElement('div');el.className='neuroniy-message from-'+from;const p=document.createElement('p');p.textContent=text;el.append(p);
  if(links.length){
   const row=document.createElement('div');row.className='neuroniy-sources';
   links.slice(0,2).forEach(link=>{
    const href=String(link.href||'');if(!/^(?:index|alumni|reviews)\.html(?:#[\w-]+)?$|^https:\/\/t\.me\/stonerized$/.test(href))return;
    const a=document.createElement('a');a.textContent=link.label||'Посмотреть на сайте';a.href=href;
    if(href.startsWith('https://')){a.className='to-yuri';a.target='_blank';a.rel='noopener';}
    else a.addEventListener('click',()=>{close();if(new URL(a.href).pathname===location.pathname){setTimeout(revealHash,0);}});
    row.append(a);
   });el.append(row);
  }
  if(note){const small=document.createElement('small');small.className='neuroniy-answer-note';small.textContent=note;el.append(small);}
  log.append(el);scroll();return el;
 }
 async function ask(text){
  const question=text.trim();if(!question||busy||question.length>700)return;
  busy=true;send.disabled=true;pet.classList.add('is-thinking');dialog.querySelectorAll('[data-neuroniy-question]').forEach(b=>b.disabled=true);
  message(question,'visitor');input.value='';input.style.height='auto';turn++;
  const pending=message('Сверяюсь с программой…');pending.classList.add('is-loading');pending.setAttribute('role','status');
  try{
   const kb=await ready();let answer;
   if(serverMode==='ai'){
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),23000);
    try{
     const response=await fetch('/api/neuroniy',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,history:history.slice(-6),page:location.pathname.split('/').pop()||'index.html'}),signal:controller.signal});
     if(!response.ok)throw Error('service');answer=await response.json();
    }catch(_){answer=FieldKnowledge.guide(question,kb,history);answer.answer='Мой разговорный модуль сейчас отдыхает. Но я нашёл ответ в программе.\n\n'+answer.answer;answer.mode='guide';}
    finally{clearTimeout(timer);}
   }else answer=FieldKnowledge.guide(question,kb,history);
   pending.remove();message(answer.answer,'neuroniy',answer.links||[],answer.mode==='ai'?'Источник — программа FIELD':'Ответ из справки по программе');
   history.push({role:'user',content:question},{role:'assistant',content:String(answer.answer).slice(0,1800)});history=history.slice(-6);
   if(turn>=2)dialog.querySelector('.neuroniy-suggestions').hidden=true;
  }catch(_){pending.remove();message('Кажется, мои карточки знаний спрятались 🙂 Пока позову Юру — он поможет разобраться.','neuroniy',[{label:'Написать Юре ↗',href:'https://t.me/stonerized'}]);}
  finally{busy=false;send.disabled=false;pet.classList.remove('is-thinking');dialog.querySelectorAll('[data-neuroniy-question]').forEach(b=>b.disabled=false);scroll();}
 }
 form.addEventListener('submit',e=>{e.preventDefault();ask(input.value);});
 dialog.querySelectorAll('[data-neuroniy-question]').forEach(button=>button.addEventListener('click',()=>ask(button.dataset.neuroniyQuestion)));
 document.querySelectorAll('[data-ask-neuroniy]').forEach(button=>button.addEventListener('click',()=>{launch.click();ask(button.dataset.askNeuroniy);}));
 document.querySelectorAll('a[href^="#week-"],a[href^="#event-"]').forEach(link=>link.addEventListener('click',()=>{setTimeout(revealHash,0);}));
})();

