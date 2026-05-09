#!/usr/bin/env python3
"""
fix_component_attributes.py

Safely adds missing class attributes to banner generator components.

- Only modifies files where the Component class lacks certain attributes.
- Creates a .bak backup before any write.
- Dry-run mode shows planned changes without writing.
- Uses Python's AST to preserve formatting and comments.
"""

import ast
import shutil
from pathlib import Path
from typing import Dict, Set, Optional

PROJECT_ROOT = Path(__file__).resolve().parent
COMPONENTS_DIR = PROJECT_ROOT / "banner_generator" / "components"

# Default values for missing attributes (can be tuned per component)
DEFAULTS = {
    "config_schema": {},
    "z_index": 100,
    "section_name": None,          # None means no TOML section
    "description": "",
}

# Overrides for specific components (by component_id)
COMPONENT_OVERRIDES = {
    # core components
    "background": {
        "z_index": 0,              # must be bottom-most
        "section_name": None,
        "description": "Background gradients, patterns, and vignette",
    },
    "title": {
        "z_index": 50,
        "section_name": None,
        "description": "Main title and subtitle (uses global title/subtitle and [layout] section)",
    },
    "badge": {
        "z_index": 150,
        "section_name": "badge",
        "description": "Series badge / label (pill‑shaped)",
        "config_schema": {
            "text": {"type": "str", "default": "", "help": "Badge text (e.g., series name)"},
            "x": {"type": "int", "default": 85, "help": "X position"},
            "y": {"type": "int", "default": 85, "help": "Y position"},
            "width": {"type": "int", "default": 220, "help": "Badge width"},
            "height": {"type": "int", "default": 36, "help": "Badge height"},
            "font_size": {"type": "int", "default": 16, "help": "Font size"},
            "align": {"type": "str", "default": "start", "help": "Text alignment: start, middle, end"},
        },
    },
    "icon": {
        "z_index": 120,
        "section_name": "icon",
        "description": "Decorative icon (Pelican, Tux, Vim, Arch, Ubuntu, or custom SVG)",
    },
    "watermark": {"z_index": 10, "section_name": "watermark", "description": "Rotating watermark overlay"},
    "decorations": {"z_index": 20, "section_name": "decorations", "description": "Code rain, floating geometry, pulsing brackets"},
    "tagline": {"z_index": 60, "section_name": "tagline", "description": "Tagline with optional separator line"},
    "meta_progress": {"z_index": 70, "section_name": "meta_progress", "description": "Metadata line and optional progress bar"},
    "credits": {"z_index": 160, "section_name": "credits", "description": "Footer credits (site name and domain)"},

    # misc components
    "status_badges": {
        "z_index": 140,
        "section_name": "status_badges",
        "description": "Tag badges (automatically filled from article tags if not overridden)",
        "config_schema": {
            "badges": {"type": "list", "default": [], "help": "List of badge texts"},
            "x": {"type": "int", "default": 85, "help": "X position"},
            "y": {"type": "int", "default": 568, "help": "Y position"},
            "font_size": {"type": "int", "default": 12, "help": "Font size"},
            "gap": {"type": "int", "default": 8, "help": "Gap between badges"},
            "pad": {"type": "int", "default": 8, "help": "Horizontal padding"},
            "max_badges": {"type": "int", "default": 4, "help": "Maximum number of badges"},
        },
    },
    "article_metadata": {"section_name": "article_metadata", "description": "Category, subcategory, series info"},
    "author_plate": {"section_name": "author_plate", "description": "Styled author name with ornaments"},
    "central_emblem": {"section_name": "central_emblem", "description": "Shield / crest / geometric medallion"},
    "geometric_shapes": {"section_name": "geometric_shapes", "description": "Bars, circles, rectangles as accents"},
    "ornamental_border": {"section_name": "ornamental_border", "description": "Elaborate SVG borders"},
    "social_icons": {"section_name": "social_icons", "description": "GitHub / Twitter / YouTube icons"},
    "multi_text": {"section_name": "multi_text", "description": "Multi‑line text block"},

    # tech components
    "terminal": {
        "z_index": 200,
        "section_name": "terminal",
        "description": "Terminal window with command lines and syntax highlighting",
        "config_schema": {
            "commands": {"type": "list", "default": [], "help": "List of shell commands"},
            "x": {"type": "int", "default": 700, "help": "X position"},
            "y": {"type": "int", "default": 80, "help": "Y position"},
            "width": {"type": "int", "default": 440, "help": "Window width"},
            "show_serving": {"type": "bool", "default": True, "help": "Show serving line"},
            "typing": {"type": "bool", "default": True, "help": "Animated typing effect"},
            "dynamic_from_article": {"type": "bool", "default": False, "help": "Extract commands from article"},
        },
    },
    "code_snippet": {
        "section_name": "code_snippet",
        "description": "Syntax‑highlighted code block (Python, etc.)",
        "config_schema": {
            "code": {"type": "list", "default": ["print('Hello World')"], "help": "Code lines"},
            "language": {"type": "str", "default": "python", "help": "Language for highlighting"},
            "title": {"type": "str", "default": "", "help": "Optional title bar text"},
            "line_numbers": {"type": "bool", "default": True, "help": "Show line numbers"},
            "dynamic_from_article": {"type": "bool", "default": False, "help": "Extract from article body"},
        },
    },
    "ascii_logo": {"section_name": "ascii_logo", "description": "Vectorised ASCII‑art logo (Tux, Vim, Arch, Ubuntu)"},
    "vim_editor": {"section_name": "vim_editor", "description": "Vim editor window with syntax highlighting"},
    "sysinfo": {"section_name": "sysinfo", "description": "Neofetch‑style system information panel"},
    "metrics": {"section_name": "metrics", "description": "Live system metrics (CPU, RAM, disk)"},
    "git": {"section_name": "git", "description": "Git log / branch display"},
    "bash_prompt": {"section_name": "bash_prompt", "description": "Simple bash prompt simulation"},
    "mini_vim": {"section_name": "mini_vim", "description": "Small Vim window with command list"},
    "package_list": {"section_name": "package_list", "description": "List of packages / dependencies"},
    "vim_keystrokes": {"section_name": "vim_keystrokes", "description": "Vim key sequence badges"},
    "vim_mode": {"section_name": "vim_mode", "description": "Vim mode indicator (NORMAL, INSERT, etc.)"},
    "vim_statusline": {"section_name": "vim_statusline", "description": "Vim‑style statusline segments"},

    # academic components
    "citation": {"section_name": "citation", "description": "Quote with author and source"},
    "definition_box": {"section_name": "definition_box", "description": "Term / definition box"},
    "equation": {"section_name": "equation", "description": "LaTeX equation rendered as SVG text"},
    "latex_source": {"section_name": "latex_source", "description": "LaTeX code block with syntax highlighting"},
    "database_relations_tables": {"section_name": "database_relations_tables", "description": "Database table schemas with relations"},
    "network_diagram": {"section_name": "network_diagram", "description": "Simple network node diagram"},
    "kanban": {"section_name": "kanban", "description": "Kanban board with columns and cards"},
    "chart_simple": {"section_name": "chart_simple", "description": "Simple bar chart"},
    "quote": {"section_name": "quote", "description": "Pull quote with optional author"},
}


