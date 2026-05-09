
#!/usr/bin/env python3
"""Unified CLI for Pelican article creation, banner generation, and editing."""
import argparse
import subprocess
import sys
import os 
import tomllib
from pathlib import Path

# ----------------------------------------------------------------------
# Config objects (they handle all paths internally)
from article_creator.config import Config
from banner_generator.config import BannerConfig
from article_creator.edit_workflow import EditWorkflow
from banner_generator.core.context import list_available_themes


def find_design(designs_dir: Path, name: str) -> Path:
    """Resolve a design name (possibly nested) to a .banner.toml file.
    
    If name contains a '/', treat it as a relative path from designs_dir.
    Otherwise, search recursively for a file named `{name}.banner.toml`.
    """
    # Direct path (supports subdirectories like 'books/fantasy/fantasy_book_cover')
    direct = designs_dir / f"{name}.banner.toml"
    if direct.exists():
        return direct

    # Search for a file with exactly this name (plus the double extension)
    target_file = f"{name}.banner.toml"
    candidates = []
    for p in designs_dir.rglob("*.banner.toml"):
        if p.name == target_file:
            candidates.append(p)

    if not candidates:
        raise FileNotFoundError(f"Design not found: {name}")
    if len(candidates) > 1:
        rel_paths = [str(c.relative_to(designs_dir)) for c in candidates]
        raise RuntimeError(
            f"Multiple designs match '{name}'. Use a more specific name (with subdirectory):\n"
            + "\n".join(f"  {p}" for p in rel_paths)
        )
    return candidates[0]


def list_designs(designs_dir: Path) -> list[str]:
    """Return simplified design names (relative path without .banner.toml)."""
    designs = []
    for p in designs_dir.rglob("*.banner.toml"):
        # Remove the suffix .banner.toml, keep relative path
        rel = p.relative_to(designs_dir).with_suffix('')
        # Remove the extra ".banner" part (the base name ends with .banner)
        # The file is e.g. "books/fantasy/fantasy_epic_deluxe.banner.toml"
        # We want "books/fantasy/fantasy_epic_deluxe"
        name = str(rel).replace('.banner', '')
        designs.append(name)
    return sorted(designs)


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
    """Generate a banner from a design preset or a complete TOML config file."""
    from banner_generator.core.context import BannerContext
    from banner_generator.core.renderer import BannerRenderer

    bcfg = BannerConfig()
    out_dir = Path(args.out_dir) if args.out_dir else bcfg.OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── list designs if requested ──
    if args.list_designs:
        designs = list_designs(bcfg.DESIGNS_DIR)
        print("Available designs (use --design <name>):")
        for d in designs:
            print(f"  {d}")
        return

    # Determine config source (file or design)
    if args.file:
        config_path = args.file.resolve()
        if not config_path.exists():
            sys.exit(f"❌ Config file not found: {config_path}")
        # Load config dict so we can override theme later
        cfg_dict = tomllib.loads(config_path.read_text(encoding="utf-8"))
        design_path = config_path  # for consistency, not directly used
    else:
        try:
            design_path = find_design(bcfg.DESIGNS_DIR, args.design)
        except (FileNotFoundError, RuntimeError) as e:
            sys.exit(f"❌ {e}")
        cfg_dict = tomllib.loads(design_path.read_text(encoding="utf-8"))

    # Override theme if --theme provided
    if args.theme:
        # Validate theme exists
        available_themes = list_available_themes(bcfg.THEMES_DIR)
        if args.theme not in available_themes:
            sys.exit(f"❌ Unknown theme: {args.theme}. Available: {', '.join(available_themes)}")
        cfg_dict["theme"] = args.theme

    # Create context
    ctx = BannerContext.from_dict(cfg_dict, themes_dir=bcfg.THEMES_DIR)

    # Generate SVG and optionally PNG
    svg_path = out_dir / "banner.svg"
    png_path = out_dir / "banner.png" if (args.png or not args.svg) else None

    ctx.config["render_mode"] = "static" if png_path else "animated"
    svg = BannerRenderer(ctx).compose()
    svg_path.write_text(svg, encoding="utf-8")

    if png_path:
        exe = "magick"
        if subprocess.run(["bash", "-lc", "command -v magick >/dev/null 2>&1"], check=False).returncode != 0:
            exe = "convert"
        subprocess.run(
            [exe, str(svg_path), "-resize", f"{ctx.canvas_w}x{ctx.canvas_h}!", str(png_path)],
            check=True,
        )
        print(f"PNG: {png_path}")
    else:
        print(f"SVG: {svg_path}")

    # Preview
    if args.preview:
        if png_path and png_path.exists():
            try:
                subprocess.Popen(
                    ["feh", str(png_path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                    close_fds=True,
                )
            except FileNotFoundError:
                sys.exit("❌ feh not found. Install feh or use another image viewer.")
        else:
            print("⚠️  No PNG generated; feh cannot preview SVG. "
                  "Open the SVG file in a browser or use an SVG-capable viewer.")


def cmd_thumbnail(args):
    """Generate a square thumbnail using a design preset + optional metadata."""
    from banner_generator.core.context import BannerContext
    from banner_generator.core.renderer import BannerRenderer
    from article_creator.slug_utils import SlugHelper
    from article_creator.working_dir import WorkingDirectory
    from article_creator.config import Config as ArticleConfig

    bcfg = BannerConfig()

    try:
        design_path = find_design(bcfg.DESIGNS_DIR, args.design)
    except (FileNotFoundError, RuntimeError) as e:
        sys.exit(f"❌ {e}")

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
    ctx.config["render_mode"] = "static"
    svg = BannerRenderer(ctx).compose()

    out_dir = Path(args.out_dir) if args.out_dir else bcfg.OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / "thumbnail.svg"
    svg_path.write_text(svg, encoding="utf-8")

    # Convert to PNG
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
    # ---- banner subcommand ----
    ban = sub.add_parser("banner", help="Generate a banner from a design preset")
    # Design listing (independent)
    ban.add_argument('--list-designs', action='store_true', help='List all available design names and exit')

    # Design or file (mutually exclusive, but not required if --list-designs)
    group = ban.add_mutually_exclusive_group(required=False)
    group.add_argument('--design', help='Design name (e.g., vim_article or books/fantasy/fantasy_book_cover). Use --list-designs to see all.')
    group.add_argument('--file', type=Path, help='Path to a complete banner .toml configuration')

    # Theme (optional)
    bcfg = BannerConfig()
    available_themes = list_available_themes(bcfg.THEMES_DIR)
    ban.add_argument('--theme', choices=available_themes,
                    help=f'Color theme to use (overrides design\'s theme). Available: {", ".join(available_themes)}')
    # Output options
    ban.add_argument("--out-dir", default=None, help="Output directory (default: banner_generator/output)")
    ban.add_argument("--svg", action="store_true", help="Output SVG only")
    ban.add_argument("--png", action="store_true", help="Output PNG")
    ban.add_argument("--preview", action="store_true", help="Open the generated PNG in feh")
    
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

