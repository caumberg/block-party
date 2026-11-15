from pathlib import Path
import re
p=Path("www/index.html")
s=p.read_text(encoding="utf-8")
marker="function renderIdle(){"
assert s.count(marker)==1, "Idle rendering anchor missing"
js=r"""
// Native Android idle reward notifications. Never run on the web.
const bpIdleNotificationIds=[41001,41002];
const bpIdleNotifyKey='bp-idle-notifications-enabled';
function bpIdlePlugin(){
  if(!window.Capacitor?.isNativePlatform?.())return null;
  return window.Capacitor.Plugins?.LocalNotifications||null;
}
async function bpIdleScheduleNotifications(){
  const plugin=bpIdlePlugin();if(!plugin)return;
  try{
    await plugin.cancel({notifications:bpIdleNotificationIds.map(id=>({id}))});
    if(localStorage.getItem(bpIdleNotifyKey)!=='yes'||!idle?.started_at)return;
    const start=Date.parse(idle.started_at),now=Date.now()+serverOffset;
    if(!Number.isFinite(start))return;
    const notifications=[
      {id:41001,at:start+3600000,title:'Block Party: idle rewards ready',body:'10 idle tokens are ready to claim!'},
      {id:41002,at:start+12600000,title:'Block Party: maximum idle rewards',body:'Your maximum 15 idle tokens are ready to claim!'}
    ].filter(n=>n.at>now+3000).map(n=>({
      id:n.id,title:n.title,body:n.body,
      schedule:{at:new Date(n.at-serverOffset)},
      extra:{blockPartyWallet:true}
    }));
    if(notifications.length)await plugin.schedule({notifications});
  }catch(error){console.warn('Idle notification scheduling failed',error)}
}
async function bpIdleNotificationSetup(){
  const plugin=bpIdlePlugin();if(!plugin)return;
  const overlay=document.getElementById('bpWalletOverlay');
  if(!overlay||document.getElementById('bpIdleNotificationToggle'))return;
  const button=document.createElement('button');
  button.type='button';button.id='bpIdleNotificationToggle';
  button.style.cssText='display:block;margin:10px auto;padding:9px 13px;border-radius:10px;background:#30235c;color:#fff;border:1px solid #aa8bff;font:inherit;cursor:pointer';
  const update=()=>{button.textContent='Idle notifications: '+(localStorage.getItem(bpIdleNotifyKey)==='yes'?'On':'Off')};update();
  (document.getElementById('bpWalletClose')?.parentElement||overlay).appendChild(button);
  button.addEventListener('click',async()=>{
    const enabled=localStorage.getItem(bpIdleNotifyKey)==='yes';
    if(!enabled){
      try{
        let result=await plugin.checkPermissions();
        if(result.display!=='granted')result=await plugin.requestPermissions();
        if(result.display!=='granted'){alert('Enable Block Party notifications in Android Settings to receive idle reward alerts.');return}
      }catch(e){console.warn(e);return}
    }
    localStorage.setItem(bpIdleNotifyKey,enabled?'no':'yes');
    update();await bpIdleScheduleNotifications();
  });
  try{await plugin.addListener('localNotificationActionPerformed',()=>{
    document.getElementById('bpWalletOpen')?.click();
  })}catch(e){console.warn(e)}
  await bpIdleScheduleNotifications();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bpIdleNotificationSetup,{once:true});
else bpIdleNotificationSetup();
"""
s=s.replace(marker,js+"\n"+marker,1)
# Refresh native alarms whenever the server provides a fresh idle cycle.
anchor="serverOffset=Date.parse(result.server_now)-Date.now();renderIdle()"
assert s.count(anchor)==1, "Idle refresh anchor missing"
s=s.replace(anchor,anchor+";void bpIdleScheduleNotifications();",1)
claim="serverOffset=Date.parse(idle.server_now)-Date.now();"
assert s.count(claim)>=1, "Idle claim anchor missing"
s=s.replace(claim,claim+"void bpIdleScheduleNotifications();",1)
p.write_text(s,encoding="utf-8")
print("Android-only idle notification bridge inserted")
