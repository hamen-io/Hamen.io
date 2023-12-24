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
                let width = document.querySelector("#doc article.article\\:document").getBoundingClientRect().width;
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

            if (i === 0) {
                const headerLogo = document.createElement("img");
                headerLogo.src = "https://hamen.io/static/media/logo.png";
                headerLogo.id = "header-logo";
                headerLogo.setAttribute("width", "24px");
                headerLogo.setAttribute("height", "24px");
                headerLogo.style.marginRight = "8px";
                anchor.appendChild(headerLogo);

                anchor.style.display = "flex";
                anchor.style.alignItems = "center";
            }

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
})