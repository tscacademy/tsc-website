/* TSC Academy: Meta pixel with consent, cookie bar, reveal, sticky CTA */
(function(){
  /* Meta pixel: nothing is sent until the visitor accepts cookies */
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
  var consent=null;try{consent=localStorage.getItem('tsc_cookie_consent');}catch(e){}
  if(consent!=='granted'){fbq('consent','revoke');}
  fbq('init','1393857408746215');fbq('track','PageView');

  function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn);}
  ready(function(){
    /* cookie bar */
    if(!consent){
      var bar=document.createElement('div');bar.className='cookie-bar show';bar.setAttribute('role','dialog');bar.setAttribute('aria-label','Cookie preferences');
      bar.innerHTML='We use Meta cookies to measure which posts and ads bring families here. Only set if you accept. <a href="/privacy.html">Privacy</a><div class="acts"><button class="ok" type="button">Accept</button><button type="button">Decline</button></div>';
      document.body.appendChild(bar);
      var bs=bar.querySelectorAll('button');
      function choose(v){try{localStorage.setItem('tsc_cookie_consent',v);}catch(e){} if(v==='granted'&&window.fbq)fbq('consent','grant'); bar.remove();}
      bs[0].onclick=function(){choose('granted');};bs[1].onclick=function(){choose('denied');};
    }
    /* Lead event on every Assessment booking click */
    document.querySelectorAll('[data-book]').forEach(function(a){a.addEventListener('click',function(){window.fbq&&fbq('track','Lead');});});
    /* reveal on scroll */
    var els=document.querySelectorAll('.reveal');
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{threshold:.12});
      els.forEach(function(el){io.observe(el);});
    } else els.forEach(function(el){el.classList.add('in');});
    /* sticky mobile CTA after the hero */
    var st=document.querySelector('.sticky'),hero=document.querySelector('.hero,.article-hero');
    if(st&&hero&&'IntersectionObserver' in window){
      new IntersectionObserver(function(es){st.classList.toggle('show',!es[0].isIntersecting);}).observe(hero);
    }
  });
})();
