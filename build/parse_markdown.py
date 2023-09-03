import re

def parse_text_content(text_content: str) -> str:
    text_content = re.sub(r"\*\*\*()(?!\\)([^.]*)\*\*\*", r"<b><i>\2</i></b>", text_content)
    text_content = re.sub(r"\*\*()(?!\\)([^.]*)\*\*", r"<b>\2</b>", text_content)
    text_content = re.sub(r"\*()(?!\\)([^.]*)\*", r"<i>\2</i>", text_content)
    text_content = re.sub(r"(?<=\S)(\^)([^ ]*)", r"<sup>\2</sup>", text_content)
    text_content = re.sub(r"(?<=\S)(\^)([^ ]*)", r"<sub>\2</sub>", text_content)
    text_content = re.sub(r"(?<!\\)(`)(.*?)(?<!\\)(`)", r"<code class=\"inline-code\">\2</code>", text_content)

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

class ParseMarkdown:
  def __init__(self, code: str) -> None:
    self.code = code.strip()
    self.info,self.title,self.body = self.split_content(self.code)
    self.info: dict = self.split_info(self.info)
    self.title: str = self.title.strip()
    self.body = self.split_body(self.body)

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
        assert ":" in line, f"Invalid `doc` property syntax; missing \":\": \"{line}\""
        key,value = [x.strip() for x in line.split(":", 1)]

        doc_info[key] = value

    return doc_info
  
  def split_body(self, body: str) -> list[Section]:
    sections = []
    body = body.strip().split("\n")
    is_code_block = False
    is_list = False
    for line in body:
      if re.findall(r"^\`\`\`", line):
        # Create new code block:
        if not is_code_block:
          sections[-1].append([line])

        # Closing a code-block:
        else:
          sections[-1][-1].append(line)
          sections[-1][-1] = "\n".join(sections[-1][-1])

        is_code_block = not is_code_block
        continue

      # Currently inside a code block:
      if is_code_block:
        sections[-1][-1].append(line)
        continue

      if is_list:
        if line.strip().startswith(is_list):
          sections[-1][-1].append(line)
          continue
        else:
          sections[-1][-1] = "\n".join(sections[-1][-1])
          is_list = False
      else:
        if line.startswith(("* ", "- ")):
          sections[-1].append([line])
          is_list = line.split(" ", 1)[0].strip()
          if is_list.endswith("."):
            is_list = is_list[:-1]
          continue

      if re.findall(r"^##\s+.*", line):
        sections.append([])

      sections[-1].append(line)

    for i,lines in enumerate(sections):
      assert len(lines) > 1, "Blank section"
      title = re.findall(r"##\s+(.*)", lines[0])[0]
      title = parse_text_content(title)
      lines = lines[1:]

      section = Section(title)
      for line in lines:
        if line.strip():
          if re.findall(r"^```[\s\S]*```$", line):
            language,code = list(re.findall(r"^```(.*)\n([\s\S]*)\n```$", line)[0])
            section.appendChild(Elements.CodeBlock(code, language))
          elif line.startswith(("* ", "- ")):
            section.appendChild(Elements.List([Elements.ListItem(x.strip()[1:].strip()) for x in line.split("\n") if x.strip() != ""], False))
          elif re.findall(r"^#{3,6}\s+", line):
            level,content = line.split(" ", 1)
            level = len(level)
            content = content.strip()
            section.appendChild(Elements.Heading(content, level))
          else:
            section.appendChild(Elements.P(line))

      sections[i] = section

    return sections

  def __str__(self) -> str:
    return f"""{"".join([x.__str__() for x in self.body])}"""