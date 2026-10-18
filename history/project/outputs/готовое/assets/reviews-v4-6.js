document.documentElement.classList.add('js');
(() => {
 const buttons=Array.from(document.querySelectorAll('[data-review-filter]'));
 const cards=Array.from(document.querySelectorAll('[data-review-type]'));
 function choose(filter){
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.reviewFilter===filter)));
  cards.forEach(card=>{card.hidden=filter!=='all'&&card.dataset.reviewType!==filter;});
  document.querySelector('.review-status').textContent='Материалов: '+cards.filter(x=>!x.hidden).length;
 }
 buttons.forEach(b=>b.addEventListener('click',()=>choose(b.dataset.reviewFilter)));
 function reveal(){
  const card=document.getElementById(location.hash.slice(1));
  if(!card?.matches('[data-review-type]'))return;
  if(card.hidden)choose('all');
  card.scrollIntoView({block:'start',behavior:'instant'});
 }
 addEventListener('hashchange',reveal);addEventListener('load',reveal);choose('all');
})();
