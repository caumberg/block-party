
// Fetch the ticket count independently of the embedded store iframe.
// This runs only when the wallet opens, never during game startup.
(function(){
 let pending=null;
 let requestGeneration=0;
 async function refreshTicketTab(){
  const target=document.getElementById('bpWalletTabTicketCount');
  if(!target || typeof window.bpCampaignRpc!=='function')return;
  if(pending)return pending;
  const generation=++requestGeneration;
  pending=(async function(){
   try{
    const result=await window.bpCampaignRpc('bp_store_get');
    const tickets=Number(result?.tickets);
    if(Number.isFinite(tickets)&&tickets>=0&&generation===requestGeneration){
     target.textContent=tickets.toLocaleString();
    }
   }catch(err){
    console.warn('Unable to refresh ticket tab balance:',err);
    // Keep any previously loaded amount instead of resetting to a spinner.
    if(target.textContent.trim()==='…')target.textContent='—';
   }
  })();
  try{await pending}finally{pending=null}
 }
 window.bpRefreshTicketTabBalance=refreshTicketTab;
 const open=document.getElementById('bpWalletOpen');
 if(open)open.addEventListener('click',refreshTicketTab);
 // Also refresh after the daily claim (which can award milestone tickets).
 const daily=document.getElementById('bpDailyClaim');
 if(daily)daily.addEventListener('click',()=>{
  // The daily claim handler awaits Supabase before emitting its completion.
  // A short deferred read is not reliable; instead refresh after wallet reload.
 },{passive:true});
 window.addEventListener('bp-wallet-initialized',()=>{
  const overlay=document.getElementById('bpWalletOverlay');
  if(overlay&&!overlay.hidden)refreshTicketTab();
 });
})();
