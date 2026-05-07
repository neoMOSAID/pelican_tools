from __future__ import annotations

from importlib import import_module


COMPONENT_MAP = {
    "background": "banner_generator.components.background",
    "watermark": "banner_generator.components.watermark",
    "terminal": "banner_generator.components.terminal",
    "icon": "banner_generator.components.icon",
    "badge": "banner_generator.components.badge",
    "title": "banner_generator.components.title",
    "meta_progress": "banner_generator.components.meta_progress",
    "tagline": "banner_generator.components.tagline",
    "credits": "banner_generator.components.credits",
    "status_badges": "banner_generator.components.status_badges",
    "decorations": "banner_generator.components.decorations",
    "social_icons": "banner_generator.components.social_icons",
    "vim_mode": "banner_generator.components.vim_mode",
    "vim_statusline": "banner_generator.components.vim_statusline",
    "mini_vim": "banner_generator.components.mini_vim",
    "vim_keystrokes": "banner_generator.components.vim_keystrokes",
    "sysinfo": "banner_generator.components.sysinfo",
    "bash_prompt": "banner_generator.components.bash_prompt",
    "ascii_logo": "banner_generator.components.ascii_logo",
    "package_list": "banner_generator.components.package_list",
    "vim_editor": "banner_generator.components.vim_editor",
    "quote": "banner_generator.components.quote",
    "network_diagram": "banner_generator.components.network_diagram",
    "database_relations_tables": "banner_generator.components.database_relations_tables",
    "kanban": "banner_generator.components.kanban",
    "git": "banner_generator.components.git",
    "metrics": "banner_generator.components.metrics",
    "article_metadata": "banner_generator.components.article_metadata",
    "code_snippet": "banner_generator.components.code_snippet",
    "definition_box": "banner_generator.components.definition_box",
    "citation": "banner_generator.components.citation",
    "chart_simple": "banner_generator.components.chart_simple",
    "equation": "banner_generator.components.equation",
    "latex_source": "banner_generator.components.latex_source",
}


def load_component(component_id: str):
    if component_id not in COMPONENT_MAP:
        raise KeyError(f"Unknown component_id: {component_id}")
    module = import_module(COMPONENT_MAP[component_id])
    return module.Component
