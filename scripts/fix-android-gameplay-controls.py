from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
anchor='</style>\n</style>\n<div id="menu">'
assert s.count(anchor)==1, f'Expected exactly one main stylesheet ending, found {s.count(anchor)}'
css="""
/* Android gameplay controls: injected into the actual main document stylesheet. */
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
/* Scale the intact original directional cross, without replacing its grid placement. */
#arena #bottom #pad{transform:scale(1.04)!important;transform-origin:center center!important}
#arena #bottom #actionStack #swap{transform:scale(1.08)!important;transform-origin:center center!important}
"""
s=s.replace(anchor,css+anchor,1)
p.write_text(s,encoding='utf-8')
print('Patched actual main gameplay CSS')
