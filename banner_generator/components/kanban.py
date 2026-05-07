
# banner_generator/components/kanban.py
from __future__ import annotations
from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "kanban"

    def render(self) -> str:
        cfg = (self.cfg.get("kanban") or {}) if isinstance(self.cfg.get("kanban"), dict) else {}
        columns = cfg.get("columns", ["To Do", "Doing", "Done"])
        cards = cfg.get("cards", ["Write article", "Generate banner", "Review"])
        x = int(cfg.get("x", 85))
        y = self.y_offset + int(cfg.get("y_offset", 20))
        col_w = int(cfg.get("column_width", 160))
        col_h = int(cfg.get("column_height", 240))
        card_h = int(cfg.get("card_height", 36))
        gap = int(cfg.get("gap", 12))
        font_size = int(cfg.get("font_size", 12))

        header_bg = self.col.get("kanban_header", "#313244")
        card_bg = self.col.get("kanban_card", "#1e1e2e")
        border = self.col.get("kanban_border", "#45475a")
        text_color = self.col.get("kanban_text", "#cdd6f4")

        parts = []
        cur_x = x
        for i, col_title in enumerate(columns):
            # Column background
            parts.append(f'<rect x="{cur_x}" y="{y}" width="{col_w}" height="{col_h}" rx="6" fill="none" stroke="{border}" stroke-width="1.5" />')
            parts.append(f'<rect x="{cur_x}" y="{y}" width="{col_w}" height="32" rx="6" fill="{header_bg}" />')
            parts.append(f'<text x="{cur_x + col_w/2}" y="{y + 22}" text-anchor="middle" font-family="\'Inter\', sans-serif" font-size="14" font-weight="bold" fill="{text_color}">{xml_escape(col_title)}</text>')
            # Cards (distribute cards among columns)
            start_idx = i * len(cards) // len(columns)
            end_idx = (i + 1) * len(cards) // len(columns)
            for j, card in enumerate(cards[start_idx:end_idx]):
                card_y = y + 40 + j * (card_h + 8)
                if card_y + card_h > y + col_h - 10:
                    break
                parts.append(f'<rect x="{cur_x + 8}" y="{card_y}" width="{col_w - 16}" height="{card_h}" rx="4" fill="{card_bg}" stroke="{border}" stroke-width="1" />')
                parts.append(
                    f'<text x="{cur_x + col_w/2}" y="{card_y + card_h/2 + 4}" text-anchor="middle" '
                    f'font-family="\'JetBrains Mono\', monospace" font-size="{font_size}" fill="{text_color}">{xml_escape(card)}</text>'
                )
            cur_x += col_w + gap

        self.used_height = col_h + 20
        return "\n".join(parts)
        