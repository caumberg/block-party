
(function(){
 const $=id=>document.getElementById(id),modal=$('bpDeveloperOverlay');
 $('bpDeveloperModeOpen')?.addEventListener('click',async()=>{
  modal.hidden=false;$('bpDeveloperUserId').textContent='Loading…';
  try{$('bpDeveloperUserId').textContent=await window.bpGetCurrentUserId()}
  catch(e){$('bpDeveloperUserId').textContent='Unable to identify account: '+e.message}
 });
 $('bpDeveloperEnter')?.addEventListener('click',async()=>{
  const status=$('bpDeveloperStatus');status.textContent='Checking Supabase developer authorization…';
  try{
   if(!await window.bpDevVerify())throw Error('This account is not authorized.');
   window.bpDevAuthorized=true;window.bpDevActive=true;
   $('bpDeveloperEnter').hidden=true;$('bpDeveloperExit').hidden=false;
   status.textContent='Developer Mode ACTIVE. Non-campaign games now have free entry and sandbox power-up inventory. Redesigned effects are still under development.';
   document.body.classList.add('bp-developer-active');
   document.getElementById('bpDeveloperModeOpen').textContent='Developer Mode ACTIVE';
  }catch(e){status.textContent='Access denied: '+e.message}
 });
 $('bpDeveloperExit')?.addEventListener('click',()=>{
  window.bpDevActive=false;window.bpDevAuthorized=false;
  $('bpDeveloperEnter').hidden=false;$('bpDeveloperExit').hidden=true;
  document.body.classList.remove('bp-developer-active');
  document.getElementById('bpDeveloperModeOpen').textContent='Enter Developer Mode';
  $('bpDeveloperStatus').textContent='Developer Mode disabled. Reload the game before playing normally.';
 });
 $('bpDeveloperClose')?.addEventListener('click',()=>modal.hidden=true);
 modal?.addEventListener('click',e=>{if(e.target===modal)modal.hidden=true});
 $('bpDeveloperCopyId')?.addEventListener('click',async()=>{
  const id=$('bpDeveloperUserId').textContent;
  if(!/^[0-9a-f]{8}-[0-9a-f-]{27,}$/i.test(id))return;
  try{await navigator.clipboard.writeText(id);$('bpDeveloperStatus').textContent='User ID copied. Use this ID to authorize your developer account in Supabase.'}
  catch(_){$('bpDeveloperStatus').textContent='Press and hold the user ID to select and copy it.'}
 });
})();
