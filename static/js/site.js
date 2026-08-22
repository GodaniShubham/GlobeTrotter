
/* Reliable Hugeicons fallback: if the remote font is unavailable, replace supported
   hgi-stroke nodes with lightweight inline SVGs. This keeps the icon API/class names
   stable for the templates while making the UI resilient offline. */
(function(){
  const paths = {
    'home-01':'<path d="M4 10.2 12 4l8 6.2V20a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1z"/><path d="M9 21h6"/>',
    'briefcase-01':'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 11h18M10 11v2h4v-2"/>',
    'add-01':'<path d="M12 5v14M5 12h14"/>',
    'route-02':'<circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M7 5h4a3 3 0 0 1 3 3v2a3 3 0 0 0 3 3h2M17 19h-4a3 3 0 0 1-3-3v-2a3 3 0 0 0-3-3H5"/>',
    'list-view':'<rect x="4" y="5" width="16" height="3" rx="1"/><rect x="4" y="10.5" width="16" height="3" rx="1"/><rect x="4" y="16" width="16" height="3" rx="1"/>',
    'location-01':'<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
    'compass-01':'<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2.2 4.8-4.8 2.2 2.2-4.8z"/>',
    'wallet-01':'<path d="M4 7.5A2.5 2.5 0 0 1 6.5 5H20v14H6.5A2.5 2.5 0 0 1 4 16.5z"/><path d="M4 8h14.5A1.5 1.5 0 0 1 20 9.5V13h-5a2 2 0 1 0 0 4h5v1.5"/><circle cx="15" cy="15" r=".7" fill="currentColor" stroke="none"/>',
    'calendar-03':'<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4M16 3v4M4 9h16M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01"/>',
    'user-group':'<circle cx="9" cy="9" r="3"/><circle cx="17" cy="10" r="2.5"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0M14 20a4.5 4.5 0 0 1 5.5-4.4"/>',
    'settings-02':'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.8 1.8 0 0 0 .36 2l.06.06-1.82 1.82-.06-.06a1.8 1.8 0 0 0-2-.36 1.8 1.8 0 0 0-1.08 1.66V20h-2.58v-.08A1.8 1.8 0 0 0 11.2 18.3a1.8 1.8 0 0 0-2 .36l-.06.06-1.82-1.82.06-.06a1.8 1.8 0 0 0 .36-2A1.8 1.8 0 0 0 6.08 13H6v-2h.08A1.8 1.8 0 0 0 7.74 9.9a1.8 1.8 0 0 0-.36-2l-.06-.06L9.14 6l.06.06a1.8 1.8 0 0 0 2 .36A1.8 1.8 0 0 0 12.28 4.8V4h2.58v.08a1.8 1.8 0 0 0 1.08 1.64 1.8 1.8 0 0 0 2-.36L18 5.3l1.82 1.82-.06.06a1.8 1.8 0 0 0-.36 2A1.8 1.8 0 0 0 21 10.98v2.04h-.08A1.8 1.8 0 0 0 19.4 15Z"/>',
    'menu-01':'<path d="M4 6h16M4 12h16M4 18h16"/>',
    'arrow-right-01':'<path d="M5 12h14M13 6l6 6-6 6"/>',
    'arrow-down-01':'<path d="M6 9l6 6 6-6"/>',
    'share-08':'<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="m8.3 10.9 7.4-4.2M8.3 13.1l7.4 4.2"/>',
    'notification-02':'<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4"/>',
    'logout-01':'<path d="M10 5H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h4M14 8l4 4-4 4M18 12H9"/>',
    'cancel-01':'<path d="m7 7 10 10M17 7 7 17"/>',
    'link-01':'<path d="M9 15 15 9"/><path d="M7 17H6a4 4 0 0 1 0-8h3M17 7h1a4 4 0 0 1 0 8h-3"/>',
    'mail-01':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    'search-01':'<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    'arrow-up-right-02':'<path d="M7 17 17 7M9 7h8v8"/>',
    'edit-02':'<path d="m4 16.5-.8 4.3 4.3-.8L19 8.5a2.1 2.1 0 0 0-3-3z"/><path d="m14.5 7.5 2 2"/>',
    'more-horizontal':'<circle cx="5" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
    'delete-02':'<path d="M5 7h14M10 11v6M14 11v6M8 7l1-3h6l1 3M7 7l1 14h8l1-14"/>',
    'message-02':'<path d="M5 5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H11l-4 3v-3H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z"/>',
    'thumbs-up':'<path d="M7 10v10H4V10h3ZM7 20h8.5a2 2 0 0 0 2-1.5l1.2-5A2 2 0 0 0 17 11h-3l.5-3.2a2.2 2.2 0 0 0-4.3-.8L8 12"/>',
    'bookmark-02':'<path d="M6 4h12v17l-6-3-6 3z"/>',
    'add-01':'<path d="M12 5v14M5 12h14"/>',
    'calendar-04':'<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4M16 3v4M4 9h16M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01M16 17h.01"/>',
    'arrow-left-01':'<path d="M19 12H5M11 6l-6 6 6 6"/>',
    'drag-drop-vertical':'<circle cx="9" cy="7" r="1" fill="currentColor" stroke="none"/><circle cx="15" cy="7" r="1" fill="currentColor" stroke="none"/><circle cx="9" cy="12" r="1" fill="currentColor" stroke="none"/><circle cx="15" cy="12" r="1" fill="currentColor" stroke="none"/><circle cx="9" cy="17" r="1" fill="currentColor" stroke="none"/><circle cx="15" cy="17" r="1" fill="currentColor" stroke="none"/>',
    'dashboard-speed-01':'<path d="M4 16a8 8 0 1 1 16 0"/><path d="m12 12 3-3"/><path d="M6 19h12"/>',
    'whatsapp':'<path d="M20 12a8 8 0 0 1-11.7 7.1L4 20l.9-4.1A8 8 0 1 1 20 12Z"/><path d="M9.2 9.2c.2-.5.4-.6.8-.6.2 0 .4 0 .5.1l.7 1.7c.1.3.1.5-.1.7l-.5.6c.4.8 1 1.4 1.8 1.8l.6-.5c.2-.2.4-.2.7-.1l1.7.7c.2.1.3.3.1.6-.2.5-.6.9-1.1 1-2.7.3-5.8-2.8-6.1-5.5Z"/>'
  };

  function replaceIcons(){
    document.querySelectorAll('i.hgi-stroke').forEach(el=>{
      if(el.dataset.svgIconReady) return;
      const cls=[...el.classList].find(c=>c.startsWith('hgi-') && c!=='hgi-stroke');
      if(!cls) return;
      const key=cls.replace(/^hgi-/,'');
      const content=paths[key] || '<circle cx="12" cy="12" r="7"/><path d="M9 12h6"/>';
      const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
      svg.setAttribute('viewBox','0 0 24 24');
      svg.setAttribute('fill','none');
      svg.setAttribute('stroke','currentColor');
      svg.setAttribute('stroke-width','1.8');
      svg.setAttribute('stroke-linecap','round');
      svg.setAttribute('stroke-linejoin','round');
      svg.setAttribute('aria-hidden','true');
      svg.classList.add('gt-inline-icon');
      svg.innerHTML=content;
      el.replaceWith(svg);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',replaceIcons);
  else replaceIcons();
})();

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
