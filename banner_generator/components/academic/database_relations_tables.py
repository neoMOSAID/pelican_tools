from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'database_relations_tables'
    description = 'Database table schemas with relations'
    component_id = 'database_relations_tables'

    def render(self) -> str:
        cfg = self.cfg.get('database_relations_tables') or {} if isinstance(self.cfg.get('database_relations_tables'), dict) else {}
        tables = cfg.get('tables', [{'name': 'users', 'columns': ['id', 'name', 'email']}, {'name': 'posts', 'columns': ['id', 'user_id', 'title']}])
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        table_w = int(cfg.get('table_width', 200))
        row_h = int(cfg.get('row_height', 24))
        header_h = int(cfg.get('header_height', 32))
        gap = int(cfg.get('gap_between_tables', 40))
        font_size = int(cfg.get('font_size', 12))
        header_bg = self.col.get('db_header_bg', '#44475a')
        header_fg = self.col.get('db_header_fg', '#f8f8f2')
        row_bg = self.col.get('db_row_bg', '#282a36')
        row_alt = self.col.get('db_row_alt', '#1e1e2e')
        border = self.col.get('db_border', '#6272a4')
        parts = []
        max_h = 0
        cur_x = x
        for table in tables:
            name = table.get('name', 'table')
            cols = table.get('columns', [])
            num_rows = len(cols)
            total_h = header_h + num_rows * row_h
            parts.append(f'<rect x="{cur_x}" y="{y}" width="{table_w}" height="{total_h}" rx="4" fill="none" stroke="{border}" stroke-width="1.5" />')
            parts.append(f'<rect x="{cur_x}" y="{y}" width="{table_w}" height="{header_h}" rx="4" fill="{header_bg}" />')
            parts.append(f'<rect x="{cur_x}" y="{y + header_h // 2}" width="{table_w}" height="{header_h // 2}" fill="{header_bg}" />')
            parts.append(f'''<text x="{cur_x + table_w / 2}" y="{y + header_h / 2 + 4}" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="{font_size}" font-weight="bold" fill="{header_fg}">{xml_escape(name)}</text>''')
            for i, col in enumerate(cols):
                row_y = y + header_h + i * row_h
                bg = row_bg if i % 2 == 0 else row_alt
                parts.append(f'<rect x="{cur_x}" y="{row_y}" width="{table_w}" height="{row_h}" fill="{bg}" />')
                parts.append(f'''<text x="{cur_x + 10}" y="{row_y + row_h / 2 + 4}" font-family="'JetBrains Mono', monospace" font-size="{font_size}" fill="{self.col.get('db_text', '#cdd6f4')}">{xml_escape(col)}</text>''')
            if len(tables) > 1 and table != tables[-1]:
                next_x = cur_x + table_w + gap
                arrow_y = y + total_h // 2
                parts.append(f'<line x1="{cur_x + table_w}" y1="{arrow_y}" x2="{next_x - 10}" y2="{arrow_y}" stroke="{border}" stroke-width="2" marker-end="url(#arrowhead)" />')
            cur_x += table_w + gap
            max_h = max(max_h, total_h)
        self._defs = f'<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="{border}" /></marker>'
        self.used_height = max_h + 15
        return '\n'.join(parts)

    def defs(self) -> str:
        return getattr(self, '_defs', '')