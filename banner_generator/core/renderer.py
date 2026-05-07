
# banner_generator/core/renderer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from .canvas import SvgDocument, join_fragments
from .factory import load_component
from .context import BannerContext


DEFAULT_Z_ORDER = [
    "background",
    "watermark",
    "decorations",
    "title",
    "meta_progress",
    "tagline",
    "article_metadata",
    "vim_editor",
    "terminal",
    "code_snippet",           # <-- add
    "latex_source",
    "network_diagram",        # add
    "database_relations_tables", # add
    "kanban",                 # add
    "sysinfo",
    "git",                    # add
    "metrics",                # add
    "vim_mode",
    "vim_statusline",
    "mini_vim",
    "vim_keystrokes",
    "bash_prompt",
    "ascii_logo",
    "package_list",
    "icon",
    "badge",
    "definition_box",
    "citation",
    "chart_simple",
    "equation",
    "status_badges",
    "social_icons",
    "credits",
    "quote",                  # add
]


@dataclass
class BannerRenderer:
    context: BannerContext

    def _enabled(self, component_id: str) -> bool:
        comp_cfg = self.context.config.get("components") or {}
        if not isinstance(comp_cfg, dict):
            return False
        key = f"show_{component_id}"
        return bool(comp_cfg.get(key, False))

    def compose(self, z_order: Optional[List[str]] = None) -> str:
        z = z_order or list(DEFAULT_Z_ORDER)
        defs_list: List[str] = []
        body_list: List[str] = []

        # First pass: collect all defs (no y offset needed)
        for cid in z:
            if not self._enabled(cid):
                continue
            ComponentClass = load_component(cid)
            comp = ComponentClass(self.context, y_offset=0)
            defs_list.append(comp.defs())

        # Second pass: render with vertical cursor
        cursor_y = 0
        for cid in z:
            if not self._enabled(cid):
                continue
            ComponentClass = load_component(cid)
            # pass current cursor as y_offset
            comp = ComponentClass(self.context, y_offset=cursor_y)
            svg_part = comp.render()
            if svg_part.strip():
                body_list.append(svg_part)
            cursor_y += comp.used_height

        doc = SvgDocument(
            width=self.context.canvas_w,
            height=self.context.canvas_h,
            defs=join_fragments(defs_list),
            body=join_fragments(body_list),
        )
        return doc.to_svg()