class ComponentAttributeInjector(ast.NodeTransformer):
    """AST transformer that adds missing class attributes to the Component class."""
    def __init__(self, component_id: str, overrides: Dict):
        self.component_id = component_id
        self.overrides = overrides
        self.modified = False

    def visit_ClassDef(self, node):
        if node.name != "Component":
            return node

        existing_attrs = {assign.targets[0].id for assign in node.body if isinstance(assign, ast.Assign) and isinstance(assign.targets[0], ast.Name)}
        new_assigns = []

        # Add missing attributes
        for attr, default in DEFAULTS.items():
            if attr not in existing_attrs:
                value = self.overrides.get(attr, default)
                # Build AST node for assignment
                if isinstance(value, dict):
                    # Create a dict node
                    keys = [ast.Constant(key) for key in value.keys()]
                    vals = [self._to_ast_node(v) for v in value.values()]
                    ast_value = ast.Dict(keys=keys, values=vals)
                elif isinstance(value, list):
                    ast_value = ast.List(elts=[self._to_ast_node(v) for v in value])
                elif value is None:
                    ast_value = ast.Constant(None)
                elif isinstance(value, str):
                    ast_value = ast.Constant(value)
                elif isinstance(value, int):
                    ast_value = ast.Constant(value)
                elif isinstance(value, bool):
                    ast_value = ast.Constant(value)
                else:
                    raise ValueError(f"Unsupported default type for {attr}: {type(value)}")

                assign = ast.Assign(
                    targets=[ast.Name(attr, ctx=ast.Store())],
                    value=ast_value,
                    lineno=node.lineno,
                )
                new_assigns.append(assign)
                self.modified = True

        if new_assigns:
            # Insert new assignments at the top of the class body
            node.body = new_assigns + node.body
        return node

    def _to_ast_node(self, obj):
        """Convert a Python literal to an AST node."""
        if isinstance(obj, dict):
            keys = [ast.Constant(k) for k in obj.keys()]
            values = [self._to_ast_node(v) for v in obj.values()]
            return ast.Dict(keys=keys, values=values)
        elif isinstance(obj, list):
            return ast.List(elts=[self._to_ast_node(v) for v in obj])
        elif isinstance(obj, str):
            return ast.Constant(obj)
        elif isinstance(obj, int) or isinstance(obj, float):
            return ast.Constant(obj)
        elif isinstance(obj, bool):
            return ast.Constant(obj)
        elif obj is None:
            return ast.Constant(None)
        else:
            raise ValueError(f"Cannot convert {obj} of type {type(obj)}")


