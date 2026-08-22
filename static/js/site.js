(function(){
  const toast = (message) => {
    const old = document.querySelector('.gt-toast'); if (old) old.remove();
    const el = document.createElement('div'); el.className='gt-toast'; el.textContent=message;
    document.body.appendChild(el);
    setTimeout(()=>el.remove(), 2200);
  };
  window.demoSubmit = function(event, message){
    event.preventDefault();
    toast(message || 'Saved');
    setTimeout(()=>{ window.location.href='/dashboard/'; }, 450);
    return false;
  };
  document.querySelectorAll('[data-toast]').forEach(btn=>btn.addEventListener('click',()=>toast(btn.dataset.toast)));
  document.querySelectorAll('[data-copy]').forEach(btn=>btn.addEventListener('click', async()=>{
    const value=btn.dataset.copy; try{await navigator.clipboard.writeText(value);toast('Link copied');}catch(e){toast('Share link ready to copy');}
  }));
  document.querySelectorAll('[data-add]').forEach(btn=>btn.addEventListener('click',()=>{
    btn.textContent='Added'; btn.classList.remove('btn-soft'); btn.classList.add('btn-primary'); toast(btn.dataset.add+' added to trip');
  }));
  const sidebar=document.getElementById('sidebar'); const toggle=document.querySelector('[data-sidebar-toggle]');
  if(toggle && sidebar) toggle.addEventListener('click',()=>sidebar.classList.toggle('is-open'));

  const setupFilters=(selector, itemSelector, filterAttr, searchSelector, searchAttr)=>{
    const buttons=[...document.querySelectorAll(selector)]; const items=[...document.querySelectorAll(itemSelector)]; const search=document.querySelector(searchSelector); let current='all';
    const apply=()=>{ const term=(search?.value||'').toLowerCase().trim(); items.forEach(item=>{const okFilter=current==='all'||item.getAttribute(filterAttr)===current; const okSearch=!term||(item.getAttribute(searchAttr)||'').toLowerCase().includes(term); item.style.display=(okFilter&&okSearch)?'':'none';}); };
    buttons.forEach(b=>b.addEventListener('click',()=>{buttons.forEach(x=>x.classList.remove('active'));b.classList.add('active');current=b.dataset[selector.includes('trip')?'tripFilter':selector.includes('discover')?'discoverFilter':'activityFilter'];apply();}));
    search?.addEventListener('input',apply); apply();
  };
  setupFilters('[data-trip-filter]','.trip-item','data-status','[data-trip-search]','data-search');
  setupFilters('[data-discover-filter]','.discover-item','data-region','[data-discover-search]','data-search');
  setupFilters('[data-activity-filter]','.activity-item','data-type','[data-activity-search]','data-search');

  const sortList=document.querySelector('[data-sort-list]');
  if(sortList){ let drag=null; sortList.querySelectorAll('[draggable="true"]').forEach(el=>{el.addEventListener('dragstart',()=>drag=el);el.addEventListener('dragover',e=>e.preventDefault());el.addEventListener('drop',()=>{if(drag&&drag!==el){const r=el.getBoundingClientRect();const after=(e.clientY-r.top)>r.height/2;el.parentNode.insertBefore(drag,after?el.nextSibling:el);} });el.addEventListener('dragend',()=>{drag=null;[...sortList.children].forEach((x,i)=>x.querySelector('.stop-index').textContent=String(i+1).padStart(2,'0'));});});}

  document.querySelectorAll('[data-password-toggle]').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const id=btn.getAttribute('data-target');
      const input=document.getElementById(id);
      if(!input) return;
      const visible=input.type==='text';
      input.type=visible?'password':'text';
      btn.classList.toggle('is-visible',!visible);
      btn.setAttribute('aria-label',visible?'Show password':'Hide password');
      btn.setAttribute('title',visible?'Show password':'Hide password');
      const icon=btn.querySelector('i');
      if(icon) icon.className=visible?'hgi-stroke hgi-view':'hgi-stroke hgi-view-off';
    });
  });
  window.handlePasswordReset=function(event){
    event.preventDefault();
    if(typeof toast==='function') toast('Reset link request ready');
    else {
      const el=document.createElement('div'); el.className='gt-toast'; el.textContent='Reset link request ready';
      document.body.appendChild(el); setTimeout(()=>el.remove(),2200);
    }
    return false;
  };

})();


