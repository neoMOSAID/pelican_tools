
# banner_generator/components/definition_box.py
from __future__ import annotations
from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "definition_box"

    def render(self) -> str:
        cfg = (self.cfg.get("definition_box") or {}) if isinstance(self.cfg.get("definition_box"), dict) else {}
        term = cfg.get("term", "Term")
        definition = cfg.get("definition", "Definition text goes here")
        x = int(cfg.get("x", 85))
        y = self.y_offset + int(cfg.get("y_offset", 20))
        width = int(cfg.get("width", 500))
        font_size = int(cfg.get("font_size", 16))

        bg = self.col.get("def_bg", "#313244")
        border = self.col.get("def_border", "#6272a4")
        term_color = self.col.get("def_term", "#50fa7b")
        def_color = self.col.get("def_text", "#cdd6f4")

        lines = definition.split(" ", 10)  # rough wrapping
        wrapped = []
        # simple wrapping (60 chars)
        while definition:
            if len(definition) < 60:
                wrapped.append(definition)
                break
            else:
                wrapped.append(definition[:60])
                definition = definition[60:]

        term_y = y + 20
        def_y = term_y + 24

        parts = [f'<rect x="{x}" y="{y}" width="{width}" height="{40 + len(wrapped)*22}" rx="8" fill="{bg}" stroke="{border}" stroke-width="1.5" />']
        parts.append(f'<text x="{x+15}" y="{term_y}" font-family="\'Inter\', sans-serif" font-size="{font_size+2}" font-weight="bold" fill="{term_color}">{xml_escape(term)}</text>')
        for i, line in enumerate(wrapped):
            parts.append(f'<text x="{x+15}" y="{def_y + i*22}" font-family="\'Inter\', sans-serif" font-size="{font_size}" fill="{def_color}">{xml_escape(line)}</text>')
        self.used_height = (40 + len(wrapped)*22) + 15
        return "\n".join(parts)
        