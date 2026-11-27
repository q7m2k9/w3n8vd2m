/* ---------- STYLE VISUEL : en-tête de marque, traits de progression, grands titres, pages Motion, sous-titres ---------- */
const TPAGE=0.35;   /* durée d'une transition de page (secondes) */
const el=(parent,cls,html)=>{const d=document.createElement('div');d.className=cls;d.innerHTML=html||'';parent.appendChild(d);return d};
const an=(t,html,css,cls)=>'<div class="an '+(cls||'')+'" data-t="'+t+'" style="'+(css||'')+'">'+html+'</div>';
const champs=t=>['Prénom','Nom de famille','Courriel'].map((c,i)=>'<div class="champ"><span class="tp" data-t="'+(t+.15+i*.22)+'">'+c+'</span></div>').join('');
const titreHtml=(l,t,centre)=>'<div class="vt'+(centre?' c':'')+'"><div class="mq"><div class="li a" data-t="'+t+'">'+l[0]+'</div></div><div class="mq"><div class="li b" data-t="'+(t+.12)+'">'+(l[1]||'')+'</div></div></div>';
const IC={
 video:'<path d="M4 7h11v10H4zM15 11l5-3v8l-5-3"/>', ciseaux:'<circle cx="6" cy="7" r="2.6"/><circle cx="6" cy="17" r="2.6"/><path d="M8.2 8.6L20 17M8.2 15.4L20 7"/>',
 envoi:'<path d="M4 12l16-8-6 17-3-7z"/>', cadeau:'<path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13M12 7c-2-4-7-3-5 0M12 7c2-4 7-3 5 0"/>', etoile:'<path d="M12 3l2.7 5.8 6.3.7-4.7 4.3 1.3 6.2L12 16.800 6.4 20l1.300-6.2L3 9.500l6.3-.7z"/>'};
