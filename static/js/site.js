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

  // Dropdowns
  document.addEventListener('click', e => {
    const trigger = e.target.closest('[data-dropdown-trigger]');
    if (trigger) {
      const dropdown = trigger.closest('.dropdown');
      const isOpen = dropdown.classList.contains('is-open');
      document.querySelectorAll('.dropdown.is-open').forEach(d => d.classList.remove('is-open'));
      if (!isOpen) dropdown.classList.add('is-open');
    } else if (!e.target.closest('.dropdown-menu')) {
      document.querySelectorAll('.dropdown.is-open').forEach(d => d.classList.remove('is-open'));
    }
  });

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


  document.querySelectorAll('[data-auth-password]').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const input=document.getElementById(btn.getAttribute('data-auth-password'));
      if(!input) return;
      const visible=input.type==='text';
      input.type=visible?'password':'text';
      btn.setAttribute('aria-label',visible?'Show password':'Hide password');
      const icon=btn.querySelector('i');
      if(icon) icon.className=visible?'hgi-stroke hgi-view':'hgi-stroke hgi-view-off';
    });
  });

})();