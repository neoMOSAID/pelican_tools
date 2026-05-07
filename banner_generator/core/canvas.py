from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SvgDocument:
    width: int
    height: int
    defs: str
    body: str

    def to_svg(self) -> str:
        return "\n".join(
            [
                '<?xml version="1.0" encoding="UTF-8"?>',
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
                f'preserveAspectRatio="xMidYMid meet" width="{self.width}" height="{self.height}">',
                "  <defs>",
                self.defs.rstrip(),
                "  </defs>",
                self.body.rstrip(),
                "</svg>",
            ]
        )


def join_fragments(frags: Iterable[str]) -> str:
    return "\n".join([f for f in frags if f and f.strip()])