/* Global share + unified activity center */
(function(){
  function getCookie(name){
    const match=document.cookie.split(';').map(v=>v.trim()).find(v=>v.startsWith(name+'='));
    return match ? decodeURIComponent(match.split('=').slice(1).join('=')) : null;
  }
  const csrf=()=>getCookie('csrftoken');

  // ---------- Share ----------
  const shareDialog=document.querySelector('[data-global-share-dialog]');
  const shareLabel=shareDialog?.querySelector('[data-global-share-label]');
  const shareDescription=shareDialog?.querySelector('[data-global-share-description]');
  const shareUrl=shareDialog?.querySelector('[data-global-share-url]');
  const shareStatus=shareDialog?.querySelector('[data-global-share-status]');
  let shareContext={};

  function inferShareContext(){
    const path=window.location.pathname;
    let url=window.location.href;
    let title=document.title.replace(/\s*[—|-]\s*GlobeTrotter.*$/i,'').trim() || 'GlobeTrotter';
    let description='Share a useful GlobeTrotter page with someone you are planning with.';
    let recordUrl=null;
    if(path.startsWith('/community/post/')){
      const source=document.querySelector('.js-community-share');
      if(source){
        url=source.dataset.shareUrl || url;
        title=source.dataset.shareTitle || title;
        recordUrl=source.dataset.shareRecordUrl || null;
      }
      description='Share this travel conversation with someone who would have a useful opinion.';
    }else if(path.startsWith('/community/')){
      title='GlobeTrotter Community';
      description='Share the community feed and find useful travel conversations.';
    }else if(path.startsWith('/trip/itinerary/')){
      url=new URL('/share/sample-trip/',window.location.origin).href;
      title='GlobeTrotter itinerary';
      description='Share this itinerary so someone else can view the route, days and stops.';
    }else if(path.startsWith('/trips/')){
      description='Share your trip planning workspace with a travel partner.';
    }
    return {url,title,description,recordUrl};
  }

  async function recordCommunityShare(channel){
    if(!shareContext.recordUrl) return null;
    try{
      const body=new URLSearchParams({channel});
      const r=await fetch(shareContext.recordUrl,{method:'POST',body,headers:{'X-CSRFToken':csrf()||'','X-Requested-With':'XMLHttpRequest','Accept':'application/json'},credentials:'same-origin'});
      if(!r.ok) return null;
      return await r.json();
    }catch(_e){return null;}
  }

  function setShareStatus(message){ if(shareStatus) shareStatus.textContent=message||''; }

  function openShare(){
    if(!shareDialog) return;
    shareContext=inferShareContext();
    if(shareLabel) shareLabel.textContent=shareContext.title;
    if(shareDescription) shareDescription.textContent=shareContext.description;
    if(shareUrl) shareUrl.textContent=shareContext.url;
    setShareStatus('');
    shareDialog.hidden=false;
    shareDialog.setAttribute('aria-hidden','false');
    document.body.classList.add('share-dialog-open');
  }
  function closeShare(){
    if(!shareDialog) return;
    shareDialog.hidden=true;
    shareDialog.setAttribute('aria-hidden','true');
    document.body.classList.remove('share-dialog-open');
  }

  document.querySelectorAll('[data-global-share]').forEach(b=>b.addEventListener('click',openShare));
  shareDialog?.querySelectorAll('[data-global-share-close]').forEach(b=>b.addEventListener('click',closeShare));
  document.addEventListener('keydown',e=>{if(e.key==='Escape' && shareDialog && !shareDialog.hidden) closeShare();});

  shareDialog?.querySelectorAll('[data-share-action]').forEach(btn=>{
    btn.addEventListener('click',async()=>{
      const action=btn.dataset.shareAction;
      const text=`${shareContext.title}\n${shareContext.url}`;
      if(action==='native'){
        if(navigator.share){
          try{await navigator.share({title:shareContext.title,text:shareContext.description,url:shareContext.url});await recordCommunityShare('native');setShareStatus('Shared from your device.');}
          catch(e){ if(e?.name!=='AbortError') setShareStatus('Share was not completed.');}
        }else{
          await navigator.clipboard?.writeText(shareContext.url);
          await recordCommunityShare('native');
          setShareStatus('Link copied. Your browser does not support device sharing.');
        }
      }
      if(action==='copy'){
        try{await navigator.clipboard.writeText(shareContext.url);await recordCommunityShare('copy');setShareStatus('Link copied to clipboard.');}
        catch(_e){setShareStatus('Copy is unavailable in this browser.');}
      }
      if(action==='whatsapp'){
        await recordCommunityShare('whatsapp');
        window.open('https://wa.me/?text='+encodeURIComponent(text),'_blank','noopener,noreferrer');
        setShareStatus('Opening WhatsApp…');
      }
      if(action==='email'){
        await recordCommunityShare('email');
        window.location.href='mailto:?subject='+encodeURIComponent(shareContext.title)+'&body='+encodeURIComponent(shareContext.description+'\n\n'+shareContext.url);
      }
    });
  });

  // ---------- Notifications ----------
  const notifButton=document.querySelector('[data-community-notifications]');
  const notifPanel=document.querySelector('[data-community-notification-panel]');
  const notifList=document.querySelector('[data-community-notification-list]');
  const notifCount=document.querySelector('.community-notification-count');
  const notifLabel=document.querySelector('[data-community-notification-unread-label]');
  const readAll=document.querySelector('[data-community-notification-read-all]');
  const filterButtons=[...document.querySelectorAll('[data-notification-filter]')];
  let notificationFilter='all';
  let notificationItems=[];

  function esc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));}
  function relative(iso){const t=new Date(iso).getTime();if(Number.isNaN(t))return '';const s=Math.max(0,Math.floor((Date.now()-t)/1000));if(s<60)return'just now';const m=Math.floor(s/60);if(m<60)return`${m}m ago`;const h=Math.floor(m/60);if(h<24)return`${h}h ago`;return`${Math.floor(h/24)}d ago`;}
  function renderNotifications(){
    if(!notifList)return;
    const items=notificationFilter==='all'?notificationItems:notificationItems.filter(n=>n.category===notificationFilter);
    if(!items.length){notifList.innerHTML='<div class="community-notification-empty">No activity in this view.</div>';return;}
    notifList.innerHTML=items.map(n=>`
      <a class="community-notification-item ${n.read?'':'unread'}" href="${esc(n.url)}" data-notification-id="${n.id}">
        <span class="community-notification-dot"></span>
        <span class="community-notification-copy"><strong>${esc(n.message)}</strong><small>${esc(relative(n.created_at))}</small></span>
      </a>`).join('');
  }
  async function loadNotifications(){
    if(!notifButton)return;
    try{
      const r=await fetch('/community/notifications/',{headers:{'Accept':'application/json','X-Requested-With':'XMLHttpRequest'},credentials:'same-origin',cache:'no-store'});
      if(!r.ok)return;
      const data=await r.json();
      notificationItems=data.items||[];
      if(notifCount){notifCount.textContent=data.unread>99?'99+':data.unread;notifCount.hidden=data.unread<1;}
      if(notifLabel)notifLabel.textContent=data.unread?`${data.unread} unread`:'';
      renderNotifications();
    }catch(_e){}
  }
  async function markRead(id){
    const body=new URLSearchParams(); if(id)body.set('id',id);
    try{await fetch('/community/notifications/read/',{method:'POST',body,headers:{'X-CSRFToken':csrf()||'','X-Requested-With':'XMLHttpRequest'},credentials:'same-origin'});}catch(_e){}
  }
  notifButton?.addEventListener('click',()=>{notifPanel.hidden=!notifPanel.hidden;if(!notifPanel.hidden)loadNotifications();});
  filterButtons.forEach(btn=>btn.addEventListener('click',()=>{filterButtons.forEach(x=>x.classList.remove('active'));btn.classList.add('active');notificationFilter=btn.dataset.notificationFilter;renderNotifications();}));
  notifList?.addEventListener('click',async e=>{const item=e.target.closest('[data-notification-id]');if(item){e.preventDefault();await markRead(item.dataset.notificationId);window.location.href=item.href;}});
  readAll?.addEventListener('click',async()=>{await markRead();await loadNotifications();});
  document.addEventListener('click',e=>{if(notifPanel&&!e.target.closest('.community-notification-wrap'))notifPanel.hidden=true;});
  loadNotifications();
  window.setInterval(loadNotifications,5000);
})();
