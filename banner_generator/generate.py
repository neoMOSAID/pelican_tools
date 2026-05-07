
#!/usr/bin/env python3
"""Generate a banner from a design TOML preset."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from banner_generator.config import BannerConfig
from banner_generator.core.context import BannerContext
from banner_generator.core.renderer import BannerRenderer


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_png(svg_path: Path, png_path: Path, width: int, height: int):
    exe = "magick"
    if subprocess.run(["bash", "-lc", "command -v magick >/dev/null 2>&1"], check=False).returncode != 0:
        exe = "convert"
    subprocess.run(
        [exe, str(svg_path), "-resize", f"{width}x{height}!", str(png_path)],
        check=True,
    )


def main():
    cfg = BannerConfig()

    ap = argparse.ArgumentParser(description="Generate an SVG/PNG banner from a design preset")
    ap.add_argument("--design", required=True,
                    help="Design name (file in designs/ without .banner.toml)")
    ap.add_argument("--out-dir", default=str(cfg.OUTPUT_DIR),
                    help="Output directory")
    ap.add_argument("--svg", action="store_true", help="Write SVG output")
    ap.add_argument("--png", action="store_true", help="Write PNG output")
    ap.add_argument("--preview", action="store_true", help="Open PNG after rendering")
    args = ap.parse_args()

    design_path = cfg.DESIGNS_DIR / f"{args.design}.banner.toml"
    if not design_path.exists():
        sys.exit(f"❌ Design not found: {design_path}")

    out_dir = Path(args.out_dir)

    ctx = BannerContext.from_toml(design_path, themes_dir=cfg.THEMES_DIR)

    if args.png or not args.svg:
        # Rasterizing: render a static frame
        ctx.config["render_mode"] = "static"
        svg = BannerRenderer(ctx).compose()
        svg_path = out_dir / "banner.svg"
        write_text(svg_path, svg)
        png_path = out_dir / "banner.png"
        render_png(svg_path, png_path, width=ctx.canvas_w, height=ctx.canvas_h)
        print(f"PNG: {png_path}")
        if args.preview:
            subprocess.run(["xdg-open", str(png_path)], check=False)
    else:
        ctx.config["render_mode"] = "animated"
        svg = BannerRenderer(ctx).compose()
        svg_path = out_dir / "banner.svg"
        write_text(svg_path, svg)
        print(f"SVG: {svg_path}")


if __name__ == "__main__":
    main()
    