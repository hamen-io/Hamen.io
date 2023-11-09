import shutil
from typing import Literal,Type
import re
from lxml import etree
import os

import lib.Types as Types
import lib.Common as Common
import lib.Exceptions as Exceptions
import lib.System as System
import lib.Elements as Elements

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
        print(self.document.__str__(True))

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
        with open(self.adsFile, "w") as file:
            file.write(content)

    def createSubdomainRedirect(self, subdomain: str, redirect: str) -> None:
        """
        
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
        with open(os.path.join(subdomain, "index.html"), "x") as file:
            file.write(f"""<script>window.location.replace("https://www.{redirect.replace(_BACKSLASH_, "/")}")</script>""")

if __name__ == "__main__":
    release = BuildSite()

    release.releaseDirectory = r"hamen.io\www"
    release.devDirectory = r"hamen.io\dev"
    release.buildVersion = (1, 0, 0)

    release.loadDev()
    release.buildSite()

    release.createSubdomainRedirect(r"docs.hamen.io", "hamen.io/docs")

    # with open(r"C:\Users\danie\Desktop\Private Directory\Hamen-Projects\hamen.io\dev\hamen.io\md\guides\code\python-course\python-basics\what-is-python\index.hdoc", "r", encoding = "utf-8") as file:
    #     code = file.read()
    #     code = re.sub(r"<!--[\s\S]*?-->", "", code)
    #     code = re.sub(r"""(\w+)={\s*(("|')?((.|\n)*?)(\3)?)\s*}""", r'\1="\4"', code)

    #     root = etree.fromstring(code)
    #     root: etree._Element
    #     assert root.tag.upper() == "DOC", f"Root element should be <Doc>; not: '{root.tag}'"

    #     doc_root = Elements.Doc()
    #     doc_root.extendAttributes(root.attrib)

    #     def attachChildren(children: etree._Element, parentElement: Elements.Element):
    #         for child in children:
    #             child: etree._Element

    #             element = None
    #             tag = child.tag

    #             # Replace namespaces:
    #             tag = re.sub(r"\{(.*)(\/)(.*)\}(.*)", r"\3:\4", tag)

    #             # Tags are case-insensitive; make lowercase for better matches:
    #             tag = tag.lower()

    #             match tag:
    #                 case "doc": element = Elements.Doc()
    #                 case "properties": element = Elements.Properties()
    #                 case "document": element = Elements.Document()
    #                 case "entry": element = Elements.Entry(key = child.attrib.get("key"), value = child.attrib.get("value"))
    #                 case "ui:h1": element = Elements.UI.H1()
    #                 case "ui:h2": element = Elements.UI.H2()
    #                 case "ui:section": element = Elements.UI.Section()
    #                 case "ui:text": element = Elements.UI.Text()
    #                 case "ui:list": element = Elements.UI.List()
    #                 case "ui:item": element = Elements.UI.Item()
    #                 case "ui:break": element = Elements.UI.Break()
    #                 case "ui:hrule": element = Elements.UI.HRule()
    #                 case "i": element = Elements.Format.i()
    #                 case "em": element = Elements.Format.em()
    #                 case "b": element = Elements.Format.b()
    #                 case "u": element = Elements.Format.u()
    #                 case "mark": element = Elements.Format.mark()
    #                 case _: raise SyntaxError(f"Unknown tag: '{tag}'")

    #             element = attachChildren(child, element)

    #             element.extendAttributes(child.attrib)
    #             element.innerText = (child.text or "").strip()
    #             parentElement.appendChild(element)

    #         return parentElement

    #     attachChildren(root, doc_root)

    #     a = Article(doc_root)