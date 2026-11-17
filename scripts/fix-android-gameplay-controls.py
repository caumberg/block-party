from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
anchor='</style>\n</style>\n<div id="menu">'
assert s.count(anchor)==1, f'Expected exactly one main stylesheet ending, found {s.count(anchor)}'
css="""
/* One authoritative Android layout: no overlapping legacy positioning. */
#arena.solo,#arena.versus{box-sizing:border-box!important;padding-top:clamp(8px,1.5dvh,20px)!important;overflow:hidden!important}
#arena.solo #top,#arena.versus #top{background:transparent!important;border:0!important;box-shadow:none!important;backdrop-filter:none!important;-webkit-backdrop-filter:none!important;margin:0 0 clamp(8px,1.2dvh,16px)!important;padding:4px 8px!important}
#arena #bpPowerBolt,body.bp-developer-active #arena:not([hidden]) #bpPowerBolt{display:none!important}
#bpMini{display:none!important}
/* Solo side HUD: anchor to the boards, not a separate full-width row. */
#arena.solo #boards{position:relative!important;width:100%!important;max-width:710px!important;display:flex!important;justify-content:center!important;align-items:flex-start!important;margin:4px auto 0!important}
#arena.solo #soloHud{position:absolute!important;inset:0 0 auto 0!important;transform:none!important;display:block!important;width:100%!important;max-width:none!important;height:0!important;margin:0!important;padding:0!important;pointer-events:none!important;z-index:2!important}
#arena.solo #soloHud .hud-card{box-sizing:border-box!important;position:absolute!important;min-width:0!important;width:min(23vw,155px)!important;height:clamp(64px,7dvh,94px)!important;min-height:0!important;max-height:none!important;margin:0!important;padding:5px!important;display:flex!important;flex-direction:column!important;justify-content:center!important;align-items:center!important;text-align:center!important;gap:3px!important}
#arena.solo #soloHud .hud-card:nth-child(1){left:2%!important;top:0!important}
#arena.solo #soloHud .hud-card:nth-child(2){left:2%!important;top:clamp(72px,8dvh,105px)!important}
#arena.solo #soloHud .hud-card:nth-child(3){left:auto!important;right:2%!important;top:0!important}
#arena.solo #soloHud .hud-label{font-size:clamp(10px,2vw,13px)!important}
#arena.solo #soloHud .hud-card strong{font-size:clamp(11px,2.6vw,17px)!important;line-height:1.15!important;overflow-wrap:anywhere!important}
#arena #boards{flex:0 0 auto!important;margin:0 auto!important}
#arena.solo #humanZone{box-sizing:border-box!important;width:min(46vw,330px)!important;flex:0 0 min(46vw,330px)!important;max-width:none!important;margin:0 auto!important}
#arena.solo #human{box-sizing:border-box!important;width:100%!important;height:min(43dvh,660px)!important;max-height:none!important;aspect-ratio:auto!important;display:block!important}
#arena.solo #bpPowerQuickDock{margin:8px auto 0!important}
#arena.solo #bottom{margin:clamp(5px,1dvh,14px) auto 0!important}
#arena.versus #human,#arena.versus #cpu{height:min(43dvh,660px)!important;max-height:660px!important;aspect-ratio:auto!important}
#arena #bpPowerQuickDock{box-sizing:border-box!important;position:relative!important;inset:auto!important;top:auto!important;left:auto!important;right:auto!important;bottom:auto!important;transform:none!important;z-index:10!important;display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;align-items:center!important;justify-content:center!important;gap:clamp(5px,1.2vw,10px)!important;width:max-content!important;max-width:calc(100% - 16px)!important;height:clamp(54px,5dvh,70px)!important;min-height:0!important;margin:3px auto 0!important;padding:3px 8px!important;overflow:visible!important;pointer-events:none!important}
#arena #bpPowerQuickDock[hidden]{display:none!important}
#arena #bpPowerQuickDock .bp-power-quick{box-sizing:border-box!important;flex:0 1 auto!important;min-width:0!important;width:clamp(43px,8vw,58px)!important;height:clamp(43px,8vw,58px)!important;pointer-events:auto!important;box-shadow:0 0 9px #9d74ff88!important}
#arena #bottom{box-sizing:border-box!important;display:flex!important;flex:0 0 auto!important;align-items:center!important;justify-content:center!important;gap:clamp(10px,3vw,22px)!important;width:min(96vw,490px)!important;margin:clamp(5px,1dvh,14px) auto 0!important;padding:0!important;position:relative!important;top:auto!important;overflow:visible!important}
#arena #bottom #pad{box-sizing:border-box!important;display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:3px!important;width:min(48vw,220px)!important;height:min(45vw,210px)!important;max-width:none!important;max-height:none!important;min-width:0!important;min-height:0!important;flex:0 0 min(48vw,220px)!important;transform:none!important;filter:drop-shadow(0 0 5px #5c94ff55)!important}
#arena #bottom #pad button{box-sizing:border-box!important;width:100%!important;height:100%!important;min-width:0!important;min-height:0!important;padding:0!important;border-radius:9px!important;font-size:clamp(17px,4vw,25px)!important}
#arena #bottom #actionStack{box-sizing:border-box!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:center!important;gap:10px!important;width:min(34vw,180px)!important;max-width:none!important;flex:0 0 min(34vw,180px)!important;align-self:center!important}
#arena #bottom #actionStack #raiseRow,#arena #bottom #actionStack #swap{box-sizing:border-box!important;position:relative!important;inset:auto!important;transform:none!important;align-self:stretch!important;width:100%!important;max-width:none!important;margin:0!important;flex:0 0 auto!important}
#arena #bottom #actionStack #raiseRow{height:clamp(42px,7vw,56px)!important;min-height:0!important}
#arena #bottom #actionStack #swap{height:clamp(68px,13vw,98px)!important;min-height:0!important;filter:drop-shadow(0 0 7px #ff54ee66)!important}
@media(max-height:750px){#arena.solo #human,#arena.versus #human,#arena.versus #cpu{height:39dvh!important}#arena #bottom #pad{height:min(38vw,175px)!important}#arena #bottom #bpPowerQuickDock{height:50px!important}}
"""
s=s.replace(anchor,css+anchor,1)
# The rotating Top 10 sidebar was retired from gameplay. Keep the global
# leaderboard screen accessible from the main menu; do not run its timer
# or let its panel cover the power-up controls in Solo mode.
old_init="""function initMiniLeaderboard(){
 clearInterval(bpMiniTimer);bpMiniCache={};bpMiniPeriod=0;bpMiniShowScore=false;
 $('bpMini').hidden=isVersus;
 if(isVersus)return;
 requestAnimationFrame(positionMiniLeaderboard);bpRenderMini();
 bpMiniTimer=setInterval(()=>{"""
