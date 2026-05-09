
from __future__ import annotations
import re
from pathlib import Path
from ..base import BaseComponent

# Hard‑coded fallback (used if icon file not found)
NAMED_ICONS = {
    "vim": "M12 2L4 20h3l1.5-4h7l1.5 4h3L12 2zm-1.2 8.5h-1.6L12 5.7l2.8 4.8h-1.6l-1.2-2-1.2 2z",
    "tux": "M12 3c-2.5 0-4.8 1.2-6.3 3.1-.8 1-1.2 2.2-1.2 3.5 0 1.5.7 2.8 1.8 3.7 1.2.9 2.8 1.2 4.5.9.5-.1 1-.3 1.5-.5.2-.1.3-.2.5-.2.2 0 .4.1.7.2 1.1.5 2.4.8 3.7.6 2-.2 3.5-1.3 4.3-2.9.2-.4.3-.8.3-1.2 0-.5-.2-1-.5-1.4-.3-.4-.7-.7-1.2-.9.4-.3.8-.7 1-1.2.2-.5.2-1.1 0-1.7-.3-.7-1-1.3-1.8-1.5-.3-.1-.7-.1-1 .1-.3.1-.6.3-.8.5-.2.3-.4.7-.4 1.1 0 .3.1.6.2.9.1.2.3.3.5.3.2 0 .4 0 .6-.1.1-.1.3-.2.3-.3.1-.2 0-.4-.1-.5-.1-.2-.2-.3-.4-.4-.3-.2-.6-.2-1 0-.3.2-.4.5-.3.8 0 .1.1.2.2.3.1.1.3.1.5.1h.2c-.3.7-1 1.2-1.8 1.3-1.1.2-2.1-.3-2.8-1.1-.3-.3-.5-.7-.5-1.2 0-.7.3-1.3.9-1.6.3-.2.7-.3 1.1-.3.5 0 1 .2 1.3.6.2.2.3.4.4.7-.1.1-.2.2-.4.3-.2.1-.4.1-.6 0-.2 0-.3-.1-.4-.3-.1-.1-.2-.3-.1-.5.1-.1.3-.2.5-.2.3 0 .5.2.6.5.1.3 0 .6-.2.8-.3.3-.8.5-1.3.4-.5 0-1-.3-1.3-.7-.3-.4-.4-.9-.3-1.4.1-.5.4-.9.8-1.1.5-.2 1-.3 1.6-.1.2.1.5.2.6.4.2.2.3.4.3.7 0 .4-.2.8-.5 1.1-.3.3-.8.4-1.3.4-.6 0-1.2-.2-1.6-.7-.3-.3-.4-.7-.5-1.1 0-.4.1-.8.4-1.1.2-.3.6-.4.9-.5.6-.1 1.2 0 1.7.3.4.3.7.7.8 1.2z",
    "arch": "M12 2c-.5 0-1 .2-1.4.6L6.3 7c-.8.8-1.2 1.8-1.2 2.9 0 2.2 1.7 3.9 3.9 3.9 1 0 1.9-.4 2.6-1l.4-.4.4.4c.7.7 1.6 1 2.6 1 2.2 0 3.9-1.7 3.9-3.9 0-1.1-.4-2.1-1.2-2.9L13.4 2.6c-.4-.4-.9-.6-1.4-.6z",
    "ubuntu": "M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm0 2.5c1.4 0 2.5 1.1 2.5 2.5S13.4 9.5 12 9.5 9.5 8.4 9.5 7s1.1-2.5 2.5-2.5zM7.5 10.3c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 0c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zM12 14c1.4 0 2.5 1.1 2.5 2.5S13.4 19 12 19s-2.5-1.1-2.5-2.5S10.6 14 12 14z",
}


