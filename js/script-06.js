(()=>{
 const by=id=>document.getElementById(id),wallet=by('bpWalletOverlay'),pane=by('bpWalletTokensPane'),storePane=by('bpWalletStorePane'),mount=by('bpWalletStoreMount'),overlay=by('bpStoreOverlay'),frame=by('bpStoreFrame');
 const tokens=by('bpWalletTabTokens'),store=by('bpWalletTabStore');
 const originalClose=window.bpCloseTicketStore;
 function restore(){if(frame.parentNode===mount)overlay.appendChild(frame)}
 function switchTo(which){const isStore=which==='store';tokens.setAttribute('aria-selected',String(!isStore));store.setAttribute('aria-selected',String(isStore));pane.hidden=isStore;storePane.hidden=!isStore;
  if(isStore){window.bpOpenTicketStore?.();mount.appendChild(frame);overlay.hidden=true;window.bpRefreshTicketStore?.()}
  else restore();
 }
 tokens.addEventListener('click',()=>switchTo('tokens'));
 store.addEventListener('click',()=>switchTo('store'));
 window.bpCloseTicketStore=()=>{if(frame.parentNode===mount){switchTo('tokens')}else originalClose?.()};
 by('bpWalletClose').addEventListener('click',()=>{restore();switchTo('tokens')});
 window.addEventListener('bp-wallet-initialized',()=>{});
 const originalOpen=window.bpOpenTicketStore;
 window.bpOpenTicketStore=function(){if(frame.parentNode===mount)restore();originalOpen?.()};
 window.bpOpenRewardsStoreTab=function(tab){
  // Use the existing unified Rewards & Store popup from Campaign.
  if(wallet.hidden)by('bpWalletOpen').click();
  switchTo(tab==='store'?'store':'tokens');
 };
})();