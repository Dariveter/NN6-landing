import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { root, site } from './paths.mjs';

const flag=process.argv.indexOf('--base-url');
const origin=new URL(flag>=0?process.argv[flag+1]:'https://dariveter.github.io/NN6-landing/');
assert(origin.protocol==='https:','Use an HTTPS publication URL for images and fonts');
assert(!origin.username&&!origin.password&&!origin.search&&!origin.hash,'Do not put credentials, query strings or fragments in the base URL');
if(!origin.pathname.endsWith('/'))origin.pathname+='/';
const abs=(value,base=origin)=>{
  if(/^(?:data:|https?:|\/\/|#|mailto:|tel:)/i.test(value))return value;
  return new URL(value,base).href;
};
const target=path.join(root,'tilda');
fs.mkdirSync(path.join(target,'zero-block'),{recursive:true});
fs.mkdirSync(path.join(target,'t123'),{recursive:true});
const pages=['index.html'];
const manifest={generatedFrom:'FIELD v4.6',assetsBase:origin.href,pages:[],note:'Zero Block exports are visual HTML/CSS references; JavaScript interactions are not imported.'};
for(const name of pages){
  let html=fs.readFileSync(path.join(site,name),'utf8');
  html=html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'');
  html=html.replace(/<link\b([^>]*?)rel="stylesheet"([^>]*?)>/gi,(tag)=>{
    const href=tag.match(/href="([^"]+)"/)?.[1];
    assert(href&&href.startsWith('assets/'),'Unexpected stylesheet reference');
    let css=fs.readFileSync(path.join(site,href),'utf8');
    const cssBase=new URL(href,origin);
    css=css.replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g,(_,q,value)=>'url("'+abs(value.trim(),cssBase)+'")');
    return '<style>\n'+css+'\n</style>';
  });
  html=html.replace(/\b(src|href)="([^"]+)"/g,(_,key,value)=>key+'="'+abs(value)+'"');
  html=html.replace(/\bsrcset="([^"]+)"/g,(_,value)=>'srcset="'+value.split(',').map(entry=>{const [url,...descriptor]=entry.trim().split(/\s+/);return [abs(url),...descriptor].join(' ');}).join(', ')+'"');
  html=html.replace(/<html\b[^>]*>/i,'<html lang="ru">');
  html=html.replace('</head>','<style>html{scroll-behavior:auto!important}body{overflow:visible!important}.reveal{opacity:1!important;transform:none!important}</style></head>');
  assert(!/<script\b/i.test(html),'Zero Block export must not contain JavaScript');
  assert(!/(?:src|href)="assets\//.test(html),'Local asset reference in Tilda export');
  const out=name.replace('.html','-inline-css.html');
  fs.writeFileSync(path.join(target,'zero-block',out),html);
  const heading=html.match(/<title>([\s\S]*?)<\/title>/i)?.[1]||'FIELD';
  const embed='<!-- Paste into one T123 block on a dedicated page. Remove default Tilda header/footer for this page. -->\n'+
    '<iframe src="'+new URL(name,origin).href+'" title="'+heading.replaceAll('"','&quot;')+'" style="display:block;width:100%;height:100vh;height:100dvh;border:0" loading="eager" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>\n';
  fs.writeFileSync(path.join(target,'t123',name),embed);
  manifest.pages.push({source:'site/'+name,zeroBlock:'tilda/zero-block/'+out,t123:'tilda/t123/'+name});
}
fs.writeFileSync(path.join(target,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log('Tilda files prepared in tilda/zero-block/ and tilda/t123/.');
console.log('A private GitHub repository does not host public images. Asset base: '+origin.href);
