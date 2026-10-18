from pathlib import Path
import re, html, shutil

root = Path(__file__).parent
out = root / 'готовое'
site = Path('/Users/bigd/Obsidian Vault/Сообщество/02 Field (продукт 2.0)/00_brief/HANDOFF — лендинг aicamp6 и A-B варианты — 2026-10-08/outputs/готовое')
assets = out / 'assets'
assets.mkdir(exist_ok=True)
for name in ('trevor.jpg', 'aardvark.jpg', 'mersi.jpg', 'knko.jpg', 'kokoro.jpg'):
    shutil.copy2(site / 'исследование-v4' / name, assets / name)
for name in ('onest.ttf', 'onest-semibold.ttf'):
    shutil.copy2(site / 'assets' / name, assets / name)

text = (out / 'Исследование.md').read_text()

def inline(s):
    s = html.escape(s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)

ids = {}
section_n = 0
parts = []
lines = text.splitlines()
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if line.startswith('# '):
        i += 1
        continue
    if line.startswith('## '):
        if section_n:
            parts.append('</section>')
        section_n += 1
        title = line[3:]
        ids[title] = f's{section_n}'
        parts.append(f'<section id="s{section_n}"><div class="section-label">{section_n:02d} / FIELD</div><h2>{inline(title)}</h2>')
        if title == 'Цветовой сценарий':
            palette = [('#0B1220','Глубина'),('#112B35','Оттенок сцены'),('#F6F3EB','Чтение'),('#7DD4C8','Кэмп'),('#E8734A','Практика'),('#3B82F6','Стратегия'),('#F5C842','Абонемент')]
            parts.append('<div class="swatches">'+''.join(f'<div><i style="background:{color}"></i><b>{label}</b><small>{color}</small></div>' for color,label in palette)+'</div>')
        i += 1
        continue
    if line.startswith('### '):
        parts.append('<h3>'+inline(line[4:])+'</h3>')
        i += 1
        continue
    if line.startswith('!['):
        match = re.fullmatch(r'!\[(.+)\]\((.+)\)', line)
        alt, src = match.groups()
        parts.append(f'<figure><a href="{html.escape(src)}" target="_blank"><img src="{html.escape(src)}" alt="{html.escape(alt)}" width="2560" height="1440" loading="lazy"></a><figcaption>{html.escape(alt)} · Снимок 08.10.2026</figcaption></figure>')
        i += 1
        continue
    if line.startswith('|'):
        rows=[]
        while i < len(lines) and lines[i].strip().startswith('|'):
            row = [x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', cell) for cell in row):
                rows.append(row)
            i += 1
        parts.append('<div class="table-wrap" tabindex="0"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>')
        for row in rows[1:]:
            parts.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>')
        parts.append('</tbody></table></div>')
        continue
    if line.startswith('- ') or re.match(r'^\d+\. ',line):
        ordered = not line.startswith('- ')
        tag = 'ol' if ordered else 'ul'
        parts.append(f'<{tag}>')
        while i < len(lines) and ((ordered and re.match(r'^\d+\. ',lines[i])) or (not ordered and lines[i].startswith('- '))):
            val = re.sub(r'^(?:- |\d+\. )','',lines[i])
            parts.append('<li>'+inline(val)+'</li>')
            i += 1
        parts.append(f'</{tag}>')
        continue
    parts.append('<p>'+inline(line)+'</p>')
    i += 1
if section_n:
    parts.append('</section>')

nav = ''.join(f'<a href="#{ids[title]}">{label}</a>' for title,label in [('Пять визуальных ориентиров','Референсы'),('Новый первый экран','Hero'),('Цена: абонемент на зимний сезон','Стоимость'),('Сценарий движения по странице','Движение'),('Порядок следующей переработки','Следующий этап')])
css = '''
@font-face{font-family:Onest;src:url('assets/onest.ttf') format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:Onest;src:url('assets/onest-semibold.ttf') format('truetype');font-weight:600 900;font-display:swap}
:root{color-scheme:light;--ink:#0b1220;--muted:#586169;--paper:#f6f3eb;--teal:#7dd4c8}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 Onest,system-ui,sans-serif}a{color:#175e66;text-underline-offset:4px}a:hover{color:#a53c19}a:focus-visible{outline:3px solid #e8734a;outline-offset:5px}header{background:linear-gradient(115deg,#0b1220,#112b35);color:#f6f3eb;padding:72px max(24px,calc((100vw - 1120px)/2)) 64px}header .eyebrow{font-size:13px;letter-spacing:.13em;color:#7dd4c8;font-weight:600}header h1{font-size:clamp(40px,6vw,80px);line-height:1.04;letter-spacing:-.06em;max-width:980px;margin:24px 0}header p{font-size:20px;max-width:740px;color:#ccdadd}header .status{display:inline-block;border:1px solid #426066;border-radius:6px;padding:8px 13px;font-size:13px;color:#e5eee9}nav{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:8px 22px;padding:16px max(24px,calc((100vw - 1120px)/2));background:#f6f3ebf5;border-bottom:1px solid #dad9d0;backdrop-filter:blur(10px)}nav a{text-decoration:none;font-weight:600;font-size:14px;white-space:nowrap}main{max-width:1120px;padding:0 24px 64px;margin:auto}main>p{font-size:13px;color:var(--muted);margin:24px 0}section{padding:56px 0;border-bottom:1px solid #d7d9d1}.section-label{font-size:11px;color:#627977;letter-spacing:.15em;font-weight:600}h2{font-size:clamp(28px,3.5vw,42px);line-height:1.15;letter-spacing:-.035em;margin:16px 0 25px}h3{font-size:25px;line-height:1.25;margin:48px 0 12px}p,li{max-width:900px}p{margin:15px 0}li{padding-left:6px;margin:12px 0}li::marker{color:#2a8587;font-weight:600}strong{font-weight:600}figure{margin:24px 0;background:#fff;border:1px solid #d9ddd6;border-radius:10px;overflow:hidden}figure img{display:block;width:100%;height:auto}figcaption{font-size:13px;color:#576568;padding:11px 16px;line-height:1.45}.table-wrap{overflow-x:auto;border:1px solid #cbd3cc;border-radius:9px;margin:25px 0;background:#fff}table{border-collapse:collapse;width:100%;font-size:15px;min-width:680px}th{text-align:left;background:#e3ece7}th,td{padding:16px;border-bottom:1px solid #dfe4df;vertical-align:top}td:first-child{font-weight:600;min-width:140px}tbody tr:last-child td{border:0}.swatches{display:grid;grid-template-columns:repeat(7,1fr);gap:12px;margin:30px 0}.swatches i{display:block;height:86px;border-radius:8px;border:1px solid #ccd3cb}.swatches b{font-size:12px;line-height:1.3;display:block;margin:8px 0 3px}.swatches small{font-size:11px;color:#586169}footer{padding:32px 24px;text-align:center;font-size:13px;background:#0b1220;color:#d8e4e0}footer a{color:#7dd4c8}@media(max-width:600px){body{font-size:16px}header{padding:42px 22px}header p{font-size:18px}main{padding:0 20px 40px}nav{padding:12px 20px;gap:7px 16px}nav a{font-size:12px}section{padding:36px 0}.swatches{grid-template-columns:repeat(4,1fr)}.swatches i{height:62px}h3{font-size:23px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{nav{display:none}header{background:#fff;color:#0b1220;padding:20px}header p,header .status{color:#0b1220}figure{break-inside:avoid}section{padding:20px 0}a{color:inherit}}
'''
doc = '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>FIELD — исследование дизайна v4</title><style>'+css+'</style></head><body><header><div class="eyebrow">FIELD / DESIGN RESEARCH / 08.10.2026</div><h1>Как сделать зимний интенсив заметным и понятным</h1><p>Пять визуальных ориентиров, анализ текущей страницы и конкретное направление для первого экрана, цены и анимации.</p><div class="status">Исследование перед версткой · опубликованный сайт не изменён</div></header><nav aria-label="Разделы исследования">'+nav+'</nav><main>'+''.join(parts)+'</main><footer>Источники и скриншоты проверены 8 октября 2026 · <a href="Исследование.md">Текст исследования</a></footer></body></html>'
(out/'Исследование.html').write_text(doc)
preview = doc
for name in ('trevor.jpg','aardvark.jpg','mersi.jpg','knko.jpg','kokoro.jpg'):
    preview = preview.replace('assets/'+name, 'исследование-v4/'+name)
preview = preview.replace('href="Исследование.md"', 'href="Исследование-v4.md"')
(site/'Исследование-v4.html').write_text(preview)
(site/'Исследование-v4.md').write_text(text.replace('assets/', 'исследование-v4/'))
print(out/'Исследование.html')
print('Sections:', section_n, '| Reference screenshots:', len(list(assets.glob('*.jpg'))))
