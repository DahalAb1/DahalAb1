#!/usr/bin/env python3
"""Generate compact project diagrams. Motion ends within five seconds."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets'
TITLES = {
    'consensus': ('Raft replication', 'A leader sends a write to two followers.'),
    'resize': ('Incremental hash-table resizing', 'Entries move from the old table to a larger table a little at a time.'),
    'sanscue': ('SansCue check-in workflow', 'Speech informs an AI draft, a moderator reviews it, and the audience responds.'),
    'network': ('Neural-network forward pass', 'Two inputs pass through two hidden neurons to one output.'),
}


def render(kind, dark, animated):
    bg, border, ink, accent, soft = (
        ('#11191c', '#35454a', '#aebfc4', '#60cbb5', '#233e39') if dark else
        ('#f6faf9', '#cdded7', '#526f68', '#167b66', '#deeee7')
    )
    def label(x, y, text):
        return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{ink}">{text}</text>'
    def line(x1, y1, x2, y2):
        return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{border}" stroke-width="1.5"/>'
    def node(x, y, r=6):
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{soft}" stroke="{accent}" stroke-width="1.5"/>'
    def packet(x, y, dx, dy, delay=0):
        return f'<circle class="packet" cx="{x}" cy="{y}" r="3" fill="{accent}" style="--dx:{dx}px;--dy:{dy}px;animation-delay:{delay}s"/>'
    parts = []
    if kind == 'consensus':
        parts += [line(70, 32, 220, 17), line(70, 32, 220, 47)]
        parts += [packet(70, 32, 150, -15), packet(70, 32, 150, 15)]
        parts += [node(70, 32, 10), node(220, 17), node(220, 47)]
        parts += [label(70, 65, 'leader'), label(300, 37, 'two followers')]
    elif kind == 'resize':
        parts += [line(107, 31, 215, 31)]
        for x, count in [(25, 4), (215, 8)]:
            for i in range(count):
                parts += [f'<rect x="{x + i*20}" y="23" width="15" height="16" rx="3" fill="{soft}" stroke="{border}"/>']
        parts += [packet(92, 31, 150, 0)]
        parts += [label(62, 65, 'old table'), label(292, 65, 'grow a little at a time')]
    elif kind == 'sanscue':
        positions = [35, 145, 255, 365]
        parts += [line(35, 29, 365, 29), packet(35, 29, 330, 0)]
        parts += [node(x, 29) for x in positions]
        parts += [label(x, 61, s) for x, s in zip(positions, ['speech', 'AI draft', 'review', 'audience'])]
    else:
        for y in [18, 42]:
            for target in [18, 42]:
                parts += [line(60, y, 200, target)]
            parts += [line(200, y, 340, 30)]
        parts += [packet(60, 18, 140, 0), packet(60, 42, 140, 0)]
        parts += [packet(200, 18, 140, 12, .9), packet(200, 42, 140, -12, .9)]
        parts += [node(x, y) for x, ys in [(60, [18, 42]), (200, [18, 42]), (340, [30])] for y in ys]
        parts += [label(60, 66, 'inputs'), label(200, 66, 'hidden layer'), label(340, 66, 'output')]
    motion = '''
    .packet { opacity:0; animation:travel 1.8s ease-in-out 2; }
    @keyframes travel {
      0%,12% { opacity:0; transform:translate(0,0); }
      22% { opacity:1; }
      72% { opacity:1; transform:translate(var(--dx),var(--dy)); }
      84%,100% { opacity:0; transform:translate(var(--dx),var(--dy)); }
    }
    @media(prefers-reduced-motion:reduce) { .packet { animation:none; } }
    ''' if animated else '.packet { opacity:0; }'
    title, desc = TITLES[kind]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="76" viewBox="0 0 400 76" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title><desc id="desc">{desc} Schematic illustration.</desc>
  <style>{motion}</style>
  <rect width="400" height="76" rx="8" fill="{bg}"/>
  <g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="13">{''.join(parts)}</g>
</svg>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for kind in TITLES:
        for dark in (False, True):
            for animated in (True, False):
                name = f"{kind}-{'static-' if not animated else ''}{'dark' if dark else 'light'}.svg"
                (OUT / name).write_text(render(kind, dark, animated))
    print('Generated 16 project diagrams (light, dark, animated, reduced motion).')
