from pathlib import Path
import base64
import re
import sys

p = Path(sys.argv[1] if len(sys.argv)>1 else 'www/index.html')
source = p.read_text(encoding='utf-8')
pattern = r'("versus-timed":")([A-Za-z0-9+/=]+)(")'
matches = list(re.finditer(pattern, source))
assert len(matches) == 1, f'Expected one embedded versus-timed preview, found {len(matches)}'
match = matches[0]
html = base64.b64decode(match.group(2)).decode('utf-8')
old = '<div class="clock" id="clock"><small>TIME REMAINING</small>00:05</div>'
wrap = '<div class="wrap">'
assert html.count(old) == 1, 'Timed preview countdown markup changed'
assert html.count(wrap) == 1, 'Timed preview canvas wrapper changed'
html = html.replace(old, '', 1)
html = html.replace(wrap, wrap + old, 1)
style = """<style id="bp-timed-animation-rebuilt">
/* Countdown is a child of the animated board canvas wrapper, not a layout row. */
.wrap{position:relative!important}
.wrap>.clock{position:absolute!important;top:10%!important;left:50%!important;transform:translateX(-50%)!important;z-index:10!important;margin:0!important;padding:4px 7px!important;width:max-content!important;max-width:34%!important;min-height:0!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:1px!important;border:1px solid #6888c9!important;border-radius:9px!important;background:#101a39e8!important;box-shadow:0 0 12px #5f8fff55!important;font-size:16px!important;line-height:1.1!important;white-space:nowrap!important;pointer-events:none!important}
.wrap>.clock small{font-size:7px!important;letter-spacing:0!important;display:block!important}
</style>"""
assert html.count('</head>') == 1
html = html.replace('</head>', style + '</head>', 1)
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
source = source[:match.start(2)] + encoded + source[match.end(2):]
p.write_text(source, encoding='utf-8')
print('Rebuilt embedded versus-timed animation: countdown lives inside canvas wrapper')
