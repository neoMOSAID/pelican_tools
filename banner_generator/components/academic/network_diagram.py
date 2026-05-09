from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'network_diagram'
    description = 'Simple network node diagram'
    component_id = 'network_diagram'

    def render(self) -> str:
        cfg = self.cfg.get('network_diagram') or {} if isinstance(self.cfg.get('network_diagram'), dict) else {}
        nodes = cfg.get('nodes', ['Client', 'Server', 'Database'])
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        scale = float(cfg.get('scale', 1.0))
        node_radius = int(30 * scale)
        line_color = self.col.get('network_line', self.col.get('separator', '#45475a'))
        node_fill = self.col.get('network_node', self.col.get('badge_bg', '#313244'))
        node_stroke = self.col.get('network_stroke', self.col.get('badge_stroke', '#94a3b8'))
        text_color = self.col.get('network_text', self.col.get('badge_text', '#cdd6f4'))
        n = len(nodes)
        spacing = 120
        if n <= 3:
            centers = [(x + i * spacing, y + node_radius) for i in range(n)]
        else:
            half = (n + 1) // 2
            centers = []
            for i in range(half):
                centers.append((x + i * spacing, y + node_radius))
            for i in range(n - half):
                centers.append((x + i * spacing, y + node_radius + 80))
        parts = []
        for i in range(len(centers) - 1):
            x1, y1 = centers[i]
            x2, y2 = centers[i + 1]
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{line_color}" stroke-width="2" stroke-dasharray="4" />')
        for (cx, cy), label in zip(centers, nodes):
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{node_radius}" fill="{node_fill}" stroke="{node_stroke}" stroke-width="2" />')
            parts.append(f'''<text x="{cx}" y="{cy + 5}" text-anchor="middle" dominant-baseline="middle" font-family="'JetBrains Mono', monospace" font-size="12" fill="{text_color}">{xml_escape(label)}</text>''')
        max_y = max((cy for _, cy in centers)) + node_radius + 15
        self.used_height = max_y - self.y_offset
        return '\n'.join(parts)