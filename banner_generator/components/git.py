
# banner_generator/components/git.py
from __future__ import annotations
from .base import BaseComponent, xml_escape

class Component(BaseComponent):
    component_id = "git"

    def render(self) -> str:
        cfg = (self.cfg.get("git") or {}) if isinstance(self.cfg.get("git"), dict) else {}
        commits = cfg.get("commits", [
            "a1b2c3d Add theme support",
            "e4f5g6h Fix markdown rendering",
            "i7j8k9l Update README"
        ])
        x = int(cfg.get("x", 85))
        y = self.y_offset + int(cfg.get("y_offset", 20))
        max_lines = int(cfg.get("max_lines", 5))
        show_branch = cfg.get("show_branch", True)
        branch_name = cfg.get("branch_name", "main")
        font_size = int(cfg.get("font_size", 13))
        line_h = int(cfg.get("line_height", 22))

        hash_color = self.col.get("git_hash", "#f5c2e7")
        msg_color = self.col.get("git_msg", self.col.get("terminal_text", "#cdd6f4"))

        commits = commits[:max_lines]
        parts = []
        if show_branch:
            parts.append(
                f'<text x="{x}" y="{y}" font-family="\'JetBrains Mono\', monospace" font-size="{font_size}" '
                f'fill="{self.col.get("git_branch", "#50fa7b")}" font-weight="bold"> {xml_escape(branch_name)}</text>'
            )
            y += line_h
        for commit in commits:
            if len(commit) > 7 and commit[0] == commit[7] == ' ':
                # assume format "hash message"
                hsh, msg = commit.split(' ', 1)
                parts.append(
                    f'<text x="{x}" y="{y}" font-family="\'JetBrains Mono\', monospace" font-size="{font_size}">'
                    f'<tspan fill="{hash_color}">{xml_escape(hsh)}</tspan> '
                    f'<tspan fill="{msg_color}">{xml_escape(msg)}</tspan>'
                    f'</text>'
                )
            else:
                parts.append(
                    f'<text x="{x}" y="{y}" font-family="\'JetBrains Mono\', monospace" '
                    f'font-size="{font_size}" fill="{msg_color}">{xml_escape(commit)}</text>'
                )
            y += line_h

        self.used_height = y - self.y_offset + 10
        return "\n".join(parts)
        