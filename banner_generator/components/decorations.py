
from __future__ import annotations

from .base import BaseComponent


class Component(BaseComponent):
    component_id = "decorations"

    def render(self) -> str:
        deco = (self.cfg.get("decorations") or {}) if isinstance(self.cfg.get("decorations"), dict) else {}
        code_rain = bool(deco.get("code_rain", self.cfg.get("code_rain", True)))
        floating_geometry = bool(deco.get("floating_geometry", self.cfg.get("floating_geometry", True)))
        pulsing_bracket = bool(deco.get("pulsing_bracket", self.cfg.get("pulsing_bracket", True)))
        scanlines = bool(deco.get("scanlines", self.cfg.get("scanlines", True)))

        # Positioning offsets (new configurable)
        x_offset = int(deco.get("x_offset", 0))
        y_offset = int(deco.get("y_offset", 0))
        scale = float(deco.get("scale", 1.0))

        parts = []

        # Wrap everything in a translated/scaled group when needed
        if x_offset != 0 or y_offset != 0 or scale != 1.0:
            parts.append(f'<g transform="translate({x_offset}, {y_offset}) scale({scale})">')

        if code_rain:
            parts.append(f"""
  <!-- Code rain -->
  <g opacity=\"0.03\" font-family=\"'JetBrains Mono', monospace\" font-size=\"16\" fill=\"{self.col.get('code_structure', '#cdd6f4')}\">
    <text x=\"50\" y=\"180\">def build():</text>
    <text x=\"230\" y=\"260\">&lt;html&gt;</text>
    <text x=\"500\" y=\"210\">import pelican</text>
    <text x=\"180\" y=\"510\">class Site</text>
    <text x=\"850\" y=\"590\">git commit</text>
    <text x=\"1050\" y=\"170\">pip install</text>
    <text x=\"300\" y=\"560\">yaml.load</text>
  </g>
""".rstrip())

        if floating_geometry:
            parts.append(f"""
  <!-- Floating geometry -->
  <g opacity=\"0.1\">
    <circle cx=\"100\" cy=\"570\" r=\"8\" fill=\"none\" stroke=\"{self.col.get('pelican_stroke', '#94a3b8')}\" stroke-width=\"2\">
      <animateTransform attributeName=\"transform\" type=\"translate\" values=\"0,0; 0,-8; 0,0\" dur=\"6s\" repeatCount=\"indefinite\" />
    </circle>
    <circle cx=\"1150\" cy=\"130\" r=\"12\" fill=\"none\" stroke=\"{self.col.get('pelican_stroke', '#94a3b8')}\" stroke-width=\"1.5\">
      <animateTransform attributeName=\"transform\" type=\"translate\" values=\"0,0; 0,10; 0,0\" dur=\"7s\" repeatCount=\"indefinite\" />
    </circle>
    <polygon points=\"560,80 570,100 550,110\" fill=\"none\" stroke=\"{self.col.get('dots_color', '#94a3b8')}\" stroke-width=\"1\">
      <animateTransform attributeName=\"transform\" type=\"rotate\" values=\"0 560 95; 10 560 95; 0 560 95\" dur=\"10s\" repeatCount=\"indefinite\" />
    </polygon>
  </g>
""".rstrip())

        if pulsing_bracket:
            parts.append(f"""
  <!-- Decorative bracket -->
  <g opacity=\"0.08\" fill=\"none\" stroke=\"{self.col.get('decorative_bracket', '#f5c2e7')}\" stroke-width=\"4\" font-family=\"'JetBrains Mono', monospace\" font-size=\"90\" font-weight=\"bold\">
    <text x=\"980\" y=\"550\" fill=\"{self.col.get('decorative_bracket', '#f5c2e7')}\" stroke=\"none\">&#123; &#125;
      <animate attributeName=\"opacity\" values=\"0.6; 1; 0.6\" dur=\"6s\" repeatCount=\"indefinite\" />
    </text>
  </g>
""".rstrip())

        if scanlines:
            parts.append(f'  <rect width="{self.w}" height="{self.h}" fill="url(#scanlines)" pointer-events="none" />')

        # Close the translation/scale group if we opened one
        if x_offset != 0 or y_offset != 0 or scale != 1.0:
            parts.append('</g>')

        return "\n".join(parts).rstrip()

        