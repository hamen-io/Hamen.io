window.addEventListener("DOMContentLoaded", () => {
  Array.from(document.querySelectorAll("input")).forEach(input => {
    if (input.getAttribute("render") !== "false") {
      let defaultOnClick = value => {};
  
      let inputWrapper = Components.UIInput({
        class: input.classList.values(),
        placeholder: input.getAttribute("placeholder"),
        id: input.getAttribute("id"),
        type: input.getAttribute("type"),
        icons: {
          prefix: input.getAttribute("prefix-icon") || "search",
          suffix: input.getAttribute("suffix-icon") || "clear"
        },
        containerStyles: input.getAttribute("contentContainerStyles") || {},
        inputStyles: input.getAttribute("inputStyles") || {},
        onInput: input?.UIComponent?.eventListeners?.input || defaultOnClick
      });
  
      input.parentElement.replaceChild(inputWrapper, input);
    }
  });

  let footer = document.querySelector("body>main>footer");
  if (!footer) footer = document.querySelector("body footer#body-footer");
  if (footer) {
    footer.parentElement.replaceChild(Components.UIFooter(), footer);
  }

  const header = document.querySelector("body>header");
  if (header) {
    header.parentElement.replaceChild(Components.UIHeader(), header);
  }

  Array.from(document.querySelectorAll("code.inline-code")).forEach(code => {
    code.innerText = code.innerText.trim()
  })
});