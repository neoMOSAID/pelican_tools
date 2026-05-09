from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'sysinfo'
    description = 'Neofetch‑style system information panel'
    component_id = 'sysinfo'
    LOGOS = {'tux': '\n<g>\n  <ellipse cx="60" cy="70" rx="38" ry="45" fill="#0b0f14"/>\n  <ellipse cx="60" cy="45" rx="28" ry="22" fill="#ffffff"/>\n  <circle cx="50" cy="42" r="3" fill="#000"/>\n  <circle cx="70" cy="42" r="3" fill="#000"/>\n  <path d="M52 55 Q60 62 68 55" stroke="#000" stroke-width="2" fill="none"/>\n</g>\n', 'arch': '\n<g>\n  <path d="M60 10 L110 120 L10 120 Z" fill="#1793d1"/>\n  <path d="M60 45 L85 95 L35 95 Z" fill="#0a0f14" opacity="0.6"/>\n</g>\n', 'debian': '\n<g>\n  <circle cx="60" cy="65" r="45" fill="#a80030"/>\n  <path d="M60 30c-20 10-20 40 0 50c20-10 20-40 0-50z" fill="#fff"/>\n</g>\n'}

    def render(self) -> str:
        cfg = self.cfg.get('sysinfo') or {} if isinstance(self.cfg.get('sysinfo'), dict) else {}
        logo = cfg.get('logo', 'tux').lower()
        entries = cfg.get('entries', ['Kernel: 6.1', 'Shell: zsh', 'Uptime: 42 days', 'WM: i3', 'Theme: dark'])
        x = int(cfg.get('x', 60))
        y = int(cfg.get('y', 80))
        fg_primary = self.col.get('sysinfo_fg', '#cdd6f4')
        fg_label = self.col.get('sysinfo_label', '#7aa2f7')
        accent = self.col.get('sysinfo_accent', '#89b4fa')
        bg = self.col.get('sysinfo_bg', '#0b0f14')
        line_h = int(cfg.get('line_height', 26))
        font = int(cfg.get('font_size', 16))
        logo_svg = self.LOGOS.get(logo, self.LOGOS['tux'])
        logo_x = x
        logo_y = y
        info_x = x + 180
        info_y = y + 10
        background = f'\n<rect x="{x - 30}" y="{y - 50}" width="520" height="220" rx="12"\nfill="{bg}" opacity="0.85"/>\n'
        logo_block = f'\n<g transform="translate({logo_x},{logo_y}) scale(0.9)">\n{logo_svg}\n</g>\n'
        info_parts = []
        for i, entry in enumerate(entries):
            if ': ' in entry:
                label, value = entry.split(': ', 1)
            else:
                label, value = (entry, '')
            yy = info_y + i * line_h
            info_parts.append(f'\n<text x="{info_x}" y="{yy}"\nfont-family="JetBrains Mono, monospace"\nfont-size="{font}"\nfill="{fg_label}">\n{xml_escape(label)}:\n</text>\n\n<text x="{info_x + 110}" y="{yy}"\nfont-family="JetBrains Mono, monospace"\nfont-size="{font}"\nfill="{fg_primary}">\n{xml_escape(value)}\n</text>\n')
        header = f'\n<text x="{info_x}" y="{y - 10}"\nfont-family="JetBrains Mono, monospace"\nfont-size="{font + 2}"\nfill="{accent}">\nSystem Information\n</text>\n'
        return '\n'.join(['<!-- Neofetch-style system info -->', background, logo_block, header, '\n'.join(info_parts)])