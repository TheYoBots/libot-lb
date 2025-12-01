(function(){
  const toggle = document.getElementById('themeToggle');
  let stored = null;
  try { stored = localStorage.getItem('libot-theme'); } catch(e) { stored = null }
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  let theme = stored || (prefersDark ? 'dark' : 'light');

  const SUN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 4V2M12 22v-2M4 12H2M22 12h-2M5 5l-1.5-1.5M20 20l-1.5-1.5M5 19L3.5 20.5M20 4l-1.5 1.5M12 8a4 4 0 100 8 4 4 0 000-8z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const MOON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function applyTheme(t){
    document.body.setAttribute('data-theme', t);
    if(!toggle) return;
    toggle.setAttribute('aria-pressed', t==='dark' ? 'true' : 'false');
    if(t === 'dark'){
      toggle.innerHTML = SUN;
      toggle.setAttribute('aria-label', 'Switch to light mode');
    } else {
      toggle.innerHTML = MOON;
      toggle.setAttribute('aria-label', 'Switch to dark mode');
    }
  }

  applyTheme(theme);

  if(!toggle) return;

  toggle.addEventListener('click', ()=>{
    theme = (theme==='dark') ? 'light' : 'dark';
    try{ localStorage.setItem('libot-theme', theme); } catch(e) {}
    applyTheme(theme);
  });

  const backBtn = document.getElementById('backBtn');
  if(backBtn){
    backBtn.addEventListener('click', ()=>{ history.back(); });
    backBtn.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') history.back(); });
  }
  const homeBtn = document.getElementById('homeBtn');
  if(homeBtn){
    homeBtn.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') window.location.href = homeBtn.getAttribute('href') || '/'; });
  }
})();
