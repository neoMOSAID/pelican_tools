
"""Component: author_plate – styled author name with separator ornaments."""

from __future__ import annotations
from .base import BaseComponent, xml_escape


class Component(BaseComponent):
    component_id = "author_plate"

    def render(self) -> str:
        cfg = self.cfg.get("author_plate", {})
        if not isinstance(cfg, dict):
            return ""

        author = cfg.get("author", "")
        if not author:
            return ""

        x = int(cfg.get("x", self.w // 2))
        y = int(cfg.get("y", self.h - 100))
        font_size = int(cfg.get("font_size", 24))
        color = cfg.get("color", self.col.get("author_color", "#e6c27a"))
        align = cfg.get("align", "middle")
        show_rule = cfg.get("show_rule", True)

        rule_parts = []
        if show_rule:
            rule_width = int(cfg.get("rule_width", 200))
            rule_y = y - 15
            rule_parts = [
                f'<line x1="{x - rule_width//2}" y1="{rule_y}" x2="{x + rule_width//2}" y2="{rule_y}" '
                f'stroke="{color}" stroke-width="1.5" opacity="0.6"/>',
                f'<circle cx="{x - rule_width//2 - 6}" cy="{rule_y}" r="3" fill="{color}" opacity="0.8"/>',
                f'<circle cx="{x + rule_width//2 + 6}" cy="{rule_y}" r="3" fill="{color}" opacity="0.8"/>'
            ]

        return "\n".join(rule_parts) + f'''
        <text x="{x}" y="{y}" font-family="'Playfair Display', 'Times New Roman', serif"
              font-size="{font_size}" fill="{color}" text-anchor="{align}" letter-spacing="3">
            {xml_escape(author)}
        </text>
        '''
        