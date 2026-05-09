from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'chart_simple'
    description = 'Simple bar chart'
    component_id = 'chart_simple'

    def render(self) -> str:
        cfg = self.cfg.get('chart_simple') or {} if isinstance(self.cfg.get('chart_simple'), dict) else {}
        data = cfg.get('data', [{'label': 'A', 'value': 30}, {'label': 'B', 'value': 70}])
        title = cfg.get('title', '')
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        bar_width = int(cfg.get('bar_width', 40))
        max_height = int(cfg.get('max_height', 150))
        gap = int(cfg.get('gap', 20))
        bar_color = self.col.get('chart_bar', '#50fa7b')
        label_color = self.col.get('chart_label', '#cdd6f4')
        title_color = self.col.get('chart_title', '#f8f8f2')
        max_val = max((d['value'] for d in data)) if data else 1
        parts = []
        if title:
            parts.append(f'''<text x="{x}" y="{y}" font-family="'Inter', sans-serif" font-size="18" font-weight="bold" fill="{title_color}">{xml_escape(title)}</text>''')
            y += 25
        cur_x = x
        for item in data:
            val = item['value']
            height = int(max_height * val / max_val)
            rect_y = y + (max_height - height)
            parts.append(f'<rect x="{cur_x}" y="{rect_y}" width="{bar_width}" height="{height}" rx="4" fill="{bar_color}" opacity="0.8" />')
            parts.append(f'''<text x="{cur_x + bar_width / 2}" y="{y + max_height + 15}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="12" fill="{label_color}">{xml_escape(item['label'])}</text>''')
            parts.append(f'''<text x="{cur_x + bar_width / 2}" y="{rect_y - 5}" text-anchor="middle" font-family="'Inter', sans-serif" font-size="12" fill="{label_color}">{val}</text>''')
            cur_x += bar_width + gap
        self.used_height = max_height + 50
        return '\n'.join(parts)