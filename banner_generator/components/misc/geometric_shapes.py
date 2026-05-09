from __future__ import annotations
from ..base import BaseComponent

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'geometric_shapes'
    description = 'Bars, circles, rectangles as accents'
    component_id = 'geometric_shapes'

    def render(self) -> str:
        cfg = self.cfg.get('geometric_shapes', {})
        if not isinstance(cfg, dict):
            return ''
        w, h = (self.w, self.h)
        c = self.col
        parts = []
        vert_bars = cfg.get('vertical_bars', [])
        for bar in vert_bars:
            x = bar.get('x', 0)
            y = bar.get('y', 0)
            width = bar.get('width', 8)
            height = bar.get('height', h)
            color = bar.get('color', c.get('vertical_bar', '#8e44ad'))
            opacity = bar.get('opacity', 0.25)
            parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}" opacity="{opacity}" />')
        horiz_bars = cfg.get('horizontal_bars', [])
        for bar in horiz_bars:
            x = bar.get('x', 0)
            y = bar.get('y', 0)
            width = bar.get('width', w)
            height = bar.get('height', 4)
            color = bar.get('color', c.get('horizontal_bar', '#d4af37'))
            opacity = bar.get('opacity', 0.4)
            parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}" opacity="{opacity}" />')
        circles = cfg.get('circles', [])
        for circ in circles:
            cx = circ.get('cx', 100)
            cy = circ.get('cy', 100)
            r = circ.get('r', 30)
            fill = circ.get('fill', c.get('circle_fill', 'none'))
            stroke = circ.get('stroke', c.get('circle_stroke', '#d4af37'))
            stroke_width = circ.get('stroke_width', 2)
            opacity = circ.get('opacity', 0.2)
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}" />')
        rects = cfg.get('rectangles', [])
        for rect in rects:
            x = rect.get('x', 0)
            y = rect.get('y', 0)
            width = rect.get('width', 100)
            height = rect.get('height', 100)
            fill = rect.get('fill', c.get('rect_fill', 'none'))
            stroke = rect.get('stroke', c.get('rect_stroke', '#c0392b'))
            stroke_width = rect.get('stroke_width', 1)
            opacity = rect.get('opacity', 0.15)
            parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}" />')
        if cfg.get('diagonal_lines', False):
            for i in range(0, h, 80):
                parts.append(f'''<line x1="0" y1="{i}" x2="{w}" y2="{i + 40}" stroke="{c.get('diagonal_stroke', '#d4af37')}" stroke-width="1" opacity="0.1" />''')
        return '\n'.join(parts)