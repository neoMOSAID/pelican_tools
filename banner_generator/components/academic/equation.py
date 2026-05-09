from __future__ import annotations
import re
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'equation'
    description = 'LaTeX equation rendered as SVG text'
    component_id = 'equation'

    def _latex_to_svg_text(self, latex: str) -> str:
        """Convert simple LaTeX to SVG-friendly text with tspan for superscript/subscript."""
        text = xml_escape(latex)

        def sup_replace(match):
            base = match.group(1)
            sup = match.group(2)
            return f'{base}<tspan dy="-6" font-size="0.7em">{sup}</tspan>'
        text = re.sub('([a-zA-Z0-9\\)])\\^([a-zA-Z0-9{}]+)', sup_replace, text)
        text = text.replace('{', '').replace('}', '')
        return text

    def render(self) -> str:
        cfg = self.cfg.get('equation') or {} if isinstance(self.cfg.get('equation'), dict) else {}
        latex = cfg.get('latex', 'E = mc^2')
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        font_size = int(cfg.get('font_size', 28))
        color = self.col.get('equation_color', self.col.get('subtitle', '#f8f8f2'))
        display = self._latex_to_svg_text(latex)
        bg = cfg.get('background', False)
        parts = []
        if bg:
            text_width = len(latex) * font_size * 0.55
            padding = 20
            parts.append(f'''<rect x="{x - 10}" y="{y - font_size - 5}" width="{text_width + padding}" height="{font_size + 15}" rx="8" fill="{self.col.get('equation_bg', '#313244')}" opacity="0.5" />''')
        parts.append(f'''<text x="{x}" y="{y}" font-family="'Times New Roman', 'STIXGeneral', 'Latin Modern Math', serif" font-style="italic" font-size="{font_size}" fill="{color}" text-anchor="start">{display}</text>''')
        self.used_height = font_size + 20
        return '\n'.join(parts)