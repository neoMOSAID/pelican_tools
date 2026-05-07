
from __future__ import annotations
from .base import BaseComponent, xml_escape

# Example minimal SVG paths for some common icons
ICON_PATHS = {
    "github": "M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.387.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.757-1.333-1.757-1.09-.745.083-.73.083-.73 1.205.085 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.418-1.305.762-1.604-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z",
    "twitter": "M23.643 4.937c-.835.37-1.732.62-2.675.733.962-.576 1.7-1.49 2.048-2.578-.9.534-1.897.922-2.958 1.13-.85-.904-2.06-1.47-3.4-1.47-2.572 0-4.658 2.086-4.658 4.66 0 .364.042.718.12 1.06-3.873-.195-7.304-2.05-9.602-4.868-.4.69-.63 1.49-.63 2.342 0 1.616.823 3.043 2.072 3.878-.764-.025-1.482-.234-2.11-.583v.06c0 2.257 1.605 4.14 3.737 4.568-.392.106-.803.162-1.227.162-.3 0-.593-.028-.877-.082.593 1.85 2.313 3.198 4.352 3.234-1.595 1.25-3.604 1.995-5.786 1.995-.376 0-.747-.022-1.112-.065 2.062 1.323 4.51 2.093 7.14 2.093 8.57 0 13.255-7.098 13.255-13.254 0-.2-.005-.402-.014-.602.91-.658 1.7-1.477 2.323-2.41z",
    "youtube": "M23.5 6.19a3.02 3.02 0 00-2.12-2.14C19.48 3.5 12 3.5 12 3.5s-7.48 0-9.38.55A3.02 3.02 0 00.5 6.19 32.39 32.39 0 000 12a32.39 32.39 0 00.5 5.81 3.02 3.02 0 002.12 2.14c1.9.55 9.38.55 9.38.55s7.48 0 9.38-.55a3.02 3.02 0 002.12-2.14 32.39 32.39 0 00.5-5.81 32.39 32.39 0 00-.5-5.81zM9.54 15.57V8.43L15.82 12l-6.28 3.57z"
}

class Component(BaseComponent):
    component_id = "social_icons"

    def render(self) -> str:
        cfg = self.cfg.get("social_icons") or {}
        if isinstance(cfg, list):
            # config can be a list of icon names or dicts
            icons = cfg
        else:
            icons = cfg.get("icons", [])

        if not icons:
            return ""

        x_start = int(cfg.get("x", 85))
        y = int(cfg.get("y", 590))
        size = int(cfg.get("size", 24))
        gap = int(cfg.get("gap", 12))
        color = self.col.get("social_icon_color", "#94a3b8")
        opacity = float(cfg.get("opacity", 0.8))

        parts = []
        for i, icon_data in enumerate(icons):
            if isinstance(icon_data, str):
                name = icon_data.lower()
            elif isinstance(icon_data, dict):
                name = icon_data.get("name", "").lower()
            else:
                continue

            path_d = ICON_PATHS.get(name)
            if not path_d:
                continue

            cx = x_start + i * (size + gap)
            # center Y so icon sits nicely
            cy = y - size / 2
            parts.append(
                f'<svg x="{cx}" y="{cy}" width="{size}" height="{size}" viewBox="0 0 24 24" '
                f'fill="{color}" opacity="{opacity}">'
                f'<path d="{path_d}"/>'
                f'</svg>'
            )

        if not parts:
            return ""

        return "  <!-- Social icons -->\n  " + "\n  ".join(parts)
        