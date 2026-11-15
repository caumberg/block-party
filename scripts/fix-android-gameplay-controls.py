from pathlib import Path
p=Path('www/index.html')
s=p.read_text(encoding='utf-8')
anchor='</style>\n</style>\n<div id="menu">'
assert s.count(anchor)==1, f'Expected exactly one main stylesheet ending, found {s.count(anchor)}'
css="""
/* Android controls: size actual pad grid AND its rows, not just the wrapper. */
#arena.solo #bottom,#arena.versus #bottom{
 width:min(96vw,620px)!important;
 display:flex!important;
 align-items:center!important;
 justify-content:center!important;
 gap:clamp(10px,2.2vw,20px)!important;
 position:relative!important;
 top:clamp(50px,7dvh,110px)!important;
 margin:0 auto!important;
 padding:0 8px!important;
 overflow:visible!important;
 box-sizing:border-box!important;
}
#arena.solo #bottom #pad,#arena.versus #bottom #pad{
 --bp-pad-size:min(48vw,240px);
 display:grid!important;
 grid-template-columns:repeat(3,minmax(0,1fr))!important;
 grid-template-rows:repeat(3,minmax(0,1fr))!important;
 gap:3px!important;
 box-sizing:border-box!important;
 width:var(--bp-pad-size)!important;
 height:var(--bp-pad-size)!important;
 min-width:var(--bp-pad-size)!important;
 min-height:var(--bp-pad-size)!important;
 max-width:var(--bp-pad-size)!important;
 max-height:var(--bp-pad-size)!important;
 flex:0 0 var(--bp-pad-size)!important;
 margin:0!important;
 align-self:center!important;
 overflow:visible!important;
}
#arena #bottom #pad button[data-key]{
 box-sizing:border-box!important;
 width:100%!important;
 height:100%!important;
 min-height:0!important;
 min-width:0!important;
 padding:0!important;
 font-size:clamp(19px,5vw,32px)!important;
 border-radius:12px!important;
}
#arena.solo #bottom #actionStack,#arena.versus #bottom #actionStack{
 width:min(34vw,185px)!important;
 max-width:min(34vw,185px)!important;
 flex:0 0 min(34vw,185px)!important;
 display:flex!important;
 flex-direction:column!important;
 align-self:center!important;
 justify-content:center!important;
 gap:12px!important;
 margin:0!important;
}
#arena #bottom #actionStack #raiseRow{
 box-sizing:border-box!important;
 width:100%!important;
 height:clamp(48px,8vw,62px)!important;
 min-height:0!important;
 max-height:62px!important;
 flex:0 0 auto!important;
}
#arena #bottom #actionStack #swap{
 box-sizing:border-box!important;
 width:100%!important;
 height:clamp(86px,16vw,120px)!important;
 min-height:0!important;
 max-height:120px!important;
 flex:0 0 auto!important;
}
"""
s=s.replace(anchor,css+anchor,1)
p.write_text(s,encoding='utf-8')
print('Patched actual main gameplay CSS')
