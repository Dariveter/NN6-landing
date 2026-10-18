'use strict';
(() => {
  document.documentElement.classList.add('js');
  const $ = (q, root = document) => root.querySelector(q);
  const $$ = (q, root = document) => Array.from(root.querySelectorAll(q));
  const alumni = document.body.dataset.audience === 'alumni';
  const prices = alumni ? {EUR: '175 €', RUB: '17 500 ₽'} : {EUR: '350 €', RUB: '35 000 ₽'};
  let currency = 'EUR';
  // Local queue only: no analytics provider, cookies, or network requests.
  const record = (event, detail = {}) => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({event, variant: 'field-recommended-v1', audience: alumni ? 'alumni' : 'new', ...detail});
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
  const tasks = {
    documents: ['Собрать отчёт из нескольких файлов', 'Каждую неделю открываете таблицы, сводите цифры и заново оформляете выводы.', '↳ Таблицы + шаблон отчёта', 'Передаёте материалы и правила', 'ИИ собирает черновик по шаблону', 'Вы проверяете цифры и выводы'],
    content: ['Подготовить серию материалов в своём стиле', 'На каждый пост снова собираете тезисы, ищете референсы и объясняете, как должен выглядеть результат.', '↳ Бриф + примеры вашего стиля', 'Задаёте тему, аудиторию и стиль', 'ИИ готовит тексты и варианты визуала', 'Вы проверяете смысл и редактируете'],
    routine: ['Получать подборку нужных материалов', 'Повторяете один и тот же поиск, открываете источники и вручную выбираете, что пригодится в работе.', '↳ Источники + правила отбора', 'Описываете поручение и расписание', 'ИИ собирает материалы по правилам', 'Вы проверяете источники и отбор']
  };
  const fields = ['#task-title', '#task-problem', '#task-file', '#task-step1', '#task-step2', '#task-step3'];
  $$('[data-task]').forEach(button => button.addEventListener('click', () => {
    $$('[data-task]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    tasks[button.dataset.task].forEach((v, i) => $(fields[i]).textContent = v);
    record('task_example_select', {task: button.dataset.task});
  }));
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
  $$('input[name=currency]').forEach(input => input.addEventListener('change', () => {
    currency = input.value;
    $('#price-value').textContent = prices[currency];
    $('#price-alternative').textContent = 'или ' + prices[currency === 'EUR' ? 'RUB' : 'EUR'];
    $('.dock-price').textContent = prices[currency]; $('.dialog-price').textContent = prices[currency];
    record('currency_select', {currency});
  }));
  const dialog = $('#checkout-dialog');
  let previousFocus;
  $('[data-checkout]').addEventListener('click', evt => {
    if (typeof dialog.showModal !== 'function') return;
    evt.preventDefault(); previousFocus = document.activeElement;
    $('.dialog-price').textContent = prices[currency];
    dialog.showModal(); document.body.style.overflow = 'hidden';
    record('checkout_preview_open', {currency});
  });
  $$('.dialog-close,.dialog-back').forEach(button => button.addEventListener('click', () => dialog.close()));
  dialog.addEventListener('click', evt => {if (evt.target === dialog) dialog.close();});
  dialog.addEventListener('close', () => {document.body.style.overflow = ''; previousFocus?.focus();});
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
  $$('.week,.faq-item').forEach(item => item.addEventListener('toggle', () => {
    if (item.open) record(item.classList.contains('week') ? 'program_expand' : 'faq_expand',
      {item: $('summary', item).textContent.trim().replace(/\s+/g, ' ').slice(0, 90)});
  }));
  const loadArt = () => {
    const script = document.createElement('script'); script.src = 'assets/field-gl.js';
    script.onerror = () => {$('#motion-toggle').hidden = true;}; document.head.append(script);
  };
  if ('requestIdleCallback' in window) requestIdleCallback(loadArt, {timeout: 1400}); else setTimeout(loadArt, 150);
})();
