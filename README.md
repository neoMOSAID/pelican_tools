# pelican_tools

![Pelican Tools Banner](tests/banner.svg)

**pelican_tools** provides a flexible, SVG‑based **banner and thumbnail generator**
for [Pelican](https://getpelican.com/) static sites.
Create beautiful, technogeek Open Graph images and square thumbnails
from simple TOML configuration files.

📝 **Read the blog post:**
[Building a Modular Banner Generator for Pelican](https://mosaid.xyz/articles/building-a-modular-banner-generator-for-pelican.html)

---

## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Quick start](#quick-start)
- [CLI commands](#cli-commands)
  - [`banner` – generate a banner](#banner--generate-a-banner)
  - [`thumbnail` – generate a thumbnail](#thumbnail--generate-a-thumbnail)
- [Configuration & customisation](#configuration--customisation)
- [Project structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)

---

## Features

- **35+ visual components** – mix and match to build stunning banners:
  - Terminal windows with typing animations
  - Code snippets, equations, network diagrams
  - Git log, Kanban board, database tables
  - Vim editor mockups, ASCII art, system info
  - Quote blocks, definition boxes, charts, badges, social icons, and more
- **14 themes** – Dracula, Nord, Gruvbox, Catppuccin, Solarized, and others
- **14 design presets** – ready‑to‑use layouts for tech, vim, docker, python, latex, …
- **Square thumbnails** – 512×512 images for article previews, using the same rich components
- **Batch‑friendly CLI** – generate banners and thumbnails from the command line,
  ideal for scripting and CI/CD
- **TOML‑native** – all configuration is clean, human‑readable TOML (no JSON, no YAML)
- **Zero external Python dependencies** – uses only the standard library (`tomllib`)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/neoMOSAID/pelican_tools
   cd pelican_tools
   ```

2. **Python version** – requires Python 3.11+ (for built‑in `tomllib`).
   No `pip install` is needed.

3. **Install ImageMagick or GraphicsMagick** (optional, for PNG/JPG output)

   ```bash
   # Debian/Ubuntu
   sudo apt install imagemagick

   # macOS
   brew install imagemagick
   ```

   If ImageMagick is not available, the toolkit can still produce high‑quality SVG files.

4. **Set up your environment**

   Edit `banner_generator/config.py` to set default paths if needed, or rely on the
   default locations inside the project. Usually no changes are necessary.

---

## Quick start

Generate a banner from a design preset:

```bash
python cli.py banner --design vim_article --png
```

Generate a thumbnail with custom text:

```bash
python cli.py thumbnail --design thumbnail_default \
  --title "My Post" --subtitle "A tutorial"
```

Use your own complete TOML configuration:

```bash
python cli.py banner --file /path/to/banner.toml --out-dir ./output --svg
```

---

## CLI commands

### `banner` – generate a banner

```
python cli.py banner (--design DESIGN | --file FILE) [--out-dir DIR] [--svg|--png]
```

**Modes**

- `--design <name>` – use a built‑in design preset (e.g. `vim_article`, `linux_homelab`).
- `--file <path>` – point to a complete `.toml` configuration file (the same format
  used by the generator).

**Options**

- `--out-dir` – output directory (default: `banner_generator/output`).
- `--svg` – save only SVG (default when no flag is given).
- `--png` – also rasterise to PNG (requires ImageMagick).

### `thumbnail` – generate a thumbnail

```
python cli.py thumbnail [--design DESIGN] [--title TITLE]
                         [--subtitle SUBTITLE] [--meta META] [--category CAT]
                         [--no-tagline] [--out-dir DIR]
```

- Default design is `thumbnail_default`.
- Command‑line overrides (`--title`, `--subtitle`, …) take precedence.
- Always produces a static square image (512×512), suitable for Pelican’s `THUMBNAIL`
  metadata field.

---

## Configuration & customisation

The banner engine is driven by **three layers**:

1. **Themes** (`banner_generator/themes/*.toml`) – colour palettes and global layout
   defaults.
2. **Designs** (`banner_generator/designs/*.banner.toml`) – presets that enable specific
   components (terminal, code snippet, etc.) and set their parameters.
3. **Per‑use configs** – any TOML file you write or generate.

All configs are TOML. The simplest way to get started is to copy an existing design
and tweak the values.

The component library (`banner_generator/components/`) is modular – new visual
elements can be added by implementing a simple `Component` class.

---

## Project structure

```
pelican_tools/
├── banner_generator/         # SVG rendering engine
│   ├── core/                 # Context, canvas, factory, renderer
│   ├── components/           # All 35+ visual components
│   ├── themes/               # Colour themes (dracula, nord, gruvbox, …)
│   ├── designs/              # Pre‑made layout presets
│   ├── config.py             # Banner generator paths
│   └── generate.py           # Standalone generation script (legacy)
├── tests/                    # Sample banners & thumbnails (SVG/PNG)
├── cli.py                    # Unified CLI entry point
└── README.md
```

> **Note:** The interactive article creation tools (`article_creator/`) are kept in a private
> repository and are not included here. This public project focuses exclusively on
> banner and thumbnail generation.

---

## Dependencies

- **Python 3.11+** (uses `tomllib` from the standard library)
- **ImageMagick** or **GraphicsMagick** (optional, for PNG/JPG output)

All Python dependencies are part of the standard library. No `pip install` is required.

---

## License

This project is licensed under the MIT License.

---

**Happy generating – may your Pelican banners always stand out!**