def find_component_id(file_path: Path) -> Optional[str]:
    """Extract component_id from the file's Component class."""
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "Component":
                for assign in node.body:
                    if isinstance(assign, ast.Assign):
                        for target in assign.targets:
                            if isinstance(target, ast.Name) and target.id == "component_id":
                                if isinstance(assign.value, ast.Constant) and isinstance(assign.value.value, str):
                                    return assign.value.value
        return None
    except Exception:
        return None


def process_file(file_path: Path, dry_run: bool) -> bool:
    """Process a single component file. Returns True if modified."""
    print(f"\nProcessing: {file_path.relative_to(PROJECT_ROOT)}")
    component_id = find_component_id(file_path)
    if not component_id:
        print("  → No component_id found -> skipping")
        return False

    # Get overrides for this component (fallback to empty dict)
    overrides = COMPONENT_OVERRIDES.get(component_id, {})

    # Read original source
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Apply transformer
    transformer = ComponentAttributeInjector(component_id, overrides)
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    if not transformer.modified:
        print("  → All attributes already present.")
        return False

    # Generate new source code
    new_source = ast.unparse(new_tree)

    if dry_run:
        print("  → Would add missing attributes:")
        for attr in DEFAULTS.keys():
            if attr not in source:
                print(f"      + {attr} = {overrides.get(attr, DEFAULTS[attr])!r}")
        return False

    # Create backup
    backup = file_path.with_suffix(".py.bak")
    shutil.copy2(file_path, backup)
    print(f"  → Backup created: {backup.name}")

    # Write modified file
    file_path.write_text(new_source, encoding="utf-8")
    print("  → File updated.")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Add missing class attributes to banner components.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without writing files.")
    args = parser.parse_args()

    if not COMPONENTS_DIR.exists():
        print(f"ERROR: Components directory not found: {COMPONENTS_DIR}")
        return 1

    # Gather all component files (skip base.py and __init__.py)
    component_files = []
    for py_file in COMPONENTS_DIR.rglob("*.py"):
        if py_file.name in ("base.py", "__init__.py"):
            continue
        component_files.append(py_file)

    if not component_files:
        print("No component files found.")
        return 0

    modified_count = 0
    for f in component_files:
        if process_file(f, dry_run=args.dry_run):
            modified_count += 1

    print(f"\nSummary: {modified_count} file(s) would be modified" if args.dry_run else f"Summary: modified {modified_count} file(s)")
    return 0


if __name__ == "__main__":
    exit(main())
