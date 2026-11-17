from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'www/index.html')
s=p.read_text(encoding='utf-8')
needle='   const previewHtml=new TextDecoder().decode(bytes);'
assert s.count(needle)==1, 'Campaign preview decoder anchor changed'
replacement="""   let previewHtml=new TextDecoder().decode(bytes);
   // Fit both versus boards in a tighter, proportional native canvas.
   // This changes the actual drawing coordinates, not a clipped CSS zoom.
   if(approvedKey.startsWith('versus')){
    if(approvedKey==='versus'){
     previewHtml=previewHtml.replace('const W=660,H=466,C=6,R=12,S=37,X=[52,386]', 'const W=510,H=466,C=6,R=12,S=37,X=[16,272]');
     previewHtml=previewHtml.replace('width:660px','width:510px');
     previewHtml=previewHtml.replace('width=\"660\"','width=\"510\"');
    }else{
     previewHtml=previewHtml.replace('const W=660,H=480,C=6,R=12,S=35,', 'const W=510,H=480,C=6,R=12,S=35,');
     previewHtml=previewHtml.replace('LEFT=43,RIGHT=393,Y=16','LEFT=18,RIGHT=282,Y=16');
     previewHtml=previewHtml.replace('width=\"660\"','width=\"510\"');
    }
   }"""
s=s.replace(needle,replacement,1)
needle2='.wrap{width:100%!important;height:auto!important;max-height:calc(100% - 30px)!important;aspect-ratio:1.48!important;margin:auto!important;flex:none!important}'
assert s.count(needle2)==1, 'Versus preview wrap CSS changed'
s=s.replace(needle2,'.wrap{width:auto!important;height:auto!important;max-height:calc(100% - 30px)!important;max-width:100%!important;aspect-ratio:510/480!important;margin:0 auto!important;flex:none!important}',1)
# Keep the versus boards immediately beneath their labels, rather than
# centering the whole animation and introducing a blank vertical band.
top_gap='justify-content:center!important;padding:2px!important;margin:0!important;border:0!important;background:transparent!important}'
assert s.count(top_gap)==1, 'Versus arena CSS anchor changed'
s=s.replace(top_gap,top_gap.replace('justify-content:center','justify-content:flex-start'),1)
# The standalone Replay footer is not part of Campaign and was peeking
# out from beneath the Line Clear preview. Hide it for every versus mode.
needle3='.eyebrow,.title,.status,.bottom,.note{display:none!important}'
assert s.count(needle3)==1, 'Versus embedded CSS selector changed'
s=s.replace(needle3,'.eyebrow,.title,.status,.bottom,.footer,.note{display:none!important}',1)

# Timed mode: make the clock a small, centered overlay on the actual boards.
# It is absolutely positioned so it consumes no extra vertical layout space.
clock_css='''.shell{position:relative!important}
html body .shell .clock{display:flex!important;position:absolute!important;top:20%!important;left:50%!important;transform:translateX(-50%)!important;z-index:5!important;pointer-events:none!important;margin:0!important;padding:2px 5px!important;min-height:0!important;width:max-content!important;max-width:100%!important;align-items:center!important;justify-content:center!important;flex-direction:column!important;font-size:16px!important;line-height:1.05!important;background:#101a39b8!important;border-radius:8px!important}
html body .shell .clock small{font-size:8px!important;letter-spacing:0!important;white-space:nowrap!important}'''
timed_anchor='   }"""'
assert s.count(timed_anchor)==1, 'Preview mode replacement anchor changed'
s=s.replace(timed_anchor,'''   }
   if(approvedKey==='versus-timed'){
    previewHtml=previewHtml.replace('</head>','<style>'+''' + repr(clock_css) + '''+'</style></head>');
   }"""''',1)
p.write_text(s,encoding='utf-8')
print('Normalized versus preview canvas geometry')
