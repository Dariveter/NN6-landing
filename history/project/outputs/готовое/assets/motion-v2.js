'use strict';
(() => {
  const canvas = document.getElementById('ambient-canvas');
  const toggle = document.getElementById('motion-toggle');
  const progress = document.querySelector('.scroll-progress');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduced.matches, frame = 0, last = 0, scroll = window.scrollY, gl, program;
  const uniforms = {};
  const syncControl = () => {
    document.body.classList.toggle('motion-paused', paused);
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.setAttribute('aria-label', paused ? 'Включить анимацию' : 'Приостановить анимацию');
    toggle.title = toggle.getAttribute('aria-label');
    toggle.textContent = paused ? '▷' : 'Ⅱ';
  };
  function resize() {
    const ratio = innerWidth < 700 ? 1 : Math.min(devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(innerWidth * ratio);
    canvas.height = Math.round(innerHeight * ratio);
    if (gl) gl.viewport(0, 0, canvas.width, canvas.height);
    draw(last);
  }
  function init() {
    try {
      gl = canvas.getContext('webgl', {alpha: true, antialias: false, depth: false, stencil: false, powerPreference: 'low-power', premultipliedAlpha: false});
      if (!gl) return;
      const shader = (type, code) => {
        const s = gl.createShader(type); gl.shaderSource(s, code); gl.compileShader(s);
        if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {gl.deleteShader(s);throw new Error('Decorative shader failed');}
        return s;
      };
      const vs = shader(gl.VERTEX_SHADER, 'attribute vec2 pos; void main(){gl_Position=vec4(pos,0.,1.);}');
      const fs = shader(gl.FRAGMENT_SHADER, `precision mediump float;
        uniform vec2 resolution; uniform float time; uniform float travel;
        void main(){
          vec2 uv=gl_FragCoord.xy/resolution; float y=uv.y+travel;
          float a=0.; vec3 c=vec3(0.);
          for(int i=0;i<6;i++){
            float f=float(i); float side=mod(f,2.);
            float center=mix(.01,.99,side)+sin(y*2.2+f*.71+time*.09)*.075;
            center+=sin(y*4.4+time*.06+f*.43)*.022;
            float d=abs(uv.x-center-f*.0035);
            float line=1.-smoothstep(.0004,.0018,d);
            float glow=(1.-smoothstep(.003,.017,d))*.075;
            float fade=.4+.35*sin(y*1.7+f*.8);
            float w=(line*.24+glow)*fade;
            vec3 color=mix(vec3(.26,.64,.55),vec3(.87,.49,.31),step(3.,f));
            c+=color*w; a+=w;
          }
          float dotY=fract(time*.025+.24); float dotX=.014+sin((dotY+travel)*2.2+time*.09)*.075+sin((dotY+travel)*4.4+time*.06)*.022;
          float orb=1.-smoothstep(.002,.005,length((uv-vec2(dotX,dotY))*vec2(resolution.x/resolution.y,1.)));
          c+=vec3(.24,.6,.5)*orb*.28; a+=orb*.28;
          gl_FragColor=vec4(c/max(a,.001),min(a,.45));
        }`);
      program = gl.createProgram(); gl.attachShader(program, vs); gl.attachShader(program, fs); gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error('Decorative shader link failed');
      gl.useProgram(program); gl.deleteShader(vs); gl.deleteShader(fs);
      const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
      const pos=gl.getAttribLocation(program,'pos');gl.enableVertexAttribArray(pos);gl.vertexAttribPointer(pos,2,gl.FLOAT,false,0,0);
      ['resolution','time','travel'].forEach(n=>uniforms[n]=gl.getUniformLocation(program,n));
      canvas.dataset.renderer='webgl'; resize();
    } catch (_error) {gl=null; canvas.hidden=true;canvas.dataset.renderer='fallback';}
  }
  function draw(t) {
    if (!gl || !program || gl.isContextLost()) return;
    gl.uniform2f(uniforms.resolution,canvas.width,canvas.height);
    gl.uniform1f(uniforms.time,t/1000);
    gl.uniform1f(uniforms.travel,-scroll/Math.max(innerHeight,1)*.53);
    gl.drawArrays(gl.TRIANGLES,0,3);
  }
  function tick(t) {
    if (paused || document.hidden || reduced.matches) {frame=0;return;}
    if (t-last >= (innerWidth<700 ? 1000/24 : 1000/30)) {draw(t);last=t;}
    frame=requestAnimationFrame(tick);
  }
  function start() {if (!paused && !document.hidden && !reduced.matches && !frame) frame=requestAnimationFrame(tick);}
  function stop() {cancelAnimationFrame(frame);frame=0;}
  function updateScroll() {
    scroll=window.scrollY;
    const max=document.documentElement.scrollHeight-innerHeight;
    progress.style.transform='scaleX('+Math.min(1,max>0?scroll/max:0)+')';
  }
  toggle.addEventListener('click',()=>{
    if(reduced.matches) {paused=true;syncControl();return;}
    paused=!paused;syncControl(); if(paused) stop(); else start();
  });
  reduced.addEventListener('change',()=>{paused=reduced.matches;canvas.hidden=reduced.matches;syncControl();stop();if(!reduced.matches){if(!gl)init();start();}});
  document.addEventListener('visibilitychange',()=>document.hidden?stop():start());
  canvas.addEventListener('webglcontextlost',ev=>{ev.preventDefault();stop();canvas.hidden=true;canvas.dataset.renderer='context-lost';});
  canvas.addEventListener('webglcontextrestored',()=>{canvas.hidden=reduced.matches;init();start();});
  addEventListener('resize',resize,{passive:true});addEventListener('scroll',updateScroll,{passive:true});
  syncControl();updateScroll(); if(!reduced.matches){init();start();}
  if('IntersectionObserver' in window && !reduced.matches){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.remove('reveal-pending');observer.unobserve(entry.target);}
    }),{threshold:.07,rootMargin:'0px 0px 35px 0px'});
    document.querySelectorAll('.section-heading,.track-card,.person,.quote-card,.join-steps li').forEach(el=>{
      if(el.getBoundingClientRect().top>innerHeight){el.classList.add('reveal-ready','reveal-pending');observer.observe(el);}
    });
  }
})();
