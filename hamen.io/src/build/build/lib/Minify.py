from csscompressor import compress as minifyCSS
from htmlmin import minify as minifyHTML
from rjsmin import jsmin as minifyJS

import lib.FileSystem as FileSystem

from typing import TextIO
import os

class Minify:
    def __init__(self, code: str = None):
        self.code = code

    def testFile(self, file: str) -> bool:
        return FileSystem.fileExtension(file)
    
    def toFile(self, file: TextIO) -> None:
        file.write(self._minify())

    def toString(self) -> str:
        return self._minify()

    # def _minify(self) -> str:
    #     return self.code
    
    def __str__(self) -> str:
        return self.toString()

class CSS(Minify):
    def _minify(self) -> str:
        return minifyCSS(self.code)

class JS(Minify):
    def _minify(self) -> str:
        return minifyJS(self.code)

class HTML(Minify):
    def _minify(self) -> str:
        return minifyHTML(self.code, True, False, False, True, True, False)