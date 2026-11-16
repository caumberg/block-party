from pathlib import Path
p=Path("www/index.html")
s=p.read_text(encoding="utf-8")
anchor="function renderIdle(){"
assert s.count(anchor)==1
js=r"""
// Android daily reward reminder, independent of idle reward notifications.
// Daily wallet eligibility resets at UTC midnight, matching bpRenderDaily().
const bpDailyNotifyKey='bp-daily-notifications-enabled';
const bpDailyNotificationId=41003;
async function bpDailyScheduleNotification(){
 const plugin=bpIdlePlugin();if(!plugin)return;
 try{
  if(localStorage.getItem(bpDailyNotifyKey)==='no'){
   await plugin.cancel({notifications:[{id:bpDailyNotificationId}]});return;
  }
  if(!wallet)return; // Preserve an existing native alarm while auth is restoring.
  const permission=await plugin.checkPermissions();
  if(permission.display!=='granted')return;
  await plugin.cancel({notifications:[{id:bpDailyNotificationId}]});
  if(!wallet.claimed_today)return; // Already eligible: don't send a stale reminder.
  const serverNow=Date.now()+serverOffset;
  const d=new Date(serverNow);
  const nextUtc=Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate()+1);
  const at=new Date(nextUtc-serverOffset);
  if(at.getTime()<=Date.now()+3000)return;
  await plugin.schedule({notifications:[{
   id:bpDailyNotificationId,
   title:'Block Party: daily reward ready!',
   body:'Your next daily reward is available. Claim it to keep your streak going!',
   schedule:{at},extra:{blockPartyWallet:true,blockPartyDailyReward:true}
  }]});
 }catch(error){console.warn('Daily reward notification scheduling failed',error)}
}
function bpDailyNotificationSettings(){
 const plugin=bpIdlePlugin();if(!plugin)return;
 const section=document.getElementById('bpIdleNotificationToggle')?.parentElement;
 if(!section||document.getElementById('bpDailyNotificationToggle'))return;
 const label=document.createElement('strong');
 label.textContent='Daily reward reminder';
 label.style.cssText='display:block;margin-top:22px';
 const description=document.createElement('p');
 description.textContent='Notify me when my next daily reward becomes available (midnight UTC).';
 description.style.cssText='font-size:13px;color:#cbd6f1;line-height:1.5';
 const button=document.createElement('button');
 button.id='bpDailyNotificationToggle';button.type='button';
 button.style.cssText='display:block;margin:10px 0;padding:9px 13px;border-radius:10px;background:#30235c;color:#fff;border:1px solid #aa8bff;font:inherit;cursor:pointer';
 const status=document.createElement('p');
 status.id='bpDailyNotificationStatus';
 status.style.cssText='font-size:12px;line-height:1.5;color:#cbd6f1;overflow-wrap:anywhere;margin:8px 0';
 const update=()=>{button.textContent='Daily reward reminders: '+(localStorage.getItem(bpDailyNotifyKey)==='no'?'Off':'On')};
 const refresh=async()=>{
  await bpDailyScheduleNotification();
  const pending=await plugin.getPending();
  const alarm=(pending.notifications||[]).find(n=>n.id===bpDailyNotificationId);
  status.textContent=alarm?.schedule?.at?'Next daily reminder: '+new Date(alarm.schedule.at).toLocaleString():(wallet?.claimed_today?'No reminder scheduled (check Android notification permission).':'Next daily reward is already available or wallet has not loaded.');
 };
 section.append(label,description,button,status);
 update();
 button.addEventListener('click',async()=>{
  const enabling=localStorage.getItem(bpDailyNotifyKey)==='no';
  if(enabling){
   let permission=await plugin.checkPermissions();
   if(permission.display!=='granted')permission=await plugin.requestPermissions();
   if(permission.display!=='granted'){
    status.textContent='Allow Block Party notifications in Android Settings first.';return;
   }
  }
  localStorage.setItem(bpDailyNotifyKey,enabling?'yes':'no');
  update();await refresh();
 });
 document.getElementById('bpSettingsOpen')?.addEventListener('click',()=>{void refresh()});
 void refresh();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(bpDailyNotificationSettings,0),{once:true});
else setTimeout(bpDailyNotificationSettings,0);
"""
s=s.replace(anchor,js+"\n"+anchor,1)
# Wallet refresh after Supabase RPC, and after daily claim, are the sources of truth.
load_anchor="wallet=await rpc('bp_wallet_get');render();status('');await refreshIdle()"
assert s.count(load_anchor)==1
s=s.replace(load_anchor,load_anchor+";void bpDailyScheduleNotification()",1)
claim_anchor="finally{busy=false;render()}\n});\nel('bpIdleClaim')"
assert s.count(claim_anchor)==1
s=s.replace(claim_anchor,"finally{busy=false;render();void bpDailyScheduleNotification()}\n});\nel('bpIdleClaim')",1)
p.write_text(s,encoding='utf-8')
print('Android daily reward reminders inserted')