new_init="""function initMiniLeaderboard(){
 clearInterval(bpMiniTimer);bpMiniTimer=null;
 $('bpMini').hidden=true;
 return;
 bpMiniCache={};bpMiniPeriod=0;bpMiniShowScore=false;
 $('bpMini').hidden=isVersus;
 if(isVersus)return;
 requestAnimationFrame(positionMiniLeaderboard);bpRenderMini();
 bpMiniTimer=setInterval(()=>{"""
assert s.count(old_init)==1, f'Expected one rotating leaderboard initializer, found {s.count(old_init)}'
s=s.replace(old_init,new_init,1)
# Belt and suspenders: even if another code path unhides it, the sidebar
# cannot visually cover the game or power-up buttons.
s=s.replace(anchor, '#bpMini{display:none!important}\\n'+anchor,1) if False else s
# Move the actual power-up dock OUT of #boards, so CSS layout has a real
# dedicated row between the play fields and the game controls.
dock_old="boards.appendChild(dock);"
dock_new="boards.insertAdjacentElement('afterend',dock);"
assert s.count(dock_old)==1, f'Expected one quick dock mount, got {s.count(dock_old)}'
s=s.replace(dock_old,dock_new,1)
# Move the existing Solo HUD, with its live counters intact, before the
# boards. This avoids trying to float a sidebar with absolute positioning.
hud_old='<div id="boards"><aside id="soloHud"'
hud_new='<div id="boards"><aside id="soloHud"'
assert s.count(hud_old)==1, f'Expected one Solo HUD markup, found {s.count(hud_old)}'
s=s.replace(hud_old,hud_new,1)
zone_old='</aside><section class="zone" id="humanZone">'
zone_new='</aside><section class="zone" id="humanZone">'
assert s.count(zone_old)==1, f'Expected one HUD/zone boundary, found {s.count(zone_old)}'
s=s.replace(zone_old,zone_new,1)
# Campaign uses the same active quick-use dock as Arcade. A campaign launch can
# bypass the Arcade loadout initializer, leaving active=[] and an empty dock.
# Populate eligible campaign power-ups from the existing inventory on render,
# without consuming inventory or changing Arcade's chosen loadout.
quick_anchor=""" const versusBattle=$('arena').classList.contains('versus')&&$('mode').value==='battle';
 const usable=items.filter(i=>window.bpPowerSession.active.includes(i[0])"""
quick_replacement=""" const versusBattle=$('arena').classList.contains('versus')&&$('mode').value==='battle';
 // Always populate the dock from owned, eligible consumables.
 // Do not require Developer Mode or a separately selected loadout.
 session.active=items.filter(i=>i[3]==='active'&&Number(inventory[i[0]]||0)>0&&devEligible(i[0])).slice(0,6).map(i=>i[0]);
 const usable=items.filter(i=>window.bpPowerSession.active.includes(i[0])"""
assert s.count(quick_anchor)==1, f'Expected one quick-use eligibility section, got {s.count(quick_anchor)}'
s=s.replace(quick_anchor,quick_replacement,1)
# Campaign has older selectors which explicitly show the retired bolt.
# Hide the actual element, including in Developer Mode, on each dock sync.
sync_old="function sync(){const dest=$('arena').classList.contains('versus')?boards:header;if(bolt.parentElement!==dest)dest.appendChild(bolt);bolt.hidden=true;renderQuick()}"
sync_new="function sync(){const dest=$('arena').classList.contains('versus')?boards:header;if(bolt.parentElement!==dest)dest.appendChild(bolt);bolt.hidden=true;bolt.style.setProperty('display','none','important');renderQuick()}"
assert s.count(sync_old)==1, f'Expected one bolt sync, got {s.count(sync_old)}'
s=s.replace(sync_old,sync_new,1)
# Normal Arcade also needs a wallet inventory refresh after the arena opens.
# The previous observer refreshed only Campaign, leaving inventory empty
# outside Developer Mode. Refresh once per launch and on account changes.
observer_old="new MutationObserver(()=>{sync();if(!$('arena').hidden&&$('arena').classList.contains('bp-campaign-power'))refresh().catch(()=>{})}).observe($('arena'),{attributes:true,attributeFilter:['class','hidden']});"
observer_new="new MutationObserver(()=>{sync();if(!$('arena').hidden)refresh().catch(e=>console.warn('Power-up inventory refresh failed',e))}).observe($('arena'),{attributes:true,attributeFilter:['class','hidden']});"
assert s.count(observer_old)==1, 'Arena inventory observer missing'
s=s.replace(observer_old,observer_new,1)

p.write_text(s,encoding='utf-8')
print('Patched actual main gameplay CSS')