const ico=n=>'<span class="ic"><svg viewBox="0 0 24 24" width="46" height="46" fill="none" stroke="#a66932" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+IC[n]+'</svg></span>';
const coche='<svg viewBox="0 0 46 46" width="56" height="56"><circle cx="23" cy="23" r="20" fill="#a66932"/><path d="M13 24l7 7 13-15" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const curseur='<svg class="cur" viewBox="0 0 34 50" width="78" height="110"><path d="M2 2v36l9-8 7 16 8-4-7-15h13z" fill="#fff" stroke="#1d1a16" stroke-width="2.600" stroke-linejoin="round"/></svg>';
const carteLien=(t,top)=>an(t,ico('envoi')+'<div><b>Le lien</b><i>sous la vidéo</i></div>','top:'+top+'px','carte lien');
const MODELES={
 commente:P=>an(P.tPost,'<div class="tete-post"><span class="av p" style="background-image:url(\''+D.avatar+'\')"></span><b>Haute Visibilité</b></div><u></u><u class="court"></u><div class="vignette">'+ico('video')+'</div>','top:660px','post')+
   an(P.tSaisie-.4,'<span class="tp" data-t="'+P.tSaisie+'">MVT</span><strong class="tap" data-t="'+P.tTap+'">Publier</strong>','top:1090px','saisie')+
   an(P.tTap+.12,'<div><small><b>toi</b> · à l\'instant</small><p>MVT</p></div><svg viewBox="0 0 24 24" width="54" height="54" fill="#a66932"><path d="M12 21C4 15 2 12 2 8.500 2 5.500 4.300 3.500 7 3.500c2 0 3.800 1.100 5 3 1.200-1.900 3-3 5-3 2.700 0 5 2 5 5 0 3.500-2 6.500-10 12.500z"/></svg>','top:1235px','poste'),
 flux:P=>'<div class="fil an" data-t="'+(P.items[0].t+.2)+'"></div>'+P.items.map((c,i)=>an(c.t,ico(c.ic)+'<div><b>'+c.nom+'</b><i>'+c.sous+'</i></div><em>'+(i+1)+'</em>','top:'+(650+i*215)+'px','carte')).join('')+'<div class="pt"></div>'+
   '<div class="fete" data-t="'+P.tYay+'">'+Array.from({length:14},(_,i)=>'<s data-a="'+(i*360/14)+'"></s>').join('')+'<span>Yay !</span></div>',
 rappel:P=>an(P.t0+.2,'<svg class="cloche" data-t="'+P.tCloche+'" viewBox="0 0 24 24" width="230" height="230" fill="none" stroke="#a66932" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16V10a6 6 0 0 1 12 0v6l2 2H4zM10 21h4"/></svg><span class="pastille">3</span>','top:670px','rond-cloche')+carteLien(P.tLien,1100),
 cadeaux:P=>an(P.tForm,champs(P.tForm)+'<div class="btn tap" data-t="'+P.tTap+'">Envoyer</div>','top:660px','form').replace('class="an ','data-o="'+P.tSortie+'" class="an ')+
   P.items.map((c,i)=>an(c.t,ico('cadeau')+'<div><b>Cadeau '+(i+1)+'</b><i>'+c.sous+'</i></div>','top:'+(690+i*200)+'px;height:170px','carte')).join(''),
 numero:P=>'<div class="surt an" data-t="'+(P.t0+.12)+'">'+P.sur+'</div><div class="gros" data-t="'+(P.t0+.05)+'">'+P.n+'</div>',
 etapes:P=>an(P.tBadge,P.badge,'top:648px','badge')+P.items.map((c,i)=>an(c.t-.35,'<span class="rond"><span class="ck" data-t="'+c.t+'">'+coche+'</span></span><div><b>Étape '+(i+1)+'</b><i>'+c.nom+'</i></div>','top:'+(750+i*155)+'px','carte')).join(''),
 priorite:P=>[0,1,2].map(i=>an(P.t0+.2+i*.1,'<span class="num"></span><u></u>','top:'+(660+i*130)+'px','file f'+i)).join('')+
   an(P.t0+.5,'<span class="num toi"></span><b>Toi</b><strong class="ck" data-t="'+(P.tMonte+.5)+'">Priorité</strong>','top:660px','file moi').replace('class="an ','data-m="'+P.tMonte+'" class="an ')+
   an(P.tTurbo,ico('etoile')+'<div><b>Montage</b><i>Vidéo Turbo</i></div>','top:1190px','carte'),
 prix:P=>an(P.tA,'<small>Tarif régulier</small><u></u><span class="barre" data-t="'+(P.tA+.35)+'"></span>','top:700px','prix gris')+an(P.tB,'<small>Liste d\'attente</small><h4>Ton tarif <i>préférentiel</i></h4><span class="ck" data-t="'+(P.tB+.3)+'">'+coche+'</span>','top:960px','prix fort'),
 produit:P=>an(P.t0+.15,'<div class="barwin"><s></s><s></s><s></s></div><div class="ecran haut">'+ico('etoile')+'</div><b>Ton produit digital</b><div class="jauge"><span class="barre" data-t="'+P.tCree+'"></span></div><i>en création</i>','top:680px','fenetre prod'),
 montage:P=>an(P.t0+.15,'<div class="barwin"><s></s><s></s><s></s></div><div class="ecran">'+ico('video')+'</div><div class="piste">'+[150,60,190,40,170,70].map((w,i)=>'<span class="clip '+(i%2?'vide':'')+'" data-w="'+w+'" data-t="'+(P.tCoupe+(i>>1)*.18)+'" style="width:'+w+'px"></span>').join('')+'<span class="tete"></span></div>','top:650px','fenetre')+
   P.items.map((c,i)=>an(c.t,coche+'<b>'+c.nom+'</b>','top:'+(1115+i*92)+'px','ligne')).join(''),
 resultat:P=>an(P.t0+.15,'<small>Résultats</small><div class="barres">'+[22,30,27,44,52,70,100].map((h,i,a)=>'<span class="br '+(i===a.length-1?'top':'')+'" data-h="'+h+'" data-t="'+(P.tDeb+i*.14)+'"></span>').join('')+'</div><small class="axe">Temps</small>','top:660px','graph')+an(P.tPro,'Ton montage','top:1255px','badge plein'),
 apercu:P=>an(P.t0+.15,'<img src="'+P.image+'" alt=""><div class="lecture"><span class="av-lec" data-t="'+(P.t0+.4)+'"></span></div>','top:645px','tel'),
 coulisses:P=>P.items.map((c,i)=>an(c.t,ico(c.ic)+'<div><b>'+c.nom+'</b><i>'+c.sous+'</i></div>','top:'+(660+i*195)+'px','carte')).join('')+an(P.tPrive,'Chaîne privée','top:1260px','badge plein'),
 clique:P=>carteLien(P.t0+.2,760)+an(P.tFleche,'<svg class="fleche" viewBox="0 0 100 130" width="260" height="340" fill="none" stroke="#a66932" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"><path d="M50 8v108M12 80l38 40 38-40"/></svg>','top:980px','zone-fleche'),
 infos:P=>an(P.tForm,champs(P.tForm)+'<div class="btn tap" data-t="'+P.tTap+'">Envoyer</div>','top:720px','form grand')};
