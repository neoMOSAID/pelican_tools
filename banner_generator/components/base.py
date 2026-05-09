

# banner_generator/components/base.py

from __future__ import annotations
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape as xml_escape


class BaseComponent(ABC):
    """Self‑contained visual element that renders SVG fragments."""

    component_id = "base"
    z_index = 100               # bottom = 0, top = 1000
    section_name = None         # TOML section name (e.g., "terminal") or None for top-level
    config_schema = {}          # dict of key -> {type, default, help}
    description = ""            # Short description for the component (used in [components] section)

    def __init__(self, context, y_offset: int = 0):
        self.ctx = context
        self.cfg = context.config
        self.col = context.colors
        self.layout = context.layout
        self.w = context.canvas_w
        self.h = context.canvas_h
        self.y_offset = y_offset
        self.used_height = 0

    def defs(self) -> str:
        return ""

    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


__all__ = ["BaseComponent", "xml_escape"]

