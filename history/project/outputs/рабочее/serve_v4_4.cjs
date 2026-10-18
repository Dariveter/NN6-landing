'use strict';
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../готовое');

const types={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.pdf':'application/pdf','.otf':'font/otf','.ttf':'font/ttf'};
http.createServer(async(req,res)=>{
 const url=new URL(req.url,'http://127.0.0.1');
 if(url.pathname.startsWith('/__capture/')){
  const name=url.pathname.split('/').pop();
  if(req.method!=='POST'||!/^[-a-zA-Z0-9]+\.(jpg|json)$/.test(name)||!['http://127.0.0.1:8848'].includes(req.headers.origin)){res.writeHead(403);res.end();return;}
  let raw='';for await(const data of req){raw+=data;if(raw.length>6000000){res.writeHead(413);res.end();return;}}
  const data=JSON.parse(raw),dir=path.join(root,'проверка/v4-4');fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,name),name.endsWith('.jpg')?Buffer.from(data.data,'base64'):JSON.stringify(data,null,2));res.writeHead(200);res.end('OK');return;
 }
 if(url.pathname==='/api/neuroniy'){
  for(const key of Object.keys(require.cache))if(key.startsWith(root+path.sep))delete require.cache[key];
  const handler=require(path.join(root,'api/neuroniy.js'));
  if(req.method==='POST'){
   let size=0,body='';let tooLarge=false;
   for await(const data of req){size+=data.length;if(size>14000){tooLarge=true;break;}body+=data;}
   if(tooLarge){res.writeHead(413,{'Content-Type':'application/json'});res.end('{"error":"too_large"}');return;}
   req.body=body;
  }
  try{await handler(req,res);}catch(_){if(!res.headersSent)res.writeHead(500,{'Content-Type':'application/json'});res.end('{"error":"unavailable"}');}
  return;
 }
 if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}
 let p;try{p=decodeURIComponent(url.pathname);}catch(_){res.writeHead(400);res.end();return;}
 if(p==='/')p='/index.html';
 const target=path.resolve(root,'.'+p),ext=path.extname(target);
 if(!target.startsWith(root+path.sep)||!(p.startsWith('/assets/')||['/index.html','/alumni.html','/reviews.html','/program-v8.pdf'].includes(p))||!types[ext]){res.writeHead(404);res.end();return;}
 try{const bytes=fs.readFileSync(target);res.writeHead(200,{'Content-Type':types[ext],'Cache-Control':'no-cache'});res.end(req.method==='HEAD'?undefined:bytes);}catch(_){res.writeHead(404);res.end();}
}).listen(8848,'127.0.0.1',()=>console.log('FIELD v4.4 local preview: http://127.0.0.1:8848'));

