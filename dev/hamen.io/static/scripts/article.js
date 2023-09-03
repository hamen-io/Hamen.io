window.addEventListener("DOMContentLoaded", () => {
  let main = document.querySelector("body>main");
  main.insertBefore(Components.UIProgressBar(), main.firstElementChild);

  // Highlight Code:// Highlight Code:
  Array.from(document.querySelectorAll(".ui\\:code-block pre")).forEach(preElement => {
    const codeContent = preElement.innerText;
    const highlightedCode = Prism.highlight(codeContent, Prism.languages.python, 'python');

    preElement.innerHTML = highlightedCode;
  });

  // 
  Array.from(document.querySelectorAll("#doc .doc-section")).forEach(section => {
    let heading = section.querySelector("h2")
    if (heading) {
      let link = document.createElement("a");
      link.href = `#${section.id}`;
      link.innerText = `#`;
      link.style.marginLeft = '8px';

      heading.appendChild(link);
    }
  })
})