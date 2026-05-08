
# banner_generator/core/factory.py
"""Discover components automatically from the components package.
No more hard‑coded COMPONENT_MAP – just drop a .py file into `components/`."""

from __future__ import annotations

import importlib
import logging
import pkgutil
from typing import Dict, Type

logger = logging.getLogger(__name__)

# Cached registry – built once at import time
_COMPONENT_REGISTRY: Dict[str, Type] = {}
_COMPONENT_IDS: list[str] = []


def _discover_components() -> None:
    """Walk the components package and register every valid component."""
    global _COMPONENT_REGISTRY, _COMPONENT_IDS

    _COMPONENT_REGISTRY.clear()
    _COMPONENT_IDS.clear()

    # Import the components package itself (so its __path__ is available)
    from .. import components as components_pkg   

    # Modules that are infrastructure, not components – skip silently
    _SKIP_SILENTLY = {'base'}

    for _, module_name, is_pkg in pkgutil.iter_modules(components_pkg.__path__):
        # Skip sub‑packages and private files (e.g. __init__, _utils)
        if is_pkg or module_name.startswith('_'):
            continue

        if module_name in _SKIP_SILENTLY:
            continue 
        
        full_name = f"banner_generator.components.{module_name}"
        try:
            module = importlib.import_module(full_name)
        except Exception as e:
            logger.warning("Skipping component %s – import error: %s", module_name, e)
            continue

        # ---------- validation contract ----------
        if not hasattr(module, 'Component'):
            logger.warning("Skipping %s – no 'Component' class found", module_name)
            continue

        comp_class = module.Component
        if not (hasattr(comp_class, 'component_id') and isinstance(comp_class.component_id, str)):
            logger.warning("Skipping %s – Component class lacks 'component_id'", module_name)
            continue

        cid = comp_class.component_id
        if cid in _COMPONENT_REGISTRY:
            logger.warning("Duplicate component id '%s' in %s – overriding", cid, module_name)

        _COMPONENT_REGISTRY[cid] = comp_class
        _COMPONENT_IDS.append(cid)

    # Always sort IDs so config generation is predictable
    _COMPONENT_IDS.sort()


def load_component(component_id: str):
    """Return the Component class for a given id, or raise KeyError."""
    if component_id not in _COMPONENT_REGISTRY:
        raise KeyError(f"Unknown component_id: {component_id}")
    return _COMPONENT_REGISTRY[component_id]


def get_all_component_ids() -> list[str]:
    """Return a sorted list of all registered component IDs."""
    return _COMPONENT_IDS[:]


# ── initial discovery ──
_discover_components()


