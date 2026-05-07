
from __future__ import annotations

from .base import BaseComponent, xml_escape


class Component(BaseComponent):
    component_id = "tagline"

    def render(self) -> str:
        tagline_cfg = (self.cfg.get("tagline") or {}) if isinstance(self.cfg.get("tagline"), dict) else {}
        # If tagline is a string (old style) or a dict, handle both
        if isinstance(self.cfg.get("tagline"), str) and not tagline_cfg:
            text = self.cfg.get("tagline")
        else:
            text = tagline_cfg.get("text") or self.cfg.get("tagline") or "Build your static site like a professional engineering system"

        x = int(tagline_cfg.get("x", 85))
        y = int(tagline_cfg.get("y", 548))
        width = int(tagline_cfg.get("width", 560))   # width of the separator line
        font_size = int(tagline_cfg.get("font_size", 16))
        color = tagline_cfg.get("color") or self.col.get("meta", "#6c7086")
        align = tagline_cfg.get("align", "start")
        show_separator = bool(tagline_cfg.get("show_separator", True))

        # Separator line (optional)
        separator_line = ""
        if show_separator:
            separator_y = y - font_size - 5   # 5px above baseline, you can adjust
            separator_line = f'<line x1="{x}" y1="{separator_y}" x2="{x + width}" y2="{separator_y}" stroke="{self.col.get("separator", "#45475a")}" stroke-width="0.5" opacity="0.5" />'

        return f"""
  <!-- Separator & tagline -->
  {separator_line}
  <text x="{x}" y="{y}" font-family="'Inter', sans-serif" font-size="{font_size}"
        fill="{color}" font-style="italic" text-anchor="{align}">
    {xml_escape(str(text))}
  </text>
""".rstrip()

