
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class Theme:
    name: str
    colors: dict
    layout: dict


def load_theme(theme_name: str, themes_dir: Path) -> Theme:
    path = themes_dir / f"{theme_name}.toml"       # now .toml
    if not path.exists():
        raise FileNotFoundError(f"Theme not found: {path}")

    data = tomllib.loads(path.read_text(encoding="utf-8"))  # parse TOML
    name = data.get("name") or theme_name
    colors = data.get("colors") or {}
    layout = data.get("layout") or {}

    # allow direct top-level tokens too
    for k, v in data.items():
        if k in {"name", "colors", "layout"}:
            continue
        layout.setdefault(k, v)

    return Theme(name=name, colors=colors, layout=layout)


@dataclass
class BannerContext:
    """Holds article config + theme + canvas metrics + optional article data."""

    config: dict
    colors: dict
    layout: dict
    canvas_w: int
    canvas_h: int
    article: dict = field(default_factory=dict)   # optional article metadata/content

    @classmethod
    def from_toml(cls, config_path: Path, themes_dir: Path, article: dict = None) -> "BannerContext":
        cfg = tomllib.loads(config_path.read_text(encoding="utf-8"))
        theme_name = (cfg.get("theme") or "tech").strip().lower()
        theme = load_theme(theme_name, themes_dir=themes_dir)

        size = (cfg.get("size") or "og").strip().lower()
        size_presets = {
            "youtube": (1280, 720),
            "twitter": (1200, 675),
            "og": (1200, 630),
            "thumbnail": (512, 512),
        }
        w, h = size_presets.get(size, size_presets["og"])
        if isinstance(cfg.get("canvas"), dict):
            w = int(cfg["canvas"].get("width", w))
            h = int(cfg["canvas"].get("height", h))

        colors = dict(theme.colors)
        layout = dict(theme.layout)

        # Apply any layout settings directly from the config (e.g., [layout] section)
        if "layout" in cfg and isinstance(cfg["layout"], dict):
            layout.update(cfg["layout"])
            
        overrides = cfg.get("overrides") or {}
        if isinstance(overrides, dict):
            colors.update(overrides.get("colors") or {})
            layout.update(overrides.get("layout") or {})

        return cls(
            config=cfg,
            colors=colors,
            layout=layout,
            canvas_w=w,
            canvas_h=h,
            article=article or {}
        )

    @classmethod
    def from_dict(cls, config_dict: dict, themes_dir: Path, article: dict = None) -> "BannerContext":
        theme_name = (config_dict.get("theme") or "tech").strip().lower()
        theme = load_theme(theme_name, themes_dir=themes_dir)

        cfg = dict(config_dict)
        colors = dict(theme.colors)
        layout = dict(theme.layout)

        title = cfg.get("title", "")
        if any('\u0600' <= c <= '\u06FF' for c in title):
            cfg["direction"] = "rtl"

        if "layout" in cfg and isinstance(cfg["layout"], dict):
            layout.update(cfg["layout"])
            
        # Apply overrides, just like from_toml
        overrides = cfg.get("overrides") or {}
        if isinstance(overrides, dict):
            colors.update(overrides.get("colors") or {})
            layout.update(overrides.get("layout") or {})

        size = (cfg.get("size") or "og").strip().lower()
        size_presets = {
            "youtube": (1280, 720),
            "twitter": (1200, 675),
            "og": (1200, 630),
            "thumbnail": (512, 512),  
        }
        w, h = size_presets.get(size, size_presets["og"])
        if isinstance(cfg.get("canvas"), dict):
            w = int(cfg["canvas"].get("width", w))
            h = int(cfg["canvas"].get("height", h))

        return cls(
            config=cfg,
            colors=colors,
            layout=layout,
            canvas_w=w,
            canvas_h=h,
            article=article or {}
        )
        