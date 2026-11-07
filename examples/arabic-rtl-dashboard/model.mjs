export const hubs = {
  ruh: {ar:'الرياض', en:'Riyadh', code:'RUH'},
  jed: {ar:'جدة', en:'Jeddah', code:'JED'},
  dmm: {ar:'الدمام', en:'Dammam', code:'DMM'},
  med: {ar:'المدينة المنورة', en:'Madinah', code:'MED'},
};
export const rows = [
  ['MC-4182','ruh','moving',9,'معدات طبية','Medical supplies'],
  ['MC-4181','jed','delayed',8,'قطع غيار','Spare parts'],
  ['MC-4180','dmm','delivered',7,'أجهزة قياس','Measuring equipment'],
  ['MC-4179','ruh','delivered',7,'مواد تغليف','Packaging materials'],
  ['MC-4178','med','moving',7,'معدات السلامة','Safety equipment'],
  ['MC-4177','jed','moving',4,'أدوات صيانة','Maintenance tools'],
  ['MC-4176','ruh','moving',3,'الأجهزة الطرفية','Peripherals'],
  ['MC-4175','dmm','delivered',2,'مستلزمات مكتبية','Office supplies'],
  ['MC-4174','med','delivered',1,'مكونات إلكترونية','Electronic components'],
].map(([id,hub,status,day,ar,en])=>({id,hub,status,day,ar,en}));

export function normalize(value) {
  return String(value).toLowerCase().normalize('NFKD').replace(/[\u0640\u064b-\u065f\u0670]/g,'').trim();
}
export function selectRows(items, {query='',hub='',status='',sort='desc'} = {}) {
  const key = normalize(query);
  return items.filter(row => (!hub || row.hub === hub) && (!status || row.status === status)
    && normalize([row.id,row.ar,row.en,...Object.values(hubs[row.hub])].join(' ')).includes(key))
    .sort((a,b) => sort === 'asc' ? a.day - b.day || a.id.localeCompare(b.id) : b.day - a.day || b.id.localeCompare(a.id));
}
export function counts(items) {
  const totals = {total:items.length,moving:0,delivered:0,delayed:0};
  for (const item of items) totals[item.status]++;
  return totals;
}
