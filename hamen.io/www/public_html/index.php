<?php

if (isset($_GET["l"])) {
    $linkTarget = $_GET["l"];

    die($linkTarget);
}

echo <<<HTML

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1664530166161360" crossorigin="anonymous"></script>
        <meta name="description" content="Hamen.io; Unleashing the Potential of Academic Excellence through Code\n">
        <meta name="author" content="Hamen.io">
        <meta name="keywords" content="hamen.io, Hamen, Daniel Hamen, education, code, quiz, docs, blogs, articles, guides, courses, calculators, software">
        <meta name="og:title" content="Hamen.io">
        <meta name="og:description" content="Hamen.io stands as the preeminent online platform, serving as the vanguard for discovering a rich spectrum of educational resources, including blogs, courses, quizzes, calculators, and myriad intellectual offerings. Its resounding motto resounds as 'Unleashing the Potential of Academic Excellence through Code'">
        <meta name="og:type" content="website">
        <meta name="referrer" content="no-referrer-when-downgrade">
        <meta name="og:locale" content="en_US">

        <title>Hamen.io</title>

        <!-- <link rel="stylesheet" href="./static/styles/index.css">
        <script type="text/javascript" src="./static/scripts/Components.js"></script>
        <script type="text/javascript" src="./static/scripts/index.js"></script> -->
        <link rel="stylesheet" href="./static/css/importFonts.css">
        <link rel="stylesheet" href="./static/css/importIcons.css">
        <link rel="stylesheet" href="./static/css/index.css">
        <link rel="stylesheet" href="./static/css/webTheme.css">

        <script type="text/javascript" src="./static/js/index.js"></script>

        <!-- Favicon: -->
        <link rel="icon" href="./favicon.png" />
    </head>
    <body>
        <header></header>
        <main class="homepage alt-sec">
            <style>
                .homepage>section#introduction {
                    min-height: calc(100vh - var(--hmn-headerSize));
                    justify-content: center;
                    align-items: center;
                }

                @media screen and (max-width:700px) {
                    .homepage #search-input,.homepage #search-bttn {
                        width: 100%;
                        max-width: 100%;
                    }
                }
            </style>
            <section id="introduction" style="padding: 2em;">
                <h1 class="title">Hamen.io</h1>
                <p style="text-align: center">Unleashing the Potential of Academic Excellence through Code</p>
                <form method="GET" action="https://www.hamen.io/search" style="width: 100%;max-width:600px;align-items: center">
                    <input type="text" id="search-input" placeholder="Search for something on our site!" style="z-index: 2">
                    <div id="search-results">
                        <ul></ul>
                    </div>
                    <style>
                        .homepage #search-results {
                            display: flex;
                            position: relative;
                            width: 100%;
                            padding: 0;
                            margin: 0;
                            max-width: 600px;
                            flex-direction: column;
                            background-color: var(--hmn-backgroundColor-white-default);
                            z-index: 1;
                            padding-top: 1em;
                        }

                        .homepage #search-results>ul {
                            display: none;
                            flex-direction: column;
                            list-style: none;
                            padding: 0;
                            margin: 0;
                            margin-top: 8px;
                            position: absolute;
                            width: 100%;
                            padding-top: 1em;
                            transform: translateY(calc(-3.25em + 1px));
                            border: 1px solid var(--hmn-borderColor-black-default);
                            border-radius: 0 0 12.5px 12.5px;
                            background-color: var(--hmn-backgroundColor-white-default);
                            overflow: hidden
                        }

                        .homepage #search-results>ul:empty {
                            display: none;
                        }

                        .homepage #search-results>ul>li {
                            padding: 16px 12px;
                        }

                        .homepage #search-results>ul>li:hover {
                            background: rgba(0, 0, 0, 0.025);
                            cursor: pointer;
                        }

                        #search-input:focus + #search-results>ul,
                        #search-results>ul:hover {
                            display: flex;
                        }
                    </style>
                    <button type="submit" id="search-bttn">
                        Search
                        <span class="material-symbols-outlined">search</span>
                    </button>
                    <script type="text/javascript">
                        window.addEventListener("DOMContentLoaded", () => {
                            const searchInput = document.querySelector("#search-input");
                            const resultList = document.querySelector("#search-results>ul");
                            fetch("https://www.hamen.io/static/data/taggedSites.json")
                                .then(async (response) => {
                                    const taggedSites = await response.json();
                                    // const data = (() => { return new Promise((resolve, reject) => {
                                        //     resolve(JSON.parse(`{"Writing Articles for Hamen Docs": "https://www.hamen.io/docs/doc/hamen/docs/writing-for-hamen-docs/index.html", "Lambda Functions in Python": "https://www.hamen.io/docs/doc/code/python/lambda-functions-in-python/index.html", "Type Annotations in Python": "https://www.hamen.io/docs/doc/code/python/type-annotation-in-python/index.html", "CSS Preprocessors: A Strict Comparison between LESS and SASS": "https://www.hamen.io/docs/doc/code/web-development/css-preprocessors-a-strict-comparison-between-less-and-sass/index.html", "Hamen Docs": "https://www.hamen.io/docs/index.html"}`))
                                        // }) })()
                                    const setResults = (contents) => {
                                        resultList.querySelectorAll("li").forEach(li => li.remove());
                                        const contentEntries = Object.entries(contents);
                                        for (const [item, url] of contentEntries) {
                                            const li = document.createElement("li");
                                            li.innerText = item;
                                            resultList.appendChild(li);
                                            li.addEventListener("click", () => window.location.assign(url));
                                        };
                                    };

                                    searchInput.addEventListener("input", () => {
                                        const searchQuery = searchInput
                                            .value
                                            .toLowerCase()
                                            .replace(/[^a-zA-Z0-9 ]/g, "")
                                            .split(" ");

                                        let candidates = {};
                                        Array.from(Object.keys(taggedSites)).forEach(key => {
                                            const initialKey = key;
                                            let value = taggedSites[key];
                                            key = key.toLowerCase();
                                            key = key.replace(/[^a-zA-Z0-9 ]/g, "");
                                            tokens = key.split(" ");

                                            let searchAmount = 0;
                                            searchQuery.forEach(searchToken => {
                                                tokens.forEach(objToken => {
                                                    if (objToken.includes(searchToken)) { searchAmount += 1 }
                                                })
                                            })

                                            if (searchAmount > 0) {
                                                if (!candidates[searchAmount]) {
                                                    candidates[searchAmount] = []
                                                };

                                                candidates[searchAmount].push({ tokens: tokens, url: value, accuracy: searchAmount / tokens.length, name: initialKey });
                                            };
                                        });

                                        let successfulCandidates = []
                                        let candidateEntries = Object.entries(candidates);
                                        candidateEntries.sort((a, b) => b[0] - a[0]);
                                        for (const [key, items] of candidateEntries) {
                                            let sortedItems = items.sort((a, b) => b.accuracy - a.accuracy);
                                            const topFive = sortedItems.slice(0, 5);
                                            successfulCandidates.push(...topFive);

                                            if (successfulCandidates.length >= 5) {
                                                break;
                                            }
                                        }

                                        successfulCandidates = successfulCandidates.slice(0, 5)
                                        setResults(
                                            (
                                                () => {
                                                    let _contents = {};
                                                    successfulCandidates.forEach(item => {
                                                        _contents[item.name] = item.url
                                                    })

                                                    return _contents
                                                }
                                            )()
                                        )
                                    })
                                })
                                .catch(() => {
                                    searchInput.addEventListener("submit", () => {
                                        alert("Sorry.\n\nAn error occurred while fetching the pages of our site; unable to process your request... You may have to try again later :*/")
                                    });
                                })
                        })
                    </script>
                </form>
            </section>
            <style>
                .homepage>section:not(:first-of-type) {
                    width: 100%;
                    align-items: center;
                }

                .homepage>section:not(:first-of-type) .body {
                    max-width: 800px;
                    flex-direction: row;
                    justify-content: center;
                    gap: 3em;
                }

                .homepage>section:not(:first-of-type) a.button {
                    margin-top: 1em;
                }

                .homepage>section:not(:first-of-type) .icon {
                    justify-content: center;
                }

                .homepage>section:not(:first-of-type) .icon>span {
                    font-size: 96px
                }

                .homepage>section:not(:first-of-type) {
                    border-top: 1px solid var(--hmn-borderColor-black-default);
                    padding: 5em 4em
                }

                .homepage>section:last-of-type {
                    border-bottom: 1px solid var(--hmn-borderColor-black-default)
                }

                @media screen and (max-width:550px) {
                    .homepage>section:not(:first-of-type) {
                        flex-direction: column;
                    }

                    .homepage>section:not(:first-of-type) .icon {
                        display: none;
                    }

                    .homepage>section:not(:first-of-type) .button {
                        margin: 0 auto
                    }

                    .homepage>section:not(:first-of-type) .body * {
                        text-align: center;
                    }
                }
            </style>
            <section id="docs">
                <div class="body">
                    <div class="details">
                        <h2 class="title">Hamen Docs</h2>
                        <p>Explore a range of high-quality blogs covering diverse topics to enhance your understanding and gain valuable insights in various domains such as code, linguistics, mathematics, and more.</p>
                        <a class="button" href="https://www.hamen.io/docs">
                            <button type="button">
                                Hamen Docs
                                <span class="material-symbols-outlined"> open_in_new </span>
                            </button>
                        </a>
                    </div>
                    <div class="icon">
                        <span class="material-symbols-outlined"> description </span>
                    </div>
                </div>
            </section>
            <!-- <section id="quizzes">
                <div class="body">
                    <div class="details">
                        <h1 class="h1 title">Hamen Quizzes</h1>
                        <p>Engage in intellectually stimulating experiences by partaking in interactive quizzes that challenges your cognitive prowess. Immerse yourself in a thought-provoking journey of questions designed to test and expand your knowledge across diverse domains. Embark on enlightening quests to uncover a new dimension of learning through the captivating realm of quizzes.</p>
                        <a class="button" href="https://www.hamen.io/quizzes">
                            <button type="button">
                                Hamen Quizzes
                                <span class="material-symbols-outlined"> open_in_new </span>
                            </button>
                        </a>
                    </div>
                    <div class="icon">
                        <span class="material-symbols-outlined"> quiz </span>
                    </div>
                </div>
            </section> -->
            <!-- <section id="software">
                <div class="body">
                    <div class="details">
                        <h1 class="h1 title">Hamen Software</h1>
                        <p>Explore an array of software solutions. Hamen Software presents a diverse selection, encompassing desktop applications, web frameworks, libraries, APIs, iOS applications, as well as supplementary frameworks, libraries, and APIs, catering to a wide spectrum of technological needs.</p>
                        <a class="button" href="https://www.hamen.io/software">
                            <button type="button">
                                Hamen Software
                                <span class="material-symbols-outlined"> open_in_new </span>
                            </button>
                        </a>
                    </div>
                    <div class="icon">
                        <span class="material-symbols-outlined"> terminal </span>
                    </div>
                </div>
            </section> -->
            <!-- <section id="calculators">
                <div class="body">
                    <div class="details">
                        <h1 class="h1 title">Hamen Calculators</h1>
                        <p>Elevate your calculations with Hamen Calculators. Our user-friendly online tools provide instant and precise results for various mathematical tasks. From equations to conversions, simplify complexity at your fingertips.</p>
                        <a class="button" href="https://www.hamen.io/calculators">
                            <button type="button">
                                Hamen Calculators
                                <span class="material-symbols-outlined"> open_in_new </span>
                            </button>
                        </a>
                    </div>
                    <div class="icon">
                        <span class="material-symbols-outlined">functions</span>
                    </div>
                </div>
            </section> -->
        </main>
        <footer></footer>
    </body>
</html>

HTML;