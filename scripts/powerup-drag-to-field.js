/* Block Party: intentional drag-to-field power-up activation.
   A tap never consumes a quick-use power-up. */
(()=>{
'use strict';
const dock=document.getElementById('bpPowerQuickDock');
const arena=document.getElementById('arena');
if(!dock||!arena||window.bpPowerDragInstalled)return;
window.bpPowerDragInstalled=true;
const css=document.createElement('style');
css.id='bp-power-drag-style';
css.textContent=`
#bpPowerQuickDock .bp-power-quick{touch-action:none!important;user-select:none!important;-webkit-user-select:none!important;-webkit-touch-callout:none!important;cursor:grab!important}
#bpPowerQuickDock .bp-power-quick:active{cursor:grabbing!important}
#bpPowerQuickDock .bp-power-quick.bp-drag-source{opacity:.55}
#bpPowerDragGhost{position:fixed;z-index:999999;pointer-events:none;transform:translate(-50%,-50%);display:grid;place-items:center;width:54px;height:54px;border:2px solid #e4c4ff;border-radius:50%;background:#24154eeF;box-shadow:0 0 18px #a86dff88;color:#fff;font-size:24px}
#human.bp-power-drop-target{outline:3px solid #d9a5ff!important;outline-offset:2px;box-shadow:0 0 15px #a86dff99!important}
`;
document.head.appendChild(css);
let drag=null;
const field=()=>document.getElementById('human');
function inField(x,y){
 const f=field();if(!f||arena.hidden)return false;
 const r=f.getBoundingClientRect();
 return r.width>0&&r.height>0&&x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom;
}
function clear(){
 if(!drag)return;
 drag.button.classList.remove('bp-drag-source');
 field()?.classList.remove('bp-power-drop-target');
 drag.ghost?.remove();
 drag=null;
}
dock.addEventListener('click',e=>{
 const b=e.target.closest('.bp-power-quick');
 if(!b)return;
 // Capture before the original onclick handler. Even an accidental tap does nothing.
 e.preventDefault();e.stopImmediatePropagation();
},true);
dock.addEventListener('pointerdown',e=>{
 const b=e.target.closest('.bp-power-quick');
 if(!b||b.disabled||arena.hidden||e.button!==0)return;
 clear();
 drag={button:b,pointerId:e.pointerId,startX:e.clientX,startY:e.clientY,moved:false,ghost:null};
 e.preventDefault();
},true);
document.addEventListener('pointermove',e=>{
 if(!drag||e.pointerId!==drag.pointerId)return;
 const dx=e.clientX-drag.startX,dy=e.clientY-drag.startY;
 if(!drag.moved&&Math.hypot(dx,dy)<24)return;
 if(!drag.moved){
  drag.moved=true;drag.button.classList.add('bp-drag-source');
  const g=document.createElement('div');g.id='bpPowerDragGhost';
  g.textContent=drag.button.querySelector('.bp-power-quick-symbol')?.textContent||'⚡';
  document.body.appendChild(g);drag.ghost=g;
 }
 drag.ghost.style.left=e.clientX+'px';drag.ghost.style.top=e.clientY+'px';
 field()?.classList.toggle('bp-power-drop-target',inField(e.clientX,e.clientY));
 e.preventDefault();
},true);
document.addEventListener('pointerup',e=>{
 if(!drag||e.pointerId!==drag.pointerId)return;
 const b=drag.button,valid=drag.moved&&inField(e.clientX,e.clientY)&&b.isConnected&&!b.disabled;
 clear();
 if(valid){
  // Existing handler performs eligibility checks, server-side consumption and effects.
  b.onclick?.call(b);
 }
 e.preventDefault();
},true);
document.addEventListener('pointercancel',e=>{if(drag&&e.pointerId===drag.pointerId)clear()},true);
window.addEventListener('blur',clear);
})();
