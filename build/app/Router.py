import HamenDocs as Hamen

Router = Hamen.Types.Router
Text = Hamen.Types.Text
TextStyles = Hamen.Types.TextStyles

class Index(Hamen.Types.Blog):
    def __init__(self) -> None:
        super().__init__()
        self.blogTitle = "Testing Blog"
        self.blogAuthor = "Daniel Hamen"
        self.blogDate = "2023-10-25"
        self.blogTags = []
        self.blogDescription = "Lorem ipsum"

    def draw(self) -> None:
        layout = self.layout

        introduction = layout.createSection("Test")
        introduction.addElement.UIText([
            "Bold Text:",
            {"B": "My Bold Text"},
            "Passing"
        ])
        introduction.addElement.UIText([
            "Bold Text:",
            {"B": "My Bold Text"},
            "Passing"
        ])

        layout.registerSection((introduction))

class DocRouter(Router):
    def __init__(self) -> None:
        super().__init__()

    @Hamen.Types.Router.defineCategory("Linguistics", type = "BLOG")
    def XLinguistics(self):
        return { Index() }

if __name__ == "__main__":
    router = DocRouter()
    router.renderRouter()
    router.buildRouter(r"build\app\test")