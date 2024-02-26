import sass
import json
import shutil
from typing import (Literal,Type,Iterable)
import re
from lxml import etree
import errno
import os
import ftplib

from hooks.Hook import Hook

_NEWLINE_ = "\n"
_BACKSLASH_ = "\\"

import lib.Types as Types
import lib.Common as Common
import lib.Exceptions as Exceptions
import lib.System as System
import lib.Elements as Elements
import lib.Templates as Templates
import lib.Configuration as Configuration
import lib.FileSystem as FileSystem
import lib.Minify as Minify
import lib.Console as Console

def flattenList(arr: list) -> list:
    arr = arr.copy()
    flatList = []
    for x in arr:
        if isinstance(x, (list, tuple, set)):
            flatList.extend(flattenList(x))
        else:
            flatList.append(x)

    return flatList

class ConfigFile:
    def __init__(self, file: str):
        self.file = file
        assert os.path.exists(file) and os.path.isfile(file) and file.lower().endswith(".config.build")
        self.config = dict()
        with open(self.file, "r") as fileStream:
            rawConfig = [x for x in fileStream.read().split(";") if x]
            self.config = {k.strip().upper(): (v[0] if len(v) == 1 else v) for k,v in {x.split("=", 1)[0]: x.split("=", 1)[1:] for x in rawConfig}.items()}
            for k,v in self.config.items():
                m = re.match(r"^(((?<!\\)(?:\\\\)*\"(?:[^\"\\]|\\.)*?\"|true|false|\d)\s*,{0,1}\s*)+$", v)
                if not m:
                    raise ValueError("Invalid value : '%s'" % v)

                m = [x[1:-1] if type(x) is str and x.startswith("\"") and x.endswith("\"") else x for x in m.groups()]

                self.config[k] = m

class BuildProcess:
    def __init__(self, buildSite: 'BuildSite'):
        self._buildSite: BuildSite = buildSite
        self._stackTrace = []

    @property
    def isComplete(self) -> bool:
        return self._isComplete

    @isComplete.setter
    def isComplete(self, value: bool) -> None:
        raise AttributeError(f"Cannot assign property, 'isComplete', of class: 'BuildProcess' as it is ReadOnly.")

    def throwError(self, errorType: str, errorMessage: str):
        self._buildSite.console.error(errorMessage, errorType)

    def assertError(self, condition: bool, errorType: str, errorMessage: str):
        if not condition:
            self.throwError(errorType, errorMessage)

    def throwWarning(self, warningType: str, warningMessage: str):
        self._buildSite.console.warn(warningMessage, warningType)

    def assertWarning(self, condition: bool, warningType: str, warningMessage: str):
        if not condition:
            self.throwWarning(warningType, warningMessage)

class BuildSite:
    def __init__(self):
        """
        Official build class for Hamen.io

        Read documentation before using
        """

        self.console = Console.Console()
        """ Provides an interface to standard output console """

        self.buildProcess = BuildProcess(self)

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
                self.console.error(f"An error occurred within `BuildSite.createImport( ... )` ; invalid `importType` property value: '{importType}'", "ImportError")

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
        os.makedirs(self.releaseDirectory)
        for root, dirs, files in os.walk(self.devDirectory):
            # Compute the destination directory for this root
            dst_root = os.path.join(self.releaseDirectory, os.path.relpath(root, self.devDirectory))

            # Create the destination directory for this root
            try:
                os.makedirs(dst_root)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            # Copy files
            ignoreFiles = [".config.build"]
            if ".config.build" in [x.lower() for x in os.listdir(root)]:
                configFile = os.path.join(root, ".config.build")
                file = ConfigFile(configFile)
                ignoreFiles.append(file.config.get("IGNORE_FILES") or [])
                ignoreFiles = flattenList([ignoreFiles])
                ignoreFiles = [x.lower().strip() for x in ignoreFiles]

            for file in files:
                if file.lower() in ignoreFiles:
                    continue

                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_root, file)
                with open(src_file, "rb") as f_src, open(dst_file, "wb") as f_dst:
                    f_dst.write(f_src.read())

        self._siteBuilt = True

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
        with open(self.adsFile, "r") as file:
            return file.read()

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
