/**
 * The copyright notice in the footer
 */
const COPYRIGHT_NOTICE = (() => {
    const notice = document.createElement("span");
    notice.classList.add("hamen:copyright-notice");
    notice.id = "hamen:copyright-notice";
    notice.innerHTML = `2023 © <a class="title inline" href="https://www.hamen.io/">Hamen.io</a>. All rights reserved. Developed by <a href="javascript:void(0);" class="title inline">Daniel Hamen</a>`;

    return notice;
})();

class EventList {
    constructor() {
        this._list = [];
    };

    subscribe(callback) {
        return new Promise((resolve, reject) => {
            this._list.push(callback);
            resolve();
        })
    };

    unsubscribe(callback) {
        if (this._list.indexOf(callback) != -1) {
            this._list.splice(this._list.indexOf(callback));
        };
    };

    trigger() {
        return new Promise((resolve, reject) => {
            let executeNext = (i, list) => {
                list[i]()
                    .then(() => {
                        if (i == list.length - 1) {
                            return resolve();
                        };
    
                        return executeNext(i+1, list);
                    })
                    .catch((error) => {
                        return reject("Error triggering event: " + i + "\n\n" + error);
                    })
            };
    
            executeNext(0, this._list);
        })
    }
};

window.Hamen = {
    onLoad: new EventList()
};

/**
 * Updates the footer & header size variables to be the actual size of the header and footer
 */
const updateCSSProportions = () => {
    const root = document.querySelector(":root");
    const header = document.querySelector("body>header");
    const footer = document.querySelector("body>footer");

    if (header)
        root.style.setProperty("--hmn-headerSize", header.getBoundingClientRect().height + "px");

    if (footer) root.style.setProperty("--hmn-footerSize", footer.getBoundingClientRect().height + "px");
};

// Update CSS proportional variables:
window.Hamen.onLoad.subscribe(() => {
    return new Promise((resolve, reject) => {
        // Update on `onLoad` event trigger:
        window.addEventListener("DOMContentLoaded", updateCSSProportions)

        // Update on resize:
        window.addEventListener("resize", updateCSSProportions);

        let i = setInterval(updateCSSProportions, 5);
        setTimeout(() => clearInterval(i), 1000)

        resolve();
    })
});

// Create footer:
window.Hamen.onLoad.subscribe(() => {
    return new Promise((resolve, reject) => {
        const footer = document.querySelector("body>footer");
        footer?.appendChild(COPYRIGHT_NOTICE)

        resolve();
    })
})

// Update proportions for breadcrumbs on doc pages:
window.Hamen.onLoad.subscribe(() => {
    return new Promise((resolve, reject) => {
        let breadcrumbs = document.querySelector(".ui\\:breadcrumbs");
        if (breadcrumbs) {
            const updateBreadcrumbsProportions = () => {
                let breadcrumbs = document.querySelector(".ui\\:breadcrumbs");
                let width = document.querySelector("#doc article.article\\:document").getBoundingClientRect().width + document.querySelector("#doc aside#doc-aside").getBoundingClientRect().width;
                width = `calc(${width}px - 2px)`
                breadcrumbs.style.width = width;
                breadcrumbs.style.minWidth = width;
                breadcrumbs.style.maxWidth = width;
            };

            updateBreadcrumbsProportions();
            window.addEventListener("DOMContentLoaded", updateBreadcrumbsProportions)
            window.addEventListener("resize", updateBreadcrumbsProportions)
        }
        resolve();
    })
});

// Implement "ui:define" hover-title-text:
window.Hamen.onLoad.subscribe(() => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll(".ui\\:engine .ui\\:define").forEach(span => {
            let def = document.createElement("div");
            def.classList.add("ui:define-text");
            def.innerHTML = `<span>&ldquo;${span.getAttribute("word")}&rdquo; ( <i>${span.getAttribute("pos")}</i> ) : ${span.getAttribute("content") }</span>`;

            span.appendChild(def);

            let updatePosition = () => {
                let positionX = (span.getBoundingClientRect().left + (span.getBoundingClientRect().width / 2)) - (def.getBoundingClientRect().width / 2);
                def.style.left = positionX + "px";
            };

            updatePosition();

            document.addEventListener("DOMContentLoaded", updatePosition);
            document.addEventListener("resize", updatePosition);
            span.addEventListener("mouseover", updatePosition);
        });

        resolve();
    })
})

