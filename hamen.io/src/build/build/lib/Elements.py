import re
from typing import Type

import lib.Exceptions as Exceptions
import lib.Common as Common
import lib.Types as Types
import lib.RenderCode as RenderCode

class Element:
    def __init__(self, *, tagName: str = "Element", innerText: str = "", selfClosing: bool = False, renderAs: str = "span", style: dict = dict(), **attributes):
        self.tagName: str = tagName.upper()
        self.children: list[Element] = list()
        self.innerText: str = innerText
        self._attributes: dict = dict()
        self.selfClosing = selfClosing
        self._acceptedAttributes = {"id": str, "class": str}
        self._renderAs: str = renderAs
        self._style: dict = style
        self.classList = Types.ClassList()

        for k,v in attributes.items():
            self.setAttribute(k, v)

    def selectChild(self, *, tag: str = None, attribute: dict = None) -> 'Element':
        _children = self.selectChildren(tag = tag, attribute = attribute)
        if _children:
            return _children[0]
        return None

    def selectChildren(self, *, tag: str = None, attribute: dict = None) -> list | list['Element']:
        assert len([x for x in (tag, attribute) if x]) == 1, f"Must specific tag OR attribute"
        if tag:
            return [x for x in self.children if x.tagName.upper() == tag.upper()]
        elif attribute:
            _children = set()
            for child in self.children:
                _children.add(child)
                for attr,val in attribute.items():
                    if child.getAttribute(attr.lower()) != val:
                        _children.remove(child)
            return _children
        else:
            raise ValueError

    @property
    def acceptedAttributes(self) -> dict:
        return {k.lower():v for k,v in self._acceptedAttributes.items()}
    
    def appendAttribute(self, key: str, type: type | list[str]) -> None:
        """ Creates an accepted attribute for this element """
        self._acceptedAttributes[key.lower()] = type

    @property
    def attributes(self) -> dict:
        attributes = self._attributes
        attributes["class"] = " ".join(self.classList.classes)

        return attributes
 
    @attributes.setter
    def attributes(self, value: dict) -> None:
        raise Exceptions.ReadOnlyError("Attributes are read-only; modify with `setAttribute` or `removeAttribute`")

    def extendAttributes(self, attributes: dict) -> None:
        for key in attributes:
            self.setAttribute(key, attributes[key])

    def __str__(self, renderTags: bool = False) -> str:
        attrs = Common.renderInlineAttributes(self.attributes)
        attrs = (" " if attrs else "") + attrs

        tag = self.tagName.lower()
        if renderTags and self._renderAs:
            tag = self._renderAs.lower()
        text = self.innerText
        children = "".join([x.__str__(renderTags) for x in self.children])

        if self.selfClosing:
            return f"<{tag}{attrs} />"

        return f"<{tag}{attrs}>{text}{children}</{tag}>"

    def appendChild(self, child: Type['Element']) -> None:
        assert not self.selfClosing, f"Cannot append child to self-closing tag"
        self.children.append(child)

    def removeChild(self, child: Type['Element']) -> None:
        if child in self.children:
            self.children.remove(child)

    def setAttribute(self, key: str, value: str) -> None:
        key = key.lower()

        if key == "class":
            [self.classList.add(x) for x in value.split(" ")]
            return

        assert key in self.acceptedAttributes, f"The given attribute, '{key}' is not a recognized attribute for the '{self.tagName}' tag."
        if isinstance(self.acceptedAttributes[key], (list, tuple, set)):
            assert value in self.acceptedAttributes[key], f"The given key, '{key}' only accepts value(s): '{list(self.acceptedAttributes[key])}', not: '{value}'"
        else:
            assert isinstance(value, self.acceptedAttributes[key]), f"Invalid type: '{type(value)}'. The given key, '{key}', only accepts type: '{self.acceptedAttributes[key]}'"

        self.attributes[key] = value

    def getAttribute(self, key: str) -> None | str:
        key = key.lower()
        return self.attributes.get(key)

    def removeAttribute(self, key: str) -> None:
        key = key.lower()
        del self.attributes[key]

class UI:
    class Title(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Title", renderAs="h1")
            self.classList.add("ui:title")

    class H1(Element):
        def __init__(self):
            super().__init__(tagName = "UI:H1", renderAs="h2")
            self.classList.add("ui:h1")

    class H2(Element):
        def __init__(self):
            super().__init__(tagName = "UI:H2", renderAs="h3")
            self.classList.add("ui:h2")

    class Section(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Section", renderAs="section")
            self.classList.add("ui:section")

    class Text(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Text", renderAs="p")
            self.classList.add("ui:text")

    class Panel(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Panel", renderAs="div")
            self.appendAttribute("type", ["TIP", "NOTE", "ALERT"])
            self.classList.add("ui:panel")

    class Code(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Code", renderAs="div", selfClosing=False)
            self.appendAttribute("language", RenderCode.supportedLanguages)
            self.appendAttribute("tabsize", str)
            self.classList.add("ui:code")

        def __str__(self, renderTags: bool = False) -> str:
            attrs = Common.renderInlineAttributes(self.attributes)
            attrs = (" " if attrs else "") + attrs

            tag = self.tagName.lower()
            if renderTags and self._renderAs:
                tag = self._renderAs.lower()
            text = self.innerText
            children = "".join([x.__str__(renderTags) for x in self.children])

            tabSize = self.getAttribute("tabsize") or "4"
            try:
                tabSize = int(tabSize)
            except:
                raise TypeError("`tabSize` attribute should be an integer")

            lines = text.split("\n")
            for lineIndex,line in enumerate(lines):
                for i,char in enumerate(line):
                    if i >= tabSize * 4 or char != " ":
                        line = line[i:]
                        line = re.split(r"^( *)(.*)$", line)[1:-1]
                        line = "".join([" " for x in list(line[0])]) + "".join(line[1])
                        lines[lineIndex] = line
                        break

            code = "<br>".join(lines)
            code = code.strip()
            if code.startswith("<br>"): code = code[len("<br>"):]
            if code.endswith("<br>"): code = code[:-len("<br>")]
            code = code.strip()
            # code = RenderCode.renderCode(code, lang=self.getAttribute("language"))
            text = f"""<pre>{code}</pre>"""

            if self.selfClosing:
                return f"<{tag}{attrs} />"

            return f"<{tag}{attrs}>{text}{children}</{tag}>"

    class Breadcrumbs(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Breadcrumbs", renderAs="div", selfClosing=True)
            self.classList.add("ui:breadcrumbs")
            self.appendAttribute("crumbs", str)
        
        def __str__(self, renderTags: bool = False) -> str:
            attrs = Common.renderInlineAttributes(self.attributes)
            attrs = (" " if attrs else "") + attrs

            tag = self.tagName.lower()
            if renderTags and self._renderAs:
                tag = self._renderAs.lower()

            return f"""<{tag}{attrs}>
    {" » ".join(['<a href="javascript:void(0);">' + x.strip() + '</a>' for x in self.getAttribute("crumbs").split(",")])}
</{tag}>"""

    class Break(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Break", renderAs="br", selfClosing=True)
            self.classList.add("ui:break")

    class HRule(Element):
        def __init__(self):
            super().__init__(tagName = "UI:HRule", renderAs="hr", selfClosing=True)
            self.classList.add("ui:hr")

    class List(Element):
        def __init__(self):
            super().__init__(tagName = "UI:List", renderAs="ul")
            self.appendAttribute("type", ["UNORDERED", "ORDERED"])
            if self.getAttribute("type") == "ORDERED":
                self._renderAs = "ol"

            self.classList.add("ui:list")

    class Item(Element):
        def __init__(self):
            super().__init__(tagName = "UI:Item", renderAs="li")
            self.classList.add("ui:list-item")

class Format:
    class b(Element):
        def __init__(self):
            super().__init__(tagName = "b", renderAs="b")
            self.classList.add("ui:inline-bold")

    class u(Element):
        def __init__(self):
            super().__init__(tagName = "u", renderAs="u")
            self.classList.add("ui:inline-underline")

    class a(Element):
        def __init__(self):
            super().__init__(tagName = "a", renderAs="a")
            self.classList.add("ui:inline-anchor")
            self.appendAttribute("href", str)
            self.appendAttribute("target", ["CURRENT_TAB", "NEW_TAB"])

    class i(Element):
        def __init__(self):
            super().__init__(tagName = "i", renderAs="i")
            self.classList.add("ui:inline-italic")

    class em(Element):
        def __init__(self):
            super().__init__(tagName = "em", renderAs="em")
            self.classList.add("ui:inline-emphasis")

    class mark(Element):
        def __init__(self):
            super().__init__(tagName = "mark", renderAs="mark")
            self.classList.add("ui:inline-mark")

    class code(Element):
        def __init__(self):
            super().__init__(tagName = "code", renderAs="code")
            self.classList.add("ui:inline-code")

class Doc(Element):
    def __init__(self):
        super().__init__(tagName = "Doc")
        self.appendAttribute("docType", ["BLOG", "GUIDE"])
        self.classList.add("article:doc")

class Properties(Element):
    def __init__(self):
        super().__init__(tagName = "Properties")
        self.classList.add("article:properties")

class Document(Element):
    def __init__(self):
        super().__init__(tagName = "Document", renderAs="article")
        self.classList.add("article:document", "ui:engine")

class Entry(Element):
    def __init__(self, key: str = None, value: str = None):
        """
        Represents the <Entry /> tag;
            attributes:
                "key" (required)
                "value" (required)
        """

        super().__init__(tagName = "Entry", selfClosing = True)

        self.appendAttribute("key", str)
        self.appendAttribute("value", str)

        self.key = key
        self.value = value

        assert self.key, f"Missing key in entry tag."
        assert self.value, f"Missing value in entry tag for key: {self.key}"