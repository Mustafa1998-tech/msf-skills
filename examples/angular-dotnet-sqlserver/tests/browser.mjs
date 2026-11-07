// Browser checks against simulated HTTP responses; use smoke.mjs for real SQL integration.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PLAYWRIGHT_MODULE??'playwright');
const launch=process.env.CHROMIUM_EXECUTABLE?{executablePath:process.env.CHROMIUM_EXECUTABLE}:{};
const browser=await chromium.launch(launch);
try{
  const page=await browser.newPage({viewport:{width:390,height:844}});
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  let archived=false, failNextSave=true;
  const row={id:1,sku:'WT-031',nameAr:'مفتاح عزم',nameEn:'Torque wrench',categoryCode:'TOOLS',quantity:14,version:'AAAAAAAAAAE='};
  await page.route('**/api/**',async route=>{
    const request=route.request();
    assert.equal(request.headers().authorization,'Bearer synthetic-browser-key');
    const url=new URL(request.url());
    if(url.pathname==='/api/categories'){
      await route.fulfill({json:[{code:'TOOLS',nameAr:'الأدوات',nameEn:'Tools'}]});
    }else if(request.method()==='GET' && url.pathname==='/api/items'){
      const requestedArchived=url.searchParams.get('archived')==='true';
      const query=url.searchParams.get('q')??'';
      const category=url.searchParams.get('category')??'';
      await route.fulfill({json:requestedArchived===archived && (!query || query===row.sku) && (!category || category===row.categoryCode)?[{...row,archived}]:[]});
    }else if(request.method()==='PUT'){
      assert.equal(request.postDataJSON().version,row.version);
      if(failNextSave){failNextSave=false;await route.fulfill({status:409,json:{code:'item_conflict'}});}
      else{row.quantity=request.postDataJSON().quantity;await route.fulfill({json:{...row,archived}});}
    }else if(url.pathname==='/api/items/1/archive' || url.pathname==='/api/items/1/restore'){
      assert.equal(request.postDataJSON().version,row.version);
      archived=url.pathname.endsWith('/archive');
      await route.fulfill({json:{...row,archived}});
    }else{
      await route.fulfill({status:404,json:{code:'unexpected_error'}});
    }
  });
  await page.goto(process.env.INVENTORY_WEB_URL??'http://127.0.0.1:4200');
  assert.equal(await page.locator('html').getAttribute('dir'),'rtl');
  await page.getByLabel('مفتاح العرض المحلي').fill('synthetic-browser-key');
  await page.getByRole('button',{name:'اتصال',exact:true}).click();
  await page.getByRole('rowheader',{name:row.sku}).waitFor();
  await page.getByRole('button',{name:'English'}).click();
  assert.equal(await page.locator('html').getAttribute('dir'),'ltr');
  await page.getByRole('button',{name:'Category All categories'}).focus();
  await page.keyboard.press('Enter');
  await page.getByLabel('Search categories by name or code').fill('TOOLS');
  await page.getByRole('button',{name:'Tools · TOOLS'}).click();
  await page.getByLabel('Search items').fill('bad-match');
  await page.getByRole('button',{name:'Apply filters'}).click();
  await page.getByText('No matching items.',{exact:false}).waitFor();
  await page.getByLabel('Search items').fill(row.sku);
  await page.getByRole('button',{name:'Apply filters'}).click();
  await page.getByRole('button',{name:'Edit '+row.sku}).click();
  await page.getByRole('spinbutton',{name:'Quantity'}).fill('18');
  await page.getByRole('button',{name:'Save',exact:true}).click();
  await page.getByRole('alert').getByText('The item or its status changed.',{exact:false}).waitFor();
  await page.getByRole('button',{name:'Cancel'}).click();
  await page.getByRole('button',{name:'Archive '+row.sku}).click();
  await page.getByRole('dialog').getByRole('button',{name:'Archive',exact:true}).click();
  await page.getByText('Item archived.').waitFor();
  await page.getByRole('button',{name:'Archived items',exact:true}).click();
  await page.getByRole('button',{name:'Restore '+row.sku}).click();
  await page.getByRole('dialog').getByRole('button',{name:'Restore',exact:true}).click();
  await page.getByText('Item restored.').waitFor();
  assert.deepEqual(errors,[]);
  console.log('Passed Angular RTL/LTR, search, category dialog, conflict feedback, archive and restore (simulated API).');
}finally{await browser.close();}
