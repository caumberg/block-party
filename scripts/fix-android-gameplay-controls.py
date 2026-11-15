from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
anchor='</style>\n</style>\n<div id="menu">'
assert s.count(anchor)==1, f'Expected exactly one main stylesheet ending, found {s.count(anchor)}'
css="""
/* Android gameplay controls: injected into the actual main document stylesheet. */
#arena #bottom{width:min(94vw,470px)!important;align-items:center!important;justify-content:center!important;gap:16px!important;overflow:visible!important}
#arena #bottom #pad{display:grid!important;box-sizing:border-box!important;width:min(38vw,190px)!important;height:min(38vw,190px)!important;max-width:min(38vw,190px)!important;max-height:min(38vw,190px)!important;min-width:0!important;min-height:0!important;flex:0 0 min(38vw,190px)!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;grid-template-rows:repeat(3,minmax(0,1fr))!important;gap:3px!important;align-self:center!important}
#arena #bottom #pad button{box-sizing:border-box!important;width:100%!important;height:100%!important;min-width:0!important;min-height:0!important;padding:0!important;font-size:clamp(16px,4vw,25px)!important;border-radius:10px!important}
#arena #bottom #actionStack{box-sizing:border-box!important;width:min(32vw,170px)!important;max-width:min(32vw,170px)!important;flex:0 0 min(32vw,170px)!important;align-self:center!important;justify-content:center!important;gap:12px!important}
#arena #bottom #actionStack #raiseRow{box-sizing:border-box!important;width:100%!important;height:clamp(42px,8vw,58px)!important;min-height:0!important;max-height:58px!important;flex:0 0 auto!important}
#arena #bottom #actionStack #swap{box-sizing:border-box!important;width:100%!important;height:clamp(65px,13vw,92px)!important;min-height:0!important;max-height:92px!important;flex:0 0 auto!important}
"""
s=s.replace(anchor,css+anchor,1)
p.write_text(s,encoding='utf-8')
print('Patched actual main gameplay CSS')
