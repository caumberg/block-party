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
    if(localStorage.getItem(bpIdleNotifyKey)!=='yes'){
      await plugin.cancel({notifications:bpIdleNotificationIds.map(id=>({id}))});return;
    }
    if(!idle?.started_at){
      // The first startup check can precede Supabase session restoration.
      // Do not cancel an already scheduled Android alarm on that failure.
      return;
    }
    const permission=await plugin.checkPermissions();
    if(permission.display!=='granted')return;
    await plugin.cancel({notifications:bpIdleNotificationIds.map(id=>({id}))});
    const start=Date.parse(idle.started_at),now=Date.now()+serverOffset;
    if(!Number.isFinite(start))return;
    const notifications=[
      {id:41001,at:start+3600000,title:'Block Party: idle rewards ready',body:'10 idle tokens are ready to claim!'},
      {id:41002,at:start+12600000,title:'Block Party: maximum idle rewards',body:'Your maximum 15 idle tokens are ready to claim!'}
    ].filter(n=>n.at>now+3000).map(n=>({
      id:n.id,title:n.title,body:n.body,
      schedule:{at:new Date(n.at)},
      extra:{blockPartyWallet:true}
    }));
    if(notifications.length)await plugin.schedule({notifications});
  }catch(error){console.warn('Idle notification scheduling failed',error)}
}
async function bpIdleNotificationSetup(){
  const plugin=bpIdlePlugin();if(!plugin)return;
  const account=document.getElementById('bpAccountOpen');
  if(!account||document.getElementById('bpSettingsOpen'))return;
  const links=document.createElement('div');
  links.id='bpAccountSettingsLinks';
  links.style.cssText='display:flex;align-items:center;justify-content:center;gap:9px;margin:13px auto 5px';
  account.parentNode.insertBefore(links,account);
  links.appendChild(account);
  account.style.cssText='display:inline-block!important;margin:0!important;border:0!important;background:none!important;padding:5px!important;color:#c9b8ff!important;font-weight:750!important;cursor:pointer';
  const separator=document.createElement('span');
  separator.textContent='|';separator.style.color='#8d88ba';links.appendChild(separator);
  const settingsLink=document.createElement('button');
  settingsLink.type='button';settingsLink.id='bpSettingsOpen';settingsLink.textContent='Settings';
  settingsLink.style.cssText=account.style.cssText+';text-decoration:underline!important;text-underline-offset:3px!important;box-shadow:none!important;outline:none!important';
  links.appendChild(settingsLink);
  account.style.textDecoration='underline';
  const modal=document.createElement('div');
  modal.id='bpSettingsOverlay';modal.hidden=true;modal.setAttribute('role','dialog');modal.setAttribute('aria-modal','true');modal.setAttribute('aria-label','Settings');
  modal.style.cssText='position:fixed;inset:0;z-index:13000;background:#050917e8;display:none;align-items:center;justify-content:center;padding:18px';
  const panel=document.createElement('section');
  panel.style.cssText='box-sizing:border-box;width:min(94vw,450px);border:1px solid #ad8cf7;border-radius:20px;background:linear-gradient(155deg,#26345d,#131b37);padding:22px;color:white;box-shadow:0 0 32px #8c5bf655';
  const header=document.createElement('div');
  header.style.cssText='display:flex;justify-content:space-between;align-items:center';
  const heading=document.createElement('h2');heading.textContent='Settings';heading.style.margin='0';
  const close=document.createElement('button');close.type='button';close.textContent='✕';close.setAttribute('aria-label','Close settings');
  close.style.cssText='background:#4d3c96;color:white;border:1px solid #a99aea;border-radius:10px;padding:8px 12px;cursor:pointer';
  header.append(heading,close);panel.appendChild(header);
  const section=document.createElement('div');section.style.marginTop='20px';
  const label=document.createElement('strong');label.textContent='Notifications';section.appendChild(label);
  const info=document.createElement('p');info.textContent='Get an Android notification when idle tokens are available after 1 hour and when rewards reach their maximum after 3½ hours.';
  info.style.cssText='font-size:13px;color:#cbd6f1;line-height:1.5';section.appendChild(info);
  panel.appendChild(section);modal.appendChild(panel);document.body.appendChild(modal);
  const dismiss=()=>{modal.hidden=true;modal.style.display='none'};
  settingsLink.addEventListener('click',()=>{modal.hidden=false;modal.style.display='flex'});
  close.addEventListener('click',dismiss);
  modal.addEventListener('click',e=>{if(e.target===modal)dismiss()});
  modal.hidden=true;
  const button=document.createElement('button');
  button.type='button';button.id='bpIdleNotificationToggle';
  button.style.cssText='display:block;margin:10px 0;padding:9px 13px;border-radius:10px;background:#30235c;color:#fff;border:1px solid #aa8bff;font:inherit;cursor:pointer';
  section.appendChild(button);
  // Real Android notification diagnostic, independent of the idle-reward server.
  const testButton=document.createElement('button');
  testButton.type='button';testButton.id='bpTestNotification';
  testButton.textContent='Send test notification (10 seconds)';
  testButton.style.cssText='display:block;margin:12px 0 6px;padding:10px 13px;border-radius:10px;background:#263c78;color:white;border:1px solid #70b9ff;font:inherit;cursor:pointer';
  section.appendChild(testButton);
  const testStatus=document.createElement('p');
  testStatus.id='bpTestNotificationStatus';
  testStatus.style.cssText='font-size:12px;line-height:1.45;color:#cbd6f1;overflow-wrap:anywhere;margin:6px 0';
  section.appendChild(testStatus);
  testButton.addEventListener('click',async()=>{
    testButton.disabled=true;
    try{
      let permission=await plugin.checkPermissions();
      if(permission.display!=='granted')permission=await plugin.requestPermissions();
      if(permission.display!=='granted'){
        testStatus.textContent='Android notification permission is not granted. Enable notifications for Block Party in Android Settings.';
        return;
      }
      const id=41999;
      await plugin.cancel({notifications:[{id}]});
      const when=new Date(Date.now()+10000);
      await plugin.schedule({notifications:[{
        id,title:'Block Party test notification',
        body:'Android notifications are working. This is a test, not an idle reward.',
        schedule:{at:when},extra:{blockPartyNotificationTest:true}
      }]});
      const pending=await plugin.getPending();
      const found=(pending.notifications||[]).some(n=>n.id===id);
      testStatus.textContent=found
        ?'Scheduled with Android for 10 seconds from now. Leave the app or lock your phone to test delivery.'
        :'Schedule call succeeded, but Android did not report the test as pending. Check notification permissions and battery restrictions.';
    }catch(error){
      console.warn('Android notification test failed',error);
      testStatus.textContent='Notification test failed: '+String(error?.message||error);
    }finally{testButton.disabled=false}
  });
  const update=()=>{button.textContent='Idle notifications: '+(localStorage.getItem(bpIdleNotifyKey)==='yes'?'On':'Off')};update();
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
    update();
    if(!enabled&&typeof refreshIdle==='function')await refreshIdle();
    else await bpIdleScheduleNotifications();
  });
  try{await plugin.addListener('localNotificationActionPerformed',()=>{
    document.getElementById('bpWalletOpen')?.click();
  })}catch(e){console.warn(e)}
  // Auth restoration is asynchronous. An immediate refresh on DOMContentLoaded
  // often happens before the Supabase session exists, so retry after startup.
  // Stop after the server returns a usable idle cycle.
  let attempts=0;
  const refreshWhenReady=async()=>{
    if(localStorage.getItem(bpIdleNotifyKey)!=='yes')return;
    if(typeof refreshIdle==='function'){
      try{await refreshIdle()}catch(error){console.warn('Idle notification refresh retry',error)}
    }
    if(idle?.started_at)await bpIdleScheduleNotifications();
  };
  await refreshWhenReady();
  const retry=setInterval(async()=>{
    attempts++;
    if(idle?.started_at||attempts>=30){clearInterval(retry);return}
    await refreshWhenReady();
  },4000);
  document.addEventListener('visibilitychange',()=>{
    if(!document.hidden)void refreshWhenReady();
  });
  // Show the real Android alarm queue, not an assumed success message.
  const scheduleStatus=document.createElement('p');
  scheduleStatus.id='bpIdleScheduleStatus';
  scheduleStatus.style.cssText='font-size:12px;line-height:1.5;color:#cbd6f1;overflow-wrap:anywhere;margin:10px 0';
  section.insertBefore(scheduleStatus,testButton);
  async function showScheduleStatus(){
    try{
      const pending=await plugin.getPending();
      const alarms=(pending.notifications||[]).filter(n=>bpIdleNotificationIds.includes(n.id));
      const first=alarms.find(n=>n.id===41001);
      const max=alarms.find(n=>n.id===41002);
      const fmt=n=>n?.schedule?.at?new Date(n.schedule.at).toLocaleString():'Not scheduled';
      scheduleStatus.textContent='1-hour alert: '+fmt(first)+' | 3½-hour alert: '+fmt(max);
      if(!alarms.length)scheduleStatus.textContent+=' (No automatic alarms pending)';
    }catch(error){scheduleStatus.textContent='Cannot read scheduled alerts: '+String(error?.message||error)}
  }
  settingsLink.addEventListener('click',async()=>{await refreshWhenReady();await showScheduleStatus()});
  button.addEventListener('click',()=>{setTimeout(()=>void showScheduleStatus(),700)});
  await showScheduleStatus();
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
