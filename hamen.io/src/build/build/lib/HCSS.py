import re
import os

class RegEx:
    string: str = r"(?<!\\)\"(?:\\\\|\\\"|[^\"])*\"(?<!\\)"

class HCSS:
    def __init__(self, code: str):
        self.code = code

        # Separate string:
        self.code = re.split(r"(" + RegEx.string + r")", self.code)

        # Separate anything that increases depth (e.g. "{}", "[]", "()", etc)
        code = []
        for item in self.code:
            if item.startswith("\"") and item.endswith("\""):
                code.append(item)
                continue

            print(item)

if __name__ == "__main__":
    os.system("clear")
    print("--- HCSS START ---\n\n")

    HCSS("""
let px: Unit = new Unit(name: "pixel", suffix: "px", compileTo: "px");

let h1: Element = new Element(name: "h1");
let h2: Element = new Element(name: "h2");
let h3: Element = new Element(name: "h3");
let h4: Element = new Element(name: "h4");
let h5: Element = new Element(name: "h5");
let h6: Element = new Element(name: "h6");

let backgroundColor: Property = new Property(name: "backgroundColor", compileTo: "background-color", type: Color);

export new StyleSheet({
    h1 {
        backgroundColor: .red;
    }
})
""")

    print("\n\n--- HCSS END ---")