const fond=mk('el','','vfond');
const pages=D.pleins.map(P=>{const e=mk('el vpage','<img class="bg" src="'+P.fond+'">'+(P.l?titreHtml(P.l,P.t0<.01?-1:P.t0+.18,P.centre):'')+MODELES[P.type](P));return {P,el:e}});
const marque=mk('el','<span class="tx">'+D.entreprise+'</span>','marque');
const traits=mk('el',D.traits.map(()=>'<span><i></i></span>').join(''),'traits');
const subs=D.sousTitres.map(g=>{const e=mk('el vsub','');const ws=g.mots.map((w,i)=>{const s=document.createElement('span');s.textContent=w.w;if(w.acc)s.className='acc';if(i<g.mots.length-1&&!g.mots[i+1].colle)s.style.marginRight='.28em';e.appendChild(s);return {w,s}});return {g,el:e,ws}});
const outro=document.createElement('img');outro.className='el';outro.id='outro';outro.src=D.outro.src;ov.appendChild(outro);
const fin=D.outro.bouton,finEl=mk('el finlien','<div class="zone an" data-t="'+fin.t+'" style="top:1290px"><div class="btn tap" data-t="'+fin.tTap+'">Clique sur le lien</div></div>'+curseur);
function animer(racine,t,P){
  racine.querySelectorAll('.li').forEach(n=>{const p=E.out(prog(t,+n.dataset.t,.5));n.style.transform='translateY('+((1-p)*115)+'%)'});
  racine.querySelectorAll('.an').forEach(n=>{const p=E.out(prog(t,+n.dataset.t,.45));n.style.opacity=clamp(p*1.4);n.style.transform='translateY('+((1-p)*70)+'px)'});
  racine.querySelectorAll('.tp').forEach(n=>{const full=n.dataset.f||(n.dataset.f=n.textContent);const k=Math.floor(clamp((t-(+n.dataset.t))/(full.length*2/30))*full.length+1e-6);n.textContent=full.slice(0,k)||' '});
  racine.querySelectorAll('.ck').forEach(n=>{const q=prog(t,+n.dataset.t,.3);n.style.opacity=clamp(q*3);n.style.transform='scale('+(.5+.5*E.back(q))+')'});
  racine.querySelectorAll('.tap').forEach(n=>{const d=t-(+n.dataset.t),k=(d>0&&d<.35)?Math.sin(d/.35*Math.PI):0;n.style.transform='scale('+(1-.06*k)+')';n.classList.toggle('actif',d>.1)});
  racine.querySelectorAll('.barre').forEach(n=>n.style.width=(E.io(prog(t,+n.dataset.t,.45))*100)+'%');
  racine.querySelectorAll('.br').forEach(n=>n.style.height=(E.out(prog(t,+n.dataset.t,.5))*(+n.dataset.h))+'%');
  racine.querySelectorAll('.clip.vide').forEach(n=>{const p=E.io(prog(t,+n.dataset.t,.5));n.style.width=(+n.dataset.w*(1-p))+'px';n.style.marginRight=(8*(1-p))+'px';n.style.opacity=1-p});
  racine.querySelectorAll('[data-o]').forEach(n=>{const q=E.io(prog(t,+n.dataset.o,.35));if(q>0){n.style.opacity=1-q;n.style.transform='translateY('+(-90*q)+'px)'}});
  racine.querySelectorAll('[data-m]').forEach(n=>{const q=E.io(prog(t,+n.dataset.m,.55));n.style.top=(1050-390*q)+'px';n.style.zIndex=2;
    racine.querySelectorAll('.file:not(.moi)').forEach((f,i)=>f.style.top=(660+i*130+130*q)+'px')});
  racine.querySelectorAll('.cloche').forEach(n=>{const d=t-(+n.dataset.t);n.style.transformOrigin='50% 12%';n.style.transform='rotate('+(d>0?Math.sin(d*22)*16*Math.exp(-d*2.4):0)+'deg)'});
  racine.querySelectorAll('.fete').forEach(n=>{const d=t-(+n.dataset.t),q=E.out(prog(t,+n.dataset.t,.5));n.style.opacity=d>0?1:0;n.lastChild.style.transform='scale('+(.5+.5*E.back(prog(t,+n.dataset.t,.4)))+')';
    n.querySelectorAll('s').forEach(p=>{const a=p.dataset.a*Math.PI/180;p.style.transform='translate('+(Math.cos(a)*(60+300*q))+'px,'+(Math.sin(a)*(30+90*q))+'px) scale('+(1-.4*q)+')';p.style.opacity=1-prog(t,+n.dataset.t+.45,.5)})});
  racine.querySelectorAll('.fleche').forEach(n=>n.style.transform='translateY('+(Math.abs(Math.sin(t*4.5))*34)+'px)');
  racine.querySelectorAll('.av-lec').forEach(n=>n.style.width=(prog(t,+n.dataset.t,1.9)*100)+'%');
  const tete=racine.querySelector('.tete');if(tete)tete.style.left=(20+prog(t,P.t0+.3,P.t1-P.t0-.4)*660)+'px';
  const gros=racine.querySelector('.gros');if(gros){const a=E.out(prog(t,+gros.dataset.t,.4)),l=prog(t,P.t0,P.t1-P.t0);gros.style.opacity=a;gros.style.transform='scale('+(.78+.22*a+.1*l)+')'}
  const pt=racine.querySelector('.pt');if(pt){const a=P.items[0].t+.4,p=((t-a)%1.2)/1.2;pt.style.opacity=t>a?Math.sin(Math.max(0,p)*Math.PI):0;pt.style.top=(690+Math.max(0,p)*464)+'px'}
  const cur=racine.querySelector('.cur');if(cur){const q=E.io(prog(t,P.tTap-.8,.75)),d=t-P.tTap,k=(d>0&&d<.35)?Math.sin(d/.35*Math.PI):0;cur.style.opacity=prog(t,P.tTap-.85,.2);cur.style.transform='translate('+(900-300*q)+'px,'+(1580-230*q)+'px) scale('+(1-.12*k)+')'}
}
function render(t){
  // pages seulement : un fond beige couvre toujours la vidéo d'origine; les pages glissent l'une après l'autre
  fond.style.opacity=1;
  pages.forEach((o,i)=>{const P=o.P,nx=pages[i+1]&&Math.abs(pages[i+1].P.t0-P.t1)<.02;
    const fin=nx?P.t1+TPAGE:P.t1;
    if(!(t>=P.t0&&t<fin)){o.el.style.opacity=0;return}
    const a=P.t0<.01?1:E.io(prog(t,P.t0,TPAGE)),s=nx?E.io(prog(t,P.t1,TPAGE)):0;
    const x=(1-a)*1080-s*1080, k=1-.09*Math.max(Math.sin(Math.PI*a),Math.sin(Math.PI*s));
    o.el.style.opacity=1;o.el.style.transform='translateX('+x+'px) scale('+k+')';o.el.style.borderRadius=(k<.999?36:0)+'px';animer(o.el,t,P)});
  const debut=D.traits[0].t0;
  marque.style.opacity=1;marque.classList.toggle('sans',t>=debut);      /* traits de progression visibles : plus de traits de chaque côté du nom */
  traits.style.opacity=t>=debut?E.out(prog(t,debut,.4)):0;
  const segs=traits.children;
  D.traits.forEach((s,i)=>segs[i].firstChild.style.width=(E.io(prog(t,s.t0,Math.min(1.6,s.t1-s.t0)))*100)+'%');
  subs.forEach(o=>{const g=o.g;if(!(t>=g.t0&&t<g.t1)){o.el.style.opacity=0;return}
    o.el.style.opacity=clamp((t-g.t0)/.08+.2);o.el.style.top=(g.y||D.mise.subY)+'px';o.el.style.transform='translate(-50%,-50%)';
    o.ws.forEach(r=>{r.s.style.opacity=.3+.7*clamp((t-(r.w.s-.1))/.14)})});
  const ox=D.outro,op=t>=ox.t0?E.io(prog(t,ox.t0,ox.fondu)):0;outro.style.opacity=op;
  finEl.style.opacity=t>=fin.t?1:0;if(t>=fin.t)animer(finEl,t,fin);
  if(dbg.style.display==='block'){const p=D.plans.find(p=>t>=p.t0&&t<p.t1)||D.plans[D.plans.length-1];dbg.querySelectorAll('.f').forEach(n=>n.remove());
    p.faces.forEach(f=>{const d=document.createElement('div');d.className='f';d.style.cssText='left:'+f[0]+'px;top:'+f[1]+'px;width:'+(f[2]-f[0])+'px;height:'+(f[3]-f[1])+'px';dbg.appendChild(d)});
    const s=dbg.querySelector('.s');s.style.cssText='left:170px;width:620px;top:'+(D.mise.subY-50)+'px;height:100px'}
}
let tFit=false;document.fonts.ready.then(()=>{subs.forEach(o=>{const w=o.el.offsetWidth;if(w>760)o.el.style.fontSize=(46*700/w).toFixed(1)+'px'})});
