const $=(s,r=document)=>r.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const RF={city:'Bengaluru'};
{const u=new URLSearchParams(location.search);let c=u.get('city');try{c=c||localStorage.getItem('rf_city')}catch(_){}if(c)RF.city=c}
const toast=m=>{const t=$('#toast');t.textContent=m;t.classList.add('on');clearTimeout(t._);t._=setTimeout(()=>t.classList.remove('on'),2800)};
const photo=i=>i.photo?`<img src="${esc(i.photo)}" alt="${esc(i.title)}">`:drawItem(i.kind,i.color);
function setCity(c,save=true){RF.city=c;if(save)try{localStorage.setItem('rf_city',c)}catch(_){}
  document.querySelectorAll('[data-city]').forEach(e=>e.textContent=c);const s=$('#city');if(s)s.value=c;document.dispatchEvent(new Event('rf:city'))}
document.addEventListener('DOMContentLoaded',()=>{
  const s=$('#city');if([...s.options].some(o=>o.value===RF.city))s.value=RF.city;else RF.city=s.value;
  document.querySelectorAll('[data-city]').forEach(e=>e.textContent=RF.city);
  s.onchange=()=>setCity(s.value);
  $('#bg').onclick=()=>$('#nav').classList.toggle('open');
  $('#dx').onclick=()=>$('#dlg').close();$('#dlg').onclick=e=>{if(e.target===$('#dlg'))$('#dlg').close()};
  const gps=$('#gps');if(gps)gps.onclick=()=>{const ls=$('#ls');
    if(!navigator.geolocation){ls.textContent='Location isn’t available in this browser. Pick a city instead.';return}
    ls.textContent='Finding you…';
    navigator.geolocation.getCurrentPosition(p=>{fetch('/api/cities').then(r=>r.json()).then(L=>{let b,d=1e9;for(const c of L){const x=(c.lat-p.coords.latitude)**2+(c.lng-p.coords.longitude)**2;if(x<d){d=x;b=c.name}}
      setCity(b);ls.textContent=`Nearest city: ${b}. Change it any time.`})},()=>{ls.textContent='Location was blocked. Pick your city from the menu instead.'},{timeout:8000})};
});
function Gallery(o){
  const st={q:o.q||'',category:o.category||'All',type:o.type||'all',days:o.days||'',sort:o.sort||'new',page:1},lim=o.limit||12;
  const W=$('#wall'),E=$('#empty'),M=$('#more'),C=$('#count'),T=$('#tabs'),cache={};let tok=0;
  const qs=()=>{const p=new URLSearchParams({city:RF.city,limit:lim,sort:st.sort,page:st.page});
    if(st.q)p.set('q',st.q);if(st.category!=='All')p.set('category',st.category);if(st.type!=='all')p.set('type',st.type);if(st.days)p.set('days',st.days);return p};
  async function tabs(){const p=qs();p.delete('category');const r=await(await fetch('/api/categories?'+p)).json();
    if(!r.some(c=>c.name===st.category))st.category='All';
    T.innerHTML=r.map(c=>`<button aria-pressed="${c.name===st.category}" data-c="${esc(c.name)}">${esc(c.name)}<em>${c.count}</em></button>`).join('')}
  async function load(append){const my=++tok;
    try{const r=await fetch('/api/items?'+qs());if(!r.ok)throw 0;const d=await r.json();if(my!==tok)return;
      const base=append?W.children.length:0;
      const html=d.items.map((i,j)=>{cache[i.id]=i;return `<button class="tag" data-id="${i.id}"><div class="ph" style="${i.photo?'':'height:'+[150,200,170,230][(base+j)%4]+'px'}">${photo(i)}</div><b>${esc(i.title)}</b><small>${esc(i.area)} · ${esc(i.when)}</small><span class="st ${i.type}">${i.type==='lost'?'Lost':'Found'}</span></button>`}).join('');
      if(append)W.insertAdjacentHTML('beforeend',html);else W.innerHTML=html;
      E.hidden=d.total>0;if(!d.total)E.textContent=`No matches in ${RF.city}. Clear a filter or search term, or report the item so the next person who looks can find it.`;
      if(C)C.textContent=`${d.total} ${d.total===1?'report':'reports'} in ${RF.city}`;
      if(M)M.hidden=!d.has_more;if(o.onLoad)o.onLoad(d);
    }catch(_){E.hidden=false;E.textContent='Reports couldn’t be loaded. Check your connection and try again.'}}
  function sync(){if(!o.sync)return;const p=new URLSearchParams();
    if(st.q)p.set('q',st.q);if(st.category!=='All')p.set('category',st.category);if(st.type!=='all')p.set('type',st.type);if(st.days)p.set('days',st.days);if(st.sort!=='new')p.set('sort',st.sort);
    history.replaceState(null,'',location.pathname+(p.toString()?'?'+p:''))}
  async function reset(){st.page=1;sync();await tabs();await load(false)}
  T.onclick=e=>{const b=e.target.closest('button');if(!b)return;st.category=b.dataset.c;reset()};
  $('#flt').innerHTML=['All','Lost','Found'].map(c=>`<button aria-pressed="${c.toLowerCase()===st.type||(c==='All'&&st.type==='all')}">${c}</button>`).join('');
  $('#flt').onclick=e=>{const b=e.target.closest('button');if(!b)return;st.type=b.textContent.toLowerCase();[...$('#flt').children].forEach(x=>x.setAttribute('aria-pressed',x===b));reset()};
  if($('#days'))$('#days').onchange=e=>{st.days=e.target.value;reset()};
  if($('#sort'))$('#sort').onchange=e=>{st.sort=e.target.value;reset()};
  if(M)M.onclick=()=>{st.page++;load(true)};
  W.onclick=e=>{const b=e.target.closest('.tag');if(!b)return;const i=cache[b.dataset.id];
    $('#dph').innerHTML=photo(i);$('#dst').textContent=i.type==='lost'?'Lost':'Found';$('#dst').className='st '+i.type;
    $('#dt').textContent=i.title;$('#dd').textContent=i.description;$('#dm').textContent=`${i.area}, ${i.city} · ${i.when}`;$('#dc').href='/item/'+i.id;$('#dlg').showModal()};
  document.addEventListener('rf:city',reset);
  document.addEventListener('DOMContentLoaded',reset);
  return {st,reset};
}
