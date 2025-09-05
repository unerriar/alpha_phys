window.ENABLE_PLOTLY_RESIZE = true;
// === Linear Motion Demo Script (Smooth Marker + Table) ===

const BACKGROUND_COLOR = '#111';
const AXIS_COLOR = '#aaa';
const PARTICLE_COLOR = 'orange';

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const plotContainer = document.getElementById('plots');

const playPauseBtn = document.getElementById('play-pause-btn');
const reloadBtn = document.getElementById('reload-btn');
const x0Slider = document.getElementById('x0-slider');
const vSlider = document.getElementById('v-slider');

// Table cells
const valX0 = document.getElementById('val-x0');
const valV = document.getElementById('val-v');
const valX = document.getElementById('val-x');

// Simulation parameters
const AXIS_MIN = -5;
const AXIS_MAX = 5;
let x0 = 0;
let v = 1;
let x = x0;
let t = 0;
let isPlaying = false;
const dt = 0.016;
const T_MAX = 10; // plot duration in seconds

// Plot axis limits
const X_PLOT_MIN = -30;
const X_PLOT_MAX = 30;
const V_PLOT_MIN = -5;
const V_PLOT_MAX = 5;

// === Maintain 8:1 Aspect Ratio ===
function setCanvasAspect() {
  const containerWidth = canvas.parentElement.clientWidth;
  canvas.width = containerWidth;
  canvas.height = Math.round(containerWidth / 8);
}

// === Initialize ===
function initDemo() {
  setCanvasAspect();
  canvas.style.backgroundColor = BACKGROUND_COLOR;
  if (plotContainer) plotContainer.style.backgroundColor = BACKGROUND_COLOR;

  x0Slider.value = x0;
  vSlider.value = v;

  drawPlots();
  drawCanvas();
  updateTable();
}

// === Draw Plots (Static lines) ===
function drawPlots() {
  if (!window.Plotly || !plotContainer) return;

  const timeArray = [0, T_MAX];
  const xArray = timeArray.map(t => x0 + v * t);
  const vArray = timeArray.map(() => v);

  const layout = {
    grid: { rows: 1, columns: 2, pattern: 'independent' },
    paper_bgcolor: BACKGROUND_COLOR,
    plot_bgcolor: BACKGROUND_COLOR,
    margin: { l: 40, r: 10, t: 10, b: 40 },
    xaxis: { title: 't, c', color: AXIS_COLOR, gridcolor: '#333', range: [0, T_MAX] },
    xaxis2: { title: 't, c', color: AXIS_COLOR, gridcolor: '#333', range: [0, T_MAX] },
    yaxis: { title: 'x, м', color: AXIS_COLOR, gridcolor: '#333', range: [X_PLOT_MIN, X_PLOT_MAX] },
    yaxis2: { title: 'v, м/с', color: AXIS_COLOR, gridcolor: '#333', range: [V_PLOT_MIN, V_PLOT_MAX] },
    showlegend: true,
    legend: { x: 0.5, y: -0.2, xanchor: 'center', orientation: 'h', font: { color: AXIS_COLOR } }
  };

  const traceX = { name: 'координата, м', x: timeArray, y: xArray, mode: 'lines', line: { color: 'orange' }, xaxis:'x', yaxis:'y' };
  const traceV = { name: 'проекция скорости, м/с', x: timeArray, y: vArray, mode: 'lines', line: { color: 'lightblue' }, xaxis:'x2', yaxis:'y2' };
  
  // Initial marker at t=0
  const markerX = { x: [0], y: [x], mode: 'markers', marker: { color:'orange', size:10 }, showlegend:false, xaxis:'x', yaxis:'y' };
  const markerV = { x: [0], y: [v], mode: 'markers', marker: { color:'lightblue', size:10 }, showlegend:false, xaxis:'x2', yaxis:'y2' };

  Plotly.newPlot(plotContainer, [traceX, markerX, traceV, markerV], layout, { displayModeBar:false });
}

// === Update marker position ===
function updateMarkers() {
  if (!window.Plotly || !plotContainer) return;
  // Time on plot loops modulo T_MAX
  const tPlot = t % T_MAX;
  Plotly.restyle(plotContainer, { x:[[tPlot],[tPlot]], y:[[x],[v]] }, [1,3]);
}

// === Canvas rendering ===
function drawCanvas() {
  ctx.fillStyle = BACKGROUND_COLOR;
  ctx.fillRect(0,0,canvas.width,canvas.height);

  const axisY = canvas.height / 2;
  const scaleX = canvas.width / (AXIS_MAX - AXIS_MIN);

  // Draw axis
  ctx.strokeStyle = AXIS_COLOR;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0,axisY);
  ctx.lineTo(canvas.width,axisY);
  ctx.stroke();

  // Draw ticks & labels
  ctx.fillStyle = AXIS_COLOR;
  ctx.font = `${Math.max(12,canvas.height*0.08)}px sans-serif`;
  ctx.textAlign = 'center';
  for(let i=AXIS_MIN;i<=AXIS_MAX;i++){
    const xPos = (i-AXIS_MIN)*scaleX;
    ctx.beginPath();
    ctx.moveTo(xPos,axisY-5);
    ctx.lineTo(xPos,axisY+5);
    ctx.stroke();
    ctx.fillText(i.toString(), xPos, axisY+20);
  }
  ctx.fillText("x, м", canvas.width/2, axisY+40);

  // Draw particle
  const px = (x-AXIS_MIN)*scaleX;
  ctx.beginPath();
  ctx.arc(px, axisY-20, 8,0,2*Math.PI);
  ctx.fillStyle = PARTICLE_COLOR;
  ctx.fill();
}

// === Update numerical table ===
function updateTable() {
  valX0.textContent = x0.toFixed(1);
  valV.textContent = v.toFixed(1);
  valX.textContent = x.toFixed(1);
}

// === Simulation step ===
function step() {
  if(!isPlaying) return;

  t += dt;
  x += v*dt;

  if(x>AXIS_MAX || x<AXIS_MIN){
    x = x0;  // reset particle
    t = 0;   // reset marker/time
  }

  updateTable();
}

// === Controls ===
playPauseBtn.addEventListener('click',()=>{
  isPlaying=!isPlaying;
  playPauseBtn.textContent=isPlaying?'Пауза':'Старт';
});

reloadBtn.addEventListener('click',()=>{
  t=0; x=x0;
  drawPlots();
  updateTable();
});

x0Slider.addEventListener('input',()=>{
  x0=parseFloat(x0Slider.value);
  x=x0;
  drawPlots();
  updateTable();
});

vSlider.addEventListener('input',()=>{
  v=parseFloat(vSlider.value);
  drawPlots();
  updateTable();
});

// === Animation loop ===
function animate(){
  step();
  drawCanvas();
  updateMarkers();
  requestAnimationFrame(animate);
}

// Handle window resize
window.addEventListener('resize',()=>{
  setCanvasAspect();
  drawCanvas();
});

initDemo();
animate();
