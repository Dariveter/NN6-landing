/* Specific routes preserve visitor intent instead of opening an unfiltered list. */
(() => {
 const select=document.getElementById('track-filter');
 document.querySelectorAll('[data-calendar-track]').forEach(link=>link.addEventListener('click',()=>{
  if(!select)return;select.value=link.dataset.calendarTrack;select.dispatchEvent(new Event('change'));
 }));
 const rail=document.querySelector('#stories .review-grid');
 if(!rail)return;
 const prev=document.querySelector('[data-story-prev]'),next=document.querySelector('[data-story-next]'),status=document.querySelector('.review-rail-status');
 const cards=Array.from(rail.querySelectorAll('.review-card'));
 function update(){
  const edge=rail.getBoundingClientRect();
  const visible=cards.map((c,i)=>({r:c.getBoundingClientRect(),i:i+1})).filter(x=>x.r.right>edge.left+30&&x.r.left<edge.right-30).map(x=>x.i);
  status.textContent=visible.length?(visible[0]===visible.at(-1)?visible[0]:visible[0]+'–'+visible.at(-1))+' из '+cards.length:'6 историй';
  prev.disabled=rail.scrollLeft<2;next.disabled=rail.scrollLeft>=rail.scrollWidth-rail.clientWidth-2;
 }
 function step(direction){
  const reduced=matchMedia('(prefers-reduced-motion:reduce)').matches||document.body.classList.contains('motion-paused');
  rail.scrollBy({left:direction*(cards[0].getBoundingClientRect().width+parseFloat(getComputedStyle(rail).gap)),behavior:reduced?'instant':'smooth'});
 }
 prev.addEventListener('click',()=>step(-1));next.addEventListener('click',()=>step(1));
 rail.addEventListener('scroll',update,{passive:true});addEventListener('resize',update);update();
})();
