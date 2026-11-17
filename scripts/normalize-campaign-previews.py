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
p.write_text(s,encoding='utf-8')
print('Normalized versus preview canvas geometry')
