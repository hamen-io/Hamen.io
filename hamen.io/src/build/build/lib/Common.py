def renderInlineAttributes(attributes: dict) -> str:
    return " ".join([f"{k}=\"" + v.replace('"', "\\\"") + "\"" for k,v in attributes.items()])