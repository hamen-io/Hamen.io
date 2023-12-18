from enum import Enum
from typing import Literal
import re
import os

os.system("clear")

supportedLanguages: list[str] = ["LESS", "SASS", "PYTHON", "JAVA", "XML", "HTML", "CSS"]

class Theme(Enum):
    white = "rgb(255, 255, 255)"
    comment = "rgb(0, 0, 255)"

class Tag:
    tagName: str
    tagValue: str
    tagColor: Theme

    def __init__(self, value: str = ""):
        self.tagValue = value

class Tags:
    class String(Tag):
        tagName = "string"
        tagColor = Theme.white

    class Number(Tag):
        tagName = "number"
        tagColor = Theme.white

    class Keyword(Tag):
        tagName = "boolean"
        tagColor = Theme.white

    class Operator(Tag):
        tagName = "boolean"
        tagColor = Theme.white

    class Variable(Tag):
        tagName = "boolean"
        tagColor = Theme.white

class CodeRenderer:
    singleLineString: list[str]
    """ Define a single-line string. Must open and close with this character """

    multiLineString: list[str]
    """ Define a multi-line string such as `\"\"\"` """
    
    reservedKeywords: list[str]
    """ List of reserved keywords in this language such as `for`, `import`, etc """

    reservedOperators: list[str]
    """ List of operators in this language such as `+`, `===`, etc """

    reservedValues: list[str]
    """ List of reserved values such as `null`, `false`, `true`, etc """

    numberTypes: list[str]

    variableName: list[str]
    """ List of Regular Expressions to match variable names (e.g. /[a-zA-Z_]+[a-zA-Z0-9_]*/ for Python-variables) """

    singleLineComment: list[str]

    builtIns: list[str]

    def __init__(self, code: str) -> None:
        self.code = code
        self.render()

    def render(self) -> list[Tag]:
        content = re.split(r"((?<!\\)\"(?:\\\\|\\\"|[^\"])*\"(?<!\\))", self.code)
        content = [Tags.String(x) if x.startswith("\"") and x.endswith("\"") else x for x in content]
        tags = []

        matches = dict()
        for l in (self.singleLineComment, self.multiLineString, self.reservedKeywords, self.reservedOperators, self.reservedValues, self.numberTypes, self.variableName, self.singleLineComment, self.builtIns):
            for k in l:
                matches[k] = f"{l=}".split("=")[0]

        for elem in content:
            if type(elem) is Tags.String:
                tags.append(tags)
                continue

            # print(re.findall(fr"({'|'.join(list(matches.keys()))})", elem))

class Languages:
    class Python(CodeRenderer):
        singleLineString = ["\"", "\'"]
        multiLineString = ["\"\"\"", "'''"]
        reservedKeywords = ["class", "def", "for", "if", "elif", "else", "case", "match", "try", "except", "return", "lambda", "import"]
        reservedOperators = ['+', '-', '*', '/', '//', '%', '**', '==', '!=', '>', '<', '>=', '<=', '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=', '&', '|', '^', '~', '<<', '>>', "(", "[", "{", ")", "]", "}"]
        reservedValues = ["True", "False", "None", "in", "not", "is"]
        numberTypes = [r"((-?)(\d*\.?\d+)([Ee](\+|\-))?)"]
        variableName = [r"^([a-zA-Z_]+[a-zA-Z0-9_]*)$"]
        singleLineComment = ["#"]
        builtIns = ['str', 'int', 'float', 'bool', 'list', 'tuple', 'set', 'dict', 'abs', 'len', 'max', 'min', 'sum', 'round', 'sorted', 'type', 'id', 'range', 'capitalize', 'casefold', 'count', 'endswith', 'find', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isupper', 'join', 'lower', 'upper', 'replace', 'split', 'strip', 'title', 'append', 'extend', 'insert', 'remove', 'pop', 'clear', 'index', 'count', 'sort', 'reverse',  'add', 'remove', 'discard', 'pop', 'clear', 'union', 'intersection', 'difference', 'symmetric_difference', 'clear', 'copy', 'get', 'items', 'keys', 'values', 'pop', 'popitem', 'update', 'divmod', 'pow', 'print', 'input', 'dir', 'help', 'id', 'len', 'callable', 'ord', 'chr', 'hash', 'lambda', 'map', 'filter', 'reduce', 'open', 'read', 'write', 'close', 'seek', 'tell', 'isinstance', 'issubclass', 'getattr', 'setattr', 'delattr', 'hasattr']

# def renderCode(code: str, *, lang: str) -> CodeRenderer:
#     match lang:
#         case "PYTHON": pass

# Languages.Python("""
# import string
                 
# def main(a: int, b: int) -> str:
#     return str(a + b)

# print("Test!")
# """)