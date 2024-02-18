var renderUIComponents=[];renderUIComponents.push(()=>{return new Promise((resolve,reject)=>{document.querySelectorAll("input.ui\\:input[type]:not(.ui\\:ignore)").forEach(input=>{if(input.isRendered||input.getAttribute("is-rendered"))return;switch(input.getAttribute("type").toUpperCase()){case"TEXT":break;case"PASSWORD":break;case"RANGE":break;case"CHECKBOX":break;default:return;}
input.addEventListener("keydown",e=>{if(e.key==="Escape"){document.activeElement.blur()}})
input.isRendered=true;input.setAttribute("is-rendered",true);})
resolve();})})
renderUIComponents.push(()=>{return new Promise((resolve,reject)=>{document.querySelectorAll(".ui\\:alert:not(.ui\\:ignore)").forEach(alert=>{if(alert.isRendered||alert.getAttribute("is-rendered"))return;const alertFill=document.createElement("div");alertFill.classList.add("fill");alert.appendChild(alertFill);switch(alert.getAttribute("type").toUpperCase().trim()){case"ALERT":innerHTMLToElement(`<div class="content">
                            <h2 class="title">
                                This page says:
                            </h2>
                            <p class="message">
                                Default alert message!
                            </p>
                            <div class="actions">
                                <button type="text" class="OK"> OK </button>
                            </div>
                        </div>`.trim()).then(html=>alert.appendChild(html));break;case"PROMPT":innerHTMLToElement(`<div class="content">
                            <h2 class="title">
                                This page says:
                            </h2>
                            <p class="message"></p>
                            <input type="text" class="input">
                            <div class="actions">
                                <button type="text" class="OK"> OK </button>
                                <button type="text" class="CANCEL"> CANCEL </button>
                            </div>
                        </div>`).then(html=>alert.appendChild(html));break;case"CONFIRM":innerHTMLToElement(`<div class="content">
                            <h2 class="title">
                                This page says:
                            </h2>
                            <p class="message"></p>
                            <div class="actions">
                                <button type="text" class="OK"> OK </button>
                                <button type="text" class="CANCEL"> CANCEL </button>
                            </div>
                        </div>`).then(html=>alert.appendChild(html));break;default:return reject(`Invalid parameter for 'type' attribute; excepted 'ALERT', 'PROMPT', or 'CONFIRM' but received '${alert.getAttribute("type")}'`);}
alert.isRendered=true;alert.setAttribute("is-rendered","");})
resolve();})})
const PageAlerts={alert:(message,title,width=512)=>{return new Promise((resolve,reject)=>{PageAlerts.closeAllAlerts();if(!new ValidationObject(message).validateExplicitHTML(["b","a","i","u"]))return reject(`Invalid HTML Tag detected in alert`);const alertDialog=document.querySelector("div.ui\\:alert#alert\\:alert");alertDialog.querySelector("p.message").innerHTML=message;alertDialog.querySelector("h2.title").innerText=title;alertDialog.querySelector(".content").style.width=width+"px";alertDialog.setAttribute("visible","");const dialogOK=alertDialog.querySelector(".actions>button.OK");Application.States.Window.focusedWindow.setValue("HIDDEN");dialogOK.focus();const OKDialog=()=>{dialogOK.removeEventListener("click",OKDialog);alertDialog.removeAttribute("visible");resolve(true);}
dialogOK.addEventListener("click",OKDialog)})},confirm:(message)=>{return new Promise((resolve,reject)=>{Application.States.Window.focusedWindow.setValue("HIDDEN");})},prompt:(message,validate=()=>{})=>{return new Promise((resolve,reject)=>{Application.States.Window.focusedWindow.setValue("HIDDEN");})},closeAllAlerts(){document.querySelectorAll(".ui\\:alert").forEach(alert=>alert.removeAttribute("visible"))},createDialog(options={fill:true,moveable:true,id:null,title:"",width:640},htmlContent=()=>document.createElement("div")){const dialog=document.createElement("dialog");dialog.classList.add("ui:dialog");if(options.id)dialog.id=options.id;if(options.fill)dialog.setAttribute("fill","");if(options.moveable)dialog.setAttribute("moveable","");const closeDialog=(_confirm=true)=>{dialog.classList.remove("visible");dialog.removeAttribute("visible");document.removeEventListener("keydown",handleKeyDown)}
const showDialog=()=>{Application.States.Window.focusedWindow.setValue("HIDDEN");dialog.classList.add("visible");dialog.setAttribute("visible","");}
const dialogWidth=options.width||640;const dialogTitle=options.title||"";const dialogFill=setDefault(options.fill,true);const dialogMoveable=setDefault(options.moveable,true);const dialogChildren=htmlContent();const dialogContent=document.createElement("div");dialogContent.classList.add("content");dialogContent.style.width=`${dialogWidth}px`;const dialogHeader=document.createElement("div");dialogHeader.classList.add("header");dialogHeader.innerHTML=`<span class="title">${dialogTitle}</span><i icon class="close"> close </i>`;const dialogClose=dialogHeader.querySelector("i.close:last-child");dialogClose.addEventListener("click",()=>closeDialog());const dialogBody=document.createElement("div");dialogBody.classList.add("body");if(dialogFill){const dialogBackground=document.createElement("div");dialogBackground.classList.add("fill");dialog.appendChild(dialogBackground);}
dialogChildren.forEach(c=>dialogBody.appendChild(c));dialogContent.appendChild(dialogHeader);dialogContent.appendChild(dialogBody);dialog.appendChild(dialogContent);document.body.appendChild(dialog);if(dialogMoveable){$(dialogContent).draggable({handle:dialogHeader,containment:"parent"})}
const handleKeyDown=e=>{if(e.key==="Escape"&&(e.shiftKey||[dialog,dialogContent,dialogHeader,dialogBody].includes(document.activeElement))){closeDialog(!e.shiftKey);}};document.addEventListener("keydown",handleKeyDown)
return{show:()=>{return new Promise((resolve,reject)=>{Application.States.Window.focusedWindow.setValue("HIDDEN");showDialog();resolve();})},hide:(forceClose=false)=>{return new Promise((resolve,reject)=>{closeDialog(!forceClose);resolve();})}}}}
function updateUI(){return new Promise(async(resolve,reject)=>{for(const promise of renderUIComponents){await promise();};resolve();})}
preLoadedEventList.push(()=>{return updateUI();})