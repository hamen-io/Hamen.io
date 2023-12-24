from hooks.Hook import Hook
import sass

class CompileSASS(Hook):
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