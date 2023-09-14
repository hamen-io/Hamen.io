import re
import os
from termcolor import colored
import colorama
import json
global warnings
import shutil
from parse_markdown import ParseMarkdown
import ftplib

colorama.init()
# global_public_path_prefix = "hamen.io"
global_public_path_prefix = ""
releases_dir = os.path.join(global_public_path_prefix, r"releases")
public_dir = os.path.join(global_public_path_prefix, r"dev\hamen.io")

class BuildVersion:
  def __init__(self, version: tuple, release_notes: str = ""):
    # Create a string based on the version:
    self.version = version
    self.version_string = "v" + "-".join(list([str(x) for x in self.version]))

    # Copy the developer directory:
    self.build_dir = os.path.join(releases_dir, self.version_string)
    if os.path.exists(self.build_dir):
        shutil.rmtree(self.build_dir)
    os.makedirs(self.build_dir)
    shutil.copytree(public_dir, os.path.join(self.build_dir, "hamen.io"))

    # Create release notes:
    self.release_notes = release_notes
    with open(os.path.join(self.build_dir, "RELEASE_NOTES.md"), "x") as release_notes:
      release_notes.write(f"""# Hamen.io Version {self.version_string} (Update Notes)\n\n{self.release_notes}""")

    self.init()

  def warn(self, message: str):
    """
    Adds a warning to stdout
    """

    print(colored("Warning: " + message, "yellow", attrs=["bold", "dark", "underline"]))

  def error(self, message: str):
    """
    Adds an error to stdout
    """

    print(colored("Error: " + message, "red", attrs=["bold", "dark", "underline"]))

  def init(self):
    """
    Creates a build; this method is different than `__init__`
    """

    public_dir = os.path.join(self.build_dir, r"hamen.io")
    docs_path = os.path.join(public_dir, r"md\docs")
    guides_path = os.path.join(public_dir, r"md\guides")

    blog_md_files = []
    guide_md_files = []
    blogs = dict()
    guides = dict()
    path_prefix = docs_path
    for category in [*os.listdir(docs_path), "GUIDES", *os.listdir(guides_path)]:
      if category == "GUIDES":
        path_prefix = guides_path
        continue

      if os.path.isdir(os.path.join(path_prefix, category)):
        if not blogs.get(category):blogs[category] = []
        if not guides.get(category):guides[category] = []

        for root, dirs, files in os.walk(os.path.join(path_prefix, category), topdown=False):
          for name in files:
            if name.endswith(".md"):
              md_file = os.path.join(root, name)
              article_info = dict()
              warnings = 0
              with open(md_file, "r", encoding="utf-8") as md:
                doc_info,title,body = re.findall(r"<doc.*>\s*([\s\S]*)\s*</doc>\s*(#\s*.*)\s([\s\S]*)", md.read())[0]
                if not re.findall(r"^#\s+", title):
                  self.warn("Title must include at least one white-space character after the \"#\"")
                  warnings += 1

                title = re.findall("#\s*(.*)", title)[0]
                doc_info = doc_info.split("\n")
                doc_info = [x for x in doc_info if x.strip() != ""]
                for line in doc_info:
                  line = line.strip()
                  try:
                    key,value = line.split(":", 1)
                    key,value = key.strip(),value.strip()
                    if key in ["tags", "category", "categorySlug"]:
                      value = value.split(",")

                    article_info[key] = value

                  except:
                    self.warn(f"Invalid document info for line: \"{line}\"")
                    warnings += 1

                article_info["title"] = title

              if warnings > 0:
                self.error(f"Article: \"{title[1:].strip()}\" not added; fix warnings, then try again")
              else:
                if article_info["type"].lower() == "guide":
                  guides[category].append(article_info)
                  guide_md_files.append(md_file)
                elif article_info["type"].lower() == "blog":
                  blogs[category].append(article_info)
                  blog_md_files.append(md_file)
                else:
                  self.error(f"Fatal: Unknown blog type: \"{article_info['type']}\"")
                  return

    articles_json = os.path.join(docs_path, "Articles.json")
    with open(articles_json, "w") as Articles:
      json.dump([blogs], Articles)

    guides_json = os.path.join(guides_path, "Guides.json")
    with open(guides_json, "w") as Guides:
      json.dump([guides], Guides)

    for guide_md in guide_md_files:
      guide_contents = None
      with open(guide_md, "r", encoding="utf-8") as md:
        guide_contents = md.read()

      guide_html_file = os.path.join(public_dir, "docs", "guides", os.path.dirname(guide_md).split("\\md\\guides\\", 1)[1])
      os.makedirs(guide_html_file)
      guide_html_file = os.path.join(guide_html_file, "index.html")

      blog_html_template = None
      guide_html_template = None
      with open(os.path.join(global_public_path_prefix, r"build\article_templates.html"), "r", encoding="utf-8") as f:
        blog_html_template = f.read()

      with open(os.path.join(global_public_path_prefix, r"build\guide_templates.html"), "r", encoding="utf-8") as f:
        guide_html_template = f.read()

      env = dict()

      with open(guide_html_file, "x+", encoding="utf-8") as html:
        guide_html = ParseMarkdown(guide_contents)
        for key in guide_html.info:
          env[key] = guide_html.info[key]

        env["articleHTML"] = guide_html.__str__()
        env["articleTitle"] = guide_html.title
        env["staticDirectory"] = (len([x for x in os.path.split(guide_html_file)[0].split("hamen.io", 2)[-1].split("\\") if x.strip() != ""]) * "../") + "static"

        required_keys = ['title', 'titleID', 'description', 'type', 'tags', 'author', 'authorID', 'date', 'url', 'category', 'categorySlug', 'articleHTML', 'articleTitle', 'moduleNumber', 'moduleSlug']
        missing_keys = [key for key in required_keys if not env.get(key)]
        assert not missing_keys, f"Missing keys in <doc>: {', '.join(missing_keys)}"

        with open(os.path.join(guides_path, env["guideURL"].replace("/", "\\").replace("guides\\", ""), "course-outline.json"), "r") as course_outline:
          env["guideOutline"] = self.remove_whitespace_not_in_string(course_outline.read())

        template = guide_html_template
        for match in re.findall(r"\{\{\s*ENV\[\s*(\"|')(.*)(\1)\s*\]\s*\}\}", template):
          key = match[1]
          template = re.sub(r"\{\{\s*ENV\[\s*(\"|')(" + key + r")(\1)\s*\]\s*\}\}", env[key], template)

        html.write(template)

    for blog_md in blog_md_files:
      article_contents = None
      with open(blog_md, "r", encoding="utf-8") as md:
        article_contents = md.read()

      article_html_file = os.path.join(public_dir, "docs", "blogs", os.path.dirname(blog_md).split("\\md\\docs\\", 1)[1])
      os.makedirs(article_html_file)
      article_html_file = os.path.join(article_html_file, "index.html")

      blog_html_template = None
      with open(os.path.join(global_public_path_prefix, r"build\article_templates.html"), "r", encoding="utf-8") as f:
        blog_html_template = f.read()

      env = dict()

      with open(article_html_file, "x+", encoding="utf-8") as html:
        article_html = ParseMarkdown(article_contents)
        for key in article_html.info:
          env[key] = article_html.info[key]

        env["articleHTML"] = article_html.__str__()
        env["articleTitle"] = article_html.title
        env["staticDirectory"] = (len([x for x in os.path.split(article_html_file)[0].split("hamen.io", 2)[-1].split("\\") if x.strip() != ""]) * "../") + "static"

        required_keys = ['title', 'titleID', 'description', 'type', 'tags', 'author', 'authorID', 'date', 'url', 'category', 'categorySlug', 'articleHTML', 'articleTitle']
        missing_keys = [key for key in required_keys if not env.get(key)]
        assert not missing_keys, f"Missing keys in <doc>: {', '.join(missing_keys)}"

        template = blog_html_template
        for match in re.findall(r"\{\{\s*ENV\[\s*(\"|')(.*)(\1)\s*\]\s*\}\}", template):
          key = match[1]
          template = re.sub(r"\{\{\s*ENV\[\s*(\"|')(" + key + r")(\1)\s*\]\s*\}\}", env[key], template)

        html.write(template)

    with open(os.path.join(public_dir, ".htaccess"), "x") as htaccess:
      htaccess.write("""<IfModule mime_module>
  AddHandler application/x-httpd-ea-php80___lsphp .php .php8 .phtml
</IfModule>

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

ErrorDocument 400 /error/index.php?error=400
ErrorDocument 402 /error/index.php?error=402
ErrorDocument 401 /error/index.php?error=401
ErrorDocument 403 /error/index.php?error=403
ErrorDocument 404 /error/index.php?error=404""")

  def remove_whitespace_not_in_string(self, code: str) -> str:
    is_str = False
    new_str = ""
    for i,char in enumerate(code):
      if char == "\"" and code[i-1] != "\\": is_str = not is_str
      if re.findall(r"\s", char) and not is_str:
        continue

      new_str += char

    return new_str

if __name__ == "__main__":
  BuildVersion((1, 0, 0))