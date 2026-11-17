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
# Consistent, proportional preview viewport for every campaign mode.
# The frame shrinks to its content instead of hiding the Play action below it.
fit_css='''</style><style id="bp-campaign-fit-v3">
#bpCampaignOverlay .bp-campaign-card{height:auto!important;min-height:0!important;max-height:calc(100dvh - 16px)!important}
#bpCampaignOverlay .bp-campaign-workspace{height:min(64dvh,690px)!important;flex:0 1 auto!important;min-height:0!important}
#bpCampaignOverlay #bpCampaignDetail{gap:4px!important;justify-content:flex-start!important}
#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(220px,31dvh,320px)!important;min-height:0!important;flex-shrink:0!important}
#bpCampaignOverlay #bpCampaignDetail .bp-cinematic-body{gap:3px!important;flex:0 0 auto!important}
#bpCampaignOverlay #bpCampaignDetail .bp-cinematic-objectives{gap:2px!important;flex-shrink:0!important}
#bpCampaignOverlay #bpCampaignDetail>button{margin-top:4px!important;flex-shrink:0!important;position:relative!important;bottom:auto!important}
@media(max-height:800px){#bpCampaignOverlay .bp-campaign-workspace{height:min(63dvh,570px)!important}#bpCampaignOverlay #bpCampaignDetail .bp-approved-preview{height:clamp(205px,29dvh,290px)!important;min-height:0!important}}
</style><style id="bp-campaign-quick-actions-css">'''
assert s.count(anchor)==1
assert s.count('</style><style id="bp-campaign-quick-actions-css">')==1
s=s.replace('</style><style id="bp-campaign-quick-actions-css">',fit_css,1)
p.write_text(s,encoding='utf-8')
print('Campaign content-sized layout installed')
