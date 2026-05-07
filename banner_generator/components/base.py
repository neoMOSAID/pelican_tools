
# banner_generator/components/base.py

from __future__ import annotations
from abc import ABC, abstractmethod
from xml.sax.saxutils import escape as xml_escape


class BaseComponent(ABC):
    """Self-contained visual element that renders SVG fragments."""

    component_id = "base"

    def __init__(self, context, y_offset: int = 0):
        self.ctx = context
        self.cfg = context.config
        self.col = context.colors
        self.layout = context.layout
        self.w = context.canvas_w
        self.h = context.canvas_h
        self.y_offset = y_offset          # vertical position passed from renderer
        self.used_height = 0              # filled after render()

    def defs(self) -> str:
        return ""

    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError


__all__ = ["BaseComponent", "xml_escape"]
