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
// Capture the actual six highlighted choices from the loadout dialog at START MATCH.
// Never infer the user's choices from the first six available items.
const loadoutNames={
 'Double Points':'double_points','Power Pause':'power_pause','Super Multiplier':'super_multiplier',
 'Special Block Generator':'special_block_generator','Garbage Shield':'garbage_shield',
 'Attack Amplifier':'attack_amplifier','Wild Block':'wild_block','Block Bomb':'block_bomb',
 'Block Lock':'block_lock','Return To Sender':'return_to_sender','Deep Freeze':'deep_freeze',
 'Mirror Match':'mirror_match','Lifesaver':'lifesaver','Blindfold':'blindfold'
};
let confirmedLoadout=null,applying=false;
function currentType(){
 const mode=document.getElementById('mode')?.value;
 const versus=document.getElementById('play')?.value==='versus';
 return (versus?'versus-':'solo-')+(mode==='battle'?'battle':mode==='timed'?'timed':'line');
}
document.addEventListener('click',e=>{
 const confirm=e.target.closest('#bpDevLoadoutDialog .bp-loadout-confirm');
 if(!confirm||confirm.disabled)return;
 const dialog=document.getElementById('bpDevLoadoutDialog');
 if(!dialog)return;
 const selected=Array.from(dialog.querySelectorAll('.bp-loadout-choice.selected'))
  .map(b=>Object.entries(loadoutNames).find(([name])=>b.textContent.trim().endsWith(name))?.[1])
  .filter(Boolean);
 if(!selected.length)return;
 confirmedLoadout={type:currentType(),ids:selected};
 // The underlying game owns the confirm action; this capture only preserves its actual UI selection.
},true);
function restoreSelectedLoadout(){
 if(applying||arena.hidden||!window.bpPowerSession)return;
 const type=currentType();
 const saved=confirmedLoadout?.type===type?confirmedLoadout.ids:window.bpDevLoadouts?.[type];
 if(!Array.isArray(saved)||!saved.length)return;
 const current=window.bpPowerSession.active||[];
 if(current.length===saved.length&&current.every((id,i)=>id===saved[i]))return;
 window.bpPowerSession.active=[...saved];
 window.bpDevLoadouts=window.bpDevLoadouts||{};
 window.bpDevLoadouts[type]=[...saved];
 applying=true;
 Promise.resolve(window.bpPowerRefreshQuick?.()).catch(console.warn).finally(()=>{applying=false});
}
new MutationObserver(()=>{
 if(arena.hidden){confirmedLoadout=null;return;}
 setTimeout(restoreSelectedLoadout,0);
 setTimeout(restoreSelectedLoadout,300);
}).observe(arena,{attributes:true,attributeFilter:['class','hidden']});
const dockObserver=new MutationObserver(()=>{if(!applying&&!arena.hidden)setTimeout(restoreSelectedLoadout,0)});
dockObserver.observe(dock,{childList:true});
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
