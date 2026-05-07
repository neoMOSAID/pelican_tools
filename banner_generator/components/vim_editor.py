
from __future__ import annotations

import re

from .base import BaseComponent, xml_escape

# Minimal syntax tokenizer (same style as terminal)
def _tokenize_line(line: str, colors: dict) -> list[tuple[str, str, bool]]:
    """Return list of (text, color, bold) for a single line of code."""
    c = colors
    tokens = []
    pattern = re.compile(
        r'(?P<comment>".*$)|'
        r'(?P<flag>--?\w+(?:=[^\s]+)?)|'
        r'(?P<path>[~/.]\S*|https?://\S+)|'
        r'(?P<quote>\'[^\']*\'|"[^"]*")|'
        r'(?P<word>[^\s]+)'
    )
    for m in pattern.finditer(line):
        if m.group("comment"):
            tokens.append((m.group("comment"), c.get("syn_comment", "#6272a4"), False))
        elif m.group("flag"):
            tokens.append((m.group("flag"), c.get("syn_flag", "#8be9fd"), False))
        elif m.group("path"):
            tokens.append((m.group("path"), c.get("syn_path", "#ff79c6"), False))
        elif m.group("quote"):
            tokens.append((m.group("quote"), c.get("syn_string", "#f1fa8c"), False))
        elif m.group("word"):
            word = m.group("word")
            if word.lower() in {"def", "class", "return", "if", "else", "elif", "for", "while", "import", "from", "as", "set", "let", "map", "nnoremap", "inoremap", "vnoremap", "call", "function", "end"}:
                tokens.append((word, c.get("syn_keyword", "#ff79c6"), True))
            elif word.lower() in {"true", "false", "none", "nil"}:
                tokens.append((word, c.get("syn_bool", "#bd93f9"), False))
            elif word.isdigit():
                tokens.append((word, c.get("syn_number", "#bd93f9"), False))
            else:
                tokens.append((word, c.get("syn_default", "#f8f8f2"), False))
    # Always add a trailing space token for readability
    return tokens


