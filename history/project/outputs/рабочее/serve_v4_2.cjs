'use strict';
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../готовое');
const handler=require(path.join(root,'api/neuroniy.js'));
const types={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.pdf':'application/pdf','.otf':'font/otf','.ttf':'font/ttf'};
http.createServer(async(req,res)=>{
 const url=new URL(req.url,'http://127.0.0.1');
 if(url.pathname==='/api/neuroniy'){
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
}).listen(8846,'127.0.0.1',()=>console.log('FIELD v4.2 local preview: http://127.0.0.1:8846'));

