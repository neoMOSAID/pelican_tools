from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'multi_text'
    description = 'Multi‑line text block'
    component_id = 'multi_text'

    def render(self) -> str:
        cfg = self.cfg.get('multi_text', {})
        if not isinstance(cfg, dict):
            return ''
        lines = cfg.get('lines', [])
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        font_size = int(cfg.get('font_size', 14))
        line_height = int(cfg.get('line_height', 22))
        color = self.col.get('multi_text_color', '#333333')
        align = cfg.get('align', 'start')
        parts = []
        cur_y = y
        for line in lines:
            parts.append(f'''<text x="{x}" y="{cur_y}" font-family="'Inter', serif" font-size="{font_size}" fill="{color}" text-anchor="{align}">{xml_escape(line)}</text>''')
            cur_y += line_height
        self.used_height = cur_y - self.y_offset
        return '\n'.join(parts)