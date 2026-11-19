
(function(){
 function setup(){
  const menu=document.getElementById('menu');
  const card=menu&&menu.querySelector('.menu-card');
  if(card&&!document.getElementById('bpArcadeClose')){
   const btn=document.createElement('button');
   btn.id='bpArcadeClose';btn.type='button';btn.textContent='×';btn.setAttribute('aria-label','Close Arcade and return to main menu');
   btn.addEventListener('click',function(){
    const back=document.getElementById('bpArcadeBack');
    if(back)back.click();
   });
   card.appendChild(btn);
  }
  const lb=document.querySelector('#bpLeaderboard .bp-lb-top');
  if(lb&&!document.getElementById('bpLbTopClose')){
   const btn=document.createElement('button');
   btn.id='bpLbTopClose';btn.type='button';btn.textContent='×';btn.setAttribute('aria-label','Close leaderboards');
   btn.addEventListener('click',function(){document.getElementById('bpLbClose')?.click();});
   lb.appendChild(btn);
  }
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup,{once:true});
 else setup();
})();
