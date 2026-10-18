from pathlib import Path
import json,shutil,hashlib,zipfile,subprocess
W=Path(__file__).parent;O=W.parent/'готовое'
R=Path('/Users/bigd/Obsidian Vault/Сообщество/Артефакты/FIELD-дизайн-v4/готовое')
T=Path('/private/tmp/field-winter-v4-2-release-20261008')
T.mkdir(exist_ok=True)
files=(O/'site-v4-2-files.txt').read_text().splitlines()
assert len(files)==52
for f in files:
    target=T/f;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(O/f,target)
config={'framework':None,'buildCommand':None,'outputDirectory':'.','functions':{'api/neuroniy.js':{'maxDuration':30}}}
(T/'vercel.json').write_text(json.dumps(config,indent=2)+'\n')
(T/'.vercel').mkdir(exist_ok=True)
(T/'.vercel/project.json').write_text(json.dumps({'projectId':'prj_Rfh6OIPqZBvgXh0dMUP37K8QhXUI','orgId':'team_IHwZNgbL9aCooZyjSyvhzYxV','projectName':'nii-field-winter-v3'},indent=2)+'\n')
gitcheck=subprocess.run(['git','rev-parse','--show-toplevel'],cwd=T,capture_output=True,text=True)
assert gitcheck.returncode!=0,'Release directory unexpectedly belongs to a Git repository'
audit={'version':'v4.2','release_directory':str(T),'not_in_git_repository':True,'public_files':[],'access':'Vercel Authentication retained; no public bypass link requested or created'}
for f in files:
    data=(T/f).read_bytes()
    audit['public_files'].append({'path':f,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(W/'vercel-v4-2-upload-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(R/'FIELD-лендинг-v4.2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(T/f,f)
    z.write(T/'vercel.json','vercel.json')
print(json.dumps({'public_files':len(files),'total_public_bytes':sum(x['bytes'] for x in audit['public_files']),'zip':str(R/'FIELD-лендинг-v4.2.zip'),'release':str(T)},ensure_ascii=False))

