import re
import os

class Template:
    def __init__(self, file: str = None):
        self.file = file
        self.fileName = os.path.splitext(self.file)[0]

    def getContents(self, **kwargs) -> str:
        contents = None
        with open(os.path.join(templatesFolderPath(), self.file), "r") as file:
            contents = file.read()

        for key,value in kwargs.items():
            contents = re.sub(r"\{\{\s*" f"{key}" r"\s*\}\}", str(value), contents)

        return contents

def templatesFolderPath() -> str:
    module = os.path.split(__file__)[0]
    return os.path.join(module, "templates")

def getTemplates() -> dict[str, Template]:
    templateDictionary = dict()
    for templateFile in os.listdir(templatesFolderPath()):
        template = Template(templateFile)
        templateDictionary[template.fileName] = template
    return templateDictionary