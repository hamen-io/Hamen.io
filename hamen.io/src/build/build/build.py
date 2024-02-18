import os
from HamenAPI import BuildSite

if __name__ == "__main__":
    os.system("clear")
    print("--- BUILD START ---\n\n")

    release = BuildSite()

    # Set build metadata:
    release.releaseDirectory = r"hamen.io/www"
    release.devDirectory = r"hamen.io/dev"
    release.buildVersion = (1, 0, 0)

    # Add resources:
    release.createImport("JAVASCRIPT", "/static/js/index.js", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/importFonts.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/importIcons.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/ui.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/webTheme.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/index.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/utilityClasses.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/prism.css", isRelative=True)
    release.createImport("STYLESHEET", "/static/css/doc.css", isRelative=True)

    # Load and build site:
    release.loadDev()
    release.buildSite()

    # Handle subdomains:
    release.createSubdomainRedirect(r"docs.hamen.io", "hamen.io/docs")
    release.createSubdomainRedirect(r"support.hamen.io", "hamen.io/support")
    release.createSubdomainRedirect(r"software.hamen.io", "hamen.io/software")

    # Handle hooks:
    from hooks.BuildDoc import BuildDoc
    from hooks.CompileSASS import CompileSASS
    from hooks.MinifyFiles import MinifyFiles
    from hooks.CreateSiteTags import CreateSiteTags
    from hooks.RenamePublicHTML import RenamePublicHTML
    release.registerHook(BuildDoc)
    release.registerHook(CompileSASS)
    release.registerHook(MinifyFiles)
    release.registerHook(RenamePublicHTML)
    release.registerHook(CreateSiteTags)
    release.executeHooks()

    print("\n\n--- BUILD END ---")