from __future__ import annotations
import os
import platform
import subprocess
from ..base import BaseComponent, xml_escape
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class Component(BaseComponent):
    config_schema = {}
    z_index = 100
    section_name = 'metrics'
    description = 'Live system metrics (CPU, RAM, disk)'
    component_id = 'metrics'

    def _get_live_metrics(self, entries_config):
        """Replace placeholders in config entries with live system data."""
        user = os.getenv('USER') or os.getenv('USERNAME') or 'unknown'
        hostname = platform.node()
        distro = 'Unknown'
        if platform.system() == 'Linux':
            try:
                if hasattr(platform, 'freedesktop_os_release'):
                    release = platform.freedesktop_os_release()
                    distro = release.get('NAME', release.get('ID', 'Linux'))
                else:
                    with open('/etc/os-release') as f:
                        for line in f:
                            if line.startswith('NAME='):
                                distro = line.split('=', 1)[1].strip().strip('"')
                                break
            except (FileNotFoundError, PermissionError, OSError):
                distro = platform.system()
        else:
            distro = platform.system()
        wm = os.getenv('XDG_CURRENT_DESKTOP') or os.getenv('DESKTOP_SESSION') or 'unknown'
        if wm == 'unknown' and platform.system() == 'Linux':
            try:
                result = subprocess.run(['wmctrl', '-m'], capture_output=True, text=True, timeout=1)
                for line in result.stdout.splitlines():
                    if line.startswith('Name:'):
                        wm = line.split(':', 1)[1].strip()
                        break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
        values = {'user': user, 'hostname': hostname, 'distro': distro, 'wm': wm, 'cpu_percent': 'N/A', 'ram_used': 'N/A', 'ram_total': 'N/A', 'ram_percent': 'N/A', 'disk_used': 'N/A', 'disk_total': 'N/A', 'disk_percent': 'N/A'}
        if HAS_PSUTIL:
            values['cpu_percent'] = f'{psutil.cpu_percent(interval=0.1)}%'
            mem = psutil.virtual_memory()
            values['ram_used'] = self._bytes_to_human(mem.used)
            values['ram_total'] = self._bytes_to_human(mem.total)
            values['ram_percent'] = f'{mem.percent}%'
            disk = psutil.disk_usage('/')
            values['disk_used'] = self._bytes_to_human(disk.used)
            values['disk_total'] = self._bytes_to_human(disk.total)
            values['disk_percent'] = f'{disk.percent}%'
        live_entries = []
        for entry in entries_config:
            for key, val in values.items():
                entry = entry.replace(f'{{{key}}}', str(val))
            live_entries.append(entry)
        return live_entries

    @staticmethod
    def _bytes_to_human(b):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if b < 1024.0:
                return f'{b:.1f} {unit}'
            b /= 1024.0
        return f'{b:.1f} PB'

    def render(self) -> str:
        cfg = self.cfg.get('metrics') or {} if isinstance(self.cfg.get('metrics'), dict) else {}
        entry_templates = cfg.get('entries', ['{user}@{hostname}', 'Distro: {distro}, WM: {wm}', 'CPU: {cpu_percent}', 'RAM: {ram_used} / {ram_total} ({ram_percent})', 'Disk: {disk_used} / {disk_total} ({disk_percent})'])
        entries = self._get_live_metrics(entry_templates)
        x = int(cfg.get('x', 85))
        y = self.y_offset + int(cfg.get('y_offset', 20))
        font_size = int(cfg.get('font_size', 14))
        gap = int(cfg.get('gap', 10))
        show_bars = cfg.get('show_bars', True)
        bar_offset = int(cfg.get('bar_x_offset', 200))
        label_color = self.col.get('metrics_label', '#6272a4')
        value_color = self.col.get('metrics_value', '#f8f8f2')
        bar_bg = self.col.get('metrics_bar_bg', '#313244')
        bar_fill = self.col.get('metrics_bar_fill', '#50fa7b')
        parts = []
        cur_y = y
        for entry in entries:
            parts.append(f'''<text x="{x}" y="{cur_y}" font-family="'Inter', sans-serif" font-size="{font_size}" fill="{label_color}">{xml_escape(entry)}</text>''')
            if show_bars and '%' in entry:
                import re
                match = re.search('(\\d+(?:\\.\\d+)?)%', entry)
                if match:
                    pct = float(match.group(1))
                    bar_w = 150
                    fill_w = int(bar_w * pct / 100)
                    bar_y = cur_y - font_size / 2 - 3
                    parts.append(f'<rect x="{x + bar_offset}" y="{bar_y:.1f}" width="{bar_w}" height="6" rx="3" fill="{bar_bg}" />')
                    parts.append(f'<rect x="{x + bar_offset}" y="{bar_y:.1f}" width="{fill_w}" height="6" rx="3" fill="{bar_fill}" />')
            cur_y += gap + font_size
        self.used_height = cur_y - self.y_offset
        return '\n'.join(parts)