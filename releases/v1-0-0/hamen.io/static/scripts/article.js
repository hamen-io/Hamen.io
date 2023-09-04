window.addEventListener("DOMContentLoaded", () => {
  let main = document.querySelector("body>main");
  main.insertBefore(Components.UIProgressBar(), main.firstElementChild);

  // Highlight Code:// Highlight Code:
  Array.from(document.querySelectorAll(".ui\\:code-block pre")).forEach(preElement => {
    const codeContent = preElement.innerText;
    const highlightedCode = Prism.highlight(codeContent, Prism.languages.python, 'python');

    preElement.innerHTML = highlightedCode;
  });

  // Add "#" after each heading:
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

  // Add tree on guides:
  if (Guide) {
    const tree = document.querySelector("main[article-type=guide]>#article-wrapper>#tree");
    if (tree) {
      const title = document.createElement("h2");
      title.innerText = Guide.course;
      tree.appendChild(title);

      let createModule = (module) => {
        const moduleSection = document.createElement("section");
        const moduleTitle = document.createElement("h3");
        moduleTitle.innerText = module.module;
        moduleSection.appendChild(moduleTitle);

        Array.from(module.topics).forEach(topic => {
          const topicAnchor = document.createElement("a");
          topicAnchor.href = "#";
          topicAnchor.innerText = topic;

          moduleSection.appendChild(topicAnchor);
        })

        return moduleSection;
      };

      Array.from(Guide.modules).forEach(module => {
        tree.appendChild(createModule(module));
      })
    }
  }
})