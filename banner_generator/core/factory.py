
"""Discover components using absolute imports and proper sys.path."""

from __future__ import annotations

import importlib
import logging
import sys
from pathlib import Path
from typing import Dict, Type

logger = logging.getLogger(__name__)

_COMPONENT_REGISTRY: Dict[str, Type] = {}
_COMPONENT_IDS: list[str] = []


def _discover_components() -> None:
    global _COMPONENT_REGISTRY, _COMPONENT_IDS

    _COMPONENT_REGISTRY.clear()
    _COMPONENT_IDS.clear()

    # Add project root to sys.path so 'banner_generator' is importable
    project_root = Path(__file__).resolve().parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    components_dir = Path(__file__).resolve().parent.parent / "components"
    if not components_dir.exists():
        logger.warning(f"Components directory not found: {components_dir}")
        return

    for py_file in components_dir.rglob("*.py"):
        if py_file.name in ("__init__.py", "base.py") or py_file.name.startswith("_"):
            continue

        # Build dotted module path relative to project root
        # Example: banner_generator/components/core/background.py
        rel_path = py_file.relative_to(project_root)
        module_path = str(rel_path.with_suffix('')).replace('/', '.')
        # module_path becomes "banner_generator.components.core.background"

        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            logger.warning(f"Skipping {py_file} – import error: {e}")
            continue

        if not hasattr(module, 'Component'):
            continue

        comp_class = module.Component
        if not (hasattr(comp_class, 'component_id') and isinstance(comp_class.component_id, str)):
            logger.warning(f"Skipping {py_file} – Component lacks 'component_id'")
            continue

        cid = comp_class.component_id
        if cid in _COMPONENT_REGISTRY:
            logger.warning(f"Duplicate component_id '{cid}' in {py_file} – overriding")

        _COMPONENT_REGISTRY[cid] = comp_class
        _COMPONENT_IDS.append(cid)

    _COMPONENT_IDS.sort()


def load_component(component_id: str):
    if component_id not in _COMPONENT_REGISTRY:
        raise KeyError(f"Unknown component_id: {component_id}")
    return _COMPONENT_REGISTRY[component_id]


def get_all_component_ids() -> list[str]:
    return _COMPONENT_IDS[:]


_discover_components()

