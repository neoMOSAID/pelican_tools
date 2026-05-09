

# pelican_tools

![Pelican Tools Banner](tests/banner.svg)

**pelican_tools** provides a flexible, SVG‑based **banner and thumbnail generator**
for [Pelican](https://getpelican.com/) static sites.
Create beautiful, tech‑oriented Open Graph images and square thumbnails
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
- [Adding new components, themes & designs](#adding-new-components-themes--designs)
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
- **14 ready‑made colour themes** – Dracula, Nord, Gruvbox, Catppuccin, Solarized, and others
- **20+ design presets** organised by category – articles/tech, books/fantasy, books/corporate, …
- **Square thumbnails** – 512×512 images for article previews, using the same rich components
- **Extensible without touching a single line of Python** – drop new components, themes, or designs into their respective folders and they are automatically discovered when the app starts.
- **Batch‑friendly CLI** – generate banners and thumbnails from the command line, ideal for scripting and CI/CD
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

   The default paths are defined in `banner_generator/config.py`; you normally won’t need to change them.

---

## Quick start

Generate a banner from a design preset:

```bash
python cli.py banner --design vim_article --png
```

Use a nested design name (recursive discovery works out of the box):

```bash
python cli.py banner --design books/fantasy/fantasy_book_cover --out-dir ./covers
```

Generate a thumbnail with custom text:

```bash
python cli.py thumbnail --design thumbnail_default \
  --title "My Post" --subtitle "A tutorial"
```

Supply your own complete TOML configuration:

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

- `--design <name>` – use a design preset. The name can be a simple file stem (e.g. `vim_article`) or a nested path like `articles/tech/linux_homelab`. The tool searches recursively, so you can organise designs into subdirectories without touching any code.
- `--file <path>` – point to a complete `.toml` configuration file.

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

1. **Themes** (`banner_generator/themes/*.toml`) – colour palettes and global layout defaults.
2. **Designs** (`banner_generator/designs/*.banner.toml`) – presets that enable specific components (terminal, code snippet, etc.) and set their parameters.
3. **Per‑use configs** – any TOML file you write or generate.

All configs are TOML. The simplest way to get started is to copy an existing design and tweak the values.

Both themes and designs can be placed in **subdirectories** and the app will find them automatically – simply reference the full path from the root of the directory (e.g. `theme = "catppuccin/mocha"`, `design = "books/fantasy/fantasy_book_cover"`).

---

## Adding new components, themes & designs

The system is **extension‑first**: you never need to edit core Python code to add visual
elements, colour schemes, or layout presets.

### Components
- Drop a `.py` file into `banner_generator/components/`.
- It must contain a class called `Component` that inherits from `BaseComponent` (see `base.py`).
- The class must define a string `component_id` and an integer `z_index` for layering.
- The component is automatically registered on startup and becomes available in every
  banner config under `[components] show_<id>`.

### Themes
- Place a `.toml` file anywhere under `banner_generator/themes/` (subdirectories allowed).
- The file must contain tables `[colors]` and `[layout]` with appropriate SVG colour keys.
- Themes are discovered recursively and listed in the config comments; you use them via
  `theme = "your/theme"`.

### Designs
- Add a `*.banner.toml` file in any subfolder of `banner_generator/designs/`.
- Follow the same structure as the existing presets: declare a theme, optional size, and
  enable the components you want in the `[components]` section.
- The CLI and interactive tools will find the design by its relative path (e.g.
  `books/mystery/mystery_book_cover`).

> **No modifications to `factory.py`, `renderer.py`, or `cli.py` are required.** Simply
> adding files to the right directories is enough – the auto‑discovery handles the rest.

---

## Project structure

```
pelican_tools/
├── banner_generator/         # SVG rendering engine
│   ├── core/                 # Context, canvas, factory, renderer
│   ├── components/           # All 35+ visual components (auto‑discovered)
│   ├── themes/               # Colour themes – nested folders supported
│   ├── designs/              # Layout presets – organised in subdirectories
│   │   ├── articles/         #    technology and academic articles
│   │   ├── books/            #    book covers (fantasy, mystery, corporate, …)
│   │   └── thumbnails/       #    thumbnail presets
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

