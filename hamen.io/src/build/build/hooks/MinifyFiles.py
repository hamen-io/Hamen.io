from hooks.Hook import Hook

from HamenAPI import Minify

class MinifyFiles(Hook):
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