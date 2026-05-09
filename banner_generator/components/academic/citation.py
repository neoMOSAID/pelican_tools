from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'citation'
    description = 'Quote with author and source'
    component_id = 'citation'

    def render(self) -> str:
        cfg = self.cfg.get('citation') or {} if isinstance(self.cfg.get('citation'), dict) else {}
        text = cfg.get('text', 'Education is the most powerful weapon.')
        author = cfg.get('author', 'Nelson Mandela')
        source = cfg.get('source', '')
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        font_size = int(cfg.get('font_size', 18))
        width = int(cfg.get('width', 500))
        color = self.col.get('citation_text', '#a6adc8')
        author_color = self.col.get('citation_author', '#6c7086')
        parts = [f'''<text x="{x}" y="{y}" font-family="'Georgia', serif" font-style="italic" font-size="{font_size}" fill="{color}" text-anchor="start" wrap="true">{xml_escape(text)}</text>''']
        y += font_size + 10
        parts.append(f'''<text x="{x + 20}" y="{y}" font-family="'Inter', sans-serif" font-size="{font_size - 2}" fill="{author_color}">— {xml_escape(author)}</text>''')
        if source:
            y += font_size - 2
            parts.append(f'''<text x="{x + 20}" y="{y}" font-family="'Inter', sans-serif" font-size="{font_size - 4}" fill="{author_color}" opacity="0.7">{xml_escape(source)}</text>''')
        self.used_height = y - self.y_offset + 20
        return '\n'.join(parts)