import sass
import json
import shutil
from typing import Literal,Type
import re
from lxml import etree
import os
import ftplib

from HamenAPI import (Common,Elements,Exceptions,System,Templates,Types,FileSystem,Minify)

_HTML_TAB_ = "    "

_NEWLINE_ = "\n"
_BACKSLASH_ = "\\"

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

class BuildSite:
    def __init__(self):
        """
        Official build class for Hamen.io

        Read documentation before using
        """

        self._siteBuilt: bool = False
        """ Site has been built """

        self.devDirectory: str = None
        """ Path to development directory """

        self.releaseDirectory: str = None
        """ Path to production/release directory """

        self.buildVersion: tuple[int, int, int] = None
        """ Build version as a tuple """

        self.hooks: list[Hook] = []
        """  """

        self._jsImports = set()
        self._cssImports = set()

    def createImport(self, importType: Literal["JAVASCRIPT", "STYLESHEET"], src: str) -> None:
        """
        Creates a resource imports; either JavaScript, or CSS/Stylesheet
        """
        match importType:
            case "JAVASCRIPT":
                self._jsImports.add(f"""<script type="text/javascript" defer src="{src}"></script> """)
            case "STYLESHEET":
                self._cssImports.add(f"""<link rel="stylesheet" href="{src}" /> """)
            case _:
                assert False, f"Invalid importType: '{importType}'"

    def getImports(self, importType: Literal["JAVASCRIPT", "STYLESHEET"]) -> list[str]:
        assert importType in ["JAVASCRIPT", "STYLESHEET"]
        return list(self._jsImports) if importType == "JAVASCRIPT" else list(self._cssImports)

    def registerHook(self, hook: Type['Hook']) -> None:
        """
        Registers a hook
        """
        if hook not in self.hooks:
            self.hooks.append(hook)

    def executeHooks(self) -> None:
        """
        Execute all callback hooks in the hook list (`self.hooks`)
        """
        for hook in self.hooks:
            hook: Type['Hook']
            hook(self.releaseDirectory, self)

    def loadDev(self) -> None:
        """
        
        """
        self.__all__: tuple = ("releaseDirectory", "buildVersion", "devDirectory")
        self.__all__: dict[str, any] = {k: getattr(self, k) for k in self.__all__}
        """ Tuple of all required properties """

        # Ensure user has specified everything necessary:
        assert all([self.__all__[x] for x in self.__all__]), f"The following attributes were not specified:\n{_NEWLINE_.join(['  - ' + str(k) for k,v in self.__all__.items() if not v])}"

        # 

    def buildSite(self) -> None:
        """
        Steps to building:
        1. Clear the /www directory
        2. Copy dev directory
        3. Go through each file in the dev directory and interpret;
            `.hdoc` -> `.html`
        """
        # Step 1: Clear the /www directory
        shutil.rmtree(self.releaseDirectory)

        # Step 2: Copy dev directory
        shutil.copytree(self.devDirectory, self.releaseDirectory)

    @property
    def siteBuilt(self) -> bool:
        """
        Returns whether the site has been built
        """
        return self._siteBuilt

    @property
    def adsFile(self) -> str:
        """
        Returns the path to the `ads.txt` file
        """
        return os.path.join(self.releaseDirectory, "ads.txt")

    @property
    def adsFileContent(self) -> str:
        """
        Returns the content of `ads.txt`
        """

    @adsFileContent.setter
    def adsFileContent(self, content: str) -> None:
        """
        Sets the content of `ads.txt`
        """

        # Ensure the site has been built:
        System.assertError(
            self.siteBuilt,
            Exceptions.ReadOnlyError(
                f"The `ads.txt` file can only be modified once the site has been built; change its root code by modifying the file directly"
            )
        )

        # Write to the `ads.txt` file:
        with open(self.adsFile, "w", encoding="utf-8") as file:
            file.write(content)

    @property
    def htaccessFile(self) -> str:
        """
        Returns the path to the `.htaccess` file
        """
        return os.path.join(self.releaseDirectory, ".htaccess")

    @property
    def htaccessFileContent(self) -> str:
        """
        Returns the content of `.htaccess`
        """

    @htaccessFileContent.setter
    def htaccessFileContent(self, content: str) -> None:
        """
        Sets the content of `.htaccess`
        """

        # Ensure the site has been built:
        System.assertError(
            self.siteBuilt,
            Exceptions.ReadOnlyError(
                f"The `.htaccess` file can only be modified once the site has been built; change its root code by modifying the file directly"
            )
        )

        # Write to the `.htaccess` file:
        with open(self.htaccessFile, "w", encoding="utf-8") as file:
            file.write(content)

    def createSubdomainRedirect(self, subdomain: str, redirect: str) -> None:
        """
        Creates a redirect so when the user accesses "{subdomain}", it goes to "{redirect}"

        Subdomains should include "hamen.io"; for example: "docs.hamen.io", "create.docs.hamen.io", etc
        Redirects should include "hamen.io"; for example: "hamen.io/docs", "hamen.io/docs/create-docs", etc
        """
        # Validate subdomain:
        assert re.findall(r"^((\w+((?<=\w)\.\w*)?)+)(\.hamen\.io)$", subdomain), f"Invalid subdomain: '{subdomain}'"

        # Validate redirect:
        assert re.findall(r"^(hamen\.io)(\/[a-zA-Z0-9_\-\.]+)+$", redirect), f"Invalid redirect: '{redirect}';\n    redirects should start with 'hamen.io/...' (where `...` is a valid path)"

        # Replace "/" with "\"
        subdomain,redirect = subdomain.replace("/", "\\"),redirect.replace("/", "\\")

        # Create `redirect` and subdomain if it does not exist:
        subdomain = os.path.join(self.releaseDirectory, subdomain)
        os.makedirs(subdomain)
        with open(os.path.join(subdomain, "index.html"), "x", encoding="utf-8") as file:
            file.write(f"""<script>window.location.replace("https://www.{redirect.replace(_BACKSLASH_, "/")}")</script>""")

