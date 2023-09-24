import re
import json

def parse_text_content(text_content: str) -> str:
    text_content = re.sub(
        r"\*\*\*()(?!\\)([^.]*)\*\*\*", r"<b><i>\2</i></b>", text_content
    )
    text_content = re.sub(r"\*\*()(?!\\)([^.]*)\*\*", r"<b>\2</b>", text_content)
    text_content = re.sub(r"\*()(?!\\)([^.]*)\*", r"<i>\2</i>", text_content)
    text_content = re.sub(r"\~\~()(?!\\)([^.]*)\~\~", r"<s>\2</s>", text_content)
    text_content = re.sub(r"\:()(?!\\)([^.]*)\:", r"<u>\2</u>", text_content)
    text_content = re.sub(r"(?<=\S)(\^)([^ ]*)", r"<sup>\2</sup>", text_content)
    text_content = re.sub(r"(?<=\S)(\^)([^ ]*)", r"<sub>\2</sub>", text_content)
    text_content = re.sub(
        r"(?<!\\)(`)(.*?)(?<!\\)(`)",
        r"""<code class="inline-code">\2</code>""",
        text_content,
    )
    text_content = re.sub(
        r"(?<!\\)\[(.*)\]\(\"(.*)\"\)", r"""<a href="\2">\1</a>""", text_content
    )

    return text_content


def title_to_id(title: str) -> str:
    id = ""
    for char in title:
        if char == " ":
            id += "-"
        elif char.isalpha():
            id += char.lower()

    return id


class Elements:
    class P:
        def __init__(self, textContent: str) -> None:
            self.textContent = parse_text_content(textContent)

        def __str__(self) -> str:
            return f"""<p>{self.textContent}</p>"""

    class ListItem:
        def __init__(self, textContent: str) -> None:
            self.textContent = parse_text_content(textContent)

        def __str__(self) -> str:
            return f"""<li>{self.textContent}</li>"""

    class Note:
        def __init__(self, textContent: list[str], type: str = "INFO"):
            self.textContent = "\n\n".join(textContent)
            self.type = type.upper()

        def __str__(self) -> str:
            body = parse_code(self.textContent, asString = True)

            icon = "info"
            match self.type:
                case "INFO":
                    icon = "info"
                case "WARNING":
                    icon = "warning"
                case "ERROR":
                    icon = "error"

            return f"""<div class="ui:note" theme="{icon.upper()}">
  <div class="icon">
    <span class="material-symbols-outlined">{icon}</span>
  </div>
  <div class="body">
    {body}
  </div>
</div>"""

    class List:
        def __init__(self, items: list, ordered: bool) -> None:
            self.items = items
            self.ordered = ordered

        def __str__(self) -> str:
            tag = "ol" if self.ordered else "ul"
            return f"""<{tag}>{"".join([x.__str__() for x in self.items])}</{tag}>"""

    class Heading:
        def __init__(self, textContent: str, level: int = 2) -> None:
            self.textContent = parse_text_content(textContent)
            self.level = level
            self.ID = title_to_id(textContent)

            assert 1 < level <= 6, f"Headings must be between 2 and 6 (inclusively)"

        def __str__(self) -> str:
            return f"""<h{self.level}>{self.textContent}</h{self.level}>"""

    class InlineElement:
        class Code:
            def __init__(self, textContent: str) -> None:
                """
                Creates inline code

                Syntax: `\`My Underlined Text\``
                """

                self.textContent = parse_text_content(textContent)

            def __str__(self) -> str:
                return f"""<code class="inline-code">{self.textContent}</code>"""

        class Bold:
            def __init__(self, textContent: str) -> None:
                """
                Creates bold text

                Syntax: `**My Bold Text**`
                """

                self.textContent = parse_text_content(textContent)

            def __str__(self) -> str:
                return f"""<b>{self.textContent}</b>"""

        class Italic:
            def __init__(self, textContent: str) -> None:
                """
                Creates strikethrough text

                Syntax: `*My Italicized Text*`
                """

                self.textContent = parse_text_content(textContent)

            def __str__(self) -> str:
                return f"""<i>{self.textContent}</i>"""

        class Strikethrough:
            def __init__(self, textContent: str) -> None:
                """
                Creates strikethrough text

                Syntax: `~~My Strikethoughed Text~~`
                """

                self.textContent = parse_text_content(textContent)

            def __str__(self) -> str:
                return f"""<s>{self.textContent}</s>"""

        class Underline:
            def __init__(self, textContent: str) -> None:
                """
                Creates underline text

                Syntax: `:My Underlined Text:`
                """

                self.textContent = parse_text_content(textContent)

            def __str__(self) -> str:
                return f"""<u>{self.textContent}</u>"""

    class CodeBlock:
        def __init__(self, code: str, language: str = "python") -> None:
            if type(code) is list:
                code = "<br>".join(code)
            self.code = code
            self.language = language
            self.metadata = language.split(":")[-1]
            if self.language == self.metadata:
                self.metadata = "code-block"
            self.metadata = self.metadata.lower()

        def __str__(self) -> str:
            if self.metadata == "syntax":
                return f"""<div class="ui:code-block"><div class="body"><pre style="text-align: center;">{self.code}</pre></div></div>"""
            else:
                return f"""<div class="ui:code-block"><div class="header"><span style="color: rgba(255, 255, 255, 0.7)">{self.language}</span></div><div class="body"><pre>{self.code}</pre></div></div>"""


