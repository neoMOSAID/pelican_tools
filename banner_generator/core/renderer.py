
# banner_generator/core/renderer.py

from __future__ import annotations
from typing import List, Optional

from .canvas import SvgDocument, join_fragments
from .factory import load_component, get_all_component_ids
from .context import BannerContext


class BannerRenderer:
    """Composes an SVG banner from enabled components, stacked by z_index."""

    def __init__(self, context: BannerContext):
        self.context = context

    def _enabled(self, component_id: str) -> bool:
        """Return True if the component is explicitly enabled via show_<id>."""
        comp_cfg = self.context.config.get("components") or {}
        key = f"show_{component_id}"
        return bool(comp_cfg.get(key, False))

    def compose(self, z_order: Optional[List[str]] = None) -> str:
        # 1) Determine the final list of component IDs to render (in order)
        if z_order is None:
            # Try to get a custom order from the banner config
            z_order = self.context.config.get("z_order")

        if z_order is None:
            # Default: take all enabled components and sort by their z_index
            all_ids = get_all_component_ids()
            enabled_ids = [cid for cid in all_ids if self._enabled(cid)]

            def _z(cid):
                Comp = load_component(cid)
                return getattr(Comp, 'z_index', 100)
            enabled_ids.sort(key=_z)
            z_order = enabled_ids

        # 2) First pass – collect defs (no y‑offset needed)
        defs_list: List[str] = []
        for cid in z_order:
            if not self._enabled(cid):
                continue
            Comp = load_component(cid)
            comp = Comp(self.context, y_offset=0)
            defs_list.append(comp.defs())

        # 3) Second pass – render with vertical cursor
        cursor_y = 0
        body_list: List[str] = []
        for cid in z_order:
            if not self._enabled(cid):
                continue
            Comp = load_component(cid)
            comp = Comp(self.context, y_offset=cursor_y)
            part = comp.render()
            if part.strip():
                body_list.append(part)
            cursor_y += comp.used_height

        doc = SvgDocument(
            width=self.context.canvas_w,
            height=self.context.canvas_h,
            defs=join_fragments(defs_list),
            body=join_fragments(body_list),
        )
        return doc.to_svg()
        