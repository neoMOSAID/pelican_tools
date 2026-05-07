
from __future__ import annotations

from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "vim_statusline"

    def render(self) -> str:
        cfg = (self.cfg.get("vim_statusline") or {}) if isinstance(self.cfg.get("vim_statusline"), dict) else {}
        y = int(cfg.get("y", self.h - 50))
        x = int(cfg.get("x", 85))
        width = int(cfg.get("width", 500))
        segments = cfg.get("segments", ["  file.md  ", "  [+]  ", "  12,4  ", "  80% ☰  "])
        font_size = int(cfg.get("font_size", 14))
        fg = self.col.get("vim_statusline_fg", "#cdd6f4")
        bg_main = self.col.get("vim_statusline_bg", "#313244")
        bg_accent = self.col.get("vim_statusline_accent", "#45475a")

        rect_h = font_size + 8
        parts = []
        cur_x = x
        for i, seg in enumerate(segments):
            txt = str(seg).strip()
            seg_w = len(txt) * font_size * 0.6 + 16
            bg = bg_accent if i % 2 == 0 else bg_main
            parts.append(f'<rect x="{cur_x}" y="{y}" width="{seg_w}" height="{rect_h}" fill="{bg}" />')
            parts.append(
                f'<text x="{cur_x + seg_w/2}" y="{y + rect_h/2 + font_size/3}" '
                f'font-family="\'JetBrains Mono\', monospace" font-size="{font_size}" fill="{fg}" '
                f'text-anchor="middle">{xml_escape(txt)}</text>'
            )
            cur_x += seg_w + 2

        return "  <!-- Vim statusline -->\n  " + "\n  ".join(parts)
        