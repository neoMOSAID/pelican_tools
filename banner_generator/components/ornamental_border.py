
"""Component: ornamental_border – elaborate SVG borders with filigree, corner pieces, and double lines."""

from __future__ import annotations
from .base import BaseComponent


class Component(BaseComponent):
    component_id = "ornamental_border"

    def render(self) -> str:
        cfg = self.cfg.get("ornamental_border", {})
        if not isinstance(cfg, dict):
            return ""

        margin = int(cfg.get("margin", 20))
        outer_stroke = cfg.get("outer_stroke", self.col.get("border_outer", "#d4af37"))
        inner_stroke = cfg.get("inner_stroke", self.col.get("border_inner", "#b8860b"))
        corner_size = int(cfg.get("corner_size", 40))
        double_line = cfg.get("double_line", True)

        w, h = self.w, self.h
        x1, y1 = margin, margin
        x2, y2 = w - margin, h - margin

        # Outer rectangle
        parts = [
            f'<rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" '
            f'fill="none" stroke="{outer_stroke}" stroke-width="2" />'
        ]

        if double_line:
            inner_margin = margin + 8
            x1i, y1i = inner_margin, inner_margin
            x2i, y2i = w - inner_margin, h - inner_margin
            parts.append(
                f'<rect x="{x1i}" y="{y1i}" width="{x2i - x1i}" height="{y2i - y1i}" '
                f'fill="none" stroke="{inner_stroke}" stroke-width="1.2" opacity="0.7" />'
            )

        # Corner ornaments (simple fleur‑de‑lis style)
        corners = [
            (x1, y1, 0),          # top‑left
            (x2, y1, 90),         # top‑right
            (x2, y2, 180),        # bottom‑right
            (x1, y2, 270)         # bottom‑left
        ]
        for cx, cy, rot in corners:
            parts.append(
                f'<g transform="translate({cx}, {cy}) rotate({rot})">'
                f'<path d="M0,0 L{corner_size},-{corner_size//2} L{corner_size//2},-{corner_size} Z" '
                f'fill="none" stroke="{outer_stroke}" stroke-width="1.5" opacity="0.8"/>'
                f'<circle cx="{corner_size//2}" cy="-{corner_size//2}" r="3" fill="{outer_stroke}"/>'
                f'</g>'
            )

        return "\n".join(parts)

        