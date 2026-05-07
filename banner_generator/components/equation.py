
# banner_generator/components/equation.py
from __future__ import annotations
import re
from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "equation"

    def _latex_to_svg_text(self, latex: str) -> str:
        """Convert simple LaTeX to SVG-friendly text with tspan for superscript/subscript."""
        # Escape XML first
        text = xml_escape(latex)
        # Handle superscripts: a^b → a<tspan dy="-6" font-size="0.7em">b</tspan>
        # This is a very naive conversion – for production consider using MathJax or pre-rendered SVGs.
        def sup_replace(match):
            base = match.group(1)
            sup = match.group(2)
            return f'{base}<tspan dy="-6" font-size="0.7em">{sup}</tspan>'
        # Pattern: something^something (non-greedy)
        text = re.sub(r'([a-zA-Z0-9\)])\^([a-zA-Z0-9{}]+)', sup_replace, text)
        # Remove braces
        text = text.replace('{', '').replace('}', '')
        return text

    def render(self) -> str:
        cfg = (self.cfg.get("equation") or {}) if isinstance(self.cfg.get("equation"), dict) else {}
        latex = cfg.get("latex", "E = mc^2")
        x = int(cfg.get("x", 85))
        y = self.y_offset + int(cfg.get("y_offset", 20))
        font_size = int(cfg.get("font_size", 28))
        color = self.col.get("equation_color", self.col.get("subtitle", "#f8f8f2"))

        # Convert LaTeX to SVG text with spans
        display = self._latex_to_svg_text(latex)

        # Optional: add a subtle background box
        bg = cfg.get("background", False)
        parts = []
        if bg:
            # Estimate text width
            text_width = len(latex) * font_size * 0.55
            padding = 20
            parts.append(f'<rect x="{x - 10}" y="{y - font_size - 5}" width="{text_width + padding}" height="{font_size + 15}" rx="8" fill="{self.col.get("equation_bg", "#313244")}" opacity="0.5" />')

        parts.append(
            f'<text x="{x}" y="{y}" font-family="\'Times New Roman\', \'STIXGeneral\', \'Latin Modern Math\', serif" '
            f'font-style="italic" font-size="{font_size}" fill="{color}" text-anchor="start">'
            f'{display}'
            f'</text>'
        )

        self.used_height = font_size + 20
        return "\n".join(parts)
        