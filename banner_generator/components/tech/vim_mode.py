from __future__ import annotations
from ..base import BaseComponent, xml_escape
MODE_COLORS = {'NORMAL': ('normal', '#50fa7b'), 'INSERT': ('insert', '#bd93f9'), 'VISUAL': ('visual', '#8be9fd'), 'COMMAND': ('command', '#ffb86c'), 'REPLACE': ('replace', '#ff5555')}

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'vim_mode'
    description = 'Vim mode indicator (NORMAL, INSERT, etc.)'
    component_id = 'vim_mode'

    def render(self) -> str:
        cfg = self.cfg.get('vim_mode') or {} if isinstance(self.cfg.get('vim_mode'), dict) else {}
        mode = str(cfg.get('mode', 'NORMAL')).upper()
        animated = bool(cfg.get('animated', True))
        position = str(cfg.get('position', 'top-right')).lower()
        w = int(cfg.get('width', 120))
        h = int(cfg.get('height', 32))
        x = int(cfg.get('x', 1050))
        y = int(cfg.get('y', 80))
        if position == 'top-right':
            x = self.w - w - int(cfg.get('margin_x', 30))
            y = int(cfg.get('margin_y', 80))
        mode_name, fill = MODE_COLORS.get(mode, (mode, '#ffffff'))
        bg = self.col.get('vim_mode_bg', '#282a36')
        stroke = self.col.get('vim_mode_stroke', '#6272a4')
        cursor = ''
        if animated:
            cursor = f'''<rect x="{x + w - 24}" y="{y + 10}" width="8" height="16" fill="{self.col.get('vim_cursor', '#ffb86c')}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" /></rect>'''
        return f'''\n  <!-- Vim mode badge -->\n  <g>\n    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{bg}" opacity="0.9" stroke="{stroke}" stroke-width="1.5" />\n    <text x="{x + 10}" y="{y + 22}" font-family="'JetBrains Mono', monospace" font-size="16" fill="{fill}" font-weight="bold">{xml_escape(mode_name)}</text>\n    {cursor}\n  </g>\n'''.rstrip()