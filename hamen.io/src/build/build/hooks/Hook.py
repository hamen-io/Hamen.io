import re
import os

import lib.FileSystem as FileSystem

class Hook:
    """
    A hook is a class that is executed after the build is complete

    A hook is ONLY able to access the production directory
    """
    def __init__(self, buildDirectory: str, buildSite) -> None:
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