from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'www/index.html')
s=p.read_text(encoding='utf-8')
anchor='</style><style id="bp-campaign-quick-actions-css">'
assert s.count(anchor)==1, f'Campaign CSS insertion point changed: {s.count(anchor)}'
css='''</style><style id="bp-campaign-compact-v2">
/* Content-sized campaign dialog. Keep the original iframe animation viewport. */
#bpCampaignOverlay .bp-campaign-card{height:auto!important;min-height:0!important;max-height:calc(100dvh - 16px)!important}
#bpCampaignOverlay .bp-campaign-workspace{flex:0 1 auto!important;height:min(72dvh,830px)!important;min-height:0!important}
#bpCampaignOverlay .bp-campaign-right{min-height:0!important}
#bpCampaignOverlay .bp-campaign-right #bpCampaignDetail{flex:1 1 auto!important;min-height:0!important;justify-content:flex-start!important;overflow-y:auto!important}
#bpCampaignOverlay #bpCampaignDetail>button{margin-top:7px!important;position:relative!important;bottom:auto!important;flex-shrink:0!important}
#bpCampaignOverlay #bpCampaignDetail .bp-cinematic-objectives{flex-shrink:0!important;gap:5px!important}
#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(340px,46dvh,460px)!important;min-height:340px!important;flex-shrink:0!important}
@media(max-height:800px){#bpCampaignOverlay .bp-campaign-workspace{height:min(72dvh,650px)!important}#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(300px,43dvh,400px)!important;min-height:300px!important}}
</style><style id="bp-campaign-quick-actions-css">'''
s=s.replace(anchor,css,1)
p.write_text(s,encoding='utf-8')
print('Campaign content-sized layout installed')
