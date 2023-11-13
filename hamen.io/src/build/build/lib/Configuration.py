import os
import re

import lib.FileSystem as FileSystem

class ConfigurationFile:
    def __init__(self, code: str = None) -> None:
        self.code = code

        assert self.code

    @staticmethod
    def loadFile(file: str) -> 'ConfigurationFile':
        assert os.path.exists(file) and os.path.isfile(file) and os.path
        with open(file, "r"):
            pass