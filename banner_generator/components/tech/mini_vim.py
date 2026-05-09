from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'mini_vim'
    description = 'Small Vim window with command list'
    component_id = 'mini_vim'

    def render(self) -> str:
        cfg = self.cfg.get('mini_vim') or {} if isinstance(self.cfg.get('mini_vim'), dict) else {}
        lines = cfg.get('lines', ['set number', 'syntax on', 'colorscheme dracula'])
        x = int(cfg.get('x', 80))
        y = int(cfg.get('y', 500))
        line_h = int(cfg.get('line_height', 18))
        font_size = int(cfg.get('font_size', 12))
        padding = int(cfg.get('padding', 10))
        bg = self.col.get('mini_vim_bg', '#282a36')
        stroke = self.col.get('mini_vim_stroke', '#6272a4')
        fg = self.col.get('mini_vim_fg', '#f8f8f2')
        ln_fg = self.col.get('mini_vim_ln', '#6272a4')
        mode_bg = self.col.get('mini_vim_mode_bg', '#50fa7b')
        mode_fg = self.col.get('mini_vim_mode_fg', '#282a36')
        text_width = max((len(l) for l in lines)) * font_size * 0.6 + 30
        box_w = padding * 2 + text_width
        box_h = padding * 2 + len(lines) * line_h + 20
        parts = []
        parts.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="6" fill="{bg}" stroke="{stroke}" stroke-width="1.5" />')
        parts.append(f'<rect x="{x}" y="{y + box_h - 20}" width="{box_w}" height="20" fill="{mode_bg}" rx="6" />')
        parts.append(f'<rect x="{x}" y="{y + box_h - 20}" width="{box_w}" height="20" fill="{mode_bg}" rx="0" />')
        parts.append(f'<rect x="{x}" y="{y + box_h - 20}" width="{box_w}" height="20" rx="6" fill="none" stroke="{stroke}" stroke-width="1.5" />')
        parts.append(f'''<text x="{x + padding}" y="{y + box_h - 6}" font-family="'JetBrains Mono', monospace" font-size="11" fill="{mode_fg}" font-weight="bold">NORMAL</text>''')
        for i, line in enumerate(lines):
            ln_x = x + padding
            ln_y = y + padding + i * line_h + font_size
            parts.append(f'''<text x="{ln_x}" y="{ln_y}" font-family="'JetBrains Mono', monospace" font-size="{font_size}" fill="{ln_fg}">{i + 1}</text>''')
            parts.append(f'''<text x="{ln_x + 24}" y="{ln_y}" font-family="'JetBrains Mono', monospace" font-size="{font_size}" fill="{fg}">{xml_escape(line)}</text>''')
        return '  <!-- Mini Vim window -->\n  ' + '\n  '.join(parts)