class Section:
    def __init__(self, title: str, id: str = None):
        self.title = title
        self.id = id
        self.children = []

        if not self.id:
            self.id = title_to_id(self.title)

    def appendChild(self, child) -> None:
        self.children.append(child)

    def __str__(self) -> str:
        children = "\n".join([x.__str__() for x in self.children])

        return f"""<section class="doc-section" id="{self.id}">
  <h2>{self.title}</h2>
  <div class="content">
    <div class="border"></div>
    <div class="body">
      {children}
    </div>
  </div>
</section>"""


def parse_token(element: str | list, UIComponents: dict = dict()) -> Elements.__base__:
    if type(element) is str:
        element = element.strip()
        if re.findall(r"^#{1,6}", element):
            level,content = list(re.findall(r"(^#{1,6})(.*)", element)[0])

            return Elements.Heading(content, len(level))

        elif element.lower().startswith("@uicomponent"):
            terms = re.match(r"^@uicomponent\.([a-z_][a-z0-9_]*)(\([\s\S]*\))", element, re.I)
            if len(terms.groups()) != 2:
                raise SyntaxError(f"Invalid syntax for @UIComponent: \"{element}\"")
            component,params = list(terms.groups())
            if component not in UIComponents:
                raise SyntaxError(f"Unknown component: \"{component}\"")
            params = f"[{params[1:-1]}]"
            params = json.loads(params)[0]
            return UIComponents[component](**params)

        else:
            return Elements.P(element)

    else:
        if element[0].startswith("```") and element[-1].startswith("```"):
            language = element[0][3:].strip()
            if not language:
                raise SyntaxError("Language not specified.")

            return Elements.CodeBlock(element[1:-1], language)

        elif element[0].startswith("!!!") and element[-1].startswith("!!!"):
            return Elements.Note(element[1:-1], element[0][3:])

        elif element[0].startswith("-"):
            def parse_list(_code: list) -> Elements.List:
                items = []
                for li in _code:
                    if type(li) is str:
                        items.append(Elements.ListItem(li.split(" ", 1)[-1]))
                    elif type(li) is list:
                        items.append(parse_list(li))

                return Elements.List(items, False)

            return parse_list(element)

    raise ValueError("Unknown value: " + str(element))


def parse_code(code: str, *, UIComponents: dict = dict(), asString: bool = False):
    code = code.strip()

    # Split code:
    parts = []
    is_code = False
    is_note = False
    is_ui_component = { "defined": False, "brace": 0, "square": 0, "bracket": 0, "size": lambda properties : properties["brace"] + properties["square"] + properties["bracket"] }
    for line in code.split("\n"):
        raw_line = line
        line = line.lstrip()

        if is_ui_component["defined"] or (line.lower().startswith("@uicomponent") and not is_code):
            if line.lower().startswith("@uicomponent"):
                parts.append(line)
                is_ui_component["defined"] = True
            else:
                parts[-1] += line.replace("\n", "")

            is_str = False
            for i,char in enumerate(line):
                if char == "\"" and line[i-1] != "\\":
                    is_str = not is_str

                if char == "{": is_ui_component["brace"] += 1
                if char == "}": is_ui_component["brace"] -= 1
                if char == "(": is_ui_component["bracket"] += 1
                if char == ")": is_ui_component["bracket"] -= 1
                if char == "[": is_ui_component["square"] += 1
                if char == "]": is_ui_component["square"] -= 1

            if is_ui_component["size"](is_ui_component) == 0:
                is_ui_component["defined"] = False

            continue

        if is_note and not line.startswith("!!!"):
            parts[-1].append(line)
            continue

        if is_code:
            parts[-1].append(raw_line)
            if line.startswith("```"):
                is_code = False

            continue

        if line:
            if line.startswith("```"):
                is_code = not is_code
                if is_code:
                    parts.append([line])
                else:
                    parts[-1].append(line)

            elif line.startswith("!!!"):
                is_note = not is_note
                if is_note:
                    parts.append([line])
                else:
                    parts[-1].append(line)

            elif re.match(r"^#{1,6}", line):
                parts.append(line)

            elif re.match(r"^-\s+", line):
                if parts[-1] and parts[-1][0] and parts[-1][0].startswith("-"):
                    parts[-1].append(line)
                else:
                    parts.append([line])

            elif re.match(r"^:-\s+", line):
                if parts[-1] and type(parts[-1][-1]) is list:
                    parts[-1][-1].append(line)
                else:
                    parts[-1].append([line])

            elif re.match(r"^-", line) or re.match(r"^:-", line):
                raise SyntaxError(f"List items must include whitespace after the marker declaration: \"{line}\"")

            else:
                if is_code:
                    parts[-1].append(raw_line)
                else:
                    parts.append(raw_line)

    tokens = []
    for part in parts:
        tokens.append(parse_token(part, UIComponents = UIComponents))

    if asString:
        return "".join([x.__str__() for x in tokens]).replace("\n", "")

    return tokens


class ParseArticle:
    def __init__(self, code: str) -> None:
        self.code = code.strip()
        self.info, self.title, self.body = self.split_content(self.code)
        self.info: dict = self.split_info(self.info)
        self.title: str = self.title.strip()

    def split_content(self, code: str) -> list[str, str, str]:
        """
        Splits `code` into:
        1. The blog info
        2. The blog title
        3. The blog body
        """

        pattern = r"<doc.*>([\s\S]*)<\/doc>\s+#\s+(.*)\s+([\s\S]+)"
        assert re.findall(pattern, code), "Doc info missing!"

        return list(re.findall(pattern, code)[0])

    def split_info(self, info: str) -> dict:
        info = [x.strip() for x in info.split("\n")]
        doc_info = dict()
        for line in info:
            if line:
                assert (
                    ":" in line
                ), f'Invalid `doc` property syntax; missing ":": "{line}"'
                key, value = [x.strip() for x in line.split(":", 1)]

                doc_info[key] = value

        return doc_info

    def __str__(self) -> str:
        code = parse_code(self.body)
        sections = [[]]
        for element in code:
            if type(element) is Elements.Heading:
                if element.level == 2:
                    sections.append([element])
            else:
                sections[-1].append(element)

        sectionList = []
        for i,sectionContent in enumerate(sections):
            if sectionContent:
                heading = sectionContent[0]
                heading: Elements.Heading

                section = Section(heading.textContent, heading.ID)
                section.children = sectionContent[1:]

                sectionList.append(section)

        return "\n".join([x.__str__() for x in sectionList])