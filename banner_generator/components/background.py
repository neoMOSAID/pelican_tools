from __future__ import annotations

from .base import BaseComponent


class Component(BaseComponent):
    component_id = "background"

    def defs(self) -> str:
        # Defaults if theme missing
        c = self.col
        def g(k, default):
            return c.get(k, default)

        progress_defs = f"""
    <linearGradient id=\"progressGradLow\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"0%\">
      <stop offset=\"0%\" stop-color=\"{g('progress_bar_fill_start', '#a6e3a1')}\" />
      <stop offset=\"100%\" stop-color=\"{g('progress_shimmer', '#cdd6f4')}\" />
    </linearGradient>
    <linearGradient id=\"progressGradMid\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"0%\">
      <stop offset=\"0%\" stop-color=\"{g('progress_bar_fill_mid', '#f9e2af')}\" />
      <stop offset=\"100%\" stop-color=\"{g('progress_shimmer', '#cdd6f4')}\" />
    </linearGradient>
    <linearGradient id=\"progressGradHigh\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"0%\">
      <stop offset=\"0%\" stop-color=\"{g('progress_bar_fill_end', '#f38ba8')}\" />
      <stop offset=\"100%\" stop-color=\"{g('progress_shimmer', '#cdd6f4')}\" />
    </linearGradient>
"""

        return f"""
    <!-- Background gradients -->
    <linearGradient id=\"bg\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"100%\">
      <stop offset=\"0%\" stop-color=\"{g('bg_start', '#0d1117')}\" />
      <stop offset=\"50%\" stop-color=\"{g('bg_mid', '#161b22')}\" />
      <stop offset=\"100%\" stop-color=\"{g('bg_end', '#0d1117')}\" />
    </linearGradient>
    <radialGradient id=\"vignette\" cx=\"50%\" cy=\"50%\" r=\"70%\">
      <stop offset=\"50%\" stop-color=\"#000\" stop-opacity=\"0\" />
      <stop offset=\"100%\" stop-color=\"#000\" stop-opacity=\"0.35\" />
    </radialGradient>
    <linearGradient id=\"keyLight\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"100%\">
      <stop offset=\"0%\" stop-color=\"#ffffff\" stop-opacity=\"0.06\" />
      <stop offset=\"100%\" stop-color=\"#000000\" stop-opacity=\"0\" />
    </linearGradient>

    <!-- Patterns -->
    <pattern id=\"dots\" x=\"0\" y=\"0\" width=\"20\" height=\"20\" patternUnits=\"userSpaceOnUse\">
      <circle cx=\"2\" cy=\"2\" r=\"1\" fill=\"{g('dots_color', '#94a3b8')}\" opacity=\"0.12\" />
    </pattern>
    <pattern id=\"grid\" x=\"0\" y=\"0\" width=\"30\" height=\"30\" patternUnits=\"userSpaceOnUse\">
      <path d=\"M 30 0 L 0 0 0 30\" fill=\"none\" stroke=\"{g('dots_color', '#94a3b8')}\" stroke-width=\"0.5\" opacity=\"0.06\" />
    </pattern>
    <pattern id=\"scanlines\" width=\"4\" height=\"4\" patternUnits=\"userSpaceOnUse\">
      <line x1=\"0\" y1=\"2\" x2=\"4\" y2=\"2\" stroke=\"#ffffff\" stroke-width=\"1\" opacity=\"0.03\" />
    </pattern>

    <!-- Title gradient & filters -->
    <linearGradient id=\"titleGrad\" x1=\"0%\" y1=\"0%\" x2=\"100%\" y2=\"0%\">
      <stop offset=\"0%\" stop-color=\"{g('title_start', '#e0eafc')}\" />
      <stop offset=\"50%\" stop-color=\"{g('title_mid', '#b8c6db')}\" />
      <stop offset=\"100%\" stop-color=\"{g('title_end', '#94a3b8')}\" />
    </linearGradient>
    <filter id=\"titleShadow\" x=\"-5%\" y=\"-5%\" width=\"110%\" height=\"110%\">
      <feDropShadow dx=\"0\" dy=\"2\" stdDeviation=\"3\" flood-color=\"#000000\" flood-opacity=\"0.4\" />
    </filter>
    <filter id=\"titleGlow\" x=\"-20%\" y=\"-20%\" width=\"140%\" height=\"140%\">
      <feGaussianBlur in=\"SourceAlpha\" stdDeviation=\"4\" result=\"blur\" />
      <feFlood flood-color=\"{g('title_glow', '#94a3b8')}\" flood-opacity=\"0.25\" result=\"color\" />
      <feComposite in=\"color\" in2=\"blur\" operator=\"in\" result=\"glow\" />
      <feMerge>
        <feMergeNode in=\"glow\" />
        <feMergeNode in=\"SourceGraphic\" />
      </feMerge>
    </filter>

    <!-- Terminal glow -->
    <filter id=\"termGlow\" x=\"-10%\" y=\"-10%\" width=\"120%\" height=\"120%\">
      <feGaussianBlur in=\"SourceAlpha\" stdDeviation=\"12\" result=\"blur\" />
      <feFlood flood-color=\"{g('terminal_glow', '#94a3b8')}\" flood-opacity=\"0.15\" result=\"color\" />
      <feComposite in=\"color\" in2=\"blur\" operator=\"in\" result=\"glow\" />
      <feMerge>
        <feMergeNode in=\"glow\" />
        <feMergeNode in=\"SourceGraphic\" />
      </feMerge>
    </filter>

    <!-- Progress gradients -->
    {progress_defs}
""".strip()

    def render(self) -> str:
        return f"""
  <!-- Base background -->
  <rect width=\"{self.w}\" height=\"{self.h}\" fill=\"url(#bg)\" />
  <rect width=\"{self.w}\" height=\"{self.h}\" fill=\"url(#grid)\" />
  <rect width=\"{self.w}\" height=\"{self.h}\" fill=\"url(#dots)\" />

  <!-- Vignette + key light -->
  <rect width=\"{self.w}\" height=\"{self.h}\" fill=\"url(#vignette)\" pointer-events=\"none\" />
  <rect width=\"{self.w}\" height=\"{self.h}\" fill=\"url(#keyLight)\" pointer-events=\"none\" />
""".rstrip()
