'use strict';
(() => {
  const body=document.body, hero=document.querySelector('.hero'), canvas=document.querySelector('#hero-canvas');
  const button=document.querySelector('#motion-toggle'), art=document.querySelector('.hero-image-wrap');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)'), small=matchMedia('(max-width: 700px)');
  let paused=reduced.matches, inHero=true, raf=0, last=0, elapsed=0, px=0, py=0, tx=0, ty=0, gl, lost=false;
  const progress=document.querySelector('.scroll-progress');
  const labels=[...document.querySelectorAll('.scene-label')];
  try{paused=paused||sessionStorage.getItem('field-motion-paused')==='true';}catch(_){}
  const active=()=>!paused&&!document.hidden;
  const scrollProgress=()=>{
    const max=document.documentElement.scrollHeight-innerHeight;
    if(progress)progress.style.transform=`scaleX(${max>0?scrollY/max:0})`;
  };
  addEventListener('scroll',scrollProgress,{passive:true});scrollProgress();
  const targets=[...document.querySelectorAll('.question-head,.track-poster,.mentor-row,.season-ticket,.camp-wordmark')];
  if('IntersectionObserver' in window){
    const obs=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('in-view');obs.unobserve(entry.target);}
    }),{threshold:.1});targets.forEach(x=>obs.observe(x));
    new IntersectionObserver(entries=>{inHero=entries[0].isIntersecting;syncLoop();},{threshold:0}).observe(hero);
    // Do not spend CPU animating illustration objects that are off screen.
    const visible=new IntersectionObserver(entries=>entries.forEach(e=>{
      e.target.style.animationPlayState=e.isIntersecting?'':'paused';
    }),{rootMargin:'40px'});
    document.querySelectorAll('.route-art,.camp-wordmark').forEach(x=>visible.observe(x));
  }
  hero.addEventListener('pointermove',event=>{
    if(small.matches||!active())return;
    const r=hero.getBoundingClientRect();tx=(event.clientX-r.left)/r.width-.5;ty=(event.clientY-r.top)/r.height-.5;
  },{passive:true});
  hero.addEventListener('pointerleave',()=>{tx=ty=0;});
  let program, timeLoc, sizeLoc, pointerLoc;
  const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error('Shader unavailable');return s;};
  const init=()=>{
    try{
      gl=canvas.getContext('webgl',{alpha:true,antialias:false,depth:false,stencil:false,powerPreference:'low-power'});
      if(!gl)return;
      const vert=shader(gl.VERTEX_SHADER,'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}');
      const frag=shader(gl.FRAGMENT_SHADER,`precision mediump float;
        uniform vec2 res;uniform vec2 pointer;uniform float t;
        void main(){
          vec2 uv=gl_FragCoord.xy/res;vec2 q=uv+pointer*.012;
          float wave=.52+.16*sin(q.x*4.3+t*.16)+.08*cos(q.x*8.0-t*.12);
          float d=q.y-wave;float band=exp(-d*d*29.);
          float contour=pow(.5+.5*cos(d*133.+q.x*4.),23.);
          float side=smoothstep(.17,.9,q.x);
          vec3 mint=vec3(.24,.69,.63),blue=vec3(.15,.35,.69);
          vec3 color=mix(mint,blue,smoothstep(.34,.91,q.x));
          float glow=band*(.13+contour*.20)*(side*.65+.35);
          float arc=.58+.13*sin(q.x*3.2-t*.12);
          float line=exp(-pow((q.y-arc)*105.,2.))*.15;
          float a=glow+line;gl_FragColor=vec4(color*a,a);
        }`);
      program=gl.createProgram();gl.attachShader(program,vert);gl.attachShader(program,frag);gl.linkProgram(program);
      if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error('WebGL unavailable');
      gl.deleteShader(vert);gl.deleteShader(frag);gl.useProgram(program);
      const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
      const attr=gl.getAttribLocation(program,'p');gl.enableVertexAttribArray(attr);gl.vertexAttribPointer(attr,2,gl.FLOAT,false,0,0);
      timeLoc=gl.getUniformLocation(program,'t');sizeLoc=gl.getUniformLocation(program,'res');pointerLoc=gl.getUniformLocation(program,'pointer');
      resize();
    }catch(_){gl=null;canvas.hidden=true;}
  };
  const draw=()=>{if(!gl||lost)return;gl.uniform1f(timeLoc,elapsed*.001);gl.uniform2f(sizeLoc,canvas.width,canvas.height);gl.uniform2f(pointerLoc,px,py);gl.drawArrays(gl.TRIANGLES,0,6);};
  function resize(){
    if(gl&&!lost){const ratio=Math.min(devicePixelRatio||1,small.matches?1:1.35);canvas.width=Math.round(hero.clientWidth*ratio);canvas.height=Math.round(hero.clientHeight*ratio);gl.viewport(0,0,canvas.width,canvas.height);draw();}
    scrollProgress();
  }
  const frame=now=>{
    raf=0;if(!active()||!inHero)return;
    const interval=small.matches?1000/24:1000/30;
    if(now-last>=interval){
      elapsed+=last?Math.min(now-last,60):0;last=now;px+=(tx-px)*.08;py+=(ty-py)*.08;
      const mobile=small.matches, drift=Math.sin(elapsed*.00042)*(mobile?3:9);
      const scroll=Math.min(scrollY,hero.offsetHeight)*(mobile?.016:.07);
      art.style.transform=`translate3d(${px*(mobile?0:25)}px,${drift+py*(mobile?0:18)+scroll}px,0) rotate(${px*(mobile?0:1.1)}deg)`;
      labels.forEach((label,i)=>{label.style.transform=`translate3d(${px*(i+1)*-7}px,${Math.sin(elapsed*.00055+i)* (mobile?2:6)+py*(i+1)*-4}px,0)`;});
      draw();
    }
    raf=requestAnimationFrame(frame);
  };
  function syncLoop(){
    if(raf){cancelAnimationFrame(raf);raf=0;}last=0;
    if(active()&&inHero)raf=requestAnimationFrame(frame);
  }
  const apply=()=>{
    body.classList.toggle('motion-paused',paused);body.classList.toggle('motion-enabled',!paused);
    button.setAttribute('aria-pressed',String(paused));button.textContent=paused?'▶':'Ⅱ';
    const label=paused?'Включить анимацию':'Приостановить анимацию';button.setAttribute('aria-label',label);button.title=label;
    if(paused){art.style.transform='none';labels.forEach(x=>x.style.transform='none');}
    syncLoop();
  };
  button.addEventListener('click',()=>{paused=!paused;try{sessionStorage.setItem('field-motion-paused',String(paused));}catch(_){}apply();});
  reduced.addEventListener('change',e=>{paused=e.matches;apply();});
  document.addEventListener('visibilitychange',syncLoop);
  canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();lost=true;});
  canvas.addEventListener('webglcontextrestored',()=>{lost=false;init();});
  addEventListener('resize',resize,{passive:true});
  init();apply();
})();
