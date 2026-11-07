import { rows, hubs, normalize, counts, selectRows } from './model.mjs';

const copy = {
  ar:{skip:'انتقل إلى المحتوى',brand:'مِرْصاد',product:'مكتب متابعة الشحنات',theme:'الوضع الداكن',demo:'بيانات تجريبية',title:'متابعة الشحنات',lede:'راجع حركة الشحنات وتابع الحالات التي تحتاج إلى تدخل.',period:'فترة العرض',kpis:'مؤشرات الشحنات',total:'إجمالي الشحنات',moving:'قيد النقل',delivered:'تم التسليم',delayed:'متأخرة',activity:'تسجيل الشحنات',chartIntro:'عدد الشحنات المسجلة حسب المجموعة الزمنية',watchLabel:'تنبيه تشغيلي',watchTitle:'شحنات تحتاج إلى متابعة',watchDetail:'شحنة واحدة متأخرة عن موعدها. افتح سجل الشحنات لمراجعة تفاصيلها.',showDelayed:'عرض الشحنات المتأخرة',ledger:'سجل الشحنات',ledgerDetail:'ابحث برقم الشحنة أو المحتوى أو مركز الشحن.',reset:'مسح البحث والتصفية',search:'بحث',placeholder:'مثال: الرياض أو \u2066MC-4182\u2069',status:'الحالة',allStatuses:'كل الحالات',hub:'مركز الشحن',allHubs:'كل المراكز',reference:'رقم الشحنة',contents:'المحتوى',registered:'تاريخ التسجيل',details:'التفاصيل',tableHint:'مرّر الجدول أفقياً لعرض كل الأعمدة.',pagination:'صفحات السجل',prev:'السابق',next:'التالي',footer:'مرصاد · نموذج تدريبي ببيانات اصطناعية',chooseHub:'اختر مركز الشحن',close:'إغلاق',searchHub:'ابحث عن مركز أو رمزه',noHubs:'لا توجد مراكز مطابقة. غيّر عبارة البحث.',empty:'لا توجد شحنات مطابقة. غيّر البحث أو امسح التصفية.',result:'الشحنات المطابقة:',of:'من',view:'عرض'},
  en:{skip:'Skip to content',brand:'Mirsad',product:'Dispatch desk',theme:'Dark mode',demo:'Demo data',title:'Shipment monitor',lede:'Review shipment activity and follow up on exceptions.',period:'Reporting period',kpis:'Shipment indicators',total:'Total shipments',moving:'In transit',delivered:'Delivered',delayed:'Delayed',activity:'Shipment registrations',chartIntro:'Shipments registered per time bucket',watchLabel:'Operations alert',watchTitle:'Shipments to follow up',watchDetail:'One shipment is past its due date. Open the ledger to review the details.',showDelayed:'View delayed shipments',ledger:'Shipment ledger',ledgerDetail:'Search by shipment ID, contents or dispatch hub.',reset:'Clear search and filters',search:'Search',placeholder:'e.g. Riyadh or MC-4182',status:'Status',allStatuses:'All statuses',hub:'Dispatch hub',allHubs:'All hubs',reference:'Shipment ID',contents:'Contents',registered:'Registered on',details:'Details',tableHint:'Scroll the table horizontally to see all columns.',pagination:'Ledger pages',prev:'Previous',next:'Next',footer:'Mirsad · Training example with synthetic data',chooseHub:'Choose a dispatch hub',close:'Close',searchHub:'Search by hub name or code',noHubs:'No matching hubs. Try a different search.',empty:'No matching shipments. Change the search or clear the filters.',result:'Matching shipments:',of:'of',view:'View'}
};
const $ = id => document.getElementById(id);
let lang='ar', theme='light';
const state={query:'',hub:'',status:'',sort:'desc',page:1};
const totals=counts(rows);
const pageSize=5;
const t=key=>copy[lang][key];
const locale=()=>lang==='ar'?'ar-SA-u-ca-gregory-nu-arab':'en-GB';
const n=value=>new Intl.NumberFormat(locale()).format(value);
const date=day=>new Intl.DateTimeFormat(locale(),{day:'numeric',month:'short',timeZone:'UTC'}).format(new Date(Date.UTC(2026,8,day)));
function element(tag, value, className) {
  const el=document.createElement(tag);
  if(value!==undefined)el.textContent=value;
  if(className)el.className=className;
  return el;
}
function idNode(id){const node=element('bdi',id);node.dir='ltr';return node;}
function renderChart(){
  const groups=[[1,3],[4,6],[7,9]];
  const values=groups.map(([from,to])=>rows.filter(row=>row.day>=from && row.day<=to).length);
  const ns='http://www.w3.org/2000/svg';
  const svg=document.createElementNS(ns,'svg');
  svg.setAttribute('viewBox','0 0 520 105');svg.setAttribute('aria-hidden','true');
  function part(tag,attrs,value){
    const node=document.createElementNS(ns,tag);
    Object.entries(attrs).forEach(([key,v])=>node.setAttribute(key,v));
    if(value!==undefined)node.textContent=value;
    svg.append(node);
  }
  for(const tick of [0,2,4,6]){
    const y=86-tick*11;
    part('line',{x1:45,x2:475,y1:y,y2:y,class:'axis'});
    part('text',{x:lang==='ar'?500:20,y:y+4,'text-anchor':'middle'},n(tick));
  }
  const x=i=>lang==='ar'?459-i*199:61+i*199;
  const y=i=>86-values[i]*11;
  part('polyline',{points:values.map((_,i)=>x(i)+','+y(i)).join(' '),class:'series'});
  groups.forEach(([from,to],i)=>{
    part('circle',{cx:x(i),cy:y(i),r:4});part('text',{x:x(i),y:103,'text-anchor':'middle'},n(from)+'\u200e–'+n(to));
  });
  $('chart').replaceChildren(svg);
  $('chart-summary').textContent=groups.map(([from,to],i)=>date(from)+' – '+date(to)+': '+n(values[i])).join(' · ');
}
function renderOptions(){
  const query=normalize($('hub-search').value);
  const options=[['',{ar:copy.ar.allHubs,en:copy.en.allHubs,code:''}],...Object.entries(hubs)]
    .filter(([,hub])=>normalize([hub.ar,hub.en,hub.code].join(' ')).includes(query));
  $('hub-options').replaceChildren(...options.map(([key,hub])=>{
    const button=element('button',hub[lang]);button.type='button';
    if(hub.code)button.append(' · ',idNode(hub.code));
    button.setAttribute('aria-pressed',String(state.hub===key));
    button.addEventListener('click',()=>{state.hub=key;state.page=1;renderRows();$('hub-dialog').close();});
    return button;
  }));
  $('hub-empty').hidden=options.length>0;
}
function openDetail(row){
  const dialog=$('detail-dialog');
  const fields=[['reference',idNode(row.id)],['contents',row[lang]],['hub',hubs[row.hub][lang]],['status',t(row.status)],['registered',date(row.day)]];
  $('detail-body').replaceChildren(...fields.flatMap(([key,value])=>{
    const dd=element('dd');dd.append(value);return [element('dt',t(key)),dd];
  }));
  dialog.showModal();
}
function renderRows(){
  const visible=selectRows(rows,state);
  const pages=Math.max(1,Math.ceil(visible.length/pageSize));
  state.page=Math.min(pages,state.page);
  $('results').textContent=t('result')+' '+n(visible.length);
  $('hub-current').textContent=state.hub?hubs[state.hub][lang]:t('allHubs');
  $('sort-head').setAttribute('aria-sort',state.sort==='asc'?'ascending':'descending');
  $('sort-icon').textContent=state.sort==='asc'?'↑':'↓';
  $('page-number').textContent=n(state.page)+' '+t('of')+' '+n(pages);
  $('prev').disabled=state.page===1;$('next').disabled=state.page===pages;
  const trs=visible.slice((state.page-1)*pageSize,state.page*pageSize).map(row=>{
    const tr=element('tr');const th=element('th');th.scope='row';th.append(idNode(row.id));
    const badge=element('span',t(row.status),'badge '+row.status);const status=element('td');status.append(badge);
    const action=element('button',t('view'),'row-action');action.type='button';
    action.setAttribute('aria-label',t('view')+' '+row.id);action.addEventListener('click',()=>openDetail(row));
    const detail=element('td');detail.append(action);
    tr.append(th,element('td',row[lang]),element('td',hubs[row.hub][lang]),status,element('td',date(row.day)),detail);
    return tr;
  });
  if(!trs.length){const tr=element('tr');const td=element('td',t('empty'));td.colSpan=6;tr.append(td);trs.push(tr);}
  $('table-body').replaceChildren(...trs);
}
function render(){
  const root=document.documentElement;
  root.lang=lang;root.dir=lang==='ar'?'rtl':'ltr';root.dataset.theme=theme;
  document.title=t('brand')+' — '+t('title');
  document.querySelectorAll('[data-i18n]').forEach(el=>el.textContent=t(el.dataset.i18n));
  document.querySelectorAll('[data-label]').forEach(el=>el.setAttribute('aria-label',t(el.dataset.label)));
  document.querySelectorAll('[data-placeholder]').forEach(el=>el.placeholder=t(el.dataset.placeholder));
  $('language').textContent=lang==='ar'?'English':'العربية';
  $('language').lang=lang==='ar'?'en':'ar';$('language').dir=lang==='ar'?'ltr':'rtl';
  $('theme').setAttribute('aria-pressed',String(theme==='dark'));
  $('period').textContent=date(1)+' – '+date(9);
  $('watch-detail').textContent=t('watchDetail');
  Object.entries(totals).forEach(([key,value])=>$('count-'+key).textContent=n(value));
  renderChart();renderRows();
}
$('theme').addEventListener('click',()=>{theme=theme==='light'?'dark':'light';document.documentElement.dataset.theme=theme;$('theme').setAttribute('aria-pressed',String(theme==='dark'));});
$('language').addEventListener('click',()=>{lang=lang==='ar'?'en':'ar';render();});
$('search').addEventListener('input',event=>{state.query=event.target.value;state.page=1;renderRows();});
$('status').addEventListener('change',event=>{state.status=event.target.value;state.page=1;renderRows();});
$('sort').addEventListener('click',()=>{state.sort=state.sort==='asc'?'desc':'asc';state.page=1;renderRows();});
function turnPage(delta,focusId){state.page+=delta;renderRows();if(document.activeElement?.disabled)$(focusId).focus();}
$('prev').addEventListener('click',()=>turnPage(-1,'next'));
$('next').addEventListener('click',()=>turnPage(1,'prev'));
$('reset').addEventListener('click',()=>{Object.assign(state,{query:'',hub:'',status:'',page:1});$('search').value='';$('status').value='';renderRows();$('search').focus();});
$('show-delayed').addEventListener('click',()=>{Object.assign(state,{query:'',hub:'',status:'delayed',page:1});$('search').value='';$('status').value='delayed';renderRows();$('ledger-title').focus();});
$('hub-button').addEventListener('click',()=>{$('hub-search').value='';renderOptions();$('hub-dialog').showModal();});
$('hub-search').addEventListener('input',renderOptions);
$('hub-dialog').addEventListener('close',()=>$('hub-button').focus());
render();
