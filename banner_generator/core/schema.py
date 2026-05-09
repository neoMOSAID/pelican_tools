
"""Global configuration schemas for banners."""

GLOBAL_SCHEMA = {
    "theme": {
        "type": "str",
        "default": "tech",
        "help": "Color theme name (choose from available themes in themes/ directory)",
        "section": None,
    },
    "size": {
        "type": "str",
        "default": "og",
        "help": "Canvas size preset: og (1200x630), youtube (1280x720), twitter (1200x675), thumbnail (512x512)",
        "section": None,
    },
    "title": {
        "type": "str",
        "default": "",
        "help": "Main title (usually the article title)",
        "section": None,
    },
    "title_line2": {
        "type": "str",
        "default": "",
        "help": "Optional second line of the title (e.g., category name)",
        "section": None,
    },
    "subtitle": {
        "type": "str",
        "default": "",
        "help": "Subtitle text (e.g., article summary)",
        "section": None,
    },
    "meta": {
        "type": "str",
        "default": "",
        "help": "Metadata line (e.g., 'Article 7 · Python')",
        "section": None,
    },
    "progress": {
        "type": "str",
        "default": "",
        "help": "Progress text (e.g., 'Part 2 of 5')",
        "section": None,
    },
    "tagline": {
        "type": "str",
        "default": "",
        "help": "Tagline text (shown with a separator line)",
        "section": None,
    },
    "series": {
        "type": "str",
        "default": "",
        "help": "Deprecated – use badge.text instead",
        "section": None,
    },
    "canvas_w": {
        "type": "int",
        "default": 1200,
        "help": "Overrides canvas width (if size preset is not used)",
        "section": None,
    },
    "canvas_h": {
        "type": "int",
        "default": 630,
        "help": "Overrides canvas height",
        "section": None,
    },
}

LAYOUT_SCHEMA = {
    "title_font_size": {"type": "int", "default": 68, "help": "Font size for main title"},
    "subtitle_font_size": {"type": "int", "default": 38, "help": "Font size for subtitle"},
    "title_x": {"type": "int", "default": 85, "help": "X position of title block"},
    "subtitle_x": {"type": "int", "default": 85, "help": "X position of subtitle (optional, defaults to title_x)"},
    "subtitle_y": {"type": "int", "default": None, "help": "Absolute Y position for subtitle (overrides automatic positioning)"},
    "title_align": {"type": "str", "default": "start", "help": "Text alignment: start, middle, end"},
    "subtitle_align": {"type": "str", "default": "start", "help": "Text alignment for subtitle"},
    "title_max_width": {"type": "int", "default": 660, "help": "Maximum width in pixels before wrapping"},
    "subtitle_max_width": {"type": "int", "default": 660, "help": "Maximum width for subtitle lines"},
    "title_margin_top": {"type": "int", "default": 30, "help": "Top margin from the component's y_offset"},
    "title_line_height": {"type": "int", "default": 48, "help": "Line height for title lines"},
    "subtitle_line_height": {"type": "int", "default": 24, "help": "Line height for subtitle lines"},
}
