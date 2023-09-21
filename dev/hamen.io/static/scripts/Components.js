class UICardList {
  constructor(
    filters = [
      {
        id: "code",
        title: "Code",
        checked: true
      }
    ], items = [{
      "code": [
        {
          title: "Types of Arrays in Python",
          author: "Daniel Hamen",
          date: "2023-08-31",
          category: ["Code", "Python", "Data Types"]
        }
      ]
    }],
    itemType = "MEDIUM"
  ) {
    this.filters = filters;
    this.items = items[0];
    this.itemType = itemType;
    this.activeFilter = filters.filter(filter => filter.checked);
    this.activeFilter = this.activeFilter.length >= 1 ? this.activeFilter[0].id : filters[0].id;

    this.filterItems;
  };

  UICardMedium(info) {
    const card = document.createElement("a");
    card.classList.add("ui:medium-card");
    const url = info["url"];
    card.href = `https://www.hamen.io/docs/${url}`;

    card.innerHTML = `
      <div class="header" style="background-color: rgb(77, 151, 255);"></div>
      <div class="body">
        <span class="category">${info.category.join(" / ")}</span>
        <h4 class="title">${info.title}</h4>
        <div class="date" style="flex-direction: row;justify-content: space-between;width: 100%;">
          <span>${info.date}</span>
          <span>by ${info.author}</span>
        </div>
      </div>
    `;

    return card;
  };

  UICardLong(info) {
    const card = document.createElement("a");
    card.classList.add("ui:long-card");
    const url = info["url"];
    card.href = `https://www.hamen.io/software/${url}`;
    const charLimit = 256;

    card.innerHTML = `
      <div class="header" style="background-color: rgb(77, 151, 255);"></div>
      <div class="body">
        <h4 class="title">${info.title}</h4>
        <p class="description"><span class="description-content">${info.description.length > 16 ? info.description.slice(0, charLimit).trim() + "..." : info.description}</span>&nbsp;<br style="display: none;"><a class="expand-more" href="#">Read More...</a></p>
      </div>
    `;

    let descriptionContent = card.querySelector(".description-content");
    let description = card.querySelector(".description");
    let a = description.querySelector("a.expand-more");
    a.addEventListener("click", e => {
      descriptionContent.innerText = a.innerText.trim() === "Read More..." ? info.description : info.description.slice(0, charLimit).trim() + "...";
      a.innerText.trim() === "Read More..." ?
        // Expand paragraph:
        (() => {
          a.innerText = "Read Less..."
          description.querySelector("br").style.display = "flex";
        })():
        // Shorten paragraph:
        (() => {
          description.querySelector("br").style.display = "none";
          a.innerText = "Read More...";
        })();

      e.preventDefault();
      e.stopImmediatePropagation();
      e.stopPropagation();
    })

    return card;
  };

  UICardList() {
    const cardList = document.createElement("div");
    cardList.classList.add("ui:card-list");

    const setItems = (items = []) => {
      Array.from(cardList.children).forEach(c => c.remove());

      Array.from(items).forEach(item => {
        switch (this.itemType) {
          case "MEDIUM":
            cardList.appendChild(this.UICardMedium(item));
            break;
          case "LONG":
            cardList.appendChild(this.UICardLong(item));
            break;
        }
      });
    };

    this.filterItems.forEach(item => {
      if (item.getAttribute("default")) {
        setItems(this.items[this.activeFilter]);
      }

      item.addEventListener("click", () => {
        setItems(this.items[item.getAttribute("filter-id")]);
      });
    })

    return cardList;
  };

  UICardListFilter(filter = { id: null, title: null }) {
    const filterElement = document.createElement("div");
    filterElement.classList.add("filter");

    filterElement.setAttribute("filter-id", filter.id);
    filterElement.innerText = filter.title;

    return filterElement;
  }

  UICardListFilters() {
    const filters = document.createElement("div");
    filters.classList.add("ui:card-list-filters");

    let filterItems = [];
    for (let i = 0; i < this.filters.length; i++) {
      const filter = this.UICardListFilter(this.filters[i]);
      if (this.filters[i].checked) {
        filter.setAttribute("default", "true");
        filter.classList.add("active");
      }

      filter.addEventListener("click", () => {
        this.activeFilter = this.filters[i].id;
        filterItems.forEach(item => {
          item.classList.remove("active");
          if (this.activeFilter === item.getAttribute("filter-id")) {
            item.classList.add("active")
          }
        })
      });

      filterItems.push(filters.appendChild(filter));
    };

    this.filterItems = filterItems;

    return filters;
  };

  appendFilters(element) {
    return new Promise((resolve, reject) => {
      element.appendChild(this.UICardListFilters());
      resolve();
    })
  };

  appendCardList(element) {
    return new Promise((resolve, reject) => {
      element.appendChild(this.UICardList());
      resolve();
    })
  };
}

