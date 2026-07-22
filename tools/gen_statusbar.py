#!/usr/bin/env python3
"""A tmux-style status bar to close the page, matching the terminal
banner's width and palette. One cohesive element instead of a ragged
row of chips."""
import os

OUT = "/Users/abhineshdahal/Documents/Raft/DahalAb1/assets"
os.makedirs(OUT, exist_ok=True)

W, H = 880, 32
BG, BORDER = "#161b22", "#30363d"
INK, MUT, GREEN = "#e6edf3", "#7d8590", "#3fb950"
FS = 12.5
CW = 7.55
PAD = 14

def seg(x, label, color, mode_box=False):
    """Returns (svg, next_x). mode_box draws a filled left segment."""
    w = len(label) * CW
    if mode_box:
        box_w = w + PAD * 2
        s = (f'<rect x="1" y="1" width="{box_w:.0f}" height="{H - 2}" fill="{MUT}" fill-opacity=".14"/>'
             f'<text x="{x + PAD:.0f}" y="{H / 2 + 4.4:.0f}" font-size="{FS}" fill="{color}" font-weight="600">{label}</text>')
        return s, x + box_w
    s = f'<text x="{x + PAD:.0f}" y="{H / 2 + 4.4:.0f}" font-size="{FS}" fill="{color}">{label}</text>'
    return s, x + PAD + w

parts = []
x = 0

# left: name, in a filled "mode" block like tmux's session name
s, x = seg(x, "abhinesh dahal", INK, mode_box=True)
parts.append(s)
parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{BORDER}" stroke-width="1"/>')

s, x = seg(x, "go · c++ · python", MUT)
parts.append(s)

# right: availability, with a live dot
right_label = "open to summer 2027"
rw = len(right_label) * CW
rx = W - PAD - rw
parts.append(f'<text x="{rx:.0f}" y="{H / 2 + 4.4:.0f}" font-size="{FS}" fill="{GREEN}">{right_label}</text>')
dot_x = rx - 16
parts.append(f'''<circle cx="{dot_x:.0f}" cy="{H / 2:.0f}" r="3.5" fill="{GREEN}">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>''')
parts.append(f'<line x1="{dot_x - 14:.0f}" y1="0" x2="{dot_x - 14:.0f}" y2="{H}" stroke="{BORDER}" stroke-width="1"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="Abhinesh Dahal, Go, C++, and Python, open to Summer 2027"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
  <clipPath id="r"><rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="6"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{W}" height="{H}" fill="{BG}"/>
    {''.join(parts)}
  </g>
  <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="6" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
</svg>'''

path = f"{OUT}/statusbar.svg"
open(path, "w").write(svg)
print(f"wrote {path} ({W}x{H})")
