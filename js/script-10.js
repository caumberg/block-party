
(function(){
 function init(){
  const menu=document.getElementById('menu'),campaign=document.getElementById('bpCampaignOpen');
  const stage=menu?.querySelector('.menu-stage'),start=document.getElementById('start');
  if(!menu||!campaign||!stage||!start||document.getElementById('bpArcadeScreen'))return;
  const launch=start.closest('.menu-launch');
  if(!launch)return;
  const home=document.createElement('div');home.id='bpArcadeHome';
  const arcade=document.createElement('button');arcade.id='bpArcadeOpen';arcade.type='button';
  arcade.innerHTML='<span class="bp-arcade-title">ARCADE <span>PLAY ›</span></span><span class="bp-arcade-sub">Classic game modes outside Campaign. Choose Solo or Versus and set your own challenge.</span><span class="bp-arcade-tags">SOLO · VERSUS · LINE CLEAR · TIMED · UNLIMITED</span>';
  campaign.before(home);home.append(campaign,arcade);
  const screen=document.createElement('div');screen.id='bpArcadeScreen';screen.hidden=true;
  const back=document.createElement('button');back.id='bpArcadeBack';back.type='button';back.textContent='‹ Main Menu';
  const title=document.createElement('div');title.className='bp-arcade-screen-title';title.textContent='🎮 ARCADE';
  const playLaunch=document.createElement('div');playLaunch.className='menu-launch';
  screen.append(back,title,stage,playLaunch);
  playLaunch.append(start);
  const footnote=launch.querySelector('.launch-footnote');
  if(footnote)playLaunch.append(footnote);
  home.after(screen);
  function showArcade(on){
   home.hidden=on;screen.hidden=!on;
   if(on)screen.scrollIntoView({block:'start',behavior:'instant'});
   else menu.scrollIntoView({block:'start',behavior:'instant'});
  }
  arcade.addEventListener('click',()=>showArcade(true));
  back.addEventListener('click',()=>showArcade(false));
  menu.classList.add('bp-menu-ready');
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
 else init();
})();
