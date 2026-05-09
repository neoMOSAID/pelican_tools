from __future__ import annotations
from ..base import BaseComponent, xml_escape
try:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name
    from pygments.token import Token
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'latex_source'
    description = 'LaTeX code block with syntax highlighting'
    component_id = 'latex_source'

    def _tokenize_fallback(self, line: str) -> list[tuple[str, str, bool]]:
        """Very simple LaTeX tokenizer (commands, comments, brackets)."""
        colors = self.col.get('pygments', {})
        cmd_color = colors.get('keyword', '#ff79c6')
        comment_color = colors.get('comment', '#6272a4')
        bracket_color = colors.get('operator', '#f1fa8c')
        default_color = colors.get('default', '#f8f8f2')
        tokens = []
        i = 0
        length = len(line)
        while i < length:
            if line[i] == '%':
                tokens.append((line[i:], comment_color, False))
                break
            elif line[i] == '\\':
                j = i + 1
                while j < length and line[j].isalpha():
                    j += 1
                cmd = line[i:j]
                tokens.append((cmd, cmd_color, True))
                i = j
                continue
            elif line[i] in '{[]}':
                tokens.append((line[i], bracket_color, False))
                i += 1
                continue
            else:
                j = i
                while j < length and line[j] not in '\\%{}[]':
                    j += 1
                if j > i:
                    tokens.append((line[i:j], default_color, False))
                i = j
        return tokens

    def _tokenize_pygments(self, line: str) -> list[tuple[str, str, bool]]:
        try:
            lexer = get_lexer_by_name('latex', stripall=False)
        except Exception:
            return self._tokenize_fallback(line)
        tokens = []
        pyg_colors = self.col.get('pygments', {})
        type_map = {Token.Keyword: 'keyword', Token.Name.Builtin: 'keyword', Token.Name.Function: 'function', Token.Comment: 'comment', Token.String: 'string', Token.Number: 'number', Token.Operator: 'operator'}
        default = pyg_colors.get('default', '#f8f8f2')
        for ttype, value in lex(line, lexer):
            if not value.strip():
                continue
            color_key = None
            for tok_class, key in type_map.items():
                if ttype in tok_class:
                    color_key = key
                    break
            color = pyg_colors.get(color_key, default) if color_key else default
            bold = ttype in Token.Keyword
            tokens.append((value, color, bold))
        return tokens

    def render(self) -> str:
        cfg = self.cfg.get('latex_source') or {} if isinstance(self.cfg.get('latex_source'), dict) else {}
        code = cfg.get('code', ['\\documentclass{article}', '\\begin{document}', 'Hello world', '\\end{document}'])
        title = cfg.get('title', 'LaTeX source')
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        font_size = int(cfg.get('font_size', 13))
        line_h = int(cfg.get('line_height', 20))
        show_line_numbers = cfg.get('line_numbers', True)
        bg = self.col.get('code_bg', '#1e1e2e')
        border = self.col.get('code_border', '#313244')
        title_bg = self.col.get('code_title_bg', '#44475a')
        title_fg = self.col.get('code_title_fg', '#cdd6f4')
        line_no_color = self.col.get('code_line_no', '#6272a4')
        tokenizer = self._tokenize_pygments if PYGMENTS_AVAILABLE else self._tokenize_fallback
        max_line_len = max((len(l) for l in code)) if code else 0
        block_w = max_line_len * font_size * 0.6 + 80
        block_h = len(code) * line_h + (40 if title else 20)
        parts = []
        parts.append(f'<rect x="{x}" y="{y}" width="{block_w}" height="{block_h}" rx="6" fill="{bg}" stroke="{border}" stroke-width="1.5" />')
        if title:
            parts.append(f'<rect x="{x}" y="{y}" width="{block_w}" height="28" rx="6" fill="{title_bg}" />')
            parts.append(f'''<text x="{x + 12}" y="{y + 20}" font-family="'JetBrains Mono', monospace" font-size="12" fill="{title_fg}">{xml_escape(title)}</text>''')
            code_y = y + 38
        else:
            code_y = y + 12
        for i, line in enumerate(code):
            line_y = code_y + i * line_h
            if show_line_numbers:
                parts.append(f'''<text x="{x + 8}" y="{line_y + line_h - 4}" font-family="'JetBrains Mono', monospace" font-size="{font_size - 1}" fill="{line_no_color}" text-anchor="end">{i + 1}</text>''')
            tokens = tokenizer(line)
            text_x = x + (40 if show_line_numbers else 12)
            parts.append(f'''<text x="{text_x}" y="{line_y + line_h - 4}" font-family="'JetBrains Mono', monospace" font-size="{font_size}">''')
            for token, color, bold in tokens:
                weight = 'font-weight="bold"' if bold else ''
                parts.append(f'<tspan fill="{color}" {weight}>{xml_escape(token)}</tspan>')
            parts.append('</text>')
        self.used_height = block_h + 15
        return '\n'.join(parts)