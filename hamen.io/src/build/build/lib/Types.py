class ClassList:
    def __init__(self, *classes) -> None:
        self._classes = set(classes)

    def add(self, *className: str) -> None:
        for class_ in className:
            self._classes.add(class_)

    def remove(self, className: str) -> None:
        self._classes.remove(className)

    def contains(self, className: str) -> bool:
        return className in self._classes

    def toggle(self, className: str) -> None:
        if self.contains(className):
            self._classes.remove(className)
        else:
            self._classes.add(className)

    @property
    def classes(self) -> list:
        return self._classes