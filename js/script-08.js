
(()=>{'use strict';
const el=document.getElementById('bpCampaignTicketCount');
let busy=false;
async function refresh(){
 if(busy||typeof window.bpCampaignRpc!=='function')return;
 busy=true;
 try{
  const data=await window.bpCampaignRpc('bp_store_get');
  const count=Number(data?.tickets);
  if(Number.isFinite(count)&&count>=0)el.textContent=count.toLocaleString();
  else el.textContent='—';
 }catch(e){console.warn('Ticket balance unavailable:',e);el.textContent='—'}
 finally{busy=false}
}
window.bpCampaignRefreshTickets=refresh;
const campaign=document.getElementById('bpCampaignOverlay');
if(campaign){
 const observer=new MutationObserver(()=>{if(!campaign.hidden)refresh()});
 observer.observe(campaign,{attributes:true,attributeFilter:['hidden']});
}
const store=document.getElementById('bpStoreOverlay');
if(store){
 const observer=new MutationObserver(()=>{if(store.hidden&&!campaign.hidden)refresh()});
 observer.observe(store,{attributes:true,attributeFilter:['hidden']});
}
document.getElementById('bpCampaignStoreOpen')?.addEventListener('click',()=>setTimeout(refresh,400));
})();
