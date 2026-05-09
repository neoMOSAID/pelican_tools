from __future__ import annotations
from ..base import BaseComponent, xml_escape

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'article_metadata'
    description = 'Category, subcategory, series info'
    component_id = 'article_metadata'

    def render(self) -> str:
        cfg = self.cfg.get('article_metadata') or {} if isinstance(self.cfg.get('article_metadata'), dict) else {}
        article = self.ctx.article or {}
        category = cfg.get('category') or article.get('category', 'Programming')
        subcategory = cfg.get('subcategory') or article.get('subcategory', '')
        framework = cfg.get('framework') or article.get('framework', 'Python')
        group_label = subcategory if subcategory else category
        series_part = cfg.get('series_part') or article.get('series_part', '')
        if series_part:
            series_display = series_part
        else:
            category_count = cfg.get('category_article_count') or article.get('category_article_count', 0)
            if category_count and isinstance(category_count, int) and (category_count > 0):
                series_display = f'{category_count} articles in {group_label}'
            else:
                series_display = self.cfg.get('progress', '')
        if 'y' in cfg:
            y = int(cfg['y'])
        else:
            y = self.y_offset + int(cfg.get('y_offset', 20))
        x = int(cfg.get('x', 85))
        font_size = int(cfg.get('font_size', 14))
        gap = int(cfg.get('gap', 12))
        icon_gap = int(cfg.get('icon_gap', 28))
        label_color = self.col.get('metadata_label', '#6272a4')
        value_color = self.col.get('metadata_value', '#f8f8f2')
        lines = []
        cat_text = category
        if subcategory:
            cat_text = f'{category} › {subcategory}'
        if cat_text:
            lines.append(('📂', cat_text))
        if framework:
            lines.append(('🐍', framework))
        if series_display:
            lines.append(('📚', series_display))
        parts = []
        cur_y = y
        for icon, text in lines:
            parts.append(f'''<text x="{x}" y="{cur_y}" font-family="'Inter', sans-serif" font-size="{font_size}" fill="{label_color}">{xml_escape(icon)}</text>''')
            parts.append(f'''<text x="{x + icon_gap}" y="{cur_y}" font-family="'Inter', sans-serif" font-size="{font_size}" fill="{value_color}">{xml_escape(text)}</text>''')
            cur_y += gap + font_size
        self.used_height = cur_y - y
        return '\n'.join(parts)