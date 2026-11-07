import assert from 'node:assert/strict';
import {randomBytes} from 'node:crypto';

const base=process.env.INVENTORY_URL??'http://127.0.0.1:5080';
const reader=process.env.Inventory__ReaderKey;
const editor=process.env.Inventory__EditorKey;
if(!reader || !editor)throw new Error('Set Inventory__ReaderKey and Inventory__EditorKey for the local API');
const code='TEST-'+randomBytes(5).toString('hex').toUpperCase();
let created;
async function request(method,path,token,body,expected){
  const res=await fetch(base+path,{method,headers:{
    ...(token?{Authorization:'Bearer '+token}:{}),
    ...(body?{'Content-Type':'application/json'}:{}),
  },body:body?JSON.stringify(body):undefined});
  const result=await res.json();
  assert.equal(res.status,expected,method+' '+path+': '+JSON.stringify(result));
  return result;
}
const item={sku:code,nameAr:'قطعة اختبار',nameEn:'Test part',categoryCode:'TOOLS',quantity:4};
try{
  await request('GET','/health/ready',null,null,200);
  assert.equal((await request('GET','/api/items',null,null,401)).code,'sign_in_required');
  assert.equal((await request('POST','/api/items',reader,item,403)).code,'write_forbidden');
  assert.equal((await request('POST','/api/items',editor,{...item,quantity:-1},400)).code,'invalid_item');
  created=await request('POST','/api/items',editor,item,201);
  assert.equal((await request('POST','/api/items',editor,item,409)).code,'sku_exists');
  assert.equal((await request('GET','/api/items?q='+encodeURIComponent(code),reader,null,200)).some(row=>row.id===created.id),true);
  assert.deepEqual(await request('GET','/api/items?q='+encodeURIComponent("' OR 1=1 --"),reader,null,200),[]);
  const id='/api/items/'+created.id;
  const original=created.version;
  created=await request('PUT',id,editor,{...item,quantity:8,version:original},200);
  assert.equal(created.quantity,8);
  assert.notEqual(created.version,original);
  assert.equal((await request('PUT',id,editor,{...item,version:original},409)).code,'item_conflict');
  created=await request('POST',id+'/archive',editor,{version:created.version},200);
  assert.equal(created.archived,true);
  assert.deepEqual(await request('GET','/api/items?q='+code,reader,null,200),[]);
  assert.equal((await request('GET','/api/items?archived=true&q='+code,reader,null,200))[0].id,created.id);
  assert.equal((await request('PUT',id,editor,{...item,version:created.version},409)).code,'item_conflict');
  created=await request('POST',id+'/restore',editor,{version:created.version},200);
  assert.equal(created.archived,false);
  console.log('Passed readiness, auth, validation, create, duplicate, literal search, stale edit, archive and restore.');
}finally{
  if(created && !created.archived){
    await request('POST','/api/items/'+created.id+'/archive',editor,{version:created.version},200);
  }
}
