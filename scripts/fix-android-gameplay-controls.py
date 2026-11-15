from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
anchor='</style>\n</style>\n<div id="menu">'
assert s.count(anchor)==1, f'Expected exactly one main stylesheet ending, found {s.count(anchor)}'
css="""
/* Android gameplay controls: injected into the actual main document stylesheet. */
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
#arena #bottom #actionStack #swap{transform:translate(-4px,-8px) scale(1.15)!important;transform-origin:center center!important}
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
p.write_text(s,encoding='utf-8')
print('Patched actual main gameplay CSS')
