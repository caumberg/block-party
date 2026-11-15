/* Android-only visual adjustments. Never loaded by GitHub Pages. */
(() => {
  const label = el => (el.textContent || '').trim().replace(/\s+/g, ' ').toUpperCase();
  function adjust() {
    const nodes = [...document.querySelectorAll('button, [role="button"], div')];
    for (const el of nodes) {
      const t = label(el);
      if (el.children.length && [...el.children].some(ch => label(ch) === t)) continue;
      if (t === 'SWAP' || t === 'RAISE ROW') {
        const rect = el.getBoundingClientRect();
        if (rect.width < 65 || rect.height < 65 || rect.top < innerHeight * .48) continue;
        const target = t === 'SWAP' ? Math.min(rect.height, rect.width * .88) : Math.min(rect.height, rect.width * .53);
        if (rect.height > target * 1.08) {
          el.style.setProperty('transform-origin', 'center center', 'important');
          el.style.setProperty('transform', 'scaleY(' + (target / rect.height).toFixed(3) + ')', 'important');
        }
      }
    }
    const arrows = [...document.querySelectorAll('button, [role="button"], div, span')]
      .filter(el => el.children.length === 0 && ['▲','▼','◀','▶','△','▽','◁','▷','↑','↓','←','→'].includes(label(el)) && el.getBoundingClientRect().top > innerHeight * .48);
    if (arrows.length >= 4) {
      const four = arrows.slice(0,4);
      let parent = four[0].parentElement;
      while (parent && !four.every(el => parent.contains(el))) parent = parent.parentElement;
      if (parent && parent !== document.body) {
        const rect = parent.getBoundingClientRect();
        if (rect.width > 100 && rect.height > rect.width * 1.06 && rect.height < innerHeight * .55) {
          parent.style.setProperty('transform-origin', 'center center', 'important');
          parent.style.setProperty('transform', 'scaleY(' + (rect.width / rect.height).toFixed(3) + ')', 'important');
        }
      }
    }
  }
  window.addEventListener('load', adjust);
  window.addEventListener('resize', adjust);
  document.addEventListener('click', () => requestAnimationFrame(adjust));
  setTimeout(adjust, 1000);
})();