class Hook:
    """
    A hook is a class that is executed after the build is complete

    A hook is ONLY able to access the production directory
    """
    def __init__(self, buildDirectory: str, buildSite: BuildSite) -> None:
        self.buildDirectory: str = buildDirectory
        self.buildSite = buildSite
        self.execute()

    def execute(self) -> bool:
        return True
    
    def searchFiles(self, *, folderPattern: str = None, filePattern: str = None, limit: int = None) -> list[FileSystem.File]:
        assert folderPattern or filePattern
        fileList = []

        for root, dirs, files in os.walk(self.buildDirectory, topdown=False):
            for file in files:
                path = os.path.join(root, file)
                if re.findall(filePattern, file):
                    fileList.append(FileSystem.File(path))

        return fileList

class Hooks:
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
<link rel="icon" href="https://www.hamen.io/static/media/favicon/favicon.ico" type="image/x-icon">

<!-- Theme Color for Mobile Browsers -->
<meta name="theme-color" content="#ffffff">

<!-- Mobile App Meta Tags -->
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="application-name" content="{title}">
<meta name="apple-mobile-web-app-title" content="{title}">
"""
                    
                    headMetadata = headMetadata.strip().split("\n")
                    headMetadata = f"\n{(_HTML_TAB_ * 2)}".join(headMetadata)

                    articleFile.write(
                        template.getContents(
                            articleBody = article.documentBody,
                            articleTitle = title,
                            headMetadata = headMetadata,
                            importStyles = f"\n{_HTML_TAB_ * 2}".join(self.buildSite.getImports("STYLESHEET")),
                            importJavaScript = f"\n{_HTML_TAB_ * 2}".join(self.buildSite.getImports("JAVASCRIPT")),
                        )
                    )

                return article

    class Sass(Hook):
        """
        Compiles all sass files
        """
        def execute(self) -> None:
            for file in self.searchFiles(filePattern=r"\.scss|\.sass"):
                with open(file.withExtension("css").fullFilePath, "x", encoding="utf-8") as cssFile:
                    with open(file.fullFilePath, "r", encoding="utf-8") as sassFile:
                        cssFile.write(
                            sass.compile(
                                string=sassFile.read(),
                                output_style="compressed"
                            )
                        )

    class Minify(Hook):
        """
        Minifies all HTML, JS, and CSS files
        """
        def execute(self) -> None:
            for file in self.searchFiles(filePattern=r"\.(html|css|js)$"):
                content: str = None

                with open(file.fullFilePath, "r", encoding="utf-8") as fileRead:
                    content: str = fileRead.read()

                with open(file.fullFilePath, "w", encoding="utf-8") as fileWrite:
                    match file.fileExtension:
                        case "html":
                            fileWrite.write(
                                Minify.HTML(content).toString()
                            )
                        case "css":
                            fileWrite.write(
                                Minify.CSS(content).toString()
                            )
                        case "js":
                            fileWrite.write(
                                Minify.JS(content).toString()
                            )
                        case _:
                            assert False, f"Invalid match: '{file.fileExtension}'"

    class RenamePublicHTML(Hook):
        """
        Renames the `hamen.io` folder to `public_html`
        """
        def execute(self) -> None:
            os.rename(os.path.join(self.buildDirectory, "hamen.io"), os.path.join(self.buildDirectory, "public_html"))

if __name__ == "__main__":
    os.system("clear")
    print("--- BUILD START ---\n\n")

    release = BuildSite()

    # Set build metadata:
    release.releaseDirectory = r"hamen.io/www"
    release.devDirectory = r"hamen.io/dev"
    release.buildVersion = (1, 0, 0)

    # Add resources:
    release.createImport("JAVASCRIPT", "https://www.hamen.io/static/js/index.js")
    release.createImport("STYLESHEET", "https://www.hamen.io/static/css/importFonts.css")
    release.createImport("STYLESHEET", "https://www.hamen.io/static/css/importIcons.css")
    release.createImport("STYLESHEET", "https://www.hamen.io/static/css/ui.css")
    release.createImport("STYLESHEET", "https://www.hamen.io/static/css/webTheme.css")
    release.createImport("STYLESHEET", "https://www.hamen.io/static/css/index.css")
    release.createImport("STYLESHEET", "https://www.hamen.io/static/css/utilityClasses.css")
    release.createImport("STYLESHEET", "https://www.hamen.io/static/css/doc.css")

    # Load and build site:
    release.loadDev()
    release.buildSite()

    # Handle subdomains:
    release.createSubdomainRedirect(r"docs.hamen.io", "hamen.io/docs")
    release.createSubdomainRedirect(r"support.hamen.io", "hamen.io/support")
    release.createSubdomainRedirect(r"software.hamen.io", "hamen.io/software")

    # Handle hooks:
    release.registerHook(Hooks.BuildDoc)
    release.registerHook(Hooks.Sass)
    release.registerHook(Hooks.Minify)
    release.registerHook(Hooks.RenamePublicHTML)
    release.executeHooks()

    print("\n\n--- BUILD END ---")