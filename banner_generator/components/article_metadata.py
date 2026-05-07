
# banner_generator/components/article_metadata.py
from __future__ import annotations
from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "article_metadata"

    def render(self) -> str:
        cfg = (self.cfg.get("article_metadata") or {}) if isinstance(self.cfg.get("article_metadata"), dict) else {}
        article = self.ctx.article or {}

        category = cfg.get("category") or article.get("category", "Programming")
        subcategory = cfg.get("subcategory") or article.get("subcategory", "")
        framework = cfg.get("framework") or article.get("framework", "Python")

        # Determine the most specific group label for the count.
        # If we are inside a subcategory, the count refers to that subcategory.
        group_label = subcategory if subcategory else category

        # --- Priority: explicit series_part > automatic count > fallback progress ---
        series_part = cfg.get("series_part") or article.get("series_part", "")
        if series_part:
            # User explicitly provided a series description (e.g. “Part 7 of 20”)
            series_display = series_part
        else:
            # No series – use automatic category count, showing the correct group label
            category_count = cfg.get("category_article_count") or article.get("category_article_count", 0)
            if category_count and isinstance(category_count, int) and category_count > 0:
                series_display = f"{category_count} articles in {group_label}"
            else:
                # Last resort: the user‑editable `progress` field from the banner config
                series_display = self.cfg.get("progress", "")

        # Positioning: explicit y overrides y_offset
        if "y" in cfg:
            y = int(cfg["y"])
        else:
            y = self.y_offset + int(cfg.get("y_offset", 20))
        
        x = int(cfg.get("x", 85))
        font_size = int(cfg.get("font_size", 14))
        gap = int(cfg.get("gap", 12))
        icon_gap = int(cfg.get("icon_gap", 28))
        
        # Colors
        label_color = self.col.get("metadata_label", "#6272a4")
        value_color = self.col.get("metadata_value", "#f8f8f2")
        
        # Build display lines – only include non‑empty fields
        lines = []
        
        # Category line (with optional subcategory)
        cat_text = category
        if subcategory:
            cat_text = f"{category} › {subcategory}"
        if cat_text:
            lines.append(("📂", cat_text))
        
        # Framework line (only if provided)
        if framework:
            lines.append(("🐍", framework))
        
        # Series / category count line (only if non‑empty)
        if series_display:
            lines.append(("📚", series_display))
        
        parts = []
        cur_y = y
        for icon, text in lines:
            # Icon
            parts.append(
                f'<text x="{x}" y="{cur_y}" font-family="\'Inter\', sans-serif" '
                f'font-size="{font_size}" fill="{label_color}">{xml_escape(icon)}</text>'
            )
            # Text
            parts.append(
                f'<text x="{x + icon_gap}" y="{cur_y}" font-family="\'Inter\', sans-serif" '
                f'font-size="{font_size}" fill="{value_color}">{xml_escape(text)}</text>'
            )
            cur_y += gap + font_size
        
        self.used_height = cur_y - y
        return "\n".join(parts)