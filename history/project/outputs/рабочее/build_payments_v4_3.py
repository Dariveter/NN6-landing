from pathlib import Path
from html import escape
import re,json
W=Path(__file__).parent;O=W.parent/'готовое'
source='https://ne-institute.com/aicamp6'
order='#order:%D0%9A%D1%8D%D0%BC%D0%BF%20%D0%9D%D0%9D6='
payments={
 'participant':{'eur':source+order+'350','rub':'https://pay.ne-institute.com/aicamp6'+order+'35000'},
 'vip':{'eur':source+order+'1000','rub':'https://pay.ne-institute.com/aicamp6'+order+'100000'},
 'alumni':{'eur':'https://allpay.to/~eygenson/0e132bee51','rub':'https://auth.robokassa.ru/merchant/Invoice/zsvU4K-XrU6vDPws1PCE7Q'}
}
legal=[
 ('oferta','Договор публичной оферты','Условия рублёвой оплаты'),
 ('privacy','Обработка персональных данных','Политика конфиденциальности'),
 ('termsandconditions','Terms and Conditions','Условия международной оплаты'),
 ('privacyeng','Privacy Policy','Политика для международной оплаты')
]
doclinks=''.join('<a href="https://ne-institute.com/'+path+'" target="_blank" rel="noopener"><strong>'+title+'<span aria-hidden="true">↗</span></strong><span>'+sub+'</span></a>' for path,title,sub in legal)
documents='<section class="documents-section" id="documents"><div class="wrap"><div class="documents-heading"><h2>Условия и документы</h2><p>Актуальные документы НИИ Нейросетей. Ознакомьтесь с ними перед оплатой.</p></div><div class="documents-grid">'+doclinks+'</div></div></section>'
def choices(p,prefix):
 return '<div class="direct-payments"><a class="button direct-pay-rub" href="'+p['rub']+'" target="_blank" rel="noopener" data-cta="'+prefix+'-rub">Оплатить в рублях <span aria-hidden="true">↗</span></a><a class="button direct-pay-eur" href="'+p['eur']+'" target="_blank" rel="noopener" data-cta="'+prefix+'-eur">Оплатить в евро <span aria-hidden="true">↗</span></a></div>'
def once(s,pattern,repl):
 s,n=re.subn(pattern,lambda m:repl(m) if callable(repl) else repl,s,count=1,flags=re.S)
 assert n,pattern
 return s
for fn in ['index.html','alumni.html','reviews.html']:
 s=(O/fn).read_text()
 s=once(s,r'<footer class="footer"',documents+'<footer class="footer"')
 # All four legal destinations, exactly as on the original landing and its two checkouts.
 if fn!='reviews.html':
  s=once(s,r'(<footer class="footer".*?<a[^>]+href="https://ne-institute.com/privacy"[^>]*>.*?</a>)',lambda m:m[1]+'<a href="https://ne-institute.com/termsandconditions" target="_blank" rel="noopener">Terms and Conditions</a><a href="https://ne-institute.com/privacyeng" target="_blank" rel="noopener">Privacy Policy</a>')
 if fn!='reviews.html':
  alumni=fn=='alumni.html';p=payments['alumni' if alumni else 'participant']
  s=once(s,r'<a class="button price-button".*?</a>',choices(p,'pay-alumni' if alumni else 'pay-participant'))
  note='Откроется платёжная страница со скидкой 50%. Приглашение — на email, указанный при оплате.' if alumni else 'Оплата откроется на сайте НИИ. После оплаты приглашение придёт на вашу почту.'
  s=once(s,r'<p class="ticket-next">.*?</p>','<p class="ticket-next">'+note+'</p>')
  vip='<details class="vip-option" id="vip"><summary><span>VIP · с персональной консультацией</span><span class="plus" aria-hidden="true">+</span></summary><div><p>Всё, что входит в участие, и персональная консультация с Дмитрием Эйгенсоном.</p><p class="vip-price price-pair"><span>1000 евро</span><span class="price-or">или</span><span>100 тысяч рублей</span></p>'+choices(payments['vip'],'pay-vip')+'<p class="small">Оформление и оплата — на сайте НИИ.</p></div></details>'
  s=once(s,r'<a class="vip-link".*?</a>',vip)
  extra=' Для оплаты в евро Allpay показывает эквивалент суммы в шекелях.' if alumni else ''
  s=once(s,r'<p class="billing-note">.*?</p>','<p class="billing-note">Подписки на ИИ-сервисы в составе участия не заявлены.'+extra+'</p><p class="payment-legal-note">Перед оплатой прочитайте <a href="#documents">оферты и политики обработки данных</a>. В корзине проверьте тариф, сумму и количество участников.</p>')
  s=once(s,r'<dialog id="checkout-dialog".*?</dialog>','')
  s=s.replace('<h3>Оплачиваете на сайте</h3>','<h3>Оплачиваете на сайте НИИ</h3>' if not alumni else '<h3>Оплачиваете участие</h3>')
  s=s.replace('Выбираете рубли или евро и оплачиваете участие банковской картой. Указываете свою электронную почту.','Выбираете рубли или евро и переходите к оформлению. Указываете электронную почту для приглашения и оплачиваете участие.')
  s=s.replace('До оплаты ознакомьтесь с офертой. Если условия для вашей ситуации непонятны, обсудите их с Юрием Рапопортом.','Условия опубликованы в <a href="https://ne-institute.com/oferta" target="_blank" rel="noopener">оферте для рублёвой оплаты</a> и <a href="https://ne-institute.com/termsandconditions" target="_blank" rel="noopener">Terms and Conditions для международной оплаты</a>. Если нужна помощь с конкретной ситуацией, обратитесь к Юрию Рапопорту.')
 (O/fn).write_text(s)
app=(O/'assets/app-v4-3.js').read_text()
app,n=re.subn(r"  const dialog = \$\('#checkout-dialog'\);.*?(?=  const dock = )",'',app,flags=re.S)
assert n==1
(O/'assets/app-v4-3.js').write_text(app)
audit={'checked':'2026-10-09','source':source,'payments':payments,'legal':[{'url':'https://ne-institute.com/'+p,'title':t} for p,t,_ in legal],
'verified':['Participant RUB checkout opens with 35000 RUB and contact fields','Participant EUR checkout opens with 350 EUR and contact fields','VIP links and amounts are present on the source landing','All four legal pages load','Alumni Robokassa 17500 RUB and Allpay 175 EUR amounts verified'],
'not_verified':['Payment submission','Order completion','Invitation email delivery'],
'upstream_findings':['Repeated #order opening adds another item to the existing Tilda cart: 2 x 350 EUR observed','English privacy policy references UAE, EU and Russian rules; international offer references Israel. No legal rewrite performed.','Existing Allpay product name is NN-6 Basic. No payment settings changed.']}
(W/'payment-sources-v4-3.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print('Official NII participant and VIP checkout links, alumni links and four legal documents connected.')

