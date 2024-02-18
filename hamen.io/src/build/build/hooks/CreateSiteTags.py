import os
import json
import re
from bs4 import BeautifulSoup
from hooks.Hook import Hook

_BLACKLISTED_SITES_ = (r"^(/artifacts)", r"^(/index\.html)", r"/writing-for-hamen-docs/")

class CreateSiteTags(Hook):
    """
    Searches through all HTML files, pulls their <h1> title text and creates a dictionary where the key is the text and the value is the page URL
    """
    def execute(self) -> None:
        tags = dict()
        for file in self.searchFiles(filePattern=r"\.html"):
            with open(file.fullFilePath, "r") as f:
                data = BeautifulSoup(f.read(), "lxml")
                h1 = data.find("h1")
                if h1:
                    page_tags = "".join([x.text for x in h1.contents if x != "None"])
                    url = file.fullFilePath.split("public_html", 1)[-1]
                    url: str
                    if not any([re.findall(x, url) for x in _BLACKLISTED_SITES_]):
                        url = "https://www.hamen.io" + url
                        tags[page_tags] = url

        tags_file = os.path.join(self.buildDirectory, "public_html", "static", "data", "taggedSites.json")
        with open(tags_file, "w+") as file:
            file.write(json.dumps(tags))