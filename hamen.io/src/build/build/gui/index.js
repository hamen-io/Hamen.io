var onLoad = [];

const conditionalClassManipulation = (element, className, condition) => {
    if (condition) {
        element.classList.add(className);
    } else {
        element.classList.remove(className);
    }
}

// Add navigation functionality:
onLoad.push(() => {
    return new Promise((resolve, reject) => {
        let viewList = document.querySelector("footer>#view-list");
        if (!viewList) return reject("`#view-list` not found.");

        let setActiveView = id => {
            document.querySelectorAll("body>main>.view").forEach(view => conditionalClassManipulation(view, "active", view.getAttribute("name") === id));
            document.querySelectorAll("body>footer>#view-list>li").forEach(li => conditionalClassManipulation(li, "active", li.getAttribute("for") === id));
        }

        viewList.querySelectorAll("li").forEach(li => {
            li.addEventListener("click", () => setActiveView(li.getAttribute("for")));
        })

        setActiveView("properties");

        resolve();
    })
})

// Add input[validation] functionality:
onLoad.push(() => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll("input[validation]").forEach(input => {
            input.addEventListener("keydown", e => {
                if (!(() => {
                    switch (input.getAttribute("validation")) {
                        case "SAFE_FILENAME":
                            return /[a-zA-Z0-9_\-\.]/gi
                    }
    
                    return /./;
                })().test(e.key)) {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    e.stopPropagation();
                }
            })
    
        })
    
        resolve()
    })
})

// Add icon to all <details>:
onLoad.push(() => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll("details").forEach(details => {
            let summary = details.querySelector("summary");
            if (summary) {
                let icon = document.createElement("span");
                icon.classList.add("material-symbols-outlined");
                icon.innerHTML = "arrow_drop_down";
                summary.prepend(icon);
            }
        })

        resolve();
    })
})

onLoad.push(() => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll("input[initial-width-to-content]").forEach(input => {
            let resizeInput = input => input.style.width = (input.value ? input.value.length : input.placeholder.length) + "ch";
            resizeInput(input)
            input.addEventListener("input", () => resizeInput(input));
        })

        resolve()
    })
})

// Set <textarea> with `initial-height-to-content="true"` to have their height equal the height of their content:
onLoad.push(() => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll("[initial-height-to-content]").forEach(elem => {
            elem.style.height = "0px";
            elem.style.minHeight = "0px";
            elem.style.height = elem.scrollHeight + "px";
            elem.addEventListener("input", () => {
                elem.style.height = "0px";
                elem.style.minHeight = "0px";
                elem.style.height = elem.scrollHeight + "px";
            })
        })
    
        resolve()
    })
})

const executeOnLoad = () => {
    return new Promise(async (resolve, reject) => {
        for (const promiseFunction of onLoad) {
            await promiseFunction();
        }

        resolve();
    })
};

// Add wrap option to <textarea>:
onLoad.push(() => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll("textarea").forEach(textarea => {
            let option = document.createElement("div");
            option.classList.add("textarea-wrap-text");
            option.innerHTML = `<div class="wrap-text-animation wrap">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
            </div>`;
            option.style.left = textarea.getBoundingClientRect().width + "px"
            option.addEventListener("click", e => {
                let wrapAnimation = option.querySelector(".wrap-text-animation");
                wrapAnimation.classList.toggle("wrap")

                if (wrapAnimation.classList.contains("wrap")) {
                    textarea.style.textWrap = "wrap";
                } else {
                    textarea.style.textWrap = "nowrap";
                }
                
                textarea.style.height = "0px";
                textarea.style.minHeight = "0px";
                textarea.style.height = textarea.scrollHeight + "px";
            })

            textarea.addEventListener("mouseover", () => option.classList.add("visible"));
            textarea.addEventListener("mouseout", () => option.classList.remove("visible"));

            textarea.insertAdjacentElement("beforebegin", option);
        })

        resolve();
    })
})

// Add default text to elements with {{ keyName }}
const addDefaultContent = () => {
    return new Promise((resolve, reject) => {
        document.querySelectorAll("[special-content]").forEach(elem => {
            elem.innerHTML = elem.innerHTML.replace(/\{\{\s*([a-zA-Z]+)\s*\}\}/gi, (match, contents) => {
                switch (contents) {
                    case "htaccessContent":
                        return `<IfModule mime_module>
  AddHandler application/x-httpd-ea-php80___lsphp .php .php8 .phtml
</IfModule>

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
    Header set Access-Control-Allow-Headers "Content-Type, Authorization"
</IfModule>

# Use local URLs for ErrorDocument to display the error page at the current URL
ErrorDocument 400 /error/index.php?error=400
ErrorDocument 402 /error/index.php?error=402
ErrorDocument 401 /error/index.php?error=401
ErrorDocument 403 /error/index.php?error=403
ErrorDocument 404 /error/index.php?error=404
`
                }

                return "UNKNOWN"
            })
        })

        resolve();
    })
};

window.addEventListener("DOMContentLoaded", () => {
    addDefaultContent()
        .then(() => {
            executeOnLoad()
                .then(() => {
                    console.log("-- LOADING COMPLETE --")
                })
        })
})