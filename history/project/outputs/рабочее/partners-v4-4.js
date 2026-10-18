
/* Manual partner browsing: no automatic motion; all logos remain readable. */
(() => {
 const rail=document.getElementById('company-grid');
 if(!rail)return;
 const prev=document.querySelector('[data-company-prev]');
 const next=document.querySelector('[data-company-next]');
 if(!prev||!next)return;
 const update=()=>{
  const max=rail.scrollWidth-rail.clientWidth;
  prev.disabled=max<=2||rail.scrollLeft<=2;
  next.disabled=max<=2||rail.scrollLeft>=max-2;
 };
 const step=direction=>{
  const card=rail.querySelector('.company-logo');
  const width=card.getBoundingClientRect().width+parseFloat(getComputedStyle(rail).columnGap||'0');
  const columns=Math.max(1,Math.floor(rail.clientWidth/width));
  const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches||document.documentElement.classList.contains('motion-paused');
  rail.scrollBy({left:direction*columns*width,behavior:reduce?'instant':'smooth'});
 };
 prev.addEventListener('click',()=>step(-1));
 next.addEventListener('click',()=>step(1));
 rail.addEventListener('scroll',update,{passive:true});
 addEventListener('resize',update,{passive:true});
 update();
})();

