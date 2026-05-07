
from __future__ import annotations

from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "package_list"

    def render(self) -> str:
        cfg = (self.cfg.get("package_list") or {}) if isinstance(self.cfg.get("package_list"), dict) else {}
        packages = cfg.get("packages", ["nginx", "docker", "ufw"])
        x = int(cfg.get("x", 85))
        y = int(cfg.get("y", 556))
        font_size = int(cfg.get("font_size", 12))
        gap = int(cfg.get("gap", 8))
        pad = int(cfg.get("pad", 6))
        bg = self.col.get("pkg_bg", "#44475a")
        fg = self.col.get("pkg_fg", "#f8f8f2")
        stroke = self.col.get("pkg_stroke", "#6272a4")
        opacity = float(cfg.get("opacity", 0.8))

        parts = []
        cur_x = x
        for pkg in packages:
            txt = str(pkg)
            w = len(txt) * font_size * 0.6 + 2 * pad
            h = font_size + 2 * pad
            parts.append(f'<rect x="{cur_x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{bg}" opacity="{opacity}" stroke="{stroke}" stroke-width="1" />')
            parts.append(f'<text x="{cur_x + w/2}" y="{y + h/2 + font_size/3}" font-family="\'JetBrains Mono\', monospace" font-size="{font_size}" fill="{fg}" text-anchor="middle">{xml_escape(txt)}</text>')
            cur_x += w + gap
        return "  <!-- Package list -->\n  " + "\n  ".join(parts)
        