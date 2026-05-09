"""Component: central_emblem – a stylised shield / crest / geometric medallion."""
from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'central_emblem'
    description = 'Shield / crest / geometric medallion'
    component_id = 'central_emblem'

    def render(self) -> str:
        cfg = self.cfg.get('central_emblem', {})
        if not isinstance(cfg, dict):
            return ''
        style = cfg.get('style', 'shield')
        x = int(cfg.get('x', self.w // 2))
        y = int(cfg.get('y', self.h // 2))
        size = int(cfg.get('size', 180))
        fill = cfg.get('fill', self.col.get('emblem_fill', 'none'))
        stroke = cfg.get('stroke', self.col.get('emblem_stroke', '#d4af37'))
        stroke_width = int(cfg.get('stroke_width', 3))
        opacity = float(cfg.get('opacity', 0.6))
        if style == 'shield':
            path = f'M{x},{y - size} L{x + size},{y - size * 0.4} L{x + size * 0.5},{y + size * 0.6} L{x},{y + size} L{x - size * 0.5},{y + size * 0.6} L{x - size},{y - size * 0.4} Z'
        elif style == 'diamond':
            path = f'M{x},{y - size} L{x + size},{y} L{x},{y + size} L{x - size},{y} Z'
        else:
            return f'<circle cx="{x}" cy="{y}" r="{size}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}" />'
        return f'<path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}" />'