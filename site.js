// Comportamento comum a todas as páginas do site: menu, ano do rodapé e o formulário da home.
(function(){
  var btn=document.querySelector('.menu-btn'), nav=document.getElementById('nav');
  btn.addEventListener('click',function(e){
    e.preventDefault();
    var open=nav.classList.toggle('open'); btn.setAttribute('aria-expanded',open?'true':'false');
  });
  nav.addEventListener('click',function(e){
    if(e.target.tagName==='A'){nav.classList.remove('open');btn.setAttribute('aria-expanded','false');}
  });
  var ano=document.getElementById('y'); if(ano)ano.textContent=new Date().getFullYear();
  var EMAIL='contato@dawrahecarmona.com.br';
  var form=document.getElementById('msg');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();
    var f=e.target, v=function(n){return (f.elements[n].value||'').trim();};
    var assunto=v('assunto')||'Agendar uma conversa';
    var corpo=v('mensagem')+'\n\n'+v('nome')+(v('telefone')?'\n'+v('telefone'):'');
    location.href='mailto:'+EMAIL+'?subject='+encodeURIComponent(assunto)+'&body='+encodeURIComponent(corpo.trim());
  });
})();
