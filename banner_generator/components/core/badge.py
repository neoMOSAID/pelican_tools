
# banner_generator/components/badge.py

from __future__ import annotations
from ..base import BaseComponent, xml_escape


class Component(BaseComponent):
    component_id = "badge"
    z_index = 150
    section_name = "badge"
    description = "Series badge / label (pill‑shaped)"
    config_schema = {
        "text": {"type": "str", "default": "", "help": "Badge text (e.g., series name)"},
        "x": {"type": "int", "default": 85, "help": "X position"},
        "y": {"type": "int", "default": 85, "help": "Y position"},
        "width": {"type": "int", "default": 220, "help": "Badge width"},
        "height": {"type": "int", "default": 36, "help": "Badge height"},
        "font_size": {"type": "int", "default": 16, "help": "Font size"},
        "align": {"type": "str", "default": "start", "help": "Text alignment: start, middle, end"},
    }
    
    def render(self) -> str:
        badge_cfg = self.cfg.get("badge") or {}
        if not isinstance(badge_cfg, dict):
            badge_cfg = {}

        text = badge_cfg.get("text") or self.cfg.get("series")
        if not text:
            return ""

        x = int(badge_cfg.get("x", 85))
        y = int(badge_cfg.get("y", 85))
        w = int(badge_cfg.get("width", 220))
        h = int(badge_cfg.get("height", 36))
        font_size = int(badge_cfg.get("font_size", 16))
        align = badge_cfg.get("align", "start").lower()

        # Horizontal alignment
        if align == "middle":
            text_x = x + w / 2
            text_anchor = "middle"
        elif align == "end":
            text_x = x + w - 12
            text_anchor = "end"
        else:  # start
            text_x = x + 12
            text_anchor = "start"

        # Vertical centering using dominant-baseline
        text_y = y + h / 2

        bg = self.col.get("badge_bg", "#313244")
        stroke = self.col.get("badge_stroke", "#94a3b8")
        text_color = self.col.get("badge_text", "#cdd6f4")

        # Make corners pill‑shaped if width > height
        rx = h // 2 if w > h else 8

        return f"""
  <!-- Series badge -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"
        fill="{bg}" opacity="0.8" stroke="{stroke}" stroke-width="1.5" />
  <text x="{text_x:.1f}" y="{text_y:.1f}" font-family="'Inter', 'Helvetica Neue', sans-serif"
        font-size="{font_size}" fill="{text_color}" font-weight="600"
        text-anchor="{text_anchor}" dominant-baseline="central" letter-spacing="1.5">{xml_escape(str(text))}</text>
"""
