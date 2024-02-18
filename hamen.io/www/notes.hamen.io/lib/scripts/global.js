function isEntity(value){return/&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-fA-F]{1,6});/ig.test(value)}
function formatChar(char){return{" ":"&nbsp;"}[char]||char;}
function useDefault(value,_default){return value===null?_default:value;}
const isset=value=>!(value===null||value===undefined);const setDefault=(value,defaultValue)=>isset(value)?value:defaultValue
function innerHTMLToElement(innerHTML){return new Promise((resolve,reject)=>{const div=document.createElement("div");div.innerHTML=innerHTML;if(div.children.length!==1)return reject("Cannot parse multiple elements as single elements; wrap your `innerHTML` string in a div or another element.");return resolve(Array.from(div.children)[0])})}
class ValidationObject{constructor(textContent=""){this.textContent=textContent;}
validateEmail(){return/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(this.textContent);}
validateExplicitHTML(tags=[],caseSensitive=false){tags=tags.map(t=>caseSensitive?t:t.toUpperCase()).map(t=>t.replace(/\W/g,/\W\1/g));const regex=new RegExp("<\\/?\\b(?!"+tags.join("|")+")\\w+\\b>","g"+(caseSensitive?"":"i"));return!regex.test(this.textContent)}}
class AppConsole{constructor(){}
log(...data){console.log(data)}
error(...data){console.error(...data)}
warn(...data){console.warn(...data)}
fatal(...data){console.error(...data);}}
const Console=new AppConsole();