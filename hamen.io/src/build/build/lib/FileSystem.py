import re
from typing import Type
import os

class FileExtension:
    def __init__(self, ext: str) -> None:
        self.ext = ext.lower()
        if self.ext.startswith("."):
            self.ext = self.ext[1:]

    def match(self, ext: str | Type['FileExtension']) -> bool:
        if not isinstance(ext, FileExtension):
            ext = FileExtension(ext)

        return self.ext.lower() == ext.ext.lower()

    def __str__(self) -> str:
        return "." + self.ext

class File:
    def __init__(self, path: str) -> None:
        self.file = os.path.split(path)[-1]
        """ Full file name; includes the base name and its filetype (no path) """

        self.fileExtension,self.fileName = [x[::-1] for x in self.file[::-1].split(".", 1)]

        self.fileExtension: str = self.fileExtension.lower()
        """ File extension; lowercase and sans-dot """

        self.fileName: str = self.fileName
        """  """

        self.filePath = str = os.path.split(path)[0]
        """  """

        self.fullFilePath: str = path
        """  """

    def withExtension(self, ext: str) -> 'File':
        if not ext.startswith("."):
            ext = "." + ext
        assert re.findall(r"^\.[a-z]+[a-z0-9]*$", ext.lower()), f"Invalid filetype: '{ext}'"

        return File(os.path.splitext(self.fullFilePath)[0] + ext.lower())

def fileExists(file: str) -> bool:
    return os.path.exists(file) and os.path.isfile(file)

def dirExists(_dir: str) -> bool:
    return os.path.exists(_dir) and os.path.isdir(_dir)

def fileExtension(file: str, includeDot: bool = True) -> str:
    """
    Returns the file extension of `file` as a string
    """
    assert os.path.isfile(file)
    return os.path.splitext(file)[-1].lower()[(0 if includeDot else 1):]