from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'bash_prompt'
    description = 'Simple bash prompt simulation'
    component_id = 'bash_prompt'

    def render(self) -> str:
        cfg = self.cfg.get('bash_prompt') or {} if isinstance(self.cfg.get('bash_prompt'), dict) else {}
        text = cfg.get('prompt', '[user@host ~]$')
        x = int(cfg.get('x', 85))
        y = int(cfg.get('y', 580))
        font_size = int(cfg.get('font_size', 18))
        user_color = self.col.get('bash_user', '#50fa7b')
        host_color = self.col.get('bash_host', '#ff79c6')
        path_color = self.col.get('bash_path', '#f1fa8c')
        prompt_color = self.col.get('bash_prompt_symbol', '#ffffff')
        parts = []
        parts.append(f'<tspan fill="{user_color}">user</tspan>')
        parts.append(f'<tspan fill="{prompt_color}">@</tspan>')
        parts.append(f'<tspan fill="{host_color}">host</tspan>')
        parts.append(f'<tspan fill="{prompt_color}"> ~]$ </tspan>')
        parts.append(f'''<tspan fill="{self.col.get('bash_cursor', '#ffb86c')}" font-weight="bold">█</tspan>''')
        return f'''\n  <!-- Bash prompt -->\n  <text x="{x}" y="{y}" font-family="'JetBrains Mono', monospace" font-size="{font_size}" fill="{prompt_color}">\n    {' '.join(parts)}\n  </text>\n'''.rstrip()