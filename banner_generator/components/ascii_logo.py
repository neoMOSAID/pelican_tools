
from __future__ import annotations
from .base import BaseComponent

VECTOR_ART = {
    "tux": {
        "body": (
            "M -50 -40 C -70 -10, -70 40, -30 70 "
            "C 0 90, 40 90, 70 70 "
            "C 100 40, 100 -10, 80 -40 "
            "C 65 -60, -35 -60, -50 -40 Z"
        ),
        "belly": (
            "M -30 -20 C -45 0, -45 30, -15 50 "
            "C 10 65, 30 65, 50 50 "
            "C 70 30, 70 0, 55 -20 C 45 -35, -20 -35, -30 -20 Z"
        ),
        "eye_left": "M -15 -10 A 6 6 0 1 0 -15 -22 A 6 6 0 1 0 -15 -10",
        "eye_right": "M 15 -10 A 6 6 0 1 0 15 -22 A 6 6 0 1 0 15 -10",
        "beak": "M -5 -5 Q 0 -12 5 -5 Q 3 -3 0 -3 Q -3 -3 -5 -5",
        "foot_left": (
            "M -30 70 Q -45 85 -35 95 Q -20 85 -20 75 Q -25 70 -30 70"
        ),
        "foot_right": (
            "M 30 70 Q 45 85 35 95 Q 20 85 20 75 Q 25 70 30 70"
        ),
    },
    "vim": {
        "outer": (
            "M -40 -45 L 40 -45 L 40 -15 L 15 -15 L 15 0 "
            "L -15 0 L -15 -15 L -40 -15 Z"
        ),
        "inner_v": "M -10 -30 L 0 -10 L 10 -30 L 12 -25 L 6 -10 L 6 20 L -6 20 L -6 -10 L -12 -25 Z",
        "inner_im": "M -15 25 L -5 25 L -5 40 L 5 40 L 5 25 L 15 25 L 15 45 L -15 45 Z",
        "dot": "M 0 -35 A 2 2 0 1 0 0 -39 A 2 2 0 1 0 0 -35",  # VIM leader dot
    },
    "arch": {
        "body": (
            "M 0 -70 L 30 50 H 15 L 0 20 L -15 50 H -30 Z"
        ),
        "inner": (
            "M 0 -40 L -10 -10 H -3 L 0 -18 L 3 -10 H 10 Z"
        ),
    },
    "ubuntu": {
        "outer": "M -50 0 A 50 50 0 1 0 50 0 A 50 50 0 1 0 -50 0",
        "inner_top": "M 0 -35 A 17 17 0 1 0 0 -1 A 17 17 0 1 0 0 -35",
        "inner_left": "M -35 0 A 17 17 0 1 0 -1 0 A 17 17 0 1 0 -35 0",
        "inner_right": "M 35 0 A 17 17 0 1 0 1 0 A 17 17 0 1 0 35 0",
    },
}


class Component(BaseComponent):
    component_id = "ascii_logo"

    def render(self) -> str:
        cfg = (self.cfg.get("ascii_logo") or {}) if isinstance(self.cfg.get("ascii_logo"), dict) else {}
        art_key = cfg.get("art", "tux").lower()
        x = int(cfg.get("x", 100))
        y = int(cfg.get("y", 100))
        scale = float(cfg.get("scale", 1.0))          # default 1.0 = intuitive size
        opacity = float(cfg.get("opacity", 0.15))
        # Primary colour – use theme’s ascii_logo_color or fallback
        fill_color = self.col.get("ascii_logo_color", "#f1fa8c")
        stroke_color = self.col.get("ascii_logo_stroke", fill_color)
        stroke_width = float(cfg.get("stroke_width", 1.5))

        art = VECTOR_ART.get(art_key)
        if not art:
            # Fallback to Tux if unknown art
            art = VECTOR_ART["tux"]

        # Build SVG group with translation and scale
        parts = []
        parts.append(
            f'<g transform="translate({x}, {y}) scale({scale})" '
            f'opacity="{opacity}">'
        )
        # Optional: subtle glow filter (reuse existing titleGlow if available)
        # Here we add a simple drop-shadow for depth
        parts.append(
            f'<filter id="asciiGlow" x="-20%" y="-20%" width="140%" height="140%">'
            f'<feGaussianBlur in="SourceAlpha" stdDeviation="3" result="blur"/>'
            f'<feFlood flood-color="{fill_color}" flood-opacity="0.3" result="color"/>'
            f'<feComposite in="color" in2="blur" operator="in" result="glow"/>'
            f'<feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>'
            f'</filter>'
        )

        # Draw all sub‑paths of the chosen art
        for path_name, d in art.items():
            parts.append(
                f'<path d="{d}" fill="{fill_color}" '
                f'stroke="{stroke_color}" stroke-width="{stroke_width}" '
                f'filter="url(#asciiGlow)" vector-effect="non-scaling-stroke" />'
            )

        parts.append("</g>")
        return "  <!-- Vector logo -->\n  " + "\n  ".join(parts)
