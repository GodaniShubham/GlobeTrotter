(function(){
  function getCookie(name){
    const match = document.cookie.split(';').map(v=>v.trim()).find(v=>v.startsWith(name+'='));
    return match ? decodeURIComponent(match.split('=').slice(1).join('=')) : null;
  }
  const csrf = getCookie('csrftoken');
  async function postAction(button){
    const url = button.dataset.url;
    if(!url) return;
    button.disabled = true;
    try{
      const response = await fetch(url, {
        method:'POST',
        headers:{'X-CSRFToken':csrf || '', 'X-Requested-With':'XMLHttpRequest', 'Accept':'application/json'},
        credentials:'same-origin'
      });
      if(response.status === 403){ window.location.href='/login/?next='+encodeURIComponent(window.location.pathname+window.location.search); return; }
      const data = await response.json();
      const postId = button.dataset.post;
      document.querySelectorAll(`[data-like-count="${postId}"]`).forEach(el=>el.textContent=data.count);
      if(button.classList.contains('js-community-like')){
        button.classList.toggle('is-active', !!data.liked);
      }
      if(button.classList.contains('js-community-save')){
        button.classList.toggle('is-active', !!data.saved);
        const label=button.querySelector('.js-save-label');
        if(label) label.textContent=data.saved?'Saved':'Save';
        if(!data.saved && window.location.pathname.includes('/community/saved/')){
          button.closest('.community-saved-card')?.remove();
        }
      }
    }catch(e){
      if(typeof toast==='function') toast('Something went wrong. Please try again.');
    }finally{button.disabled=false;}
  }
  document.querySelectorAll('.js-community-like,.js-community-save').forEach(btn=>btn.addEventListener('click',()=>postAction(btn)));
})();
