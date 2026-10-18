import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { site } from './paths.mjs';

const arg = process.argv.indexOf('--port');
const port = Number(arg >= 0 ? process.argv[arg+1] : process.env.PORT || 3000);
if (!Number.isInteger(port) || port<1 || port>65535) throw Error('Invalid port');
const types={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.pdf':'application/pdf','.otf':'font/otf','.ttf':'font/ttf'};
const server=http.createServer((req,res)=>{
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}
  let name;
  try {name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);}
  catch {res.writeHead(400);res.end();return;}
  if(name==='/api/neuroniy'){
    res.writeHead(200,{'Content-Type':'application/json','Cache-Control':'no-store'});
    res.end(req.method==='HEAD'?undefined:JSON.stringify({mode:'guide',version:'FIELD-winter-v4.6'}));return;
  }
  if(name==='/')name='/index.html';
  const file=path.resolve(site,'.'+name);
  if(!file.startsWith(site+path.sep)||!(name.startsWith('/assets/')||['/index.html'].includes(name))||!types[path.extname(file)]){res.writeHead(404);res.end();return;}
  try{
    const bytes=fs.readFileSync(file);
    res.writeHead(200,{'Content-Type':types[path.extname(file)],'Cache-Control':'no-store'});
    res.end(req.method==='HEAD'?undefined:bytes);
  }catch{res.writeHead(404);res.end();}
});
server.on('error',err=>{console.error(err.code==='EADDRINUSE'?'Port is busy. Try: npm start -- --port 3001':err.message);process.exitCode=1;});
server.listen(port,'127.0.0.1',()=>console.log('FIELD preview: http://127.0.0.1:'+port+'\nPaid AI is disabled in this local preview.'));
