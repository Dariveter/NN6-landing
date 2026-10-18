import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { root, site } from './paths.mjs';

const pages = ['index.html'];
const ids = {};
let checkedLinks = 0;
for (const name of pages) {
  const html = fs.readFileSync(path.join(site, name), 'utf8');
  const values = [...html.matchAll(/\bid="([^"]+)"/g)].map(x => x[1]);
  assert.equal(values.length, new Set(values).size, name + ': duplicate id');
  ids[name] = new Set(values);
}
for (const name of pages) {
  const html = fs.readFileSync(path.join(site, name), 'utf8');
  for (const [,ref] of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
    if (/^(?:https?:|data:|mailto:|tel:|javascript:|\/\/)/i.test(ref)) continue;
    const [filePart, fragment] = ref.split('#');
    const file = decodeURIComponent(filePart.split('?')[0] || name).replace(/^\//, '');
    const dest = path.resolve(site, file);
    assert(dest.startsWith(site + path.sep), name + ': path outside site');
    assert(fs.existsSync(dest), name + ': missing ' + ref);
    if (fragment && ids[file]) assert(ids[file].has(decodeURIComponent(fragment)), name + ': missing anchor ' + ref);
    checkedLinks++;
  }
  for (const tag of html.matchAll(/<img\b[^>]*>/g)) assert(/\balt=/.test(tag[0]), name + ': missing image alt');
}
const walk = dir => fs.readdirSync(dir, {withFileTypes:true}).flatMap(e => {
  const file = path.join(dir,e.name);
  assert(!e.isSymbolicLink(), 'Unexpected symbolic link: ' + file);
  return e.isDirectory() ? walk(file) : [file];
});
for (const file of [...walk(site), path.join(root,'api/neuroniy.js')].filter(p=>p.endsWith('.js'))) {
  const result = spawnSync(process.execPath, ['--check',file], {encoding:'utf8'});
  assert.equal(result.status, 0, result.stderr);
}
const current = fs.readFileSync(path.join(site,'index.html'),'utf8');
assert(current.includes('CEO НИИ Нейросетей'), 'CEO title');
assert(!current.includes('CEO NII NeuroCity'), 'Outdated CEO title');
assert.equal((current.match(/class="person"/g)||[]).length, 10, 'Expert count');
assert.equal((current.match(/class="event event-/g)||[]).length, 22, 'Calendar count');
for (const name of ['index.html']) {
  const page = fs.readFileSync(path.join(site,name),'utf8');
  assert(!page.includes('company-logo') && !page.includes('id="companies"'), name + ': company logos must stay removed');
  assert(!page.includes('Творческая мастерская'), name + ': not part of the КП');
}
const tests = spawnSync(process.execPath, [path.join(root,'tests/neuroniy.cjs')], {
  cwd: root, encoding:'utf8', env:{...process.env, NEURONIY_ENABLED:'false'}
});
process.stdout.write(tests.stdout || '');
assert.equal(tests.status, 0, tests.stderr);
console.log(JSON.stringify({pages:pages.length,checkedReferences:checkedLinks,syntax:'OK',internalLinks:'OK'},null,2));
