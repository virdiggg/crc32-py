def clean_utf8(text):
    # Encode to bytes, ignoring errors, then decode back to string
    return text.encode('utf-8', 'ignore').decode('utf-8')

def color_text(text, color):
    colors = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"