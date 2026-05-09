
from __future__ import annotations

import re

from ..base import BaseComponent, xml_escape


class Component(BaseComponent):
    component_id = "terminal"
    z_index = 200
    section_name = "terminal"
    description = "Terminal window with command lines and syntax highlighting"
    config_schema = {
        "commands": {"type": "list", "default": [], "help": "List of shell commands to display"},
        "x": {"type": "int", "default": 700, "help": "X position of the terminal window"},
        "y": {"type": "int", "default": 80, "help": "Y position"},
        "width": {"type": "int", "default": 440, "help": "Window width in pixels"},
        "show_serving": {"type": "bool", "default": True, "help": "Show 'Serving at ...' line"},
        "typing": {"type": "bool", "default": True, "help": "Enable animated typing effect"},
        "line_height": {"type": "int", "default": 22, "help": "Line height in pixels"},
        "cmd_gap": {"type": "int", "default": 6, "help": "Extra gap between commands"},
        "dynamic_from_article": {"type": "bool", "default": False, "help": "Extract commands from article body (banner_meta.toml: terminal_commands)"},
        "x_offset": {"type": "int", "default": 0, "help": "Additional X offset"},
        "y_offset": {"type": "int", "default": 0, "help": "Additional Y offset"},
    }
    
    def _get_dynamic_commands(self, article: dict) -> list | None:
        """
        Get terminal commands from the sidecar (primary) or article body.
        Returns a list of strings or None if nothing found.
        """
        # 1. Explicit sidecar key (banner_meta.toml content merged into ctx.article)
        if "terminal_commands" in article and article["terminal_commands"]:
            return article["terminal_commands"]

        # 2. Fallback: extract from article body
        body = article.get("content", "")
        if not body:
            return None

        cmd_lines = re.findall(r'^\s*[\$\>]\s*(.+)$', body, re.MULTILINE)
        cmd_lines += re.findall(r'^\s*[a-zA-Z0-9_\-@:~/.]+\$ (.+)$', body, re.MULTILINE)
        if cmd_lines:
            clean = [line.strip() for line in cmd_lines if line.strip()]
            return clean[:5]   # limit to 5 commands
        return None

    def _syntax_highlight(self, cmd: str):
        c = self.col
        tokens = []
        pattern = re.compile(
            r'(?P<flag>--?\w+(?:=[^\s]+)?)|'
            r'(?P<path>[~/.]\S*|https?://\S+)|'
            r'(?P<quote>"[^"]*"|\'[^\']*\')|'
            r'(?P<word>[^\s]+)'
        )
        for m in pattern.finditer(cmd):
            if m.group('flag'):
                tokens.append((m.group('flag'), c.get('syn_flag', '#94e2d5'), False))
            elif m.group('path'):
                tokens.append((m.group('path'), c.get('syn_path', '#f5c2e7'), False))
            elif m.group('quote'):
                tokens.append((m.group('quote'), c.get('syn_cmd', '#a6e3a1'), False))
            elif m.group('word'):
                word = m.group('word')
                if word.lower() in {'pip','python','pelican','mkdocs','npm','git','sudo','apt','docker','poetry'}:
                    tokens.append((word, c.get('syn_cmd', '#a6e3a1'), True))
                elif word in {'install','update','build','serve','dev'}:
                    tokens.append((word, c.get('syn_pkg', '#fab387'), False))
                else:
                    tokens.append((word, c.get('terminal_text', '#a6adc8'), False))
        return tokens

    def _render_typing(self, line: str, y: int, x: int) -> str:
        c = self.col
        parts = []
        parts.append(f'<tspan font-weight="bold" fill="{c.get("terminal_prompt_accent", "#94e2d5")}">$</tspan>')
        parts.append(f'<tspan fill="{c.get("terminal_prompt", "#cdd6f4")}"> </tspan>')

        tokens = self._syntax_highlight(line)
        idx = 0
        for text, color, bold in tokens:
            font_weight = 'font-weight="bold"' if bold else ''
            for ch in text:
                delay = idx * 0.08
                idx += 1
                parts.append(
                    f'<tspan fill="{color}" {font_weight} opacity="0">{xml_escape(ch)}'
                    f'<set attributeName="opacity" to="1" begin="{delay}s" />'
                    f'</tspan>'
                )
            parts.append('<tspan> </tspan>')
            idx += 1

        cursor_delay = max(0.1, idx * 0.08)
        parts.append(
            f'<tspan fill="{c.get("terminal_cursor", "#f6a2d2")}" font-weight="bold" opacity="0">'
            f'█<set attributeName="opacity" to="1" begin="{cursor_delay}s" />'
            f'<animate attributeName="opacity" values="1;0;1" dur="0.8s" begin="{cursor_delay}s" repeatCount="indefinite" />'
            f'</tspan>'
        )

        return (
            f'<text x="{x}" y="{y}" font-family="\'JetBrains Mono\', \'SF Mono\', \'Fira Code\', monospace" '
            f'font-size="18" fill="{c.get("terminal_text", "#a6adc8")}">{"".join(parts).rstrip()}</text>'
        )

    def _render_line(self, line: str, y: int, x: int, is_active: bool, typing: bool, static: bool) -> str:
        if static:
            return (
                f'<text x="{x}" y="{y}" font-family="\'JetBrains Mono\', \'SF Mono\', \'Fira Code\', monospace" '
                f'font-size="18" fill="{self.col.get("terminal_text", "#a6adc8")}">'
                f'{xml_escape("$ " + line)}'
                f'</text>'
            )
        if typing and is_active:
            return self._render_typing(line, y, x)

        c = self.col
        prompt_colour = c.get('terminal_prompt_accent', '#94e2d5') if is_active else c.get('terminal_prompt', '#cdd6f4')
        parts = [f'<tspan font-weight="bold" fill="{prompt_colour}">$</tspan> ']
        for text, color, bold in self._syntax_highlight(line):
            font_weight = 'font-weight="bold"' if bold else ''
            parts.append(f'<tspan fill="{color}" {font_weight}>{xml_escape(text)}</tspan> ')
        if is_active:
            parts.append(
                f'<tspan fill="{c.get("terminal_cursor", "#f6a2d2")}" font-weight="bold">'
                '<animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite" />'
                '█</tspan>'
            )
        colour = c.get('terminal_text', '#a6adc8') if not is_active else c.get('terminal_text_active', '#cdd6f4')
        return (
            f'<text x="{x}" y="{y}" font-family="\'JetBrains Mono\', \'SF Mono\', \'Fira Code\', monospace" '
            f'font-size="18" fill="{colour}">{"".join(parts).rstrip()}</text>'
        )

    # ------------------------------------------------------------------
    # NEW: text wrapping helper
    # ------------------------------------------------------------------
    def _wrap_text(self, text: str, max_width: int, font_size: int) -> list:
        """Break a terminal command into multiple lines to fit max_width pixels."""
        char_width = font_size * 0.6         # monospace approximation
        max_chars = max(1, int(max_width / char_width))
        words = text.split(' ')
        lines = []
        current_line = []
        current_len = 0

        for word in words:
            word_len = len(word)
            # If the word itself is longer than a line, split it forcefully
            if word_len > max_chars:
                # Flush any accumulated line first
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                    current_len = 0
                # Split the long word
                for i in range(0, word_len, max_chars):
                    lines.append(word[i:i+max_chars])
                continue

            # Normal case: try to fit word onto the current line
            if current_len == 0:
                # First word on line
                current_line.append(word)
                current_len = word_len
            else:
                if current_len + 1 + word_len <= max_chars:
                    current_line.append(word)
                    current_len += 1 + word_len
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_len = word_len

        if current_line:
            lines.append(' '.join(current_line))
        return lines if lines else ['']

    # ------------------------------------------------------------------
    # REWRITTEN render method with wrapping & dynamic height
    # ------------------------------------------------------------------

    def _render_command_line(
        self,
        text: str,
        x: int,
        y: int,
        is_prompt: bool,
        show_cursor: bool,
        font_size: int,
        static: bool,
        typing: bool,
    ) -> str:
        """Render one terminal line, optionally with prompt, syntax highlighting and cursor."""
        c = self.col
        prompt_color = c.get("terminal_prompt_accent", "#94e2d5")
        default_fg = c.get("terminal_text", "#a6adc8")
        active_fg = c.get("terminal_text_active", "#cdd6f4")
        cursor_color = c.get("terminal_cursor", "#f6a2d2")

        # Tokens for syntax highlighting
        tokens = self._syntax_highlight(text) if text else []

        # Build tspan elements for the command text
        tspan_parts = []
        for word, color, bold in tokens:
            weight = 'font-weight="bold"' if bold else ''
            tspan_parts.append(f'<tspan fill="{color}" {weight}>{xml_escape(word)}</tspan>')

        line_color = active_fg if show_cursor else default_fg   # active commands slightly brighter

        # Determine content: optional "$ " prompt
        if is_prompt:
            prompt_tspan = f'<tspan font-weight="bold" fill="{prompt_color}">$</tspan> '
            line_content = f"{prompt_tspan}{' '.join(tspan_parts)}"   # spaces between tokens
        else:
            line_content = ' '.join(tspan_parts)

        # Cursor (blinking block) if requested
        cursor_span = ""
        if show_cursor:
            cursor_span = (
                f' <tspan fill="{cursor_color}" font-weight="bold">'
                '<animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite" />'
                '█</tspan>'
            )

        return (
            f'<text x="{x}" y="{y}" font-family="\'JetBrains Mono\', \'SF Mono\', \'Fira Code\', monospace" '
            f'font-size="{font_size}" fill="{line_color}" xml:space="preserve">'
            f'{line_content}{cursor_span}</text>'
        )

    def render(self) -> str:
        term_cfg = (self.cfg.get("terminal") or {}) if isinstance(self.cfg.get("terminal"), dict) else {}

        # Dynamic command extraction
        dynamic = term_cfg.get("dynamic_from_article", False)
        if dynamic and hasattr(self.ctx, 'article') and self.ctx.article:
            dynamic_cmds = self._get_dynamic_commands(self.ctx.article)
            if dynamic_cmds:
                term_cfg["commands"] = dynamic_cmds

        cmds = term_cfg.get("commands")
        if cmds is None:
            cmds = self.cfg.get("terminal_commands")
        cmds = cmds or []

        if not cmds:
            return ""

        # Layout
        base_x = int(term_cfg.get("x", 700)) + int(term_cfg.get("x_offset", 0))
        base_y = int(term_cfg.get("y", 80)) + int(term_cfg.get("y_offset", 0))
        static = str(self.cfg.get("render_mode", "")) == "static"
        typing_enabled = bool(term_cfg.get("typing", True)) and not static
        show_serving = bool(term_cfg.get("show_serving", True))

        win_width = int(term_cfg.get("width", 440))   # ← new: configurable width

        title_bar_h = 32
        content_pad_top = 20
        content_left = 35            # distance from left window edge to text
        content_right_pad = 20
        scrollbar_width = 6
        scrollbar_right_margin = 10

        font_size = 18
        line_h = int(term_cfg.get("line_height", 22))
        cmd_gap = int(term_cfg.get("cmd_gap", 6))

        # Width available for command text
        cmd_max_width = win_width - content_left - content_right_pad

        # Prompt " $ " width (for continuation indentation)
        prompt_pixels = int(font_size * 1.2)   # roughly width of "$ "

        # --- First pass: wrap all commands and collect layout data ---
        wrapped_cmds = []          # list of lists of wrapped lines per command
        total_cmd_lines = 0
        for cmd in cmds:
            wrapped = self._wrap_text(cmd, cmd_max_width, font_size)
            wrapped_cmds.append(wrapped)
            total_cmd_lines += len(wrapped)

        # Build a flat list of line descriptors
        line_items = []
        current_y = base_y + title_bar_h + content_pad_top
        line_no = 0

        for idx, (original_cmd, wrapped_lines) in enumerate(zip(cmds, wrapped_cmds)):
            is_active = (idx == len(cmds) - 1)
            is_long = len(wrapped_lines) > 1

            for line_i, line_text in enumerate(wrapped_lines):
                is_prompt = (line_i == 0)
                x_text = base_x + content_left
                if not is_prompt:
                    x_text += prompt_pixels

                show_cursor = is_active and (line_i == len(wrapped_lines) - 1) and not (typing_enabled and not is_long)

                ln = None
                if is_prompt:
                    line_no += 1
                    ln = line_no

                line_items.append((line_text, current_y, x_text, is_prompt, ln, is_active, show_cursor, typing_enabled and is_active and not is_long and line_i==0))
                current_y += line_h
            current_y += cmd_gap

        # Serving line
        serving_y = current_y + 5
        if show_serving:
            current_y = serving_y + 30 + 8
        else:
            current_y += 10

        # Total window height
        box_h = current_y - base_y + 10

        # Scrollbar
        scrollbar_x = base_x + win_width - scrollbar_width - scrollbar_right_margin
        scrollbar_y = base_y + title_bar_h + 4
        scrollbar_h = box_h - title_bar_h - 8
        thumb_h = max(30, scrollbar_h * min(1.0, len(cmds) / total_cmd_lines)) if total_cmd_lines else 60
        scrollbar = (
            f'<rect x="{scrollbar_x}" y="{scrollbar_y}" width="{scrollbar_width}" height="{scrollbar_h}" rx="3" fill="#45475a" opacity="0.3" />'
            f'<rect x="{scrollbar_x + 1}" y="{scrollbar_y + 5}" width="{scrollbar_width - 2}" height="{thumb_h}" rx="2" fill="#6c7086" opacity="0.5" />'
        )

        # Vertical divider
        divider_x = base_x + 20
        divider_y1 = base_y + title_bar_h + 10
        divider_y2 = current_y - 20

        # Render lines
        rendered_lines = []
        for (text, y, x_text, is_prompt, ln, is_active, show_cursor, use_typing) in line_items:
            if ln is not None:
                rendered_lines.append(
                    f'<text x="{divider_x - 2}" y="{y}" font-family="\'JetBrains Mono\', monospace" font-size="14" '
                    f'fill="{self.col.get("terminal_text_faded", "#585b70")}" opacity="0.6" text-anchor="end">{ln}</text>'
                )
            if use_typing:
                rendered_lines.append(self._render_typing(text, y, x_text))
            else:
                rendered_lines.append(
                    self._render_command_line(
                        text, x_text, y, is_prompt, show_cursor,
                        font_size, static, False
                    )
                )

        # Serving line
        serving_line = ""
        if show_serving:
            serving_line = (
                f'<text x="{base_x + content_left}" y="{serving_y}" font-family="\'JetBrains Mono\', \'SF Mono\', monospace" font-size="16" '
                f'fill="{self.col.get("terminal_serving", "#94a3b8")}" opacity="0.9">'
                f'➜ Serving at http://localhost:8000'
                f'<tspan fill="{self.col.get("terminal_cursor", "#f6a2d2")}" font-weight="bold">'
                '<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" />█</tspan>'
                f'</text>'
            )

        return f"""
    <!-- Terminal window -->
    <g filter="url(#termGlow)">
        <rect x="{base_x}" y="{base_y}" width="{win_width}" height="{box_h}" rx="12" fill="{self.col.get('terminal_bg', '#1e1e2e')}" fill-opacity="0.92" stroke="{self.col.get('terminal_stroke', '#313244')}" stroke-width="2" />
        <rect x="{base_x}" y="{base_y}" width="{win_width}" height="{title_bar_h}" rx="12" fill="{self.col.get('terminal_titlebar', '#45475a')}" />
        <rect x="{base_x}" y="{base_y + 12}" width="{win_width}" height="20" fill="{self.col.get('terminal_titlebar', '#45475a')}" />
        <circle cx="{base_x + 18}" cy="{base_y + 16}" r="6" fill="{self.col.get('btn_red', '#f38ba8')}" />
        <circle cx="{base_x + 38}" cy="{base_y + 16}" r="6" fill="{self.col.get('btn_yellow', '#fab387')}" />
        <circle cx="{base_x + 58}" cy="{base_y + 16}" r="6" fill="{self.col.get('btn_green', '#a6e3a1')}" />
        <text x="{base_x + win_width // 2}" y="{base_y + 20}" font-family="'Inter', 'Helvetica Neue', sans-serif" font-size="12" fill="{self.col.get('terminal_text', '#a6adc8')}" text-anchor="middle" font-weight="500">Terminal — mosaid@mosaid-pc pelican-dev</text>

        <line x1="{divider_x}" y1="{divider_y1}" x2="{divider_x}" y2="{divider_y2}" stroke="#45475a" stroke-width="1" opacity="0.3" />

        {"".join(rendered_lines)}
        {serving_line}
        {scrollbar}
    </g>
    """.rstrip()
    