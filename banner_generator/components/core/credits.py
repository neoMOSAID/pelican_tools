from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 160
    section_name = 'credits'
    description = 'Footer credits (site name and domain)'
    component_id = 'credits'

    def render(self) -> str:
        credits = self.cfg.get('credits') or {}
        if not isinstance(credits, dict):
            credits = {}
        line1 = credits.get('line1') or self.cfg.get('credits_line1') or 'MOSAID Tutorials'
        line2 = credits.get('line2') or self.cfg.get('credits_line2') or 'mosaid.xyz'
        font_size1 = int(credits.get('font_size1', credits.get('font_size', 18)))
        font_size2 = int(credits.get('font_size2', credits.get('font_size', 14)))
        x1 = int(credits.get('x1', credits.get('x', 1170)))
        y1 = int(credits.get('y1', credits.get('y', 580)))
        align1 = str(credits.get('align1', credits.get('align', 'end')))
        x2 = int(credits.get('x2', x1))
        y2 = int(credits.get('y2', y1 + font_size2 + 6))
        align2 = str(credits.get('align2', align1))
        color = self.col.get('credits', '#6c7086')
        return f'''\n    <!-- Credits -->\n    <text x="{x1}" y="{y1}" font-family="'Inter', 'Helvetica Neue', sans-serif" font-size="{font_size1}"\n            fill="{color}" font-weight="600" text-anchor="{align1}">{xml_escape(str(line1))}</text>\n    <text x="{x2}" y="{y2}" font-family="'JetBrains Mono', 'Fira Code', monospace" font-size="{font_size2}"\n            fill="{color}" text-anchor="{align2}" opacity="0.8">{xml_escape(str(line2))}</text>\n    '''