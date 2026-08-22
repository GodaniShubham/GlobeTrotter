
(function(){
  function csrf(){
    const found=document.cookie.split(';').map(v=>v.trim()).find(v=>v.startsWith('csrftoken='));
    return found ? decodeURIComponent(found.split('=').slice(1).join('=')) : '';
  }

  async function post(url, data){
    const body=data instanceof FormData?data:new URLSearchParams(data);
    const r=await fetch(url,{method:'POST',body,headers:{'X-CSRFToken':csrf(),'X-Requested-With':'XMLHttpRequest','Accept':'application/json'},credentials:'same-origin'});
    const payload=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(payload.message||'Could not save this change.');
    return payload;
  }

  function notify(message){
    if(typeof toast==='function'){toast(message);return;}
    const node=document.createElement('div');node.className='gt-toast';node.textContent=message;document.body.appendChild(node);setTimeout(()=>node.remove(),2200);
  }

  document.querySelectorAll('.js-add-city').forEach(button=>{
    button.addEventListener('click',async()=>{
      button.disabled=true;
      try{
        await post(button.dataset.url,{trip_id:button.dataset.trip,city_id:button.dataset.city});
        notify('Destination added to your trip.');
        window.location.href=`/trip/builder/?trip=${button.dataset.trip}`;
      }catch(e){notify(e.message);button.disabled=false;}
    });
  });

  document.querySelectorAll('.js-add-activity').forEach(button=>{
    button.addEventListener('click',async()=>{
      button.disabled=true;
      try{
        await post(button.dataset.url,{trip_stop_id:button.dataset.stop,activity_id:button.dataset.activity});
        notify('Activity added to your itinerary.');
        const trip=new URLSearchParams(window.location.search).get('trip')||'';
        window.location.href=`/trip/builder/?trip=${trip}`;
      }catch(e){notify(e.message);button.disabled=false;}
    });
  });

  const stopSelector=document.querySelector('[data-stop-selector]');
  if(stopSelector){
    stopSelector.addEventListener('change',()=>{
      const url=new URL(window.location.href);
      url.searchParams.set('stop',stopSelector.value);
      window.location.href=url.toString();
    });
  }

  document.querySelectorAll('.js-delete-stop').forEach(button=>{
    button.addEventListener('click',async()=>{
      if(!confirm('Remove this destination and its planned activities?')) return;
      try{
        await post(button.dataset.url,{});
        window.location.reload();
      }catch(e){notify(e.message);}
    });
  });

  document.querySelectorAll('.js-delete-activity').forEach(button=>{
    button.addEventListener('click',async()=>{
      if(!confirm('Remove this activity from the itinerary?')) return;
      try{
        await post(button.dataset.url,{});
        window.location.reload();
      }catch(e){notify(e.message);}
    });
  });

  const list=document.querySelector('[data-stop-list]');
  const saveOrder=document.querySelector('[data-save-order]');
  if(list && saveOrder){
    let dragged=null;
    list.querySelectorAll('[data-stop-id]').forEach(item=>{
      item.addEventListener('dragstart',()=>{dragged=item;item.classList.add('is-dragging');});
      item.addEventListener('dragend',()=>{item.classList.remove('is-dragging');dragged=null;});
      item.addEventListener('dragover',e=>{
        e.preventDefault();
        if(!dragged || dragged===item) return;
        const rect=item.getBoundingClientRect();
        const after=(e.clientY-rect.top)>rect.height/2;
        item.parentNode.insertBefore(dragged, after?item.nextSibling:item);
      });
    });
    saveOrder.addEventListener('click',async()=>{
      const ids=[...list.querySelectorAll('[data-stop-id]')].map(n=>n.dataset.stopId);
      const body=new URLSearchParams();
      body.set('trip_id',document.querySelector('[data-itinerary-workspace]').dataset.tripId);
      ids.forEach(id=>body.append('stop_ids',id));
      try{await post('/trip/stops/reorder/',body);notify('Stop order saved.');window.location.reload();}
      catch(e){notify(e.message);}
    });
  }
})();
