from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=p.read_text(encoding='utf-8')
old='#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(205px,28vh,285px)!important}'
new='#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(340px,46vh,460px)!important;flex-shrink:0!important}'
assert s.count(old)==1 or s.count(new)==1, 'Campaign preview height rule not found'
s=s.replace(old,new,1)
old2='@media(max-height:800px){#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(175px,25vh,240px)!important}}'
new2='@media(max-height:800px){#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(300px,43vh,400px)!important}}'
assert s.count(old2)==1 or s.count(new2)==1, 'Compact campaign preview rule not found'
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('Restored campaign gameplay preview height')