window.Hamen.onLoad.subscribe(() => {
    return new Promise((resolve, reject) => {
        let breadcrumbs = document.querySelector(".ui\\:breadcrumbs");
        if (breadcrumbs) {
            document.querySelector(":root").style.setProperty("--doc-ui-breadcrumbs-height", breadcrumbs.getBoundingClientRect().height + "px")
        }
        resolve()
    })
})

// Create header:
window.Hamen.onLoad.subscribe(() => {
    return new Promise((resolve, reject) => {
        const header = document.querySelector("body>header");
        if (!header) return resolve();
        const headerContent = document.createElement("div");
        headerContent.classList.add("header-content");
        headerContent.style.alignItems = "center";
        headerContent.style.marginRight = "12px"

        const headerItems = {
            "Hamen.io": "https://www.hamen.io",
            "Docs": "https://www.hamen.io/docs"
        };

        Object.keys(headerItems).forEach((item, i) => {
            const anchor = document.createElement("a");
            anchor.href = headerItems[item];
            anchor.target = "_self";
            anchor.classList.add("title");

            // Add header logo to first item ( anchor with text: "Hamen.io" ) :
            if (i === 0) {
                // const headerLogo = document.createElement("svg");
                // headerLogo.src = "https://hamen.io/static/media/logo.png";
                // headerLogo.id = "header-logo";
                // headerLogo.setAttribute("width", "24px");
                // headerLogo.setAttribute("height", "24px");

                const headerLogoSize = 24;
                const headerLogo = (() => {
                    let _logo = document.createElement("div");
                    _logo.innerHTML = `<?xml version="1.0" encoding="UTF-8"?><svg id="Layer_2" data-name="Layer 2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 484.96 484.96" width="${headerLogoSize}" height="${headerLogoSize}"><defs><style>.hmn-favicon-logo-svg-cls-1 {fill: none;stroke: #e6e7e8;stroke-linejoin: bevel;stroke-width: 24px;}.hmn-favicon-logo-svg-cls-2, .hmn-favicon-logo-svg-cls-3, .hmn-favicon-logo-svg-cls-4 {stroke-width: 0px;}.hmn-favicon-logo-svg-cls-3 {fill: #2a2b2c;}.hmn-favicon-logo-svg-cls-4 {fill: #e6e7e8;}</style></defs><g id="Layer_1-2" data-name="Layer 1"><g><rect class="hmn-favicon-logo-svg-cls-3" x="107.02" y="107.02" width="270.92" height="270.92" transform="translate(-100.44 242.48) rotate(-45)"/><path class="hmn-favicon-logo-svg-cls-2" d="M242.48,67.88l174.6,174.6-174.6,174.6L67.88,242.48,242.48,67.88M242.48,33.94L33.94,242.48l208.54,208.54,208.54-208.54L242.48,33.94h0Z"/></g><g><polyline class="hmn-favicon-logo-svg-cls-1" points="282.22 402.16 282.14 293.23 282.22 178.48"/><polyline class="hmn-favicon-logo-svg-cls-1" points="202.73 87.45 202.73 191.72 202.73 306.73"/><line class="hmn-favicon-logo-svg-cls-1" x1="282.22" y1="242.36" x2="202.73" y2="242.36"/></g><path class="hmn-favicon-logo-svg-cls-4" d="M242.48,67.88l174.6,174.6-174.6,174.6L67.88,242.48,242.48,67.88M242.48,33.94L33.94,242.48l208.54,208.54,208.54-208.54L242.48,33.94h0Z"/><path class="hmn-favicon-logo-svg-cls-3" d="M242.48,33.94l208.54,208.54-208.54,208.54L33.94,242.48,242.48,33.94M242.48,0l-16.97,16.97L16.97,225.51,0,242.48l16.97,16.97,208.54,208.54,16.97,16.97,16.97-16.97,208.54-208.54,16.97-16.97-16.97-16.97L259.45,16.97,242.48,0h0Z"/></g></svg>`
                    return _logo.firstElementChild;
                })()
                headerLogo.style.marginRight = "8px";
                anchor.appendChild(headerLogo);

                anchor.style.display = "flex";
                anchor.style.alignItems = "center";
            };

            let innerText = document.createElement("span");
            innerText.innerText = item;

            anchor.appendChild(innerText);
            
            headerContent.appendChild(anchor);
        });

        header.appendChild(headerContent);

        resolve();
    })
});

window.addEventListener("load", () => {
    window.Hamen.onLoad.trigger();
});