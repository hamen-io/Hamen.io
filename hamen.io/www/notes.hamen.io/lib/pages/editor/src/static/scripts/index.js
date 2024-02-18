function UUID(){return"10000000-1000-4000-8000-100000000000".replace(/[018]/g,c=>(c^crypto.getRandomValues(new Uint8Array(1))[0]&15>>c/4).toString(16));}
class SubscriptionList{constructor(){this._subscriptions={};}
subscribe(callback){let ID="";do{ID=UUID();}while(Object.keys(this._subscriptions).includes(ID));this._subscriptions[ID]=callback;return ID;}
unsubscribe(identifier){if(typeof identifier==="string"){delete this._subscriptions[identifier];}else{const targetID=Object.entries(this._subscriptions).find((id,callback)=>callback===identifier);if(targetID){delete this._subscriptions[targetID[0]]}}}
trigger(...args){Object.values(this._subscriptions).forEach(c=>c(...args))}}
class State{constructor(initialValue,options={isConstant:false,fixedType:false,onChange:[]}){this._projectedValue=initialValue;this.isConstant=useDefault(options.isConstant,false);this.fixedType=useDefault(options.fixedType,false);this.onChange=new SubscriptionList();options.onChange.forEach(callback=>this.onChange.subscribe(callback));}
getValue(){return this._projectedValue}
setValue(value){if(this.fixedType&&typeof value!==typeof(this.getValue()))throw`Cannot re-assign constant state.`;this.onChange.trigger(value,this._projectedValue);this._projectedValue=value;}}
class Module{constructor({moduleName,moduleAuthor,moduleVersion,modulePermissions}){this.uniqueID=UUID();this.moduleName={_x:moduleName,get x(){return _x},set x(v){if(typeof v!=="string"){console.error(`Error: Module<${uniqueID}> has an invalid type for the name: "${typeof v}" ; provided value: '${v}'`);}else if(4>v.length>64){console.error(`Error: Module<${uniqueID}> has an invalid length for the name; names should be between 4 and 64 characters (inclusive) but provided value has a length of: ${v.length}`);}else{_x=v;}}};this.moduleAuthor=moduleAuthor;this.moduleVersion=moduleVersion;this.modulePermissions=modulePermissions;}}
class Registry{constructor(){this._values=[];}
register(_){this._values.push(_)}
unregister(_){this._values.filter(c=>c!=_);}
get values(){return this._values}}
class EventList{constructor(eventNames=[]){this._events={};eventNames.forEach(ev=>this._events[ev]=[]);}
addEventListener(eventName,callback){if(this._events[eventName]){this._events[eventName].push(callback)}else{Console}}}
class Keycode{constructor(key,{ctrlKey=false,altKey=false,shiftKey=false,metaKey=false}){this.key=key;this.ctrlKey=ctrlKey;this.altKey=altKey;this.shiftKey=shiftKey;this.metaKey=metaKey;}
compareTo(key){return key.altKey===this.altKey&&key.ctrlKey===this.ctrlKey&&key.key===this.key&&key.metaKey===this.metaKey&&key.shiftKey===this.shiftKey;}}
class HotkeyList{constructor(){this.keyCodeList=[]}
contains(key){return!(this.keyCodeList.filter(k=>k.compareTo(key)).length===0)}
registerHotkey(operatingSystem,conditions={key:"",ctrlKey:false,altKey:false,shiftKey:false,metaKey:false},callback=()=>{},onlyIf=()=>true){if(operatingSystem==="MAC"&&window.navigator.platform.toLowerCase().startsWith("mac")||!window.navigator.platform.toLowerCase().startsWith("mac")){this.keyCodeList.push(new Keycode(conditions.key,{altKey:useDefault(conditions.altKey,false),ctrlKey:useDefault(conditions.ctrlKey,false),shiftKey:useDefault(conditions.shiftKey,false),metaKey:useDefault(conditions.metaKey,false)}))
window.addEventListener("keydown",e=>{if(e.key===conditions.key&&e.shiftKey===(conditions.shiftKey===true?true:false)&&e.altKey===(conditions.altKey===true?true:false)&&e.ctrlKey===(conditions.ctrlKey===true?true:false)&&e.metaKey===(conditions.metaKey===true?true:false)&&onlyIf()){callback();e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();}})}}}
var Application={Modules:new Registry(),Events:{Editor:{onDocumentRename:new SubscriptionList(),onFullscreen:new SubscriptionList(),},Application:{onActionMenuExpand:new SubscriptionList()},Window:{onLoad:new SubscriptionList()}},UI:{Elements:{},Regions:{}},Common:{},States:{Window:{focusedWindow:new State("HIDDEN",{onChange:[(nV)=>{document.querySelectorAll(`.window`).forEach(win=>nV===win.getAttribute("win-id")?win.classList.add("focused"):win.classList.remove("focused"))}]})}},Document:{newDocument(){},openDocument(){},saveDocument(){},saveDocumentAs(){}},FileSystem:{listGroup(root){},createGroup(){},removeGroup(){},renameGroup(){}},Editor:undefined,Keyboard:{Hotkeys:new HotkeyList()}}
class Accents extends Module{constructor(){super({moduleName:"Accents",moduleAuthor:"Hamen.io",moduleVersion:[1,0,0],modulePermissions:[]})}}
Application.Modules.register(Accents);