
# banner_generator/components/meta_progress.py

from __future__ import annotations
from .base import BaseComponent, xml_escape


def _progress_width(progress_text: str) -> int:
    try:
        parts = str(progress_text).split()
        current = int(parts[1])
        total = int(parts[3])
        return int(560 * current / total)
    except Exception:
        return 112


def _progress_fill(progress_text: str) -> str:
    try:
        parts = str(progress_text).split()
        current = int(parts[1])
        total = int(parts[3])
        pct = current / total
    except Exception:
        pct = 0.2
    if pct < 0.4:
        return "url(#progressGradLow)"
    if pct < 0.8:
        return "url(#progressGradMid)"
    return "url(#progressGradHigh)"


class Component(BaseComponent):
    component_id = "meta_progress"

    def render(self) -> str:
        meta_cfg = self.cfg.get("meta_progress") or {}
        if not isinstance(meta_cfg, dict):
            meta_cfg = {}

        meta_text = self.cfg.get("meta")
        progress_text = self.cfg.get("progress")

        # Skip if both are empty or None
        if not meta_text and not progress_text:
            self.used_height = 0
            return ""

        # Positioning & styling (x is absolute, y is relative to cursor)
        meta_x = int(meta_cfg.get("x", 85))
        # Use the passed y_offset as base Y
        base_y = self.y_offset
        meta_y = base_y + int(meta_cfg.get("y_offset", 20))   # offset from cursor
        font_size = int(meta_cfg.get("font_size", 22))
        anchor = str(meta_cfg.get("anchor", "start"))
        show_progress = bool(meta_cfg.get("show_progress", True))
        progress_y_offset = int(meta_cfg.get("progress_y_offset", 25))
        bar_width = int(meta_cfg.get("progress_bar_width", 560))

        parts = []

        # Meta line (only if non‑empty)
        if meta_text:
            parts.append(
                f'<text x="{meta_x}" y="{meta_y}" '
                f'font-family="\'JetBrains Mono\', \'SF Mono\', monospace" '
                f'font-size="{font_size}" fill="{self.col.get("meta", "#6c7086")}" '
                f'font-weight="600" text-anchor="{anchor}">{xml_escape(str(meta_text))}</text>'
            )

        # Progress bar (only if non‑empty)
        if show_progress and progress_text:
            pw = _progress_width(progress_text)
            fill = _progress_fill(progress_text)

            bar_y = meta_y + progress_y_offset
            parts.append(
                f'<rect x="{meta_x}" y="{bar_y}" width="{bar_width}" height="6" rx="3" '
                f'fill="{self.col.get("progress_bar_bg", "#313244")}" />'
            )
            parts.append(
                f'<rect x="{meta_x}" y="{bar_y}" width="{pw}" height="6" rx="3" fill="{fill}" />'
            )
            parts.append(
                f'<text x="{meta_x}" y="{bar_y + 24}" '
                f'font-family="\'JetBrains Mono\', monospace" font-size="13" '
                f'fill="{self.col.get("meta", "#6c7086")}">{xml_escape(str(progress_text))}</text>'
            )

        # Estimate consumed height (meta line + maybe progress)
        h = 40 if (meta_text and progress_text) else 30
        self.used_height = h

        return "  <!-- Meta & progress -->\n  " + "\n  ".join(parts)
        