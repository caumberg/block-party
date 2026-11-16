from pathlib import Path
p=Path("www/index.html")
s=p.read_text(encoding="utf-8")
anchor=".bp-day-tile.ready.center{border-color:#55e49d;background:linear-gradient(140deg,#205c55,#2b6a58)}"
assert s.count(anchor)==1, "Daily reward style anchor changed"
css=r"""
/* Claimable daily reward: gold, distinct from completed green tiles.
   Animate an inner glow rather than the carousel's transform, so 3D
   positioning and swipe transitions remain intact. */
.bp-day-tile.ready{
 border:2px solid #ffe88b!important;
 background:linear-gradient(145deg,#fff1a2 0%,#eab94d 32%,#ad681e 75%,#79400f 100%)!important;
 color:#36200a!important;
 box-shadow:inset 0 2px 12px #fff4b6bb,0 0 19px #ffd35b99,0 14px 22px #0008!important;
 overflow:visible!important;
}
.bp-day-tile.ready.center{
 border:3px solid #fff0a0!important;
 background:linear-gradient(145deg,#fff3b3 0%,#f9cf58 34%,#dc9329 74%,#a35a17 100%)!important;
 box-shadow:inset 0 2px 12px #fff7d2dd,0 0 27px #ffc947bb,0 17px 27px #0009!important;
}
.bp-day-tile.ready .bp-day-number,.bp-day-tile.ready .bp-day-state{color:#382006!important;text-shadow:0 1px 1px #fff3b677}
.bp-day-tile.ready .bp-day-amount{color:#3c2105!important;text-shadow:0 1px 1px #fff5b588}
.bp-day-tile.ready .bp-day-icon{animation:bpGiftBounce 1.25s ease-in-out infinite;transform-origin:50% 85%;filter:drop-shadow(0 4px 3px #6a3a1466)}
.bp-day-tile.ready.center::after{content:"";position:absolute;inset:4px;border-radius:11px;pointer-events:none;border:1px solid #fff7c3aa;animation:bpClaimPulse 1.25s ease-in-out infinite}
@keyframes bpGiftBounce{0%,100%{transform:translateY(0) scale(1)}35%{transform:translateY(-12px) scale(1.08)}55%{transform:translateY(0) scale(.96)}72%{transform:translateY(-4px) scale(1.03)}}
@keyframes bpClaimPulse{0%,100%{opacity:.4;box-shadow:inset 0 0 4px #fff8bd55}50%{opacity:1;box-shadow:inset 0 0 15px #fff7c6bb}}
@media(prefers-reduced-motion:reduce){.bp-day-tile.ready .bp-day-icon,.bp-day-tile.ready.center::after{animation:none!important}}
"""
s=s.replace(anchor,anchor+"\n"+css,1)
p.write_text(s,encoding="utf-8")
print("Gold animated claimable daily reward style applied")
