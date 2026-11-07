import {Component, provideZonelessChangeDetection, signal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {bootstrapApplication} from '@angular/platform-browser';
import {ar, en} from './copy';

type Category={code:string;nameAr:string;nameEn:string};
type Draft={sku:string;nameAr:string;nameEn:string;categoryCode:string;quantity:number|null;version?:string};
type Item=Draft & {id:number;archived:boolean;version:string};
type CopyKey=keyof typeof ar;
class ApiError extends Error {constructor(readonly code:string){super(code);}}

@Component({
  selector:'inventory-root',
  imports:[FormsModule],
  templateUrl:'./inventory.html'
})
class Inventory {
  readonly language=signal<'ar'|'en'>('ar');
  readonly connected=signal(false);
  readonly busy=signal(false);
  readonly saving=signal(false);
  readonly items=signal<Item[]>([]);
  readonly categories=signal<Category[]>([]);
  readonly error=signal<CopyKey|null>(null);
  readonly actionError=signal<CopyKey|null>(null);
  readonly notice=signal<CopyKey|null>(null);
  readonly mode=signal<'add'|'edit'|'archive'|'restore'>('add');
  readonly current=signal<Item|null>(null);
  private token='';
  key='';
  search='';
  category='';
  archived=false;
  before:number|undefined;
  categorySearch='';
  pickingForDraft=false;
  draft:Draft=this.emptyDraft();
  t(key:CopyKey){return (this.language()==='ar'?ar:en)[key];}
  label(item:{nameAr:string;nameEn:string}){return this.language()==='ar'?item.nameAr:item.nameEn;}
  categoryLabel(code:string){const found=this.categories().find(category=>category.code===code);return found?this.label(found):code;}
  number(value:number|null){return value===null?'—':new Intl.NumberFormat(this.language()==='ar'?'ar-SA':'en').format(value);}
  toggleLanguage(){
    this.language.update(value=>value==='ar'?'en':'ar');
    document.documentElement.lang=this.language();
    document.documentElement.dir=this.language()==='ar'?'rtl':'ltr';
    document.title=this.t('brand')+' — '+this.t('title');
  }
  private async request<T>(path:string,method='GET',body?:unknown):Promise<T>{
    const res=await fetch('/api/'+path,{method,headers:{Authorization:'Bearer '+this.token,
      ...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined});
    if(!res.ok){const problem=await res.json().catch(()=>null);throw new ApiError(problem?.code??'unexpected_error');}
    return await res.json() as T;
  }
  private asCopy(reason:unknown):CopyKey{
    return reason instanceof ApiError && Object.hasOwn(ar,reason.code)?reason.code as CopyKey:'unexpected_error';
  }
  async connect(){
    if(this.busy())return;
    this.token=this.key.trim();this.key='';this.error.set(null);this.busy.set(true);
    try{
      this.categories.set(await this.request<Category[]>('categories'));
      this.items.set(await this.request<Item[]>('items'));
      this.connected.set(true);
    }catch(reason){this.token='';this.error.set(this.asCopy(reason));}
    finally{this.busy.set(false);}
  }
  disconnect(){
    if(this.busy() || this.saving())return;
    this.token='';this.connected.set(false);this.items.set([]);this.categories.set([]);
    this.before=undefined;this.archived=false;this.category='';this.search='';
    this.error.set(null);this.notice.set(null);
  }
  async load(before?:number){
    if(this.busy())return;
    this.busy.set(true);this.error.set(null);
    const params=new URLSearchParams({q:this.search.trim(),category:this.category,archived:String(this.archived)});
    if(before)params.set('before',String(before));
    try{this.items.set(await this.request<Item[]>('items?'+params));this.before=before;}
    catch(reason){this.error.set(this.asCopy(reason));this.items.set([]);}
    finally{this.busy.set(false);}
  }
  selectArchive(archived:boolean){if(this.busy())return;this.archived=archived;this.notice.set(null);void this.load();}
  older(){const rows=this.items();if(rows.length===25)void this.load(rows[24].id);}
  options(){
    const query=this.categorySearch.trim().toLowerCase();
    return this.categories().filter(category=>[category.code,category.nameAr,category.nameEn].join(' ').toLowerCase().includes(query));
  }
  showCategories(dialog:HTMLDialogElement,forDraft:boolean){
    this.categorySearch='';this.pickingForDraft=forDraft;dialog.showModal();
  }
  selectCategory(dialog:HTMLDialogElement,code:string){
    if(this.pickingForDraft)this.draft.categoryCode=code;else this.category=code;
    dialog.close();
  }
  emptyDraft():Draft{return {sku:'',nameAr:'',nameEn:'',categoryCode:'',quantity:0};}
  openAction(dialog:HTMLDialogElement,mode:'add'|'edit'|'archive'|'restore',row:Item|null=null){
    this.mode.set(mode);this.current.set(row);this.actionError.set(null);
    this.draft=row?{sku:row.sku,nameAr:row.nameAr,nameEn:row.nameEn,categoryCode:row.categoryCode,quantity:row.quantity,version:row.version}:this.emptyDraft();
    dialog.showModal();
  }
  async submit(dialog:HTMLDialogElement){
    if(this.saving())return;
    this.saving.set(true);this.actionError.set(null);
    const row=this.current(), mode=this.mode();
    let message:CopyKey='saved';
    try{
      if(mode==='add')await this.request('items','POST',this.draft);
      else if(mode==='edit' && row)await this.request('items/'+row.id,'PUT',this.draft);
      else if((mode==='archive'||mode==='restore') && row){
        await this.request('items/'+row.id+'/'+mode,'POST',{version:row.version});
        message=mode==='archive'?'archivedOk':'restoredOk';
      }
      dialog.close();
      await this.load(this.before);
      this.notice.set(message);
      document.getElementById('item-list-heading')?.focus();
    }catch(reason){this.actionError.set(this.asCopy(reason));}
    finally{this.saving.set(false);}
  }
}
bootstrapApplication(Inventory,{providers:[provideZonelessChangeDetection()]}).catch(console.error);
