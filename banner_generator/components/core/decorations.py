from __future__ import annotations
from ..base import BaseComponent

class Component(BaseComponent):
    config_schema = {}
    z_index = 20
    section_name = 'decorations'
    description = 'Code rain, floating geometry, pulsing brackets'
    component_id = 'decorations'

    def render(self) -> str:
        deco = self.cfg.get('decorations') or {} if isinstance(self.cfg.get('decorations'), dict) else {}
        code_rain = bool(deco.get('code_rain', self.cfg.get('code_rain', True)))
        floating_geometry = bool(deco.get('floating_geometry', self.cfg.get('floating_geometry', True)))
        pulsing_bracket = bool(deco.get('pulsing_bracket', self.cfg.get('pulsing_bracket', True)))
        scanlines = bool(deco.get('scanlines', self.cfg.get('scanlines', True)))
        x_offset = int(deco.get('x_offset', 0))
        y_offset = int(deco.get('y_offset', 0))
        scale = float(deco.get('scale', 1.0))
        parts = []
        if x_offset != 0 or y_offset != 0 or scale != 1.0:
            parts.append(f'<g transform="translate({x_offset}, {y_offset}) scale({scale})">')
        if code_rain:
            parts.append(f'''\n  <!-- Code rain -->\n  <g opacity="0.03" font-family="'JetBrains Mono', monospace" font-size="16" fill="{self.col.get('code_structure', '#cdd6f4')}">\n    <text x="50" y="180">def build():</text>\n    <text x="230" y="260">&lt;html&gt;</text>\n    <text x="500" y="210">import pelican</text>\n    <text x="180" y="510">class Site</text>\n    <text x="850" y="590">git commit</text>\n    <text x="1050" y="170">pip install</text>\n    <text x="300" y="560">yaml.load</text>\n  </g>\n'''.rstrip())
        if floating_geometry:
            parts.append(f'''\n  <!-- Floating geometry -->\n  <g opacity="0.1">\n    <circle cx="100" cy="570" r="8" fill="none" stroke="{self.col.get('pelican_stroke', '#94a3b8')}" stroke-width="2">\n      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="6s" repeatCount="indefinite" />\n    </circle>\n    <circle cx="1150" cy="130" r="12" fill="none" stroke="{self.col.get('pelican_stroke', '#94a3b8')}" stroke-width="1.5">\n      <animateTransform attributeName="transform" type="translate" values="0,0; 0,10; 0,0" dur="7s" repeatCount="indefinite" />\n    </circle>\n    <polygon points="560,80 570,100 550,110" fill="none" stroke="{self.col.get('dots_color', '#94a3b8')}" stroke-width="1">\n      <animateTransform attributeName="transform" type="rotate" values="0 560 95; 10 560 95; 0 560 95" dur="10s" repeatCount="indefinite" />\n    </polygon>\n  </g>\n'''.rstrip())
        if pulsing_bracket:
            parts.append(f'''\n  <!-- Decorative bracket -->\n  <g opacity="0.08" fill="none" stroke="{self.col.get('decorative_bracket', '#f5c2e7')}" stroke-width="4" font-family="'JetBrains Mono', monospace" font-size="90" font-weight="bold">\n    <text x="980" y="550" fill="{self.col.get('decorative_bracket', '#f5c2e7')}" stroke="none">&#123; &#125;\n      <animate attributeName="opacity" values="0.6; 1; 0.6" dur="6s" repeatCount="indefinite" />\n    </text>\n  </g>\n'''.rstrip())
        if scanlines:
            parts.append(f'  <rect width="{self.w}" height="{self.h}" fill="url(#scanlines)" pointer-events="none" />')
        if x_offset != 0 or y_offset != 0 or scale != 1.0:
            parts.append('</g>')
        return '\n'.join(parts).rstrip()