from __future__ import annotations
import re
from ..base import BaseComponent
DEFAULT_WATERMARK_SVG = '<?xml version="1.0" encoding="UTF-8"?>\n<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n  <defs>\n    <filter id="glow">\n      <feGaussianBlur stdDeviation="2.5" result="blur"/>\n      <feMerge>\n        <feMergeNode in="blur"/>\n        <feMergeNode in="SourceGraphic"/>\n      </feMerge>\n    </filter>\n    <pattern id="stripes" patternUnits="userSpaceOnUse" width="6" height="6">\n      <rect width="6" height="3" fill="#00ccff" opacity="0.25"/>\n      <rect y="3" width="6" height="3" fill="transparent"/>\n    </pattern>\n    <clipPath id="topHalf"><rect x="0" y="0" width="200" height="85"/></clipPath>\n    <clipPath id="bottomHalf"><rect x="0" y="115" width="200" height="85"/></clipPath>\n  </defs>\n  <circle cx="100" cy="100" r="90" fill="none" stroke="#00ccff" stroke-opacity="0.6" stroke-width="2" filter="url(#glow)"/>\n  <circle cx="100" cy="100" r="90" fill="url(#stripes)" clip-path="url(#topHalf)"/>\n  <circle cx="100" cy="100" r="90" fill="#00ccff" opacity="0.12" clip-path="url(#bottomHalf)"/>\n  <line x1="40" y1="92" x2="160" y2="92" stroke="#00ccff" stroke-opacity="0.7" stroke-width="1" filter="url(#glow)"/>\n  <line x1="40" y1="108" x2="160" y2="108" stroke="#00ccff" stroke-opacity="0.7" stroke-width="1" filter="url(#glow)"/>\n  <text x="100" y="100" text-anchor="middle" dominant-baseline="middle" font-family="monospace" font-size="14" fill="#00ccff" filter="url(#glow)">MOSAID Tutorials</text>\n</svg>'

def _parse_svg_inner(raw_svg: str):
    raw_svg = (raw_svg or '').strip() or DEFAULT_WATERMARK_SVG.strip()
    if raw_svg.lower().startswith('<?xml'):
        raw_svg = raw_svg[raw_svg.find('?>') + 2:].strip()
    w, h = (200.0, 200.0)
    inner_raw = raw_svg
    if raw_svg.lower().startswith('<svg'):
        match = re.search('viewBox\\s*=\\s*"([\\d\\.\\s]+)"', raw_svg)
        if match:
            parts = match.group(1).split()
            if len(parts) == 4:
                w = float(parts[2])
                h = float(parts[3])
        else:
            match_w = re.search('width\\s*=\\s*"([\\d\\.]+)"', raw_svg)
            match_h = re.search('height\\s*=\\s*"([\\d\\.]+)"', raw_svg)
            if match_w:
                w = float(match_w.group(1))
            if match_h:
                h = float(match_h.group(1))
        end_tag = raw_svg.find('>')
        inner_raw = raw_svg[end_tag + 1:]
        if inner_raw.endswith('</svg>'):
            inner_raw = inner_raw[:-6].strip()
    inner_raw = re.sub('\\sopacity\\s*=\\s*"[^"]*"', '', inner_raw)
    return (inner_raw, w, h)

class Component(BaseComponent):
    config_schema = {}
    z_index = 10
    section_name = 'watermark'
    description = 'Rotating watermark overlay'
    component_id = 'watermark'

    def render(self) -> str:
        svg_text = self.cfg.get('watermark_svg') or DEFAULT_WATERMARK_SVG
        inner, w, h = _parse_svg_inner(svg_text)
        wm_cfg = self.cfg.get('watermark') or {} if isinstance(self.cfg.get('watermark'), dict) else {}
        opacity = float(wm_cfg.get('opacity', 0.15))
        scale = float(wm_cfg.get('scale', 0.8))
        rotate_dur = str(wm_cfg.get('rotate_dur', '30s'))
        x = self.w - w * scale - float(wm_cfg.get('x_offset', 300))
        y = self.h - h * scale - float(wm_cfg.get('y_offset', 40))
        return f'\n  <!-- Watermark (single, rotating vector) -->\n  <g transform="translate({x:.2f}, {y:.2f}) scale({scale})" opacity="{opacity}">\n    <g>\n      <animateTransform attributeName="transform" type="rotate"\n        from="0 {w / 2:.2f} {h / 2:.2f}" to="360 {w / 2:.2f} {h / 2:.2f}"\n        dur="{rotate_dur}" repeatCount="indefinite" />\n      {inner}\n    </g>\n  </g>\n'.rstrip()