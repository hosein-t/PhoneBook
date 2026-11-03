from tkinter.font import Font



def shorten_text(text, max_width, font_name="Samim WOL", size=16) -> str:
    font = Font(family=font_name, size=size)

    if font.measure(text) <= max_width:
        return text

    while text and font.measure("..." + text) > max_width:
        text = text[:-1]

    return "..." + text
