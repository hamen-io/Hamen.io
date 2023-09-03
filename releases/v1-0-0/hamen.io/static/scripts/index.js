window.addEventListener("DOMContentLoaded", () => {
  Array.from(document.querySelectorAll("input")).forEach(input => {
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
    });

    input.parentElement.replaceChild(inputWrapper, input);
  });

  const footer = document.querySelector("body>main>footer");
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