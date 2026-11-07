// Exercises validation and permission boundaries before SQL access.
import assert from 'node:assert/strict';
const base=process.env.INVENTORY_URL??'http://127.0.0.1:5080';
const reader=process.env.Inventory__ReaderKey, editor=process.env.Inventory__EditorKey;
if(!reader || !editor)throw new Error('Set the same two demo keys as the API.');
async function check(method,path,token,body,status,code){
  const response=await fetch(base+path,{method,headers:{
    ...(token?{Authorization:'Bearer '+token}:{}),
    ...(body?{'Content-Type':'application/json'}:{}),
  },body:body?JSON.stringify(body):undefined});
  assert.equal(response.status,status);
  assert.equal((await response.json()).code,code);
  if(status===401)assert.equal(response.headers.get('www-authenticate'),'Bearer');
}
await check('GET','/api/items',null,null,401,'sign_in_required');
await check('GET','/api/items','invalid',null,401,'sign_in_required');
await check('POST','/api/items',reader,{},403,'write_forbidden');
await check('POST','/api/items',editor,{sku:'INVALID SKU',quantity:-1},400,'invalid_item');
await check('POST','/api/items/1/archive',editor,{version:'invalid'},400,'invalid_version');
await check('GET','/api/items?before=-1',reader,null,400,'invalid_filter');
console.log('Passed missing/invalid credentials, reader mutation rejection, and invalid item, version and cursor.');