class Component(BaseComponent):
    component_id = "vim_editor"

    def render(self) -> str:
        cfg = (self.cfg.get("vim_editor") or {}) if isinstance(self.cfg.get("vim_editor"), dict) else {}
        lines = cfg.get("lines", [
            "nnoremap <leader>w :w<CR>",
            "set relativenumber",
            "colorscheme dracula",
            "\" that's it, folks"
        ])
        filename = str(cfg.get("filename", "init.vim"))
        show_line_numbers = bool(cfg.get("line_numbers", True))
        mode = str(cfg.get("mode", "NORMAL"))

        # Positioning – default to terminal-like area
        x = int(cfg.get("x", 700))
        y = int(cfg.get("y", 80))
        width = int(cfg.get("width", 440))
        height = int(cfg.get("height", 320))
        titlebar_h = 32
        gutter_w = 32 if show_line_numbers else 0
        code_x = x + gutter_w + 14
        font_size = int(cfg.get("font_size", 15))
        line_h = int(cfg.get("line_height", 22))
        padding = int(cfg.get("padding", 10))
        mode_h = 22  # height of bottom mode line

        bg = self.col.get("vim_editor_bg", "#1e1e2e")
        stroke = self.col.get("vim_editor_stroke", "#313244")
        title_bg = self.col.get("vim_editor_titlebar", "#45475a")
        title_fg = self.col.get("vim_editor_title_fg", "#cdd6f4")
        fg = self.col.get("vim_editor_fg", "#f8f8f2")
        ln_fg = self.col.get("vim_editor_ln", "#6272a4")
        mode_bg = self.col.get("vim_editor_mode_bg", "#50fa7b")
        mode_fg = self.col.get("vim_editor_mode_fg", "#282a36")
        status_bg = self.col.get("vim_editor_status_bg", "#313244")
        status_fg = self.col.get("vim_editor_status_fg", "#cdd6f4")
        cursor_color = self.col.get("vim_editor_cursor", "#ffb86c")
        syn_colors = self.col  # pass through for tokenizer

        # Warn if too many lines for the available space
        code_area_height = height - titlebar_h - mode_h - 10
        max_lines = code_area_height // line_h
        if len(lines) > max_lines:
            lines = lines[:max_lines]

        static = str(self.cfg.get("render_mode", "")) == "static"

        # ---- Build SVG ----
        parts = []

        # Outer window
        parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="10" '
            f'fill="{bg}" fill-opacity="0.95" stroke="{stroke}" stroke-width="2" />'
        )

        # Title bar
        parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{titlebar_h}" rx="10" fill="{title_bg}" />'
        )
        parts.append(
            f'<rect x="{x}" y="{y+12}" width="{width}" height="20" fill="{title_bg}" />'  # flatten bottom of rounded rect
        )
        # Traffic light buttons
        parts.append(f'<circle cx="{x+16}" cy="{y+16}" r="6" fill="{self.col.get("btn_red", "#f38ba8")}" />')
        parts.append(f'<circle cx="{x+36}" cy="{y+16}" r="6" fill="{self.col.get("btn_yellow", "#fab387")}" />')
        parts.append(f'<circle cx="{x+56}" cy="{y+16}" r="6" fill="{self.col.get("btn_green", "#a6e3a1")}" />')
        # Title text
        parts.append(
            f'<text x="{x+width/2}" y="{y+22}" font-family="\'Inter\', sans-serif" font-size="12" '
            f'fill="{title_fg}" text-anchor="middle" font-weight="500">VIM – {xml_escape(filename)}</text>'
        )

        # Line numbers and code
        code_start_y = y + titlebar_h + padding + font_size
        for i, line in enumerate(lines):
            ly = code_start_y + i * line_h
            if show_line_numbers:
                # line number
                num = i + 1
                parts.append(
                    f'<text x="{x+18}" y="{ly}" font-family="\'JetBrains Mono\', monospace" '
                    f'font-size="{font_size-2}" fill="{ln_fg}" text-anchor="end">{num}</text>'
                )
            # Render line with syntax highlighting
            if static:
                # Clean version for PNG
                parts.append(
                    f'<text x="{code_x}" y="{ly}" font-family="\'JetBrains Mono\', monospace" '
                    f'font-size="{font_size}" fill="{fg}">{xml_escape(line)}</text>'
                )
            else:
                tokens = _tokenize_line(line, syn_colors)
                tspan_parts = []
                for text, color, bold in tokens:
                    fontw = 'font-weight="bold"' if bold else ''
                    tspan_parts.append(f'<tspan fill="{color}" {fontw}>{xml_escape(text)}</tspan>')
                parts.append(
                    f'<text x="{code_x}" y="{ly}" font-family="\'JetBrains Mono\', monospace" '
                    f'font-size="{font_size}" fill="{fg}">{" ".join(tspan_parts)}</text>'
                )

        # Mode line (bottom of editor)
        mode_y = y + height - mode_h
        parts.append(
            f'<rect x="{x}" y="{mode_y}" width="{width}" height="{mode_h}" rx="0" fill="{mode_bg}" />'
        )
        # Round bottom corners
        parts.append(
            f'<rect x="{x}" y="{mode_y+mode_h-10}" width="{width}" height="10" fill="{mode_bg}" rx="0" />'
        )
        parts.append(
            f'<rect x="{x}" y="{y+height-10}" width="{width}" height="10" fill="{mode_bg}" rx="10" />'
        )
        # parts.append(
        #     f'<rect x="{x}" y="{y+height-10}" width="{width}" height="10" fill="none" stroke="{stroke}" stroke-width="2" rx="10" />'
        # )
        # Mode text
        mode_text = f"-- {mode} --"
        parts.append(
            f'<text x="{x+10}" y="{mode_y+16}" font-family="\'JetBrains Mono\', monospace" font-size="13" '
            f'fill="{mode_fg}" font-weight="bold">{mode_text}</text>'
        )
        # Blinking cursor only if not static
        if not static:
            # Place cursor at end of the first line, for instance (or custom)
            # We'll just show a cursor in the mode line as well
            parts.append(
                f'<text x="{x+width-30}" y="{mode_y+16}" font-family="\'JetBrains Mono\', monospace" '
                f'font-size="13" fill="{cursor_color}" font-weight="bold">'
                f'<animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite" />█</text>'
            )

        # Statusline (above mode line, inside the editor area)
        status_y = mode_y - 18
        parts.append(
            f'<rect x="{x+4}" y="{status_y}" width="{width-8}" height="16" fill="{status_bg}" rx="2" opacity="0.8" />'
        )
        parts.append(
            f'<text x="{x+12}" y="{status_y+12}" font-family="\'JetBrains Mono\', monospace" font-size="11" '
            f'fill="{status_fg}">{xml_escape(filename)} [+]</text>'
        )
        parts.append(
            f'<text x="{x+width-20}" y="{status_y+12}" font-family="\'JetBrains Mono\', monospace" font-size="11" '
            f'fill="{status_fg}" text-anchor="end">1,1</text>'
        )

        return "  <!-- Vim editor window -->\n  " + "\n  ".join(parts)
        