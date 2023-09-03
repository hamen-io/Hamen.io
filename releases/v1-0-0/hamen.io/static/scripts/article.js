window.addEventListener("DOMContentLoaded", () => {
  let main = document.querySelector("body>main");
  main.insertBefore(Components.UIProgressBar(), main.firstElementChild);

  // Highlight Code:// Highlight Code:
  Array.from(document.querySelectorAll(".ui\\:code-block pre")).forEach(preElement => {
    const codeContent = preElement.innerText;
    const highlightedCode = Prism.highlight(codeContent, Prism.languages.python, 'python');

    preElement.innerHTML = highlightedCode;
  });
})