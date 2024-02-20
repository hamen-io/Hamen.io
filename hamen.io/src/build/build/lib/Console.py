from typing import Literal
import sys
import os

class ConsoleColors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

def style(text: str, *styles: Literal["RESET", "BOLD", "DIM", "ITALIC", "UNDERLINE", "BLINK", "REVERSE", "HIDDEN", "BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "BRIGHT_BLACK", "BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW", "BRIGHT_BLUE", "BRIGHT_MAGENTA", "BRIGHT_CYAN", "BRIGHT_WHITE"], dangle: bool = False) -> str:
    prefix = ""
    for style in styles:
        match style:
            case "RESET": prefix += ConsoleColors.RESET
            case "BOLD": prefix += ConsoleColors.BOLD
            case "DIM": prefix += ConsoleColors.DIM
            case "ITALIC": prefix += ConsoleColors.ITALIC
            case "UNDERLINE": prefix += ConsoleColors.UNDERLINE
            case "BLINK": prefix += ConsoleColors.BLINK
            case "REVERSE": prefix += ConsoleColors.REVERSE
            case "HIDDEN": prefix += ConsoleColors.HIDDEN
            case "BLACK": prefix += ConsoleColors.BLACK
            case "RED": prefix += ConsoleColors.RED
            case "GREEN": prefix += ConsoleColors.GREEN
            case "YELLOW": prefix += ConsoleColors.YELLOW
            case "BLUE": prefix += ConsoleColors.BLUE
            case "MAGENTA": prefix += ConsoleColors.MAGENTA
            case "CYAN": prefix += ConsoleColors.CYAN
            case "WHITE": prefix += ConsoleColors.WHITE
            case "BRIGHT_BLACK": prefix += ConsoleColors.BRIGHT_BLACK
            case "BRIGHT_RED": prefix += ConsoleColors.BRIGHT_RED
            case "BRIGHT_GREEN": prefix += ConsoleColors.BRIGHT_GREEN
            case "BRIGHT_YELLOW": prefix += ConsoleColors.BRIGHT_YELLOW
            case "BRIGHT_BLUE": prefix += ConsoleColors.BRIGHT_BLUE
            case "BRIGHT_MAGENTA": prefix += ConsoleColors.BRIGHT_MAGENTA
            case "BRIGHT_CYAN": prefix += ConsoleColors.BRIGHT_CYAN
            case "BRIGHT_WHITE": prefix += ConsoleColors.BRIGHT_WHITE

    return f"{prefix}{text.__str__()}{ConsoleColors.RESET if not dangle else ""}"

class Console:
    def __init__(self, *, logFile: str = None):
        self.logFile = logFile
    
    def _assembleOutput(self, *content, end: str = "\n", sep: str = " "):
        return sep.join(list([x.__str__() for x in content])) + end
    
    def _out(self, output: str) -> None:
        sys.stdout.write(output)

    def log(self, *content, end: str = "\n", sep: str = " ", condition: bool = True) -> None:
        if condition:
            self._out(self._assembleOutput(*content, end = end, sep = sep))

    def error(self, errorMessage: str, errorName: str = "Error", *, end: str = "\n", justifyMessage: bool = True, condition: bool = True) -> None:
        if condition:
            errorName = f"{errorName} : "
            self._out(f"{style(errorName, "RED", "BOLD")}{style(self._justifyIndentation(errorMessage.__str__(), len(errorName)), "RED", "ITALIC") if justifyMessage else errorMessage.__str__()}{end}")

    def warn(self, warningMessage: str, warningName: str = "Warning", *, end: str = "\n", justifyMessage: bool = True, condition: bool = True) -> None:
        if condition:
            warningName = f"{warningName} : "
            self._out(f"{style(warningName, "MAGENTA", "BOLD")}{style(self._justifyIndentation(warningMessage.__str__(), len(warningName)) if justifyMessage else warningMessage.__str__(), "MAGENTA", "ITALIC")}{end}")
    
    def clear(self, *, condition: bool = True) -> None:
        if condition:
            os.system("clear")

    def _justifyIndentation(self, text: str, to: int) -> str:
        text = text.split("\n")
        return text[0] + ("\n" + "\n".join([" " * to + x for x in text[1:]]) if len(text) > 1 else "")
