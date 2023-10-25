import shutil
import os
import re
from typing import Literal

class TextStyles:
    class Style:
        def __init__(self, text: str) -> None:
            self.text = text
            self.styleName = "STYLE"

    class Bold(Style):
        def __init__(self, text: str) -> None:
            super().__init__(text)
            self.styleName = "BOLD"

    class Underline(Style):
        def __init__(self, text: str) -> None:
            super().__init__(text)
            self.styleName = "UNDERLINE"

    class Strikethrough(Style):
        def __init__(self, text: str) -> None:
            super().__init__(text)
            self.styleName = "STRIKETHROUGH"

    class Normal(Style):
        def __init__(self, text: str) -> None:
            super().__init__(text)
            self.styleName = "NORMAL"

class Text:
    def __init__(self, text: str | list[TextStyles.Style]) -> None:
        self.text = [TextStyles.Normal(text)] if type(text) is str else text
        self.text: list[TextStyles.Style]

    def __str__(self) -> str:
        return " ".join(self.text)

    def plainText(self) -> str:
        return " ".join([x.text for x in self.text])

class AddElement:
    def __init__(self, appendElement = lambda x : ""):
        self._appendElement = appendElement

    def createInnerHTML(self, text: list | str) -> None:
        if type(text) is str:
            text = [text]

        final_text = []
        for term in text:
            if type(term) is str:
                final_text.append(f"<span>{term}</span>")
            elif type(term) is dict:
                term: dict
                if len(term) != 1:
                    raise SyntaxError("1: Unknown Term: " + str(term))

                style,content = list(*term.items())
                for val,sub in {
                    ">": "&lt;",
                    "<": "&gt;",
                    }.items():
                    content = content.replace(val, sub)

                tag = []
                match style.upper():
                    case "BD" | "B" | "BOLD":
                        tag = ["b class=\"ui:bold\"", "b"]
                    case "UL" | "U" | "UNDERLINE":
                        tag = ["u class=\"ui:underline\"", "u"]
                    case "ST" | "S" | "STRIKETHROUGH":
                        tag = ["del class=\"ui:strikethrough\"", "del"]
                    case "CD" | "C" | "CODE":
                        tag = ["cd class=\"ui:inline-code\"", "cd"]
                    case _:
                        raise SyntaxError("Unknown style: " + str(style))

                final_text.append(f"<{tag[0]}>{content}</{tag[-1]}>")
            else:
                raise SyntaxError("2: Unknown Term: " + str(term))

        return "&nbsp;".join(final_text)

    def UIText(self, text: list | str) -> None:
        element = f"<p class=\"ui:paragraph\">{self.createInnerHTML(text)}</p>"

        self._appendElement(element)

class Section:
    def __init__(self):
        self._layout = []
        self._title: str
        self._id: str
        self.addElement = AddElement(lambda e : self._layout.append(e))

    @property
    def title(self) -> Text:
        return self._title
    
    @title.setter
    def title(self, title: str) -> None:
        self._title = title
        self._id = re.sub(r"[^A-Za-z0-9_ ]", "", title)

    @property
    def ID(self) -> str:
        return self._id
    
    def renderHTML(self) -> str:
        return f"""<section id="{self._id}"><header class="section:head"><h2 class="section:heading">{self._title}</h2></header><div class="section:body">{"".join(self._layout)}</div></section>"""

class Layout:
    def __init__(self):
        self._layout = []

    def createSection(self, title: Text) -> Section:
        s = Section()
        s.title = title

        return s

    def registerSection(self, section: tuple[Section] | Section) -> None:
        if type(section) is Section:
            section = [section]

        for s in section:
            self._layout.append(s)

    def renderHTML(self) -> str:
        content = []
        for section in self._layout:
            section: Section
            content.append(section.renderHTML())

        return "".join(content)

class DrawingError(Exception):
    """
    Error in the `draw` method of `Blog`
    """

class Blog:
    def __init__(self) -> None:
        self._blogTitle: str
        self._blogAuthor: str
        self._blogAuthorID: str
        self._blogDescription: str
        self._blogDate: str
        self._blogTags: list[str]
        self.layout = Layout()

    @property
    def blogTitle(self) -> str:
        return self._blogTitle

    @blogTitle.setter
    def blogTitle(self, value: str) -> None:
        assert type(value) is str, f"Invalid blog name"
        self._blogTitle = value

    @property
    def blogDate(self) -> str:
        return self._blogDate

    @blogDate.setter
    def blogDate(self, value: str) -> None:
        self._blogDate = value

    @property
    def blogDescription(self) -> str:
        return self._blogDescription

    @blogDescription.setter
    def blogDescription(self, value: str) -> None:
        self._blogDescription = value

    @property
    def blogTags(self) -> list:
        return self._blogTags

    @blogTags.setter
    def blogTags(self, tags: list[str]) -> None:
        self._blogTags = tags

    @property
    def blogAuthorID(self) -> str:
        return self._blogAuthorID

    @property
    def blogAuthor(self) -> str:
        return self._blogAuthor

    @blogAuthor.setter
    def blogAuthor(self, value: str) -> None:
        assert type(value) is str, f"Invalid blog name"
        self._blogAuthor = value
        self._blogAuthorID = re.sub(r"[^a-zA-Z]", "", value).lower()

    def renderHTML(self) -> str:
        self.draw()

        return re.sub(r"(?<!\\)\s", "", """
<!DOCTYPE\ HTML>
<html>
    <head>
        <title>{TITLE}\ &bull;\ Hamen\ Docs</title>
    </head>
    <body>
        <header></header>
        <main>
            <article>
                <section\ id="article-title">
                    <h1>{TITLE}</h1>
                    <p>By\ {AUTHOR};\ written\ {DATE}</p>
                </section>
                {BODY}
            </article>
        </main>
        <footer></footer>
    </body>
</html>
""").replace("\\ ", " ").format(
        TITLE = self.blogTitle,
        DATE = self.blogDate,
        AUTHOR = self.blogAuthor,
        BODY = self.layout.renderHTML()
    )

    def draw(self) -> None:
        raise DrawingError("No `draw` method specified.")

class Guide:
    def __init__(self) -> None:
        self._guides = dict()

    def createModule(self, moduleName: Text, contents: tuple = ()) -> None:
        assert not self._guides[moduleName], f"Module: \"{moduleName}\" already exists!"

        self._guides[moduleName] = list(contents)

    def appendArticle(self, module: Text, article: Blog) -> None:
        assert self._guides[module], f"Module: \"{module}\" does not exist!"

        self._guides[module].append(article)

class Router:
    def __init__(self):
        self._blogs = dict()
        self._guides = dict()
        self.blacklist = set()

    def renderRouter(self):
        for name in dir(self):
            method = getattr(self, name)
            if callable(method) and re.findall(r"^X[A-Z]", name) and name not in self.blacklist:
                method()

    @staticmethod
    def defineCategory(categoryName: str, *, type: Literal["GUIDE", "BLOG"]):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                if type == "BLOG":
                    self._blogs[categoryName] = result
                elif type == "GUIDE":
                    self._guides[categoryName] = result
                return result

            return wrapper

        return decorator
    
    def buildRouter(self, directory: str) -> None:
        docsDirectory = os.path.join(directory, "d")
        guidesDirectory = os.path.join(docsDirectory, "guides")
        blogsDirectory = os.path.join(docsDirectory, "blogs")

        if os.listdir(directory):
            shutil.rmtree(directory)

        # 
        [os.makedirs(x) for x in (docsDirectory, guidesDirectory, blogsDirectory)]