
# banner_generator/components/title.py

from __future__ import annotations
from .base import BaseComponent, xml_escape

def _wrap_text_semantic(text: str, max_width: int, font_size: int, char_factor: float) -> list[str]:
    """
    Wraps text at phrase boundaries (commas, conjunctions, prepositions) when possible.
    Falls back to simple word wrap.
    """
    if not text:
        return []
    
    # Approximate character limit per line
    max_chars = int(max_width / (font_size * char_factor))
    if max_chars < 10:
        max_chars = 10
    
    words = text.split()
    lines = []
    current_line = []
    
    # Preferred break points (lower index = higher priority)
    break_markers = [', ', ' and ', ' of ', ' for ', ' with ', ' on ', ' at ', ' by ', ' from ', ' to ']
    
    for word in words:
        # Test with current line + word
        test_line = ' '.join(current_line + [word])
        if len(test_line) <= max_chars:
            current_line.append(word)
            continue
        
        # We need to break. Try to find a good break point in the current line.
        if current_line:
            line_str = ' '.join(current_line)
            # Look for best break marker from right to left
            best_pos = -1
            best_marker = None
            for marker in break_markers:
                pos = line_str.rfind(marker)
                if pos > best_pos and pos > max_chars * 0.5:  # avoid breaking too early
                    best_pos = pos
                    best_marker = marker
            if best_pos > 0:
                # split at marker
                first_part = line_str[:best_pos + len(best_marker)].rstrip()
                second_part = line_str[best_pos + len(best_marker):].strip()
                lines.append(first_part)
                # continue with second_part + current word
                current_line = second_part.split() if second_part else []
                current_line.append(word)
            else:
                # simple break
                lines.append(line_str)
                current_line = [word]
        else:
            # single word too long - force break
            lines.append(word)
            current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

class Component(BaseComponent):
    component_id = "title"

    def render(self) -> str:
        title = self.cfg.get("title", "")
        subtitle = self.cfg.get("subtitle", "")
        line2 = self.cfg.get("title_line2", "")
        direction = self.cfg.get("direction", "ltr")   # read direction from config

        # Title layout
        title_font      = int(self.layout.get("title_font_size", 68))
        subtitle_font   = int(self.layout.get("subtitle_font_size", 38))
        title_x         = int(self.layout.get("title_x", 85))
        title_align     = str(self.layout.get("title_align", "start"))
        subtitle_align  = str(self.layout.get("subtitle_align", "start"))
        title_max_w     = int(self.layout.get("title_max_width", 560))
        subtitle_max_w  = int(self.layout.get("subtitle_max_width", 560))
        line_height     = int(self.layout.get("title_line_height", int(title_font * 1.2)))
        subtitle_line_h = int(self.layout.get("subtitle_line_height", int(subtitle_font * 1.3)))

        # Separate subtitle positioning (absolute, not relative)
        subtitle_x = self.layout.get("subtitle_x")
        if subtitle_x is None:
            subtitle_x = title_x
        else:
            subtitle_x = int(subtitle_x)

        subtitle_y_override = self.layout.get("subtitle_y")
        if subtitle_y_override is not None:
            subtitle_y_override = int(subtitle_y_override)

        margin_top = int(self.layout.get("title_margin_top", 30))

        # RTL mirroring: flip X coordinates
        if direction == "rtl":
            title_x = self.w - title_x
            if subtitle_x is not None:
                subtitle_x = self.w - subtitle_x
            # For RTL, "start" means right edge, so we may want to keep it as is
            # but we add direction attribute to text.
        else:
            # Keep original
            pass

        y = self.y_offset + margin_top
        out = []

        # Helper to build text element with direction
        def _text_element(x, y, font_size, fill, weight, anchor, content, extra_classes=""):
            direction_attr = f'direction="{direction}"' if direction == "rtl" else ""
            return f'<text x="{x}" y="{y}" font-family="\'Inter\', \'Helvetica Neue\', sans-serif" font-size="{font_size}" fill="{fill}" font-weight="{weight}" {direction_attr} text-anchor="{anchor}" {extra_classes}>{content}</text>'

        # Title lines (wrapped)
        lines = _wrap_text_semantic(title, max_width=title_max_w,
                          font_size=title_font, char_factor=0.55)
        for line in lines:
            # Glow layer
            out.append(
                _text_element(title_x, y, title_font, "url(#titleGrad)", "800", title_align,
                              xml_escape(line), 'opacity="0.3" filter="url(#titleGlow)"')
            )
            # Shadow layer
            out.append(
                _text_element(title_x, y, title_font, "url(#titleGrad)", "800", title_align,
                              xml_escape(line), 'filter="url(#titleShadow)"')
            )
            y += line_height

        # Underline
        underline_y = y - int(title_font * 0.45)
        out.append(
            f'<rect x="{title_x}" y="{underline_y}" width="360" height="3" rx="1.5" '
            f'fill="url(#titleGrad)" opacity="0.35" filter="url(#titleGlow)" />'
        )

        # Second title line (if any)
        if line2:
            y += 10
            out.append(
                _text_element(title_x, y, title_font, "url(#titleGrad)", "800", title_align,
                              xml_escape(str(line2)), 'filter="url(#titleShadow)" letter-spacing="-1.5"')
            )
            y += line_height

        # Subtitle lines – use absolute coordinates if subtitle_y is set
        subtitle_lines = _wrap_text_semantic(subtitle, max_width=subtitle_max_w,
                                    font_size=subtitle_font, char_factor=0.52)
        if subtitle_lines:
            if subtitle_y_override is not None:
                sub_y = subtitle_y_override
            else:
                sub_y = y + 20
            for line in subtitle_lines:
                out.append(
                    _text_element(subtitle_x, sub_y, subtitle_font, self.col.get("subtitle", "#a6adc8"),
                                  "600", subtitle_align, xml_escape(line))
                )
                sub_y += subtitle_line_h
            y = sub_y

        self.used_height = y - self.y_offset + 20
        return "  <!-- Title block -->\n  " + "\n  ".join(out)

        