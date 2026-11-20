
(()=>{
const $=id=>document.getElementById(id),bolt=$('bpPowerBolt'),overlay=$('bpPowerOverlay'),list=$('bpPowerList'),status=$('bpPowerStatus');
const items=[['double_points','🌟','Double Points','active'],['power_pause','⏱️','Power Pause','active'],['super_multiplier','⚡','Super Multiplier','active'],['special_block_generator','🎲','Special Block Generator','active'],['garbage_shield','🛡️','Garbage Shield','active'],['attack_amplifier','💥','Attack Amplifier','active'],['wild_block','🌈','Wild Block','active'],['block_bomb','💣','Block Bomb','active'],['block_lock','🔒','Block Lock','active'],['return_to_sender','📦','Return To Sender','active'],['deep_freeze','🧊','Deep Freeze','active'],['mirror_match','🪞','Mirror Match','active'],['lifesaver','🛟','Lifesaver','active'],['blindfold','🙈','Blindfold','active']];
const names=Object.fromEntries(items.map(i=>[i[0],i[2]]));let inventory={},selectedPassive=null,selectedActive=[],phase='game',pendingResolve=null,busy=false,seq=0,requests=new Map();
window.bpPowerSession={passive:null,active:[],used:[],assisted:false};
const header=$('humanZone').querySelector('header'),boards=$('boards');
const dock=document.createElement('div');dock.id='bpPowerQuickDock';dock.setAttribute('aria-label','Quick-use power-ups');boards.appendChild(dock);
let quickMessageTimer;
function quickNotice(message){
 let note=$('bpPowerQuickNotice');if(!note){note=document.createElement('div');note.id='bpPowerQuickNotice';boards.appendChild(note)}
 note.textContent=message;note.hidden=false;clearTimeout(quickMessageTimer);quickMessageTimer=setTimeout(()=>note.hidden=true,2400);
}
function devEligible(id){
 if($('arena').hidden)return false;
 const mode=$('mode').value,versus=$('arena').classList.contains('versus');
 if(['double_points','super_multiplier'].includes(id))return mode==='timed';
 if(id==='power_pause')return mode==='timed'&&!versus;
 if(['special_block_generator','garbage_shield','attack_amplifier'].includes(id))return versus&&mode==='battle';
 if(['return_to_sender','mirror_match'].includes(id))return versus&&mode==='battle';if(['block_lock','blindfold'].includes(id))return versus;if(['deep_freeze','lifesaver'].includes(id))return true;
 return ['wild_block','block_bomb'].includes(id);
}
function renderQuick(){
 dock.replaceChildren();const session=window.bpPowerSession;
 if(!session||$('arena').hidden)return;
 const versusBattle=$('arena').classList.contains('versus')&&$('mode').value==='battle';
 const usable=items.filter(i=>window.bpPowerSession.active.includes(i[0])&&Number(inventory[i[0]]||0)>0&&
 devEligible(i[0]));
 for(const item of usable){
  const [id,emoji,name,kind]=item,qty=Number(inventory[id]||0);
  if(qty<=0)continue;
  const b=document.createElement('button');b.type='button';b.className='bp-power-quick';b.title=name+' · '+qty+' available';b.setAttribute('aria-label','Use '+name+', '+qty+' available');b.disabled=busy;
  const symbol=document.createElement('span');symbol.className='bp-power-quick-symbol';symbol.textContent=emoji;
  const count=document.createElement('span');count.className='bp-power-quick-count';count.textContent='×'+qty;
  b.append(symbol,count);b.onclick=()=>use(id);dock.appendChild(b);
 }
 dock.hidden=!dock.childElementCount;
 // Solo: center the quick-use row beneath the board, not beside it.
 if(!$('arena').classList.contains('versus')){
  const field=$('humanZone').getBoundingClientRect();
  dock.style.position='fixed';
  dock.style.left=(field.left+field.width/2)+'px';
  dock.style.top=Math.max(0,field.bottom+8)+'px';
  dock.style.width='max-content';
  dock.style.transform='translateX(-50%)';
  dock.style.maxHeight='none';
 }else{
  for(const key of ['position','left','top','width','transform','maxHeight'])dock.style[key]='';
 }
}

function sync(){if(bolt?.isConnected)bolt.remove();renderQuick()}new MutationObserver(()=>{sync();if(!$('arena').hidden&&$('arena').classList.contains('bp-campaign-power'))refresh().catch(()=>{})}).observe($('arena'),{attributes:true,attributeFilter:['class','hidden']});sync();window.addEventListener('resize',()=>{if(!$('arena').hidden)renderQuick()});
function valid(item,l){if(!l)return true;if(l.type==='obstacles')return false;if(item==='time_extension')return l.type==='solo-timed';if(['special_block_magnet' ,'garbage_shield','attack_amplifier'].includes(item))return l.type==='versus';return true}
async function refresh(){
 if(window.bpDevActive){
  inventory=Object.fromEntries(items.map(i=>[i[0],99]));
  renderQuick();return inventory;
 }
 const d=await window.bpCampaignRpc('bp_store_get');inventory=d?.inventory||{};renderQuick();return inventory;
}
function row(item,mode){const [id,emoji,name,kind]=item,qty=Number(inventory[id]||0),r=document.createElement('button');r.type='button';r.className='bp-power-item bp-power-select';r.disabled=busy||qty<=0;const left=document.createElement('div'),strong=document.createElement('strong'),small=document.createElement('small');strong.textContent=emoji+' '+name;small.textContent=(kind==='passive'?'Passive':'Active')+' · Owned ×'+qty;left.append(strong,small);const right=document.createElement('strong');right.textContent=mode==='equip'?((kind==='passive'?selectedPassive===id:selectedActive.includes(id))?'✓ EQUIPPED':'EQUIP'):'USE';r.append(left,right);r.onclick=()=>mode==='equip'?toggle(id,kind):mode==='activate'?activatePassive(id):use(id);return r;}
function render(){list.replaceChildren();const equip=phase==='equip';const session=window.bpPowerSession;const versusBattle=!equip&&$('arena').classList.contains('versus')&&$('mode').value==='battle';
const source=equip?items.filter(i=>i[3]==='passive'):items.filter(i=>window.bpPowerSession.active.includes(i[0])&&Number(inventory[i[0]]||0)>0&&
 devEligible(i[0]));
for(const item of source){
 if(equip&&!valid(item[0],window.bpPowerUpcoming))continue;
 const passiveInGame=!equip&&item[3]==='passive';
 const r=row(item,equip?'equip':passiveInGame?'activate':'use');
 if(passiveInGame){
  const already=session.passive===item[0];
  r.lastChild.textContent=already?'ACTIVE':session.passive?'ONE PASSIVE MAX':'ACTIVATE';
  r.disabled=busy||already||!!session.passive||Number(inventory[item[0]]||0)<1;
 }
 if(!equip&&!passiveInGame&&Number(inventory[item[0]]||0)<1)r.disabled=true;
 list.append(r)
}
if(!list.children.length)status.textContent=equip?'No compatible passive power-ups available. You can still play without one.':'No active power-ups available. Buy more in the Store.';$('bpPowerCount').textContent=Object.values(inventory).reduce((a,v)=>a+Number(v||0),0);$('bpPowerCount').hidden=false;$('bpPowerDone').textContent=equip?'START MATCH':'BACK TO GAME';$('bpPowerStore').style.display=equip?'none':'';renderQuick();}
function toggle(id,kind){if(kind!=='passive')return;selectedPassive=selectedPassive===id?null:id;status.textContent='Choose one compatible passive for the entire match, or start without one. Active power-ups are available during gameplay.';render()}
function close(confirmed=false){overlay.hidden=true;if(phase==='game')window.bpPowerPause?.(false);if(pendingResolve){const resolve=pendingResolve;pendingResolve=null;resolve(confirmed)}}
async function openGame(){if($('arena').hidden)return;if(!$('arena').classList.contains('bp-campaign-power'))return;phase='game';overlay.hidden=false;window.bpPowerPause?.(true);status.textContent=$('arena').classList.contains('versus')&&$('mode').value==='battle'?'Use active power-ups directly from the quick-use bubbles.':'Active power-ups are available directly from the quick-use bubbles.';try{await refresh();render()}catch(e){status.textContent=e.message||'Inventory unavailable'}}
window.bpPowerPrepareLaunch=async l=>{
 window.bpPowerSession={passive:null,active:[],used:[],assisted:false};
 if(l.type==='obstacles')return true;
 await refresh();
 const versus=l.type==='versus'||l.type.startsWith('versus-'),mode=(l.type==='versus'||l.type.includes('battle'))?'battle':l.type.includes('timed')?'timed':'line';
 const eligible=items.filter(i=>Number(inventory[i[0]]||0)>0&&(
  ['wild_block','block_bomb','deep_freeze','lifesaver'].includes(i[0])||
  (versus&&['block_lock','blindfold'].includes(i[0]))||
  (mode==='timed'&&['double_points','super_multiplier'].includes(i[0]))||
  (mode==='timed'&&!versus&&i[0]==='power_pause')||
  (versus&&mode==='battle'&&['special_block_generator','garbage_shield','attack_amplifier','return_to_sender','mirror_match'].includes(i[0]))
 )).map(i=>i[0]);
 let chosen=eligible.slice(0,6);
 if(eligible.length>6){
  const saved=window.bpDevLoadouts?.[l.type];if(saved){chosen=saved.filter(id=>eligible.includes(id)).slice(0,6);}
  const dialog=document.createElement('div');dialog.id='bpDevLoadoutDialog';
  dialog.innerHTML='<div class="bp-loadout-panel"><h2>⚡ Choose your 6 power-ups</h2><p>Select up to six power-up types for this match. No inventory is consumed until activation.</p><div class="bp-loadout-grid"></div><div class="bp-loadout-footer"><span class="bp-loadout-count"></span><button type="button" class="bp-loadout-cancel">CANCEL</button><button type="button" class="bp-loadout-confirm">START MATCH</button></div></div>';
  document.body.appendChild(dialog);const grid=dialog.querySelector('.bp-loadout-grid'),count=dialog.querySelector('.bp-loadout-count'),confirm=dialog.querySelector('.bp-loadout-confirm');
  function paint(){grid.replaceChildren();for(const id of eligible){const item=items.find(i=>i[0]===id),b=document.createElement('button');b.type='button';b.className='bp-loadout-choice'+(chosen.includes(id)?' selected':'');b.textContent=item[1]+' '+item[2];b.setAttribute('aria-pressed',String(chosen.includes(id)));b.onclick=()=>{chosen=chosen.includes(id)?chosen.filter(v=>v!==id):chosen.length<6?[...chosen,id]:chosen;paint()};grid.appendChild(b)}count.textContent=chosen.length+' / 6 selected';confirm.disabled=chosen.length===0;}
  paint();const accepted=await new Promise(resolve=>{dialog.querySelector('.bp-loadout-cancel').onclick=()=>resolve(false);confirm.onclick=()=>resolve(true)});dialog.remove();if(!accepted)return false;
  window.bpDevLoadouts=window.bpDevLoadouts||{};window.bpDevLoadouts[l.type]=[...chosen];
 }
 window.bpPowerSession.active=chosen;return true;
};
window.bpPowerPause=paused=>{for(const id of ['human','cpu']){const f=$(id);if(f?.contentWindow)f.contentWindow.postMessage({bp:'power-pause',paused},'*')}};
window.bpPowerMessage=d=>{if(d.bp==='power-event'){status.textContent=d.detail||'Power-up activated';return;}const fn=requests.get(d.request);if(fn){requests.delete(d.request);fn(d)}};
function engineRequest(bp,item){return new Promise((resolve,reject)=>{const request=++seq;requests.set(request,resolve);$('human').contentWindow.postMessage({bp,item,request},'*');setTimeout(()=>{if(requests.has(request)){requests.delete(request);reject(Error('Game engine did not respond'))}},2500)})}
async function activatePassive(id){
 if(busy||window.bpPowerSession.passive||!['special_block_magnet' ,'garbage_shield','attack_amplifier'].includes(id))return;
 if(!$('arena').classList.contains('versus')||$('mode').value!=='battle'){status.textContent='This passive requires Versus Special Battle.';return}
 busy=true;status.textContent='Activating '+names[id]+'…';
 try{
  if(!window.bpDevActive)await window.bpCampaignRpc('bp_power_consume',{p_item:id});
  window.bpPowerSession.passive=id;
  window.bpPowerSession.assisted=true;
  if(!window.bpDevActive)inventory[id]=Math.max(0,Number(inventory[id]||0)-1);
  $('human').contentWindow.postMessage({bp:'power-config',passive:id},'*');
  status.textContent=names[id]+' is now active for this battle.';quickNotice(status.textContent);
  render();
 }catch(e){status.textContent='Could not activate: '+(e.message||e);quickNotice(status.textContent)}
 finally{busy=false;renderQuick()}
}
async function use(id){if(busy||!window.bpPowerSession.active.includes(id)||!devEligible(id)||Number(inventory[id]||0)<1)return;busy=true;status.textContent='Checking selected board position…';try{const check=await engineRequest('dev-power-check',id);if(!check.eligible)throw Error('No eligible blocks at the cursor. Move the cursor and try again.');if(!window.bpDevActive)await window.bpCampaignRpc('bp_power_consume',{p_item:id});const result=await engineRequest('dev-power-use',id);if(!result.success)throw Error('Inventory deducted, but board changed before activation. Contact support.');window.bpPowerSession.used.push(id);window.bpPowerSession.assisted=true;if(!window.bpDevActive)inventory[id]=Math.max(0,(Number(inventory[id])||0)-1);status.textContent=names[id]+' activated!';quickNotice(status.textContent);bpDevAnimation(id);render();setTimeout(()=>{if(!overlay.hidden)close()},400)}catch(e){status.textContent=e.message||'Activation failed';quickNotice(status.textContent)}finally{busy=false;renderQuick()}}

const bpDevAnimationCss=document.createElement('style');bpDevAnimationCss.textContent=`
@keyframes bpDevPowerFlash{0%{transform:translate(-50%,-50%) scale(.4);opacity:0}15%{transform:translate(-50%,-50%) scale(1.15);opacity:1}75%{opacity:1}100%{transform:translate(-50%,-50%) scale(1.05);opacity:0}}
.bp-dev-power-fx{position:fixed;top:44%;left:50%;z-index:9999;pointer-events:none;transform:translate(-50%,-50%);padding:20px 30px;border:2px solid #c9a5ff;border-radius:24px;background:#170e37ed;color:#fff;font-size:clamp(20px,5vw,35px);font-weight:900;text-align:center;box-shadow:0 0 60px #a04aff;animation:bpDevPowerFlash 1.4s ease-out forwards}
.bp-dev-timer{position:fixed;bottom:10px;left:50%;transform:translateX(-50%);z-index:9900;padding:7px 12px;background:#24133de8;border:1px solid #ae8aff;border-radius:14px;color:white;font-size:12px;max-width:95vw;text-align:center}`;document.head.appendChild(bpDevAnimationCss);
let bpDevTimers={};
function bpDevAnimation(id){const item=items.find(i=>i[0]===id);if(!item)return;const fx=document.createElement('div');fx.className='bp-dev-power-fx';fx.textContent=item[1]+' '+item[2];document.body.appendChild(fx);setTimeout(()=>fx.remove(),1500);
 const seconds={double_points:20,power_pause:20,super_multiplier:20,special_block_generator:20,garbage_shield:30,block_lock:20,deep_freeze:15,blindfold:10}[id];if(seconds){bpDevTimers[id]=Date.now()+seconds*1000;const timer=document.getElementById('bpDevTimer')||Object.assign(document.createElement('div'),{id:'bpDevTimer',className:'bp-dev-timer'});document.body.appendChild(timer);}}
setInterval(()=>{const timer=document.getElementById('bpDevTimer');if(!timer)return;if($('arena').hidden){timer.remove();bpDevTimers={};return;}const active=Object.entries(bpDevTimers).filter(([id,until])=>until>Date.now());bpDevTimers=Object.fromEntries(active);timer.textContent=active.map(([id,until])=>names[id]+': '+Math.ceil((until-Date.now())/1000)+'s').join(' · ');if(!active.length)timer.remove()},250);
window.bpPowerRefreshQuick=async()=>{try{await refresh()}catch(e){quickNotice('Power-ups unavailable')}};$('bpPowerClose').onclick=()=>close(false);$('bpPowerDone').onclick=()=>close(phase==='equip');$('bpPowerStore').onclick=()=>{close(false);window.bpOpenTicketStore?.()};overlay.addEventListener('click',e=>{if(e.target===overlay)close(false)});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!overlay.hidden)close(false)});new MutationObserver(()=>{
 if($('arena').hidden&&phase==='game'&&!overlay.hidden)close(false);
 if(!$('arena').hidden){refresh().then(render).catch(console.warn)}
}).observe($('arena'),{attributes:true,attributeFilter:['hidden']});
})();
