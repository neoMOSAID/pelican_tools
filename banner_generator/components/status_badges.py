
# banner_generator/components/status_badges.py

from __future__ import annotations

from .base import BaseComponent, xml_escape


class Component(BaseComponent):
    component_id = "status_badges"

    def render(self) -> str:
        config = self.cfg.get("status_badges")
        if isinstance(config, list):
            badges = config
            x = 85
            y = 568
            font_size = 12
            gap = 8
            pad = 8
            bg = None
            fg = None
            stroke = None
            opacity = 0.7
        elif isinstance(config, dict):
            badges = config.get("badges") or config.get("list") or []
            x = int(config.get("x", 85))
            y = int(config.get("y", 568))
            font_size = int(config.get("font_size", 12))
            gap = int(config.get("gap", 8))
            pad = int(config.get("pad", 8))
            bg = config.get("bg")
            fg = config.get("fg")
            stroke = config.get("stroke")
            opacity = float(config.get("opacity", 0.7))
        else:
            badges = self.cfg.get("status_badges")
            if badges is None:
                badges = self.cfg.get("badges")
            if not badges:
                return ""
            x = 85
            y = 568
            font_size = 12
            gap = 8
            pad = 8
            bg = None
            fg = None
            stroke = None
            opacity = 0.7

        if not badges:
            return ""

        bg = bg or self.col.get("badge_bg", "#313244")
        fg = fg or self.col.get("badge_text", "#cdd6f4")
        stroke = stroke or self.col.get("badge_stroke", "#94a3b8")

        char_w = font_size * 0.6
        rect_h = font_size + 2 * pad

        parts = []
        cur_x = x
        for text in badges:
            txt = str(text)
            rect_w = len(txt) * char_w + 2 * pad
            parts.append(
                f'<rect x="{cur_x}" y="{y}" width="{rect_w}" height="{rect_h}" rx="4" '
                f'fill="{bg}" opacity="{opacity}" stroke="{stroke}" stroke-width="1" />'
            )
            # Vertically center text
            text_y = y + rect_h / 2
            parts.append(
                f'<text x="{cur_x + rect_w/2}" y="{text_y:.1f}" text-anchor="middle" '
                f'dominant-baseline="central" '
                f'font-family="\'JetBrains Mono\', monospace" font-size="{font_size}" '
                f'fill="{fg}">{xml_escape(txt)}</text>'
            )
            cur_x += rect_w + gap

        return '  <!-- Status badges -->\n  ' + "\n  ".join(parts)
        