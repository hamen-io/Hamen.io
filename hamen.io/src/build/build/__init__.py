import sass
import json
import shutil
from typing import Literal,Type
import re
from lxml import etree
import os
import ftplib

from HamenAPI import (Common,Elements,Exceptions,System,Templates,Types,FileSystem,Minify)
from hooks.Hook import Hook

_NEWLINE_ = "\n"
_BACKSLASH_ = "\\"

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

    def createImport(self, importType: Literal["JAVASCRIPT", "STYLESHEET"], src: str, *, isRelative: bool = False) -> None:
        """
        Creates a resource imports; either JavaScript, or CSS/Stylesheet
        """
        prefix = "{{STATIC_FOLDER}}" if isRelative else ""
        match importType:
            case "JAVASCRIPT":
                self._jsImports.add(f"""<script type="text/javascript" defer src="{prefix}{src}"></script> """)
            case "STYLESHEET":
                self._cssImports.add(f"""<link rel="stylesheet" href="{prefix}{src}" /> """)
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

if __name__ == "__main__":
    os.system("clear")
    print("--- BUILD START ---\n\n")

    release = BuildSite()

    # Set build metadata:
    release.releaseDirectory = r"hamen.io/www"
    release.devDirectory = r"hamen.io/dev"
    release.buildVersion = (1, 0, 0)

    # Add resources:
    release.createImport("JAVASCRIPT", "/static/js/index.js", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/importFonts.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/importIcons.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/ui.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/webTheme.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/index.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/utilityClasses.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/prism.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/doc.css", isRelative=True)

    # Load and build site:
    release.loadDev()
    release.buildSite()

    # Handle subdomains:
    release.createSubdomainRedirect(r"docs.hamen.io", "hamen.io/docs")
    release.createSubdomainRedirect(r"support.hamen.io", "hamen.io/support")
    release.createSubdomainRedirect(r"software.hamen.io", "hamen.io/software")

    # Handle hooks:
    from hooks.BuildDoc import BuildDoc
    from hooks.CompileSASS import CompileSASS
    from hooks.MinifyFiles import MinifyFiles
    from hooks.RenamePublicHTML import RenamePublicHTML
    release.registerHook(BuildDoc)
    release.registerHook(CompileSASS)
    release.registerHook(MinifyFiles)
    release.registerHook(RenamePublicHTML)
    release.executeHooks()

    print("\n\n--- BUILD END ---")