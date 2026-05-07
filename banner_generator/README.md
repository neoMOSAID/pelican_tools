# banner_generator

Modular SVG banner generator for the **"Static, But Smarter"** series (and beyond).

## Features
- Composable component pipeline (background, watermark, terminal, title, meta/progress, etc.)
- Theme files in YAML (`themes/*.yml`)
- Article-specific config in TOML (`configs/*.banner.toml`)
- Outputs SVG + PNG (via ImageMagick `magick`)

## Quick start
```bash
cd banner_generator
python generate.py --config configs/example_article.banner.toml --out-dir output --png
```

## Requirements
- Python 3.11+
- ImageMagick (`magick`) for PNG output

## Config
See `configs/example_article.banner.toml`.

## Themes
See `themes/tech.yml` and `themes/dracula.yml`.
