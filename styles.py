LIGHT_THEME = {
    "bg": "#f5f5f5",
    "frame_bg": "#ffffff",
    "canvas_bg": "#ffffff",
    "accent": "#2c3e50",
    "secondary": "#7f8c8d",
    "alert": "#e74c3c",
    "border": "#bdc3c7",
    "text": "#2c3e50",
    "button_bg": "#2c3e50",
    "button_fg": "#ffffff"
}


DARK_THEME = {
    "bg": "#1a1a1a",
    "frame_bg": "#2d2d2d",
    "canvas_bg": "#2d2d2d",
    "accent": "#ecf0f1",
    "secondary": "#95a5a6",
    "alert": "#e74c3c",
    "border": "#3f3f3f",
    "text": "#ecf0f1",
    "button_bg": "#34495e",
    "button_fg": "#ffffff"
}


current_theme = LIGHT_THEME

def toggle_theme():
    global current_theme
    if current_theme == LIGHT_THEME:
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME
    return current_theme

def get_style(key):
    return current_theme.get(key, "")

FONT_FAMILY = "Helvetica"
FONT_BOLD = (FONT_FAMILY, 12, "bold")
FONT_NORMAL = (FONT_FAMILY, 10)
FONT_SMALL = (FONT_FAMILY, 9)
FONT_CLOCK_NUMS = (FONT_FAMILY, 14, "bold")
