window.addEventListener("load", async () => {
    for (const promise of preLoadedEventList) {
        await promise();
    }

    postLoadedEventList.forEach(c => c());

    const windowPanels = () => Array.from(document.querySelectorAll(".window"));
    window.addEventListener("mousedown", e => {
        if (!document.hasFocus() || e?.target?.closest("[preserve-focus]") !== null) return;

        windowPanels().forEach(window => {
            const windowID = window.getAttribute("win-id");
            if (!windowID) return Console.error(`Fatal: Unknown window ID : '${windowID}'`)

            if (window.contains(e.target)) {
                window.classList.add("focused");

                Application.States.Window.focusedWindow.setValue(windowID);
            } else {
                window.classList.remove("focused");
            }
        })
    })

    window.addEventListener("blur", () => Application.States.Window.focusedWindow.setValue("HIDDEN"));


    const editor = new Editor();
    editor.actionBarExpanded = false;
    document.body.setAttribute("loaded", "true");
    document.body.isLoaded = true;

    Application.Editor = editor;

    Application.Editor.init();
})