
#!/usr/bin/env python3
"""Generate SVG banners for all themes and all designs."""
import sys
import shutil
import subprocess
from pathlib import Path

# Allow importing from parent directory
sys.path.insert(0, str(Path(__file__).parent))

from banner_generator.core.context import BannerContext
from banner_generator.core.renderer import BannerRenderer
from banner_generator.config import BannerConfig


def render_to_files(cfg: dict, themes_dir: Path, out_stem: str,
                    svg_dir: Path, png_dir: Path, magick_path: str = None):
    """Render a config dict to SVG (in svg_dir) and PNG (in png_dir if magick_path)."""
    ctx = BannerContext.from_dict(cfg, themes_dir=themes_dir)
    ctx.config["render_mode"] = "static"
    svg_content = BannerRenderer(ctx).compose()

    svg_path = svg_dir / f"{out_stem}.svg"
    svg_path.write_text(svg_content, encoding="utf-8")
    print(f"  → {svg_path}")

    if magick_path:
        png_path = png_dir / f"{out_stem}.png"
        subprocess.run([
            magick_path, str(svg_path),
            "-resize", f"{ctx.canvas_w}x{ctx.canvas_h}!",
            str(png_path)
        ], check=True)
        print(f"  → {png_path}")


def main():
    script_dir = Path(__file__).parent
    themes_dir = script_dir / "banner_generator" / "themes"
    designs_dir = script_dir / "banner_generator" / "designs"
    out_dir = script_dir / "tests" / "banners"

    # Validate
    if not themes_dir.exists():
        sys.exit(f"Themes directory not found: {themes_dir}")
    if not designs_dir.exists():
        sys.exit(f"Designs directory not found: {designs_dir}")

    # Create output subdirectories for SVG and PNG
    svg_dir = out_dir / "svg"
    png_dir = out_dir / "png"
    svg_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)

    # Check for ImageMagick
    magick_path = shutil.which("magick") or shutil.which("convert")
    can_convert = magick_path is not None
    if not can_convert:
        print("⚠️ ImageMagick not found – PNG generation disabled")

    import tomllib

    # ------------------------------------------------------------
    # 1. Generate banners for all themes (using base config)
    # ------------------------------------------------------------
    base_config_path = script_dir / "tests" / "base_config.toml"
    if not base_config_path.exists():
        print(f"⚠️ Base config not found: {base_config_path} – skipping theme gallery")
    else:
        base_cfg = tomllib.loads(base_config_path.read_text(encoding="utf-8"))
        theme_files = list(themes_dir.glob("*.toml"))
        if not theme_files:
            print("⚠️ No theme files found – skipping theme gallery")
        else:
            print(f"\n📦 Generating banners for {len(theme_files)} themes...\n")
            for theme_file in sorted(theme_files):
                theme_name = theme_file.stem
                print(f"Theme: {theme_name}")
                cfg = base_cfg.copy()
                cfg["theme"] = theme_name
                out_stem = f"theme_{theme_name}"
                render_to_files(cfg, themes_dir, out_stem,
                                svg_dir, png_dir,
                                magick_path if can_convert else None)

    # ------------------------------------------------------------
    # 2. Generate banners for all design presets
    # ------------------------------------------------------------
    design_files = sorted(designs_dir.glob("*.banner.toml"))
    if not design_files:
        print("⚠️ No design files found – skipping design gallery")
    else:
        print(f"\n🎨 Generating banners for {len(design_files)} designs...\n")
        for design_path in design_files:
            design_name = design_path.stem.replace(".banner", "")
            print(f"Design: {design_name}")
            try:
                design_cfg = tomllib.loads(design_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  ❌ Failed to load design: {e}")
                continue
            # Ensure theme is valid (fallback to 'tech' if missing)
            if "theme" not in design_cfg:
                design_cfg["theme"] = "tech"
            out_stem = f"design_{design_name}"
            render_to_files(design_cfg, themes_dir, out_stem,
                            svg_dir, png_dir,
                            magick_path if can_convert else None)

    print(f"\n✅ SVG banners saved to: {svg_dir}")
    if can_convert:
        print(f"✅ PNG banners saved to: {png_dir}")
    else:
        print("⚠️ PNG images were not generated (ImageMagick missing).")


if __name__ == "__main__":
    main()

    