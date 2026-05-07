
# banner_generator/components/quote.py
from __future__ import annotations
from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "quote"

    def render(self) -> str:
        cfg = (self.cfg.get("quote") or {}) if isinstance(self.cfg.get("quote"), dict) else {}
        text = cfg.get("text", "")
        if not text:
            return ""

        author = cfg.get("author", "")
        x = int(cfg.get("x", 85))
        y = self.y_offset + int(cfg.get("y_offset", 20))
        font_size = int(cfg.get("font_size", 20))
        style = cfg.get("style", "italic")
        author_font = int(cfg.get("author_font_size", 14))

        color = self.col.get("quote_text", self.col.get("subtitle", "#a6adc8"))
        author_color = self.col.get("quote_author", self.col.get("meta", "#6c7086"))

        lines = []
        # Quote text
        lines.append(
            f'<text x="{x}" y="{y}" font-family="\'Inter\', \'Georgia\', serif" '
            f'font-size="{font_size}" fill="{color}" font-style="{style}">“{xml_escape(text)}”</text>'
        )
        y += font_size + 10
        # Author
        if author:
            lines.append(
                f'<text x="{x + 20}" y="{y}" font-family="\'Inter\', sans-serif" '
                f'font-size="{author_font}" fill="{author_color}" font-style="normal">— {xml_escape(author)}</text>'
            )
            y += author_font + 10

        self.used_height = y - self.y_offset
        return "\n".join(lines)
        