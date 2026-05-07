
from __future__ import annotations

from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "vim_keystrokes"

    def render(self) -> str:
        cfg = (self.cfg.get("vim_keystrokes") or {}) if isinstance(self.cfg.get("vim_keystrokes"), dict) else {}
        keys = cfg.get("keys", ["dd", "yy", "p", "gg=G"])
        x = int(cfg.get("x", 85))
        y = int(cfg.get("y", 560))
        key_w = int(cfg.get("key_width", 42))
        key_h = int(cfg.get("key_height", 28))
        gap = int(cfg.get("gap", 8))
        font_size = int(cfg.get("font_size", 14))
        bg = self.col.get("vim_key_bg", "#44475a")
        fg = self.col.get("vim_key_fg", "#f8f8f2")

        parts = []
        cur_x = x
        for key in keys:
            txt = str(key)
            parts.append(f'<rect x="{cur_x}" y="{y}" width="{key_w}" height="{key_h}" rx="4" fill="{bg}" opacity="0.8" />')
            parts.append(f'<text x="{cur_x + key_w/2}" y="{y + key_h/2 + font_size/3}" font-family="\'JetBrains Mono\', monospace" font-size="{font_size}" fill="{fg}" text-anchor="middle">{xml_escape(txt)}</text>')
            cur_x += key_w + gap
        return "  <!-- Vim keystrokes -->\n  " + "\n  ".join(parts)
        