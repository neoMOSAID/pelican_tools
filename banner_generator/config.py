
"""Central configuration for the banner generator subsystem."""
from __future__ import annotations
from pathlib import Path

class BannerConfig:
    # Derived from the location of this file
    PROJECT_ROOT = Path(__file__).resolve().parent.parent   # pelican_tools/
    BANNER_ROOT = Path(__file__).resolve().parent           # banner_generator/

    THEMES_DIR  = BANNER_ROOT / "themes"                    # banner_generator/themes
    DESIGNS_DIR = BANNER_ROOT / "designs"                   # was configs/
    OUTPUT_DIR  = BANNER_ROOT / "output"                    # default output

    # Optional environment overrides
    def __init__(self):
        self.dry_run = False
        self.verbose = False
        