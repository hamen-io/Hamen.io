def add_blog(markdown: str) -> None:
  pass

if __name__ == "__main__":
  markdown_path = r""
  with open(markdown_path, "r") as markdown:
    add_blog(markdown.read())