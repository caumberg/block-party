/* Block Party: intentional drag-to-either-field power-up activation. */
(()=>{
'use strict';
const dock=document.getElementById('bpPowerQuickDock'),arena=document.getElementById('arena');
if(!dock||!arena||window.bpPowerDragInstalled)return;
window.bpPowerDragInstalled=true;
const style=document.createElement('style');style.id='bp-power-drag-style';style.textContent=`
#bpPowerQuickDock .bp-power-quick{touch-action:none!important;user-select:none!important;-webkit-user-select:none!important;-webkit-touch-callout:none!important;cursor:grab!important}
#bpPowerQuickDock .bp-power-quick.bp-drag-source{opacity:.5}
#bpPowerDragGhost{position:fixed;z-index:999999;pointer-events:none;transform:translate(-50%,-50%);display:grid;place-items:center;width:54px;height:54px;border:2px solid #e4c4ff;border-radius:50%;background:#24154eef;box-shadow:0 0 18px #a86dff88;color:#fff;font-size:24px}
#human.bp-power-drop-target,#cpu.bp-power-drop-target{outline:3px solid #d9a5ff!important;outline-offset:2px;box-shadow:0 0 15px #a86dff99!important}
`;document.head.appendChild(style);
// The game's actual launch routine owns the selected IDs. Capture its output,
// not button labels or a guessed mode. Keep that exact selection authoritative.
let launchSelection=null,restoring=false;
if(typeof window.bpPowerPrepareLaunch==='function'){
 const originalPrepare=window.bpPowerPrepareLaunch;
 window.bpPowerPrepareLaunch=async function(...args){
  launchSelection=null;
  const accepted=await originalPrepare.apply(this,args);
  if(accepted&&window.bpPowerSession){
   const ids=window.bpPowerSession.active;
   launchSelection=Array.isArray(ids)?[...ids]:null;
   if(window.bpDevActive&&launchSelection?.length){
    console.info('[Block Party] Confirmed developer loadout:',launchSelection);
   }
  }
  return accepted;
 };
}
function restoreLaunchSelection(){
 if(restoring||arena.hidden||!launchSelection?.length||!window.bpPowerSession)return;
 const actual=window.bpPowerSession.active||[];
 if(actual.length===launchSelection.length&&actual.every((id,i)=>id===launchSelection[i]))return;
 restoring=true;
 window.bpPowerSession.active=[...launchSelection];
 Promise.resolve(window.bpPowerRefreshQuick?.()).catch(console.warn).finally(()=>{restoring=false});
}
new MutationObserver(()=>{
 if(arena.hidden){launchSelection=null;return;}
 queueMicrotask(restoreLaunchSelection);
 setTimeout(restoreLaunchSelection,100);
 setTimeout(restoreLaunchSelection,500);
}).observe(arena,{attributes:true,attributeFilter:['class','hidden']});
new MutationObserver(()=>{
 if(!restoring&&!arena.hidden)queueMicrotask(restoreLaunchSelection);
}).observe(dock,{childList:true});
let drag=null;
const fields=()=>[document.getElementById('human'),document.getElementById('cpu')].filter(Boolean);
function targetAt(x,y){
 if(arena.hidden)return null;
 return fields().find(f=>{const r=f.getBoundingClientRect();return r.width>0&&r.height>0&&x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom})||null;
}
function clear(){
 if(!drag)return;
 drag.button.classList.remove('bp-drag-source');
 fields().forEach(f=>f.classList.remove('bp-power-drop-target'));
 drag.ghost?.remove();drag=null;
}
dock.addEventListener('click',e=>{
 if(!e.target.closest('.bp-power-quick'))return;
 e.preventDefault();e.stopImmediatePropagation();
},true);
dock.addEventListener('pointerdown',e=>{
 const b=e.target.closest('.bp-power-quick');
 if(!b||b.disabled||arena.hidden||e.button!==0)return;
 clear();drag={button:b,pointerId:e.pointerId,startX:e.clientX,startY:e.clientY,moved:false,ghost:null};
 e.preventDefault();
},true);
document.addEventListener('pointermove',e=>{
 if(!drag||e.pointerId!==drag.pointerId)return;
 if(!drag.moved&&Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)<24)return;
 if(!drag.moved){
  drag.moved=true;drag.button.classList.add('bp-drag-source');
  const g=document.createElement('div');g.id='bpPowerDragGhost';
  g.textContent=drag.button.querySelector('.bp-power-quick-symbol')?.textContent||'⚡';
  document.body.appendChild(g);drag.ghost=g;
 }
 drag.ghost.style.left=e.clientX+'px';drag.ghost.style.top=e.clientY+'px';
 const target=targetAt(e.clientX,e.clientY);
 fields().forEach(f=>f.classList.toggle('bp-power-drop-target',f===target));
 e.preventDefault();
},true);
document.addEventListener('pointerup',e=>{
 if(!drag||e.pointerId!==drag.pointerId)return;
 const b=drag.button,valid=drag.moved&&!!targetAt(e.clientX,e.clientY)&&b.isConnected&&!b.disabled;
 clear();
 if(valid)b.onclick?.call(b);
 e.preventDefault();
},true);
document.addEventListener('pointercancel',e=>{if(drag&&e.pointerId===drag.pointerId)clear()},true);
window.addEventListener('blur',clear);
})();
