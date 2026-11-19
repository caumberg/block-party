
window.addEventListener('message',function(e){
 const frame=document.getElementById('bpStoreFrame');
 if(!frame||e.source!==frame.contentWindow||e.data?.type!=='bp-store-balances')return;
 const value=Number(e.data.tickets);
 if(Number.isFinite(value)){const target=document.getElementById('bpWalletTabTicketCount');if(target)target.textContent=value.toLocaleString();}
});
