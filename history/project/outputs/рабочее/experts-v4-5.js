
/* Expert biographies: native dialog, focus restoration and inline no-JS fallback. */
(() => {
 const dialog=document.getElementById('expert-dialog');
 if(!dialog)return;
 let opener=null;
 const name=dialog.querySelector('#expert-dialog-name');
 const expertise=dialog.querySelector('#expert-dialog-expertise');
 const photo=dialog.querySelector('#expert-dialog-photo');
 const body=dialog.querySelector('#expert-dialog-body');
 function open(card,trigger){
  if(!card||dialog.open)return;
  opener=trigger;
  name.textContent=card.querySelector('h3').textContent.trim();
  expertise.textContent=card.querySelector('.person-expertise').textContent.trim();
  const sourcePhoto=card.querySelector('.person-photo-button img');
  photo.src=sourcePhoto.getAttribute('src');photo.alt=sourcePhoto.alt;photo.dataset.expert=card.dataset.expert;
  body.replaceChildren(...Array.from(card.querySelector('.person-bio').children,el=>el.cloneNode(true)));
  dialog.showModal();
  document.body.classList.add('expert-dialog-open');
 }
 document.querySelectorAll('[data-expert]').forEach(card=>{
  card.querySelectorAll('[data-expert-open]').forEach(trigger=>trigger.addEventListener('click',()=>open(card,trigger)));
  const summary=card.querySelector('.person-details > summary');
  summary.addEventListener('click',event=>{event.preventDefault();open(card,summary);});
 });
 dialog.addEventListener('close',()=>{
  document.body.classList.remove('expert-dialog-open');
  opener?.focus({preventScroll:true});
 });
 dialog.addEventListener('click',event=>{
  const r=dialog.getBoundingClientRect();
  if(event.target===dialog&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))dialog.close();
 });
 const revealExpert=()=>{
  if(!/^#expert-/.test(location.hash))return;
  const card=document.getElementById(location.hash.slice(1));
  if(!card)return;
  card.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});
  open(card,card.querySelector('.person-name-button'));
 };
 addEventListener('hashchange',revealExpert);addEventListener('load',revealExpert);
})();