const Components = {
  UIInput(options = { onClear, placeholder: null, id: null, class: null, type: null, icons: { prefix: "search", suffix: "clear" }}) {
    const inputWrapper = document.createElement("div");
    inputWrapper.classList.add("input-wrapper");

    if (options.icons.prefix) {
      const prefixIcon = document.createElement("span");
      prefixIcon.classList.add("material-symbols-outlined", "prefix-icon");
      prefixIcon.innerHTML = options.icons.prefix;

      inputWrapper.classList.add("has-prefix-icon");
      inputWrapper.appendChild(prefixIcon);
    };

    if (!options.onClear) {
      options.onClear = (input) => {
        input.value = "";
      };
    };

    const input = document.createElement("input");
    input.placeholder = options.placeholder || "";
    input.type = options.type || "text";
    input.id = options.id || "";
    input.classList.add(...(options.class || []));

    inputWrapper.appendChild(input);

    if (options.icons.suffix) {
      const suffixIcon = document.createElement("span");
      suffixIcon.classList.add("material-symbols-outlined", "suffix-icon");
      suffixIcon.innerHTML = options.icons.suffix;

      let updateVisibility = () => {
        if (input.value.length > 0) {
          suffixIcon.style.display = "flex";
        } else {
          suffixIcon.style.display = "none";
        }
      };
      
      inputWrapper.classList.add("has-suffix-icon");
      inputWrapper.appendChild(suffixIcon);
      
      updateVisibility();
      input.addEventListener("input", updateVisibility);
      
      suffixIcon.addEventListener("click", () => {
        options.onClear(input);
      });
    };

    const border = document.createElement("span");
    border.classList.add("border");

    inputWrapper.appendChild(border);

    return inputWrapper;
  }, UIFooter() {
    const footer = document.createElement("footer");
    footer.classList.add("ui:footer");
    footer.innerHTML = `
      <p class="fancy sub">
        <span>2023 © <a href="https://www.hamen.io/">Hamen.io</a>. All rights reserved. Developed by <a href="javascript:void(0);">Daniel Hamen</a>
        </span>
      </p>
    `;

    return footer;
  }, UIHamburger(onClick = (toggled) => {}) {
    const hamburger = document.createElement("div");
    hamburger.classList.add("ui:hamburger");

    hamburger.innerHTML = `
    <span></span>
    <span></span>
    <span></span>
    `;

    hamburger.addEventListener("click", () => {
      hamburger.classList.toggle("toggled");

      onClick(hamburger.classList.contains("toggled"));
    })

    return hamburger;
  }, UIHeader() {
    const header = document.createElement("header");
    header.innerHTML = `
    <ul>
        <li style="margin-right: auto;" list-id="title">
            <a class="title fancy" href="https://www.hamen.io/">Hamen.io</a>
        </li>
        <li list-id="docs">
            <a class="title fancy fs-sub" href="https://www.hamen.io/docs">Docs</a>
        </li>
        <!--
        <li list-id="quizzes">
            <a class="title fancy fs-sub" href="https://www.hamen.io/quizzes">Quizzes</a>
        </li>
        -->
        <li list-id="software">
            <a class="title fancy fs-sub" href="https://www.hamen.io/software">Software</a>
        </li>
        <li list-id="hamburger"></li>
        <li list-id="background"></li>
        <ul list-id="mobile-menu">
          <li list-id="docs">
              <a class="title fancy fs-sub" href="https://www.hamen.io/docs">Docs</a>
          </li>
          <!--
          <li list-id="quizzes">
              <a class="title fancy fs-sub" href="https://www.hamen.io/quizzes">Quizzes</a>
          </li>
          -->
          <li list-id="software">
              <a class="title fancy fs-sub" href="https://www.hamen.io/software">Software</a>
          </li>
        </ul>
    </ul>`;

    const mobileMenu = header.querySelector("[list-id=mobile-menu]");
    const background = header.querySelector("[list-id=background]");

    header.querySelector("[list-id=hamburger]").appendChild(Components.UIHamburger((toggled) => {
      if (toggled) { mobileMenu.classList.add("visible");background.classList.add("visible"); }
      else { mobileMenu.classList.remove("visible");background.classList.remove("visible"); }
    }));

    const hamburger = header.querySelector("[list-id=hamburger] .ui\\:hamburger");

    background.addEventListener("click", () => {
      hamburger.classList.remove("toggled");
      mobileMenu.classList.remove("visible");
      background.classList.remove("visible");
    })

    return header;
  }, UICardList: UICardList,
  UIProgressBar() {
    const progressBar = document.createElement("div");
    progressBar.classList.add("ui:progress-bar");
    const fill = document.createElement("div");
    fill.classList.add("fill");
  
    progressBar.appendChild(fill);
  
    let main = document.querySelector("body>main");
    let header = document.querySelector("body>header");
  
    let updateScrollBar = () => {
      let headerSize = header.clientHeight; // Use clientHeight for content height
  
      fill.style.top = headerSize + "px";
      fill.style.width = (main.scrollTop / (main.scrollHeight - main.clientHeight)) * 100 + "%";
    };
  
    updateScrollBar(); // Initialize the progress bar
    main.addEventListener("scroll", updateScrollBar);
    main.addEventListener("resize", updateScrollBar);
  
    return progressBar;
  }
  
};