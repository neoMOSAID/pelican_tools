
#!/usr/bin/env python3
"""Unified CLI for Pelican article creation, banner generation, and editing."""
import argparse
import subprocess
import sys
import tomllib
from pathlib import Path

# ----------------------------------------------------------------------
# Config objects (they handle all paths internally)
from article_creator.config import Config
from banner_generator.config import BannerConfig
from article_creator.edit_workflow import EditWorkflow

# ----------------------------------------------------------------------
def cmd_article(args):
    cfg = Config()
    cfg.dry_run = args.dry_run
    cfg.verbose = args.verbose
    from article_creator.workflow import ArticleWorkflow
    workflow = ArticleWorkflow(cfg)
    try:
        workflow.run()
    except KeyboardInterrupt:
        print("\n\n👋 Workflow cancelled by user.")
        sys.exit(0)


def cmd_banner(args):
    """Generate a banner from a design preset."""
    from banner_generator.core.context import BannerContext
    from banner_generator.core.renderer import BannerRenderer

    bcfg = BannerConfig()
    design_path = bcfg.DESIGNS_DIR / f"{args.design}.banner.toml"
    if not design_path.exists():
        sys.exit(f"❌ Design not found: {design_path}")

    out_dir = Path(args.out_dir) if args.out_dir else bcfg.OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    ctx = BannerContext.from_toml(design_path, themes_dir=bcfg.THEMES_DIR)

    if args.png or not args.svg:
        # Rasterizing: render static then convert
        ctx.config["render_mode"] = "static"
        svg = BannerRenderer(ctx).compose()
        svg_path = out_dir / "banner.svg"
        svg_path.write_text(svg, encoding="utf-8")

        exe = "magick"
        if subprocess.run(["bash", "-lc", "command -v magick >/dev/null 2>&1"], check=False).returncode != 0:
            exe = "convert"
        png_path = out_dir / "banner.png"
        subprocess.run(
            [exe, str(svg_path), "-resize", f"{ctx.canvas_w}x{ctx.canvas_h}!", str(png_path)],
            check=True,
        )
        print(f"PNG: {png_path}")
    else:
        ctx.config["render_mode"] = "animated"
        svg = BannerRenderer(ctx).compose()
        svg_path = out_dir / "banner.svg"
        svg_path.write_text(svg, encoding="utf-8")
        print(f"SVG: {svg_path}")


def cmd_thumbnail(args):
    """Generate a square thumbnail using a design preset + optional metadata."""
    from banner_generator.core.context import BannerContext
    from banner_generator.core.renderer import BannerRenderer
    from article_creator.slug_utils import SlugHelper
    from article_creator.working_dir import WorkingDirectory
    from article_creator.config import Config as ArticleConfig

    bcfg = BannerConfig()
    design_path = bcfg.DESIGNS_DIR / f"{args.design}.banner.toml"
    if not design_path.exists():
        sys.exit(f"❌ Design not found: {design_path}")

    # Build config dict from the preset
    cfg = tomllib.loads(design_path.read_text(encoding="utf-8"))

    # Override with work‑dir data if available
    if args.work_dir:
        wd_path = Path(args.work_dir)
        acfg = ArticleConfig()
        wd = WorkingDirectory(wd_path, acfg)
        wd.load_metadata()
        cfg["title"] = wd.title or cfg["title"]
        if args.category:
            cfg["meta"] = f"Article {wd.article_id} · {args.category}"
        if wd.summary and not args.no_tagline:
            cfg["subtitle"] = wd.summary[:80]
        if wd.bannertitle:
            cfg["title_line2"] = wd.bannertitle  # or wd.thumbtitle

    # Command‑line overrides (highest priority)
    if args.title:
        cfg["title"] = args.title
    if args.subtitle:
        cfg["subtitle"] = args.subtitle
    if args.meta:
        cfg["meta"] = args.meta

    # Render
    ctx = BannerContext.from_dict(cfg, themes_dir=bcfg.THEMES_DIR)
    # Thumbnails are always static (no typing animations)
    ctx.config["render_mode"] = "static"
    svg = BannerRenderer(ctx).compose()

    out_dir = Path(args.out_dir) if args.out_dir else bcfg.OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / "thumbnail.svg"
    svg_path.write_text(svg, encoding="utf-8")

    # Convert to PNG (required for thumbnails)
    exe = "magick"
    if subprocess.run(["bash", "-lc", "command -v magick >/dev/null 2>&1"], check=False).returncode != 0:
        exe = "convert"
    png_path = out_dir / "thumbnail.png"
    subprocess.run(
        [exe, str(svg_path), "-resize", f"{ctx.canvas_w}x{ctx.canvas_h}!", str(png_path)],
        check=True,
    )
    print(f"✅ Thumbnail: {png_path}")


def cmd_edit(args):
    """Edit an existing published article: metadata, content, images, and move across categories."""
    cfg = Config()
    cfg.dry_run = args.dry_run
    cfg.verbose = args.verbose
    workflow = EditWorkflow(cfg)
    try:
        workflow.run()
    except KeyboardInterrupt:
        print("\n\n👋 Edit session cancelled by user.")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Pelican Tools")
    sub = parser.add_subparsers(dest="command", required=True)

    # ---- article subcommand ----
    art = sub.add_parser("article", help="Interactive article workflow")
    art.add_argument("--dry-run", action="store_true", help="Simulate without changes")
    art.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    # ---- banner subcommand ----
    ban = sub.add_parser("banner", help="Generate a banner from a design preset")
    ban.add_argument("--design", required=True, help="Design name (e.g. vim_article)")
    ban.add_argument("--out-dir", default=None, help="Output directory (default: banner_generator/output)")
    ban.add_argument("--svg", action="store_true", help="Output SVG only")
    ban.add_argument("--png", action="store_true", help="Output PNG")

    # ---- thumbnail subcommand ----
    thumb = sub.add_parser("thumbnail", help="Generate a square thumbnail")
    thumb.add_argument("--design", default="thumbnail_default",
                    help="Design preset name (default: thumbnail_default)")
    thumb.add_argument("--work-dir", help="Path to an article working directory (reads title.txt etc.)")
    thumb.add_argument("--title", help="Override title")
    thumb.add_argument("--subtitle", help="Override subtitle")
    thumb.add_argument("--meta", help="Override meta line")
    thumb.add_argument("--category", help="Category name (for meta line)")
    thumb.add_argument("--no-tagline", action="store_true", help="Don't use summary as subtitle")
    thumb.add_argument("--out-dir", default=None, help="Output directory")

    # ---- edit subcommand ----
    edit = sub.add_parser("edit", help="Edit an existing Pelican article")
    edit.add_argument("--dry-run", action="store_true", help="Simulate changes (no files modified)")
    edit.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.command == "article":
        cmd_article(args)
    elif args.command == "banner":
        cmd_banner(args)
    elif args.command == "thumbnail":
        cmd_thumbnail(args)
    elif args.command == "edit":
        cmd_edit(args)

if __name__ == "__main__":
    main()

    