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
  try {
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
  
          Array.from(Object.keys(module.topics)).forEach(topic => {
            const topicAnchor = document.createElement("a");
            topicAnchor.classList.add("title");
            if (topic.startsWith(ModuleNumber.toString().trim())) topicAnchor.classList.add("active");
            topicAnchor.href = module.topics[topic];
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
  } catch (error) {
    
  }

  document.addEventListener("DOMContentLoaded", () => {
    try {
      if (typeof MathJax !== "undefined") {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
      }
    } catch {}
  });

  Array.from(document.querySelectorAll(".ui\\:chart")).forEach(chart => {
    const canvas = chart.querySelector("canvas");

    switch (chart.getAttribute("chart-id")) {
      case "secant-example-i":
        (() => {
          function f(x) {
            return ((Math.pow(x, 2)) + (4 * x) - (2));
          }

          var x1 = -1;
          var x2 = -5;
          var y1 = -5;
          var y2 = 3;

          var data = {
            labels: [],
            datasets: [
              {
                label: 'f(x) = 3x^2 + 4x - 6',
                data: [],
                borderColor: 'blue',
                borderWidth: 2,
                fill: false,
              },
              {
                label: 'Secant Line',
                data: [{ x: x1, y: y1 }, { x: x2, y: y2 }],
                borderColor: 'red',
                borderWidth: 2,
                fill: false,
                showLine: true,
              }
            ]
          };

          var ctx = canvas.getContext('2d');
          var chartContent = new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
              scales: {
                x: {
                  type: 'linear',
                  position: 'bottom'
                },
                y: {
                  min: -10,
                  max: 10,
                  type: 'linear',
                  position: 'left'
                }
              }
            }
          });

          for (var x = -10; x <= 10; x += 0.5) {
            data.labels.push(x.toFixed(2));
            data.datasets[0].data.push(f(x).toFixed(2));
          }

          chartContent.update();
        })()
    }
  })
})