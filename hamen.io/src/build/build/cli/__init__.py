import os

class CLI:
    def __init__(self):
        self._cwd: str = os.path.dirname(__file__)

    @property
    def cwd(self) -> str:
        return self._cwd
    
    @cwd.setter
    def cwd(self, path: str) -> None:
        if os.path.isfile(path):
            path = os.path.dirname(path)

        if not os.path.isabs(path):
            self._cwd = path
        self._cwd = path

    def init(self) -> None:
        pass

if __name__ == "__main__":
    CLI()