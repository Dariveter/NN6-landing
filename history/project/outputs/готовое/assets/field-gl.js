'use strict';
// Decorative WebGL 1 point field; HTML and SVG always remain the fallback.
(() => {
  const canvas = document.querySelector('#field-canvas'), art = canvas.closest('.hero-art');
  const toggle = document.querySelector('#motion-toggle'), reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const economical = navigator.connection?.saveData || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2);
  let gl, program, raf = 0, visible = false, paused = false, failed = false, last = 0, elapsed = 0;
  let timeUniform, ratioUniform, pixelUniform;
  const stop = () => {if (raf) cancelAnimationFrame(raf); raf = 0; last = 0;};
  const fallback = () => {failed = true; stop(); art.classList.remove('gl-ready'); art.dataset.motion = 'fallback'; toggle.hidden = true;};
  if (reduced.matches || economical) {art.dataset.motion = 'static'; toggle.hidden = true; return;}
  try {
    gl = canvas.getContext('webgl', {alpha: true, antialias: false, depth: false, stencil: false, powerPreference: 'low-power'});
    if (!gl) {fallback(); return;}
    const vertex = [
      'attribute vec3 a_seed;',
      'uniform float u_time; uniform float u_ratio; uniform float u_pixel;',
      'varying float v_tint; varying float v_alpha;',
      'void main(){',
      'float a=a_seed.x; float b=a_seed.y;',
      'float wave=sin(a*3.0+u_time*.24)*.06;',
      'float ring=.97+cos(b)*.24+wave;',
      'vec3 p=vec3(cos(a)*ring,sin(b)*.25,sin(a)*ring);',
      'float r=.48+u_time*.055;',
      'p.xz=mat2(cos(r),-sin(r),sin(r),cos(r))*p.xz;',
      'float tilt=.92;',
      'p.yz=mat2(cos(tilt),-sin(tilt),sin(tilt),cos(tilt))*p.yz;',
      'float spin=-.25;',
      'p.xy=mat2(cos(spin),-sin(spin),sin(spin),cos(spin))*p.xy;',
      'float depth=3.5-p.z;',
      'vec2 projected=p.xy*2.30/depth;',
      'projected.x/=u_ratio; projected.y+=.045;',
      'gl_Position=vec4(projected,0.0,1.0);',
      'gl_PointSize=(1.3+a_seed.z*1.15)*u_pixel*3.0/depth;',
      'v_tint=(sin(a+b)+1.0)*.5;',
      'v_alpha=.32+((p.z+1.2)/2.4)*.6;',
      '}'
    ].join('\n');
    const fragment = [
      'precision mediump float;', 'varying float v_tint; varying float v_alpha;',
      'void main(){', 'float d=length(gl_PointCoord-vec2(.5));',
      'float alpha=(1.0-smoothstep(.19,.5,d))*v_alpha;',
      'vec3 c=mix(vec3(.40,.76,.68),vec3(.82,.91,.72),v_tint*.78);',
      'gl_FragColor=vec4(c,alpha);', '}'
    ].join('\n');
    const shader = (type, source) => {
      const s = gl.createShader(type); gl.shaderSource(s, source); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {gl.deleteShader(s); throw new Error('Shader compilation failed');}
      return s;
    };
    const vs = shader(gl.VERTEX_SHADER, vertex), fs = shader(gl.FRAGMENT_SHADER, fragment);
    program = gl.createProgram(); gl.attachShader(program, vs); gl.attachShader(program, fs); gl.linkProgram(program);
    gl.deleteShader(vs); gl.deleteShader(fs);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error('Shader link failed');
    gl.useProgram(program);
    const count = 3456, seeds = new Float32Array(count*3);
    for (let i=0;i<count;i++) {
      seeds[i*3] = Math.floor(i/18)/192*Math.PI*2;
      seeds[i*3+1] = (i%18)/18*Math.PI*2;
      seeds[i*3+2] = (Math.sin(i*78.233)*43758.5453)%1*.5+.5;
    }
    const buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buffer); gl.bufferData(gl.ARRAY_BUFFER, seeds, gl.STATIC_DRAW);
    const attribute = gl.getAttribLocation(program, 'a_seed');
    gl.enableVertexAttribArray(attribute); gl.vertexAttribPointer(attribute, 3, gl.FLOAT, false, 0, 0);
    timeUniform = gl.getUniformLocation(program, 'u_time');
    ratioUniform = gl.getUniformLocation(program, 'u_ratio');
    pixelUniform = gl.getUniformLocation(program, 'u_pixel');
    gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.clearColor(0,0,0,0);
    const draw = () => {
      if (failed || gl.isContextLost()) return;
      gl.clear(gl.COLOR_BUFFER_BIT); gl.uniform1f(timeUniform, elapsed); gl.drawArrays(gl.POINTS, 0, count);
    };
    const resize = () => {
      if (failed) return;
      const r = art.getBoundingClientRect(), pixel = Math.min(devicePixelRatio || 1, innerWidth<621 ? 1.25 : 1.5);
      canvas.width = Math.max(1, Math.round(r.width*pixel)); canvas.height = Math.max(1, Math.round(r.height*pixel));
      gl.viewport(0,0,canvas.width,canvas.height);
      gl.uniform1f(ratioUniform, r.width/r.height); gl.uniform1f(pixelUniform, pixel); draw();
    };
    const frame = stamp => {
      raf = 0;
      if (paused || reduced.matches || !visible || document.hidden || failed) return;
      if (!last || stamp-last>=1000/30) {
        if (last) elapsed += Math.min((stamp-last)/1000,.08);
        last = stamp; draw();
      }
      raf = requestAnimationFrame(frame);
    };
    const sync = () => {
      stop();
      const running = !paused && !reduced.matches && visible && !document.hidden && !failed;
      art.dataset.motion = running ? 'running' : 'paused';
      if (running) raf = requestAnimationFrame(frame);
    };
    toggle.addEventListener('click', () => {
      paused = !paused; toggle.setAttribute('aria-pressed', String(paused));
      toggle.setAttribute('aria-label', paused ? 'Включить анимацию' : 'Приостановить анимацию');
      toggle.textContent = paused ? '▷' : 'Ⅱ'; sync();
    });
    document.addEventListener('visibilitychange', sync);
    reduced.addEventListener('change', () => {toggle.hidden = reduced.matches; sync();});
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting; sync();
    }, {threshold: .01}).observe(art);
    else {visible = true; sync();}
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(art); else addEventListener('resize', resize, {passive: true});
    canvas.addEventListener('webglcontextlost', evt => {evt.preventDefault(); fallback();});
    addEventListener('pagehide', stop); addEventListener('pageshow', sync);
    resize(); art.classList.add('gl-ready');
  } catch (_error) {fallback();}
})();
