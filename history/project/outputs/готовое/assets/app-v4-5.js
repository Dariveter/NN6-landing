'use strict';
(() => {
  document.documentElement.classList.add('js');
  const $ = (q, root = document) => root.querySelector(q);
  const $$ = (q, root = document) => Array.from(root.querySelectorAll(q));
  const alumni = document.body.dataset.audience === 'alumni';
  const prices = alumni ? {EUR: '175 €', RUB: '17 500 ₽'} : {EUR: '350 €', RUB: '35 000 ₽'};
  let currency = 'unselected';
  // Local queue only: no analytics provider, cookies, or network requests.
  const record = (event, detail = {}) => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({event, variant: 'field-winter-v4.5', audience: alumni ? 'alumni' : 'new', ...detail});
  };
  $$('[data-cta]').forEach(a => a.addEventListener('click', () => record('cta_click', {placement: a.dataset.cta, currency})));
  const menuButton = $('.menu-button'), menu = $('#mobile-nav');
  const closeMenu = () => {
    menu.hidden = true; menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Открыть меню');
  };
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menu.hidden = !open;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
  });
  $$('a', menu).forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', evt => {if (evt.key === 'Escape' && !menu.hidden) {closeMenu(); menuButton.focus();}});
  matchMedia('(min-width: 861px)').addEventListener('change', evt => {if (evt.matches) closeMenu();});
  const demoButtons=$$('[data-demo]'), demoPanels=$$('[data-demo-panel]');
  const selectDemo = (key) => {demoButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.demo===key)));demoPanels.forEach(p=>p.hidden=p.dataset.demoPanel!==key);};
  demoButtons.forEach(b=>b.addEventListener('click',()=>{selectDemo(b.dataset.demo);record('task_example_select',{task:b.dataset.demo});}));
  selectDemo('documents');
  let month = 'nov';
  const updateCalendar = () => {
    const track = $('#track-filter').value;
    let count = 0;
    $$('.event').forEach(event => {
      event.hidden = event.dataset.month !== month || (track !== 'all' && event.dataset.track !== track);
      if (!event.hidden) count++;
    });
    $('#calendar-status').textContent = 'Показано событий: ' + count;
  };
  $$('[data-month-filter]').forEach(button => button.addEventListener('click', () => {
    month = button.dataset.monthFilter;
    $$('[data-month-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    updateCalendar(); record('calendar_month_select', {month});
  }));
  $('#track-filter').addEventListener('change', updateCalendar);
  updateCalendar();
  const dock = $('.mobile-dock');
  if ('IntersectionObserver' in window) {
    const states = {hero: true, price: false, footer: false};
    const observed = new Map([[$('.hero'), 'hero'],[$('.price-card'), 'price'],[$('.footer'), 'footer']]);
    const dockObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {states[observed.get(entry.target)] = entry.isIntersecting;});
      dock.hidden = states.hero || states.price || states.footer;
    }, {threshold: 0});
    observed.forEach((_key, element) => dockObserver.observe(element));
    const seen = new Set();
    const sectionObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting && !seen.has(entry.target.id)) {
        seen.add(entry.target.id); record('section_view', {section: entry.target.id});
      }
    }), {threshold: .15});
    $$('#tasks,#how,#program,#price,#join').forEach(s => sectionObserver.observe(s));
  }
  $$('.week,.faq-item,.event,.person-details,.mentor-details').forEach(item => item.addEventListener('toggle', () => {
    if (item.open) record(item.classList.contains('week') ? 'program_expand' : 'faq_expand',
      {item: $('summary', item).textContent.trim().replace(/\s+/g, ' ').slice(0, 90)});
  }));
  const loadArt = () => {
    const script = document.createElement('script'); script.src = 'assets/motion-v4.js';
    script.onerror = () => {$('#motion-toggle').hidden = true;}; document.head.append(script);
  };
  if ('requestIdleCallback' in window) requestIdleCallback(loadArt, {timeout: 1400}); else setTimeout(loadArt, 150);
})();


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

