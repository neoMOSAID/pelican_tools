from __future__ import annotations
import re
from ..base import BaseComponent, xml_escape
try:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name
    from pygments.token import Token
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

class Component(BaseComponent):
    config_schema = {'code': {'type': 'list', 'default': ["print('Hello World')"], 'help': 'Code lines'}, 'language': {'type': 'str', 'default': 'python', 'help': 'Language for highlighting'}, 'title': {'type': 'str', 'default': '', 'help': 'Optional title bar text'}, 'line_numbers': {'type': 'bool', 'default': True, 'help': 'Show line numbers'}, 'dynamic_from_article': {'type': 'bool', 'default': False, 'help': 'Extract from article body'}}
    z_index = 100
    section_name = 'code_snippet'
    description = 'Syntax‑highlighted code block (Python, etc.)'
    component_id = 'code_snippet'
    DEFAULT_PYGMENTS_COLORS = {'keyword': '#ff79c6', 'function': '#50fa7b', 'class': '#8be9fd', 'variable': '#f8f8f2', 'string': '#f1fa8c', 'docstring': '#f1fa8c', 'comment': '#6272a4', 'number': '#bd93f9', 'operator': '#ff79c6', 'default': '#f8f8f2'}

    def _get_dynamic_code(self, article: dict) -> list | None:
        """
        Get code lines from the sidecar (primary) or from the article body.
        Returns a list of strings or None.
        """
        if 'featured_code' in article and article['featured_code']:
            return article['featured_code']
        body = article.get('content', '')
        if not body:
            return None
        match = re.search('```python\\n(.*?)```', body, re.DOTALL)
        if match:
            lines = match.group(1).splitlines()
            return lines[:10]
        match = re.search('```\\w*\\n(.*?)```', body, re.DOTALL)
        if match:
            lines = match.group(1).splitlines()
            return lines[:10]
        return None

    def _tokenize_fallback(self, line: str, lang: str) -> list[tuple[str, str, bool]]:
        colors = self.col.get('pygments', {})
        keyword_color = colors.get('keyword', '#ff79c6')
        string_color = colors.get('string', '#f1fa8c')
        comment_color = colors.get('comment', '#6272a4')
        number_color = colors.get('number', '#bd93f9')
        default_color = colors.get('default', '#f8f8f2')
        indent = line[:len(line) - len(line.lstrip())]
        tokens = []
        if indent:
            tokens.append((indent, default_color, False))
        rest = line.lstrip()
        if not rest:
            return tokens
        keywords = {'def', 'class', 'return', 'if', 'else', 'elif', 'for', 'while', 'import', 'from', 'try', 'except', 'finally', 'with', 'as', 'yield', 'lambda', 'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None', 'pass', 'break', 'continue', 'global', 'nonlocal', 'raise', 'assert', 'del'}
        pattern = re.compile('(?:[fFrRbB]?\\"(?:\\\\.|[^\\"])*\\")|(?:[fFrRbB]?\\\'(?:\\\\.|[^\\\'])*\\\')|#.*$|\\b\\d+\\b|[^\\s]+')
        for match in pattern.finditer(rest):
            token = match.group(0)
            if token.startswith('#'):
                tokens.append((token, comment_color, False))
            elif token.startswith(('"', "'")) or (len(token) > 1 and token[1] in ('"', "'") and (token[0].lower() in 'frb')):
                tokens.append((token, string_color, False))
            elif token.isdigit():
                tokens.append((token, number_color, False))
            elif token in keywords:
                tokens.append((token, keyword_color, True))
            else:
                tokens.append((token, default_color, False))
        return tokens

    def _tokenize_pygments(self, line: str, lang: str) -> list[tuple[str, str, bool]]:
        """Use Pygments to tokenize a line — preserves leading whitespace."""
        indent = line[:len(line) - len(line.lstrip())]
        tokens = []
        pyg_colors = self.col.get('pygments', {})
        default_color = pyg_colors.get('default', '#f8f8f2')
        if indent:
            tokens.append((indent, default_color, False))
        rest = line.lstrip()
        if not rest:
            return tokens
        try:
            lexer = get_lexer_by_name(lang, stripall=False)
        except Exception:
            fallback_tokens = self._tokenize_fallback(rest, lang)
            tokens.extend(fallback_tokens)
            return tokens
        type_map = {Token.Keyword: 'keyword', Token.Keyword.Constant: 'keyword', Token.Keyword.Declaration: 'keyword', Token.Keyword.Namespace: 'keyword', Token.Keyword.Reserved: 'keyword', Token.Keyword.Type: 'keyword', Token.Name.Function: 'function', Token.Name.Class: 'class', Token.Name.Variable: 'variable', Token.String: 'string', Token.String.Doc: 'docstring', Token.Comment: 'comment', Token.Comment.Single: 'comment', Token.Comment.Multiline: 'comment', Token.Number: 'number', Token.Number.Integer: 'number', Token.Number.Float: 'number', Token.Operator: 'operator', Token.Operator.Word: 'keyword'}
        for ttype, value in lex(rest, lexer):
            if not value:
                continue
            color_key = None
            for token_class, key in type_map.items():
                if ttype in token_class:
                    color_key = key
                    break
            color = pyg_colors.get(color_key) or self.DEFAULT_PYGMENTS_COLORS.get(color_key) or default_color if color_key else default_color
            bold = ttype in Token.Keyword or ttype in Token.Name.Function
            tokens.append((value, color, bold))
        if lang == 'python':
            merged = []
            i = 0
            while i < len(tokens):
                val, col, bold = tokens[i]
                if val == '*' and i + 1 < len(tokens) and (tokens[i + 1][0] == '*'):
                    merged.append(('**', col, bold))
                    i += 2
                elif val in ('f', 'r', 'u', 'b', 'fr', 'rf', 'br', 'rb') and i + 1 < len(tokens):
                    next_val, next_col, next_bold = tokens[i + 1]
                    if next_val and next_val[0] in ('"', "'"):
                        merged.append((val + next_val, col, bold))
                        i += 2
                    else:
                        merged.append((val, col, bold))
                        i += 1
                else:
                    merged.append((val, col, bold))
                    i += 1
            return merged
        return tokens

    def render(self) -> str:
        cfg = self.cfg.get('code_snippet') or {} if isinstance(self.cfg.get('code_snippet'), dict) else {}
        dynamic = cfg.get('dynamic_from_article', False)
        if dynamic and hasattr(self.ctx, 'article') and self.ctx.article:
            dynamic_code = self._get_dynamic_code(self.ctx.article)
            if dynamic_code:
                cfg['code'] = dynamic_code
        code = cfg.get('code', ["print('Hello World')"])
        language = cfg.get('language', 'python')
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        font_size = int(cfg.get('font_size', 13))
        line_h = int(cfg.get('line_height', 20))
        title = cfg.get('title', '')
        show_line_numbers = cfg.get('line_numbers', True)
        bg = self.col.get('code_bg') or self.col.get('terminal_bg', '#1e1e2e')
        border = self.col.get('code_border', '#313244')
        title_bg = self.col.get('code_title_bg', '#44475a')
        title_fg = self.col.get('code_title_fg', '#cdd6f4')
        line_no_color = self.col.get('code_line_no', '#6272a4')
        tokenizer = self._tokenize_pygments if PYGMENTS_AVAILABLE else self._tokenize_fallback
        user_width = cfg.get('width')
        if user_width:
            block_w = int(user_width)
        else:
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
                parts.append(f'''<text x="{x + 20}" y="{line_y + line_h - 4}" font-family="'JetBrains Mono', monospace" font-size="{font_size - 1}" fill="{line_no_color}" text-anchor="end">{i + 1}</text>''')
            tokens = tokenizer(line, language)
            text_x = x + (40 if show_line_numbers else 12)
            parts.append(f'''<text x="{text_x}" y="{line_y + line_h - 4}" font-family="'JetBrains Mono', monospace" font-size="{font_size}" xml:space="preserve">''')
            for token, color, bold in tokens:
                weight = 'font-weight="bold"' if bold else ''
                parts.append(f'<tspan fill="{color}" {weight}>{xml_escape(token)}</tspan>')
            parts.append('</text>')
        self.used_height = block_h + 15
        return '\n'.join(parts)