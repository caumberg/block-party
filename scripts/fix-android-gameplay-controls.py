from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
anchor='</style>\n</style>\n<div id="menu">'
assert s.count(anchor)==1, f'Expected exactly one main stylesheet ending, found {s.count(anchor)}'
css="""
/* Android gameplay controls: injected into the actual main document stylesheet. */
/* Quick-use power-ups are a horizontal toolbar below the playing field in
   BOTH Solo and Versus, never floating over the board or HUD. */
#arena #bpPowerQuickDock{
 position:relative!important;
 inset:auto!important;
 top:auto!important;
 left:auto!important;
 right:auto!important;
 bottom:auto!important;
 transform:none!important;
 display:flex!important;
 flex-direction:row!important;
 flex-wrap:wrap!important;
 justify-content:center!important;
 align-items:center!important;
 gap:clamp(6px,1.5vw,11px)!important;
 width:calc(100% - 28px)!important;
 max-width:650px!important;
 min-height:0!important;
 margin:clamp(12px,1.8dvh,22px) auto 0!important;
 padding:4px 10px!important;
 box-sizing:border-box!important;
 overflow:visible!important;
}
#arena #bpPowerQuickDock[hidden]{display:none!important}
#arena #bpPowerQuickDock .bp-power-quick{flex:0 0 auto!important}
#arena #bottom{margin-top:clamp(18px,2.5dvh,38px)!important}
#arena #bottom #actionStack{align-items:stretch!important}
#arena #bottom #actionStack #raiseRow,
#arena #bottom #actionStack #swap{margin-inline:0!important;align-self:stretch!important}
/* Solo HUD becomes three compact cards across the width above the board. */
#arena.solo #soloHud{
 position:relative!important;
 inset:auto!important;
 transform:none!important;
 display:grid!important;
 grid-template-columns:repeat(3,minmax(0,1fr))!important;
 gap:7px!important;
 width:calc(100% - 24px)!important;
 max-width:690px!important;
 margin:0 auto 10px!important;
 padding:0!important;
 align-items:stretch!important;
}
#arena.solo #soloHud .hud-card{
 width:auto!important;
 min-width:0!important;
 height:auto!important;
 min-height:68px!important;
 margin:0!important;
 padding:7px 4px!important;
 font-size:clamp(10px,2.5vw,14px)!important;
 display:flex!important;
 flex-direction:column!important;
 align-items:center!important;
 justify-content:center!important;
 text-align:center!important;
}
#arena.solo #soloHud .hud-card strong{font-size:clamp(12px,3.3vw,18px)!important;line-height:1.2!important}
#arena.solo #soloHud .hud-card .hud-label{font-size:clamp(10px,2.4vw,13px)!important}
/* Float enlarged power-ups just above the field's lower edge.
   Negative margin deliberately overlays the field, not the controls. */
#arena #bpPowerQuickDock{
 z-index:210!important;
 position:relative!important;
 margin:-64px auto 0!important;
 min-height:64px!important;
 padding:7px 9px 10px!important;
 width:max-content!important;
 max-width:calc(100% - 26px)!important;
 gap:clamp(7px,1.5vw,13px)!important;
 flex-wrap:nowrap!important;
 pointer-events:none!important;
}
#arena #bpPowerQuickDock .bp-power-quick{
 pointer-events:auto!important;
 width:clamp(44px,8vw,60px)!important;
 height:clamp(44px,8vw,60px)!important;
 min-width:0!important;
 flex:0 1 auto!important;
 box-shadow:0 0 10px #9d74ff88,0 3px 8px #0009!important;
}
#arena #bpPowerQuickDock .bp-power-quick-symbol{font-size:clamp(19px,4vw,27px)!important}
#arena #bpPowerQuickDock .bp-power-quick-count{font-size:clamp(11px,2.5vw,14px)!important}
#arena.solo #bottom,#arena.versus #bottom{
 margin-top:clamp(34px,4.3dvh,66px)!important;
 align-items:center!important;
}
#arena #bottom #actionStack{
 align-self:center!important;
 justify-content:center!important;
 gap:12px!important;
}
#arena #bottom #actionStack #raiseRow,
#arena #bottom #actionStack #swap{
 position:relative!important;
 left:0!important;
 right:auto!important;
 margin:0!important;
 transform:none!important;
 width:100%!important;
}
/* Compact Solo HUD; remove the excessive vertical padding inherited from
   the original sidebar cards. */
#arena.solo #soloHud{margin-bottom:6px!important;align-items:stretch!important}
#arena.solo #soloHud .hud-card{
 height:64px!important;min-height:0!important;max-height:64px!important;
 padding:4px 6px!important;gap:2px!important;
 overflow:hidden!important;box-sizing:border-box!important;
}
#arena.solo #soloHud .hud-card strong{font-size:clamp(12px,3vw,17px)!important}
#arena.solo #soloHud .hud-card .hud-label{font-size:clamp(9px,2.2vw,12px)!important}
/* Power-ups belong directly below the field, with no negative margin.
   Reserve their own height so no playable bottom-row blocks are covered. */
#arena #bpPowerQuickDock{
 margin:3px auto 0!important;
 min-height:64px!important;
 height:64px!important;
 z-index:5!important;
 transform:none!important;
 align-content:center!important;
 padding:5px 8px!important;
}
#arena.solo #bottom,#arena.versus #bottom{margin-top:clamp(8px,1.4dvh,20px)!important}
#arena #bottom #actionStack{align-items:stretch!important}
#arena #bottom #actionStack #raiseRow,
#arena #bottom #actionStack #swap{width:100%!important;max-width:none!important}
/* Hide the obsolete Solo lightning-bolt menu launcher, not the individual
   lightning power-up tiles on the actual game board. */
#arena.solo #bpPowerMenuTrigger,
#arena.solo #bpPowerMenuButton,
#arena.solo #bpPowerupMenuTrigger{display:none!important}
/* Retired rotating in-game leaderboard must never cover power-ups. */
#bpMini{display:none!important}
#arena #bottom{width:min(94vw,470px)!important;align-items:center!important;justify-content:center!important;gap:16px!important;overflow:visible!important;position:relative!important;top:0!important;margin-inline:auto!important}
#arena #bottom #pad{display:grid!important;box-sizing:border-box!important;width:min(45vw,225px)!important;height:min(42vw,212px)!important;max-width:min(42vw,212px)!important;max-height:min(42vw,212px)!important;min-width:0!important;min-height:0!important;flex:0 0 min(42vw,212px)!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:3px!important;align-self:center!important}
#arena #bottom #pad button{box-sizing:border-box!important;width:100%!important;height:100%!important;min-width:0!important;min-height:0!important;padding:0!important;font-size:clamp(16px,4vw,25px)!important;border-radius:10px!important}
#arena #bottom #actionStack{box-sizing:border-box!important;width:min(34vw,180px)!important;max-width:min(34vw,180px)!important;flex:0 0 min(34vw,180px)!important;align-self:center!important;justify-content:center!important;gap:12px!important}
#arena #bottom #actionStack #raiseRow{box-sizing:border-box!important;width:100%!important;height:clamp(42px,8vw,58px)!important;min-height:0!important;max-height:58px!important;flex:0 0 auto!important}
#arena #bottom #actionStack #swap{box-sizing:border-box!important;width:100%!important;height:clamp(75px,15vw,106px)!important;min-height:0!important;max-height:106px!important;flex:0 0 auto!important}
/* Approved composition: move the entire header and boards down, not just controls.
   Use normal flow so the controls follow the boards without overlap. */
#arena.solo,#arena.versus{padding-top:clamp(20px,3.2dvh,52px)!important;box-sizing:border-box!important}
#arena.solo #top,#arena.versus #top{margin-top:0!important;margin-bottom:clamp(20px,3.2dvh,46px)!important}
#arena.solo #top .arcade-logo,#arena.versus #top .arcade-logo{transform:scale(1.07);transform-origin:center center}
#arena.solo #top #back,#arena.versus #top #back{transform:scale(1.06);transform-origin:left center}
#arena.solo #bottom,#arena.versus #bottom{margin-top:clamp(16px,2.5dvh,36px)!important}
@media(max-height:780px){
 #arena.solo,#arena.versus{padding-top:clamp(8px,1.5dvh,20px)!important}
 #arena.solo #top,#arena.versus #top{margin-bottom:clamp(8px,1.5dvh,20px)!important}
 #arena.solo #bottom,#arena.versus #bottom{margin-top:10px!important}
}
/* The approved mockup has no framed top banner. Keep its controls in place
   while removing the existing full-width border/background panel. */
#arena.solo #top,#arena.versus #top{
 background:transparent!important;
 background-image:none!important;
 border:0!important;
 border-radius:0!important;
 box-shadow:none!important;
 outline:0!important;
 backdrop-filter:none!important;
 -webkit-backdrop-filter:none!important;
}
/* Add the soft edge treatment from the approved rendering without changing
   the D-pad geometry or touch targets. Effects stay outside the buttons. */
#arena #bottom #pad{filter:drop-shadow(0 0 5px rgba(92,148,255,.35))!important}
#arena #bottom #actionStack #swap{filter:drop-shadow(0 0 7px rgba(255,84,238,.42))!important}
/* Scale the intact original directional cross, without replacing its grid placement. */
#arena #bottom #pad{transform:translateX(-11px) scale(1.11)!important;transform-origin:center center!important}
#arena #bottom #actionStack #swap{transform:none!important;transform-origin:center center!important}
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
hud_new='<aside id="soloHud"'
assert s.count(hud_old)==1, f'Expected one Solo HUD markup, found {s.count(hud_old)}'
s=s.replace(hud_old,hud_new,1)
zone_old='</aside><section class="zone" id="humanZone">'
zone_new='</aside><div id="boards"><section class="zone" id="humanZone">'
assert s.count(zone_old)==1, f'Expected one HUD/zone boundary, found {s.count(zone_old)}'
s=s.replace(zone_old,zone_new,1)
p.write_text(s,encoding='utf-8')
print('Patched actual main gameplay CSS')
