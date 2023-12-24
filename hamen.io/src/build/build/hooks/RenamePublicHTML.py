from hooks.Hook import Hook

import os

class RenamePublicHTML(Hook):
    """
    Renames the `hamen.io` folder to `public_html`
    """
    def execute(self) -> None:
        os.rename(os.path.join(self.buildDirectory, "hamen.io"), os.path.join(self.buildDirectory, "public_html"))