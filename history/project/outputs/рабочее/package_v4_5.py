from pathlib import Path
import json,shutil,hashlib,zipfile,subprocess,re
W=Path(__file__).parent;O=W.parent/'готовое'
R=Path('/Users/bigd/Obsidian Vault/Сообщество/Артефакты/FIELD-дизайн-v4/готовое')
T=Path('/private/tmp/field-winter-v4-5-release-20261009')
files=(O/'site-v4-4-files.txt').read_text().splitlines()
mapping={name:name.replace('v4-4','v4-5') for name in files if any(name.startswith('assets/'+prefix) for prefix in ['app-','style-','neuroniy-engine-','neuroniy-knowledge-','neuroniy-v']) and 'v4-4' in name}
files=sorted(mapping.get(f,f) for f in files if f!='program-v8.pdf')
files+= ['assets/yuri.webp','assets/johanna-v4-5.webp']
files=sorted(set(files))
assert len(files)==59
T.mkdir(exist_ok=True);R.mkdir(parents=True,exist_ok=True)
for f in files:
 target=T/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/f,target)
config={'framework':None,'buildCommand':None,'outputDirectory':'.','functions':{'api/neuroniy.js':{'maxDuration':30}}}
(T/'vercel.json').write_text(json.dumps(config,indent=2)+'\n')
(T/'.vercel').mkdir(exist_ok=True)
(T/'.vercel/project.json').write_text(json.dumps({'projectId':'prj_Rfh6OIPqZBvgXh0dMUP37K8QhXUI','orgId':'team_IHwZNgbL9aCooZyjSyvhzYxV','projectName':'nii-field-winter-v3'},indent=2)+'\n')
assert subprocess.run(['git','rev-parse','--show-toplevel'],cwd=T,capture_output=True).returncode!=0
(O/'проверка/v4-5').mkdir(parents=True,exist_ok=True)
checks={}
for fn in ['index.html','alumni.html','reviews.html']:
 s=(O/fn).read_text();ids=re.findall(r'\bid="([^"]+)"',s)
 assert len(ids)==len(set(ids)),(fn,'duplicate ids')
 for src in re.findall(r'(?:src|href)="(assets/[^"#?]+)',s):
  assert src in files,(fn,'missing dependency',src)
 assert 'program-v8.pdf' not in s
 assert 'checkout-dialog' not in s
 for url in ['oferta','privacy','privacyeng','termsandconditions']:
  assert 'https://ne-institute.com/'+url+'"' in s
 if fn!='reviews.html':
  assert len(re.findall('class="event event-',s))==19
  assert len(re.findall('class="person"',s))==10
  assert s.count('data-expert-open')==20
  assert s.count('class="person-bio"')==10
  assert 'CEO NII NeuroCity' in s
  assert 'portrait-initials' not in s
  assert 'Выпускникам кэмпов НИИ — −50%' not in s
  assert len(re.findall('class="workflow-card ',s))==6
  assert s.count('class="company-logo ')==19
  assert s.count('data-series-part=')==6
  assert s.count('data-series-link')==6
  assert 'Что вам хочется<br> отдать ИИ?' in s
  assert 'Что уже получилось<br> у наших участников' in s
  assert 'Что получилось у участников?' not in s
  assert 'И того, что хочется упростить.' not in s
  assert 'до 90' not in s and 'Решения ваших задач' not in s and 'профориентации подростков' not in s
  assert 'Валентин Васин и приглашённые эксперты' in s
  assert 'коммьюнити-менеджер Field' in s
  assert 'компетенции' not in s[s.index('class="team-explainer"'):s.index('class="team-explainer"')+200]
  assert 'Теория' not in s and 'Обсудить участие' not in s
  assert ':::quantity' not in s
  for id in ['event-nov-02','event-nov-04','event-dec-08']:
   assert '<details id="'+id+'"' in s
  assert s.index('id="how"')<s.index('id="workflows"')<s.index('id="stories"')<s.index('id="tasks"')
 checks[fn]={'ids':len(ids),'public_asset_references_valid':True,'documents':4}
for fn in [f for f in files if f.endswith('.js')]:
 p=subprocess.run(['/Users/bigd/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node','--check',str(T/fn)],capture_output=True,text=True)
 assert p.returncode==0,(fn,p.stderr)
audit={'version':'v4.5','release_directory':str(T),'not_in_git_repository':True,'public_files':[],'access':'Public production alias requested by owner; preview authentication unchanged','static_checks':checks}
for f in files:
 data=(T/f).read_bytes();audit['public_files'].append({'path':f,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(O/'site-v4-5-files.txt').write_text('\n'.join(files)+'\n')
(W/'vercel-v4-5-upload-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
(O/'проверка/v4-5/static-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(R/'FIELD-лендинг-v4.5.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(T/f,f)
 z.write(T/'vercel.json','vercel.json')
with zipfile.ZipFile(R/'FIELD-лендинг-v4.5.zip') as z:assert z.testzip() is None
print(json.dumps({'files':len(files),'bytes':sum(x['bytes'] for x in audit['public_files']),'checks':checks,'zip':str(R/'FIELD-лендинг-v4.5.zip'),'release':str(T)},ensure_ascii=False))