class Component(BaseComponent):
    component_id = "icon"
    z_index = 120
    section_name = "icon"
    description = "Decorative icon (Pelican, Tux, Vim, Arch, Ubuntu, or custom SVG)"
    config_schema = {
        "type": {"type": "str", "default": "pelican", "help": "Icon type: pelican, tux, vim, arch, ubuntu, custom"},
        "x": {"type": "int", "default": 95, "help": "X position"},
        "y": {"type": "int", "default": 465, "help": "Y position"},
        "scale": {"type": "float", "default": 0.9, "help": "Scale factor"},
        "path_d": {"type": "str", "default": "", "help": "Custom SVG path data (if type = custom)"},
    }
    
    # Path to the icons directory (relative to this file’s location)
    ICONS_DIR = Path(__file__).resolve().parent.parent / "icons"

    def _load_icon_paths(self, name: str) -> list[str]:
        """Return a list of path 'd' strings from an SVG file, or empty if not found."""
        svg_file = self.ICONS_DIR / f"{name}.svg"
        if not svg_file.exists():
            return []      # fallback to NAMED_ICONS later

        content = svg_file.read_text(encoding="utf-8")
        # Extract all d="..." attributes from <path ...> elements
        return re.findall(r'<path[^>]*\sd\s*=\s*"([^"]*)"', content)

    def render(self) -> str:
        icon_cfg = (self.cfg.get("icon") or {}) if isinstance(self.cfg.get("icon"), dict) else {}
        icon_type = (icon_cfg.get("type") or "pelican").strip().lower()
        if icon_type == "none":
            return ""

        # Position & scale
        icon_x = int(icon_cfg.get("x", 95))
        icon_y = int(icon_cfg.get("y", 465))
        scale   = float(icon_cfg.get("scale", 0.9)) if icon_type == "pelican" else float(icon_cfg.get("scale", 1.5))

        # ------------------------------------------------------------------
        # Pelican special case (keeps its animated eye)
        if icon_type == "pelican":
            return f"""
  <!-- Pelican icon -->
  <g transform="translate({icon_x}, {icon_y}) scale(0.9)" fill="none" stroke="{self.col.get('pelican_stroke', '#94a3b8')}" stroke-width="3" opacity="0.6">
    <path d="M0 40 Q 20 20 40 30 Q 60 10 80 40 Q 60 60 40 60 Q 20 60 0 40 Z" />
    <circle id="pelicanEye" cx="28" cy="38" r="6" fill="{self.col.get('pelican_eye', '#94a3b8')}" />
    <path d="M70 25 L 90 15 L 85 35 Z" stroke-width="2.5">
      <animateTransform attributeName="transform" type="rotate" values="0 70 25; 4 70 25; 0 70 25" dur="5s" repeatCount="indefinite" />
    </path>
  </g>
""".rstrip()

        # ------------------------------------------------------------------
        # Custom inline path
        if icon_type == "custom" and icon_cfg.get("path_d"):
            d = icon_cfg["path_d"]
            return f"""
  <!-- Custom icon -->
  <g transform="translate({icon_x}, {icon_y}) scale({scale})" fill="none" stroke="{self.col.get('pelican_stroke', '#94a3b8')}" stroke-width="3" opacity="0.6">
    <path d="{d}" />
  </g>
""".rstrip()

        # ------------------------------------------------------------------
        # Try to load from icons/ directory
        paths = self._load_icon_paths(icon_type)
        if paths:
            # For file‑based icons, we fill with the theme's stroke colour
            # (change to 'fill' if you prefer filled icons)
            fill_color = self.col.get('pelican_stroke', '#94a3b8')
            paths_svg = "\n".join(f'    <path d="{p}" />' for p in paths)
            return f"""
  <!-- {icon_type} icon (from file) -->
  <g transform="translate({icon_x}, {icon_y}) scale({scale})" fill="{fill_color}" opacity="0.6">
{paths_svg}
  </g>
""".rstrip()

        # ------------------------------------------------------------------
        # Fallback to hardcoded dictionary
        if icon_type in NAMED_ICONS:
            d = NAMED_ICONS[icon_type]
            return f"""
  <!-- {icon_type} icon (fallback) -->
  <g transform="translate({icon_x}, {icon_y}) scale({scale})" fill="{self.col.get('pelican_stroke', '#94a3b8')}" opacity="0.6">
    <path d="{d}" />
  </g>
""".rstrip()

        # Unknown
        return ""

        