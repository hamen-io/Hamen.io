/**
 * 
 */
var renderUIComponents = [];

/**
 * Creates the "ui:input" elements
 * 
 * Notes that each <input class="ui:input"> tag MUST contain a `type="..."` value or it will be ignored
 */
renderUIComponents.push(() => {
    return new Promise((resolve, reject) => {
        /**
         * Iterate through each `input` element
         * 
         * Note the selector, `input.ui\\:input[type]:not(.ui\\:ignore)` selects "input" elements that explicitly:
         * 1. Contain the `ui:input` class
         * 2. Contain the `type` attribute
         * 3. Do NOT contain the the "ui:ignore" class
         */
        document.querySelectorAll("input.ui\\:input[type]:not(.ui\\:ignore)").forEach(input => {
            // Skip if already rendered:
            if (input.isRendered || input.getAttribute("is-rendered")) return;

            switch (input.getAttribute("type").toUpperCase()) {
                case "TEXT":
                    break;
                case "PASSWORD":
                    break;
                case "RANGE":
                    break;
                case "CHECKBOX":
                    break;

                // Skip inputs without any `type` definition
                default:
                    return;
            }

            input.addEventListener("keydown", e => {
                if (e.key === "Escape") {
                    document.activeElement.blur()
                }
            })

            input.isRendered = true;
            input.setAttribute("is-rendered", true);
        })

        resolve();
    })
})

renderUIComponents.push(() => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll(".ui\\:alert:not(.ui\\:ignore)").forEach(alert => {
            if (alert.isRendered || alert.getAttribute("is-rendered")) return;

            const alertFill = document.createElement("div");
            alertFill.classList.add("fill");

            alert.appendChild(alertFill);

            switch (alert.getAttribute("type").toUpperCase().trim()) {
                case "ALERT":
                    innerHTMLToElement(
                        `<div class="content">
                            <h2 class="title">
                                This page says:
                            </h2>
                            <p class="message">
                                Default alert message!
                            </p>
                            <div class="actions">
                                <button type="text" class="OK"> OK </button>
                            </div>
                        </div>`
                            .trim()
                    )
                        .then(
                            html => 
                                alert.appendChild(html)
                        ); break;
                case "PROMPT":
                    innerHTMLToElement(
                        `<div class="content">
                            <h2 class="title">
                                This page says:
                            </h2>
                            <p class="message"></p>
                            <input type="text" class="input">
                            <div class="actions">
                                <button type="text" class="OK"> OK </button>
                                <button type="text" class="CANCEL"> CANCEL </button>
                            </div>
                        </div>`
                    )
                        .then(
                            html =>
                                alert.appendChild(html)
                        ); break;
                case "CONFIRM":
                    innerHTMLToElement(
                        `<div class="content">
                            <h2 class="title">
                                This page says:
                            </h2>
                            <p class="message"></p>
                            <div class="actions">
                                <button type="text" class="OK"> OK </button>
                                <button type="text" class="CANCEL"> CANCEL </button>
                            </div>
                        </div>`
                    )
                        .then(
                            html =>
                                alert.appendChild(html)
                        ); break;
                default:
                    return reject(`Invalid parameter for 'type' attribute; excepted 'ALERT', 'PROMPT', or 'CONFIRM' but received '${alert.getAttribute("type")}'`);
            }

            alert.isRendered = true;
            alert.setAttribute("is-rendered", "");
        })

        resolve();
    })
})

/**
 * @typedef {{ fill: boolean, moveable: boolean, id: string | null, title: string, width: number }} CreateDialogOptions
 * @typedef {{ show: () => Promise<any>, hide: ( forceClose: boolean = false ) => Promise<any> }} ActiveDialogActions
 */

/**
 * @global
 * 
 * @type {{
 *  alert: (message: string, title: string, width: number) => Promise<boolean>,
 *  createDialog: (options: CreateDialogOptions, htmlContent: () => HTMLElement) => ActiveDialogActions
 * }}
 */
const PageAlerts = {
    /**
     * 
     * @param {string} message The message to be displayed. No advanced syntax allowed other than <b>, <i>, <u>, and <br> (additionally, HTML entities can be displayed)
     * @returns {Promise<boolean>} Resolves when user clicks "OK". When `true`, the user clicked "OK", otherwise it was forced to close (for example, by `pageAlerts.closeAll()`)
     */
    alert: (message, title, width = 512) => {
        return new Promise((resolve, reject) => {
            PageAlerts.closeAllAlerts();

            if (!new ValidationObject(message).validateExplicitHTML(["b", "a", "i", "u"])) return reject(`Invalid HTML Tag detected in alert`);

            const alertDialog = document.querySelector("div.ui\\:alert#alert\\:alert");
            alertDialog.querySelector("p.message").innerHTML = message;
            alertDialog.querySelector("h2.title").innerText = title;
            alertDialog.querySelector(".content").style.width = width + "px";

            alertDialog.setAttribute("visible", "");
            const dialogOK = alertDialog.querySelector(".actions>button.OK");
            Application.States.Window.focusedWindow.setValue("HIDDEN");
            dialogOK.focus();

            const OKDialog = () => {
                dialogOK.removeEventListener("click", OKDialog);
                alertDialog.removeAttribute("visible");
                resolve(true);
            }

            dialogOK.addEventListener("click", OKDialog)
        })
    },

    confirm: (message) => {
        return new Promise((resolve, reject) => {
            Application.States.Window.focusedWindow.setValue("HIDDEN");

        })
    },

    prompt: (message, validate = () => { }) => {
        return new Promise((resolve, reject) => {
            Application.States.Window.focusedWindow.setValue("HIDDEN");

        })
    },

    /**
     * Closes all `pageAlerts -> [ alert, confirm, prompt ]`
     */
    closeAllAlerts() { document.querySelectorAll(".ui\\:alert").forEach(alert => alert.removeAttribute("visible")) },

    /**
     * 
     * @param {CreateDialogOptions} options 
     * @param {() => HTMLElement} htmlContent 
     * @returns {ActiveDialogActions}
     */
    createDialog(options = { fill: true, moveable: true, id: null, title: "", width: 640 }, htmlContent = () => document.createElement("div")) {
        const dialog = document.createElement("dialog");
        dialog.classList.add("ui:dialog");
        if (options.id) dialog.id = options.id;
        if (options.fill) dialog.setAttribute("fill", "");
        if (options.moveable) dialog.setAttribute("moveable", "");

        const closeDialog = (_confirm = true) => {
            dialog.classList.remove("visible");
            dialog.removeAttribute("visible");
            document.removeEventListener("keydown", handleKeyDown)
        }

        const showDialog = () => {
            Application.States.Window.focusedWindow.setValue("HIDDEN");
            dialog.classList.add("visible");
            dialog.setAttribute("visible", "");
        }

        const dialogWidth = options.width || 640;
        const dialogTitle = options.title || "";
        const dialogFill = setDefault(options.fill, true);
        const dialogMoveable = setDefault(options.moveable, true);
        const dialogChildren = htmlContent();

        const dialogContent = document.createElement("div");
        dialogContent.classList.add("content");
        dialogContent.style.width = `${dialogWidth}px`;

        const dialogHeader = document.createElement("div");
        dialogHeader.classList.add("header");
        dialogHeader.innerHTML = `<span class="title">${dialogTitle}</span><i icon class="close"> close </i>`;

        const dialogClose = dialogHeader.querySelector("i.close:last-child");
        dialogClose.addEventListener("click", () => closeDialog());

        const dialogBody = document.createElement("div");
        dialogBody.classList.add("body");

        if (dialogFill) {
            const dialogBackground = document.createElement("div");
            dialogBackground.classList.add("fill");

            dialog.appendChild(dialogBackground);
        }

        dialogChildren.forEach(c => dialogBody.appendChild(c));
        dialogContent.appendChild(dialogHeader);
        dialogContent.appendChild(dialogBody);

        dialog.appendChild(dialogContent);

        document.body.appendChild(dialog);

        if (dialogMoveable) {
            $(dialogContent).draggable({
                handle: dialogHeader,
                containment: "parent"
            })
        }

        const handleKeyDown = e => {
            if (e.key === "Escape" && (e.shiftKey || [dialog, dialogContent, dialogHeader, dialogBody].includes(document.activeElement))) {
                closeDialog(!e.shiftKey);
            }
        }; document.addEventListener("keydown", handleKeyDown)

        return {
            show: () => {
                return new Promise((resolve, reject) => {
                    Application.States.Window.focusedWindow.setValue("HIDDEN");
                    showDialog();
                    resolve();
                })
            },
            hide: (forceClose = false) => {
                return new Promise((resolve, reject) => {
                    closeDialog(!forceClose);
                    resolve();
                })
            }
        }
    }
}

function updateUI() {
    return new Promise(async (resolve, reject) => {
        for (const promise of renderUIComponents) {
            await promise();
        };

        resolve();
    })
}

/**
 * Add the `renderUIComponent` list to the `preLoadedEventList` in a promise that
 * finished ONCE each UI component in the current document has been rendered
 *     — that is, when each callback has been executed to completion.
 */
preLoadedEventList
    .push(() => {
        return updateUI();
    })