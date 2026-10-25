"""Offline baseline checks. Never exercise hardware, credentials or deployment."""
import ast
import json
import os
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'.kodi/config.json').read_text())
profile=config['profile']


def run(*args):
    subprocess.run(args,cwd=ROOT,check=True)


if profile in ('python','hardware-python'):
    paths=[p for p in ROOT.rglob('*.py') if not any(part.startswith('.') or part in
           ('node_modules','__pycache__') for part in p.relative_to(ROOT).parts)]
    assert paths,'No Python sources found'
    for p in paths:
        ast.parse(p.read_text(),filename=str(p.relative_to(ROOT)))
    tests=ROOT/'tests'
    if tests.is_dir(): run(sys.executable,'-m','pytest','tests','-q','-p','no:cacheprovider')
    print(f'Validated {len(paths)} Python sources; hardware and network integration require a bench check.')
elif profile=='hermes':
    run(sys.executable,'-m','pytest','plugins/telegram-session-reset-handoff/tests','-q','-p','no:cacheprovider')
elif profile=='astro':
    run('npm','run','build')
elif profile=='static':
    class Assets(HTMLParser):
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs)
            value=attrs.get('src') if tag in ('img','script','source') else None
            if value and not urlsplit(value).scheme and not value.startswith('//'):
                target=ROOT/unquote(urlsplit(value).path.lstrip('/'))
                assert target.is_file(),f'Missing local asset: {target.relative_to(ROOT)}'
    assert (ROOT/'index.html').is_file(),'Missing index.html'
    for p in ROOT.glob('*.html'):
        text=p.read_text(); assert '<html' in text.lower() and '</html>' in text.lower(),str(p)
        Assets().feed(text)
    print('HTML and local asset references passed.')
elif profile=='inventory':
    import yaml
    data=yaml.safe_load((ROOT/'inventory.yaml').read_text())
    assert isinstance(data,dict) and isinstance(data.get('nodes'),dict) and data['nodes']
    assert (ROOT/'README.md').is_file()
    print(f'Inventory structure passed: {len(data["nodes"])} nodes. No infrastructure commands run.')
else:
    raise ValueError('Unknown operator-selected QA profile')
