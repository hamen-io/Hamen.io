from hooks.Hook import Hook

import os
import shutil
import json
import lib.Templates as Templates
import lib.Elements as Elements
from lxml import etree
import re

_HTML_TAB_ = "    "
_NEWLINE_ = "\n"
_PRISM_PACKAGES_ = Elements.supportedLanguages

class Article:
    def __init__(self, docRoot: Elements.Doc):
        self.docRoot = docRoot
        self.docType = self.docRoot.getAttribute("docType")

        childTags = [x.tagName for x in self.docRoot.children]
        assert len(self.docRoot.children) == 2 and all(
            [x in childTags for x in (
                "DOCUMENT",
                "PROPERTIES"
            )]
        ), f"Root tags ( `<Doc>` ) should have exactly two children: `<Properties>`, and `<Document>`"

        self.propertyEntries: dict = {child.getAttribute("key"): child.getAttribute("value") for child in self.docRoot.selectChild(tag = "PROPERTIES").selectChildren(tag = "ENTRY")}
        self.document: Elements.Document = self.docRoot.selectChild(tag = "DOCUMENT")
        self.documentBody: str = self.document.__str__(True)

class BuildDoc(Hook):
    """
    Builds all the .hdoc files
    """
    def execute(self) -> bool:
        manifestList = []
        for file in self.searchFiles(filePattern = r"^(.*\.hdoc)$"):
            hdoc = self._handleHDOC(file.fullFilePath)

            manifestFolder = os.path.join(file.filePath, "manifest")
            os.mkdir(manifestFolder)

            articlePathname = file.fullFilePath.split("xml")[-1].replace("\\", "/")[:-4] + "html"

            with open(os.path.join(manifestFolder, "manifest.json"), "x", encoding="utf-8") as manifestJson:
                manifest = {
                    "articleTitle": hdoc.propertyEntries.get("title"),
                    "articleAuthor": hdoc.propertyEntries.get("author"),
                    "articleAuthorID": hdoc.propertyEntries.get("authorID"),
                    "articleID": hdoc.propertyEntries.get("titleID"),
                    "articleDescription": hdoc.propertyEntries.get("description"),
                    "articleTags": [x.lower().strip() for x in ("" or hdoc.propertyEntries.get("tags")).split(",")],
                    "articleDate": {
                        "published": hdoc.propertyEntries.get("date:published"),
                        "modified": hdoc.propertyEntries.get("date:modified")
                    },
                    "articlePathURL": f"https://www.hamen.io/docs/doc{articlePathname}",
                    "articleCategory": hdoc.propertyEntries.get("category"),
                    "articleSubCategory": hdoc.propertyEntries.get("subcategory"),
                    "articleBreadcrumbs": hdoc.propertyEntries.get("breadcrumbs"),
                }

                manifestList.append(manifest)
                json.dump(manifest, manifestJson)

        # Copy the entire /artifacts/docs/xml/ directory to /docs/doc
        target = os.path.join(self.buildDirectory, "hamen.io", "docs", "doc")
        shutil.copytree(os.path.join(self.buildDirectory, "hamen.io", "artifacts", "docs", "xml"), target)

        with open(os.path.join(self.buildDirectory, "hamen.io", "artifacts", "docs", "manifest.json"), "x", encoding="utf-8") as manifestJson:
            json.dump(manifestList, manifestJson)

        return True

    def _handleHDOC(self, hdoc: str) -> Article:
        with open(hdoc, "r", encoding = "utf-8") as file:
            code = file.read()
            # code = re.sub(r"<!--[\s\S]*?-->", "", code)
            # code = re.sub(r"""(\w+)={\s*(("|')?((.|\n)*?)(\3)?)\s*}""", r'\1="\4"', code)

            root = etree.fromstring(code)
            root: etree._Element
            assert root.tag.upper() == "DOC", f"Root element should be <Doc>; not: '{root.tag}'"

            doc_root = Elements.Doc()
            doc_root.extendAttributes(root.attrib)

            def attachChildren(children: etree._Element, parentElement: Elements.Element):
                for child in children:
                    child: etree._Element

                    element = None
                    tag = child.tag

                    # Replace namespaces:
                    tag = re.sub(r"\{(.*)(\/)(.*)\}(.*)", r"\3:\4", tag)

                    # Tags are case-insensitive; make lowercase for better matches:
                    tag = tag.lower()

                    match tag:
                        case "doc": element = Elements.Doc()
                        case "properties": element = Elements.Properties()
                        case "document": element = Elements.Document()
                        case "entry": element = Elements.Entry(key = child.attrib.get("key"), value = child.attrib.get("value"))
                        case "ui:title": element = Elements.UI.Title()
                        case "ui:h1": element = Elements.UI.H1()
                        case "ui:h2": element = Elements.UI.H2()
                        case "ui:section": element = Elements.UI.Section()
                        case "ui:text": element = Elements.UI.Text()
                        case "ui:list": element = Elements.UI.List()
                        case "ui:code": element = Elements.UI.Code()
                        case "ui:breadcrumbs": element = Elements.UI.Breadcrumbs()
                        case "ui:item": element = Elements.UI.Item()
                        case "ui:break": element = Elements.UI.Break()
                        case "ui:hrule": element = Elements.UI.HRule()
                        case "i": element = Elements.Format.i()
                        case "a": element = Elements.Format.a()
                        case "em": element = Elements.Format.em()
                        case "b": element = Elements.Format.b()
                        case "u": element = Elements.Format.u()
                        case "mark": element = Elements.Format.mark()
                        case "code": element = Elements.Format.code()
                        case _: raise SyntaxError(f"Unknown tag: '{tag}'")

                    element = attachChildren(child, element)

                    element.extendAttributes(child.attrib)
                    element.innerText = child.text or ""
                    parentElement.appendChild(element)

                return parentElement

            attachChildren(root, doc_root)

            article = Article(doc_root)
            articleFilePath = os.path.join(
                os.path.split(hdoc)[0],
                "index.html"
            )
            assert not os.path.exists(articleFilePath), ""

            with open(articleFilePath, "x", encoding="utf-8") as articleFile:
                template = Templates.getTemplates()["article"]

                # 
                encoding = article.propertyEntries.get("encoding")
                lang = article.propertyEntries.get("lang")
                title = article.propertyEntries.get("title")
                titleID = article.propertyEntries.get("titleID")
                description = article.propertyEntries.get("description")
                tags = article.propertyEntries.get("tags")
                author = article.propertyEntries.get("author")
                authorID = article.propertyEntries.get("authorID")
                datePublished = article.propertyEntries.get("date:published")
                dateModified = article.propertyEntries.get("date:modified")
                __all_meta__ = {"encoding": encoding, "lang": lang, "title": title, "titleID": titleID, "description": description, "tags": tags, "author": author, "authorID": authorID, "datePublished": datePublished, "dateModified": dateModified}
                assert all(list(__all_meta__.values())), f"Missing data: [{', '.join([x for x in __all_meta__ if not __all_meta__[x]])}]"

                headMetadata = f"""
<!-- Basic Information -->
<meta name="author" content="Hamen.io">
<meta name="description" content="{description}">
<meta name="keywords" content="{", ".join([x.strip() for x in tags.split(",")])}">

<!-- Canonical Link -->
<link rel="canonical" href="https://www.hamen.io">

<!-- Open Graph Meta Tags (for social media) -->
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://www.hamen.io/static/media/favicon/favicon.png">
<meta property="og:url" content="https://www.hamen.io">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Hamen.io">

<!-- X.com Card Meta Tags (for X.com) -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@HamenIO">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://www.hamen.io/static/media/favicon/favicon.png">

<!-- Robots Meta Tag -->
<meta name="robots" content="index, follow">

<!-- Favicon -->
<link rel="icon" href="https://www.hamen.io/favicon.png" type="image/x-icon">

<!-- Theme Color for Mobile Browsers -->
<meta name="theme-color" content="#ffffff">

<!-- Mobile App Meta Tags -->
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="application-name" content="{title}">
<meta name="apple-mobile-web-app-title" content="{title}">

<!-- Prism.JS -->
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
{
_NEWLINE_.join([
    "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/components/prism-" + x + ".min.js\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"></script>"
        for x in _PRISM_PACKAGES_
])
}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css">
"""
                
                headMetadata = headMetadata.strip().split("\n")
                headMetadata = f"\n{(_HTML_TAB_ * 2)}".join(headMetadata)

                staticRelativePathPrefix = "../" * (len([x for x in articleFilePath.split("hamen.io/artifacts")[-1].split("/") if x.strip()]) - 1)
                staticRelativePathPrefix = staticRelativePathPrefix.rstrip("/")
                articleFile.write(
                    template.getContents(
                        articleBody = article.documentBody,
                        articleTitle = title,
                        articleAside = "",
                        headMetadata = headMetadata,
                        importStyles = f"\n{_HTML_TAB_ * 2}".join([re.sub(r"\{\{\s*STATIC_FOLDER\s*\}\}", staticRelativePathPrefix, x) for x in self.buildSite.getImports("STYLESHEET")]),
                        importJavaScript = f"\n{_HTML_TAB_ * 2}".join([re.sub(r"\{\{\s*STATIC_FOLDER\s*\}\}", staticRelativePathPrefix, x) for x in self.buildSite.getImports("JAVASCRIPT")]),
                    )
                )

            return article