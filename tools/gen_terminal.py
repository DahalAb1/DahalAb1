#!/usr/bin/env python3
"""Generate a mac-terminal-style animated banner: commands typed live,
real raft-demo output printed. Single SVG, self-backgrounded, works on
both GitHub themes."""

import os

OUT = "/Users/abhineshdahal/Documents/Raft/DahalAb1/assets"
os.makedirs(OUT, exist_ok=True)

CYCLE = 18.0
CHAR_W = 7.7
FS = 14
LH = 22
X_PROMPT = 26
PROMPT = "~ %"
X_CMD = X_PROMPT + int(4 * CHAR_W)  # after "~ % "

BG, BORDER, BAR = "#0d1117", "#30363d", "#161b22"
INK, MUT, DIM, GREEN = "#e6edf3", "#7d8590", "#8b949e", "#3fb950"
DOTS = ["#ff5f57", "#febc2e", "#28c840"]

rows = []  # (kind, y, payload)
Y0 = 72

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def discrete(attr, pairs, extra=""):
    """pairs: list of (time, value); builds a discrete SMIL animate."""
    vals = ";".join(str(v) for _, v in pairs)
    times = ";".join(f"{t / CYCLE:.4f}" for t, _ in pairs)
    return (f'<animate attributeName="{attr}" values="{vals}" keyTimes="{times}" '
            f'calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite" {extra}/>')

def appear(t_on, t_off=CYCLE - 0.5):
    pairs = [(0, 0)]
    if t_on > 0: pairs.append((t_on, 1))
    else: pairs[0] = (0, 1)
    pairs.append((t_off, 0))
    if t_off < CYCLE: pairs.append((CYCLE, 0))
    # dedupe trailing
    return discrete("opacity", pairs)

parts = []

def prompt_line(y, t_on):
    parts.append(f'''<g opacity="0">{appear(t_on)}
      <text x="{X_PROMPT}" y="{y}" font-size="{FS}" fill="{MUT}">{esc(PROMPT)}</text></g>''')

def typed_command(idx, y, cmd, t_start, t_per_char=0.11):
    n = len(cmd)
    w = n * CHAR_W
    width_pairs = [(0, 0)]
    if t_start > 0: width_pairs.append((t_start, 0))
    for ch in range(1, n + 1):
        width_pairs.append((t_start + ch * t_per_char, f"{ch * CHAR_W:.1f}"))
    t_done = t_start + n * t_per_char
    width_pairs.append((CYCLE - 0.5, 0))
    vals = ";".join(str(v) for _, v in width_pairs)
    times = ";".join(f"{t / CYCLE:.4f}" for t, _ in width_pairs)
    parts.append(f'''
    <clipPath id="cmd{idx}"><rect x="{X_CMD}" y="{y - 14}" height="20" width="0">
      <animate attributeName="width" values="{vals}" keyTimes="{times}"
               calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>
    </rect></clipPath>
    <text x="{X_CMD}" y="{y}" clip-path="url(#cmd{idx})" font-size="{FS}"
          fill="{INK}" textLength="{w:.0f}">{esc(cmd)}</text>''')
    # moving block cursor while typing
    x_pairs = [(t, f"{X_CMD + 2 + (float(v) if v != 0 else 0):.1f}") for t, v in width_pairs]
    xvals = ";".join(v for _, v in x_pairs)
    parts.append(f'''
    <g opacity="0">{appear(t_start - 0.45 if t_start > 0.45 else 0, t_done + 0.6)}
      <rect y="{y - 12}" width="8" height="15" fill="{INK}" fill-opacity=".65">
        <animate attributeName="x" values="{xvals}" keyTimes="{times}"
                 calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>
      </rect></g>''')
    return t_done

def output_line(y, t_on, spans):
    body = "".join(f'<tspan fill="{col}">{esc(txt)}</tspan>' for txt, col in spans)
    parts.append(f'''<g opacity="0">{appear(t_on)}
      <text x="{X_PROMPT}" y="{y}" font-size="{FS}">{body}</text></g>''')

# ---- the script of the terminal session ----
y = Y0
prompt_line(y, 0)
t = typed_command(0, y, "whoami", 0.7)
y += LH
output_line(y, t + 0.35, [("abhinesh dahal · cs + applied math @ texas state", DIM)])

y += LH
prompt_line(y, t + 1.3)
t2 = typed_command(1, y, "cat focus.txt", t + 1.7)
y += LH
output_line(y, t2 + 0.4, [("distributed systems · software engineering", DIM)])

y += LH
prompt_line(y, t2 + 1.5)
t3 = typed_command(2, y, "echo $SEEKING", t2 + 1.9)
y += LH
output_line(y, t3 + 0.4, [("swe internship · ", DIM), ("summer 2027", GREEN)])

y += LH
idle_on = t3 + 1.2
prompt_line(y, idle_on)
parts.append(f'''<g opacity="0">{appear(idle_on)}
  <rect x="{X_CMD + 2}" y="{y - 12}" width="8" height="15" fill="{INK}" fill-opacity=".65">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.55;0.5501;1" dur="1.1s" repeatCount="indefinite"/>
  </rect></g>''')

H = y + 26
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 {H}" width="880" height="{H}" role="img"
     aria-label="Terminal session: Abhinesh Dahal, CS and Applied Math student at Texas State; focused on distributed systems and software engineering; seeking a Summer 2027 software engineering internship"
     font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
  <rect x="1" y="1" width="878" height="{H - 2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <path d="M1 35 h878" stroke="{BORDER}" stroke-width="1"/>
  <rect x="1.75" y="1.75" width="876.5" height="33" rx="9" fill="{BAR}"/>
  <circle cx="26" cy="18" r="6" fill="{DOTS[0]}"/>
  <circle cx="46" cy="18" r="6" fill="{DOTS[1]}"/>
  <circle cx="66" cy="18" r="6" fill="{DOTS[2]}"/>
  <text x="440" y="23" text-anchor="middle" font-size="12" fill="{MUT}">abhinesh · zsh · 110x24</text>
  {''.join(parts)}
</svg>'''

path = f"{OUT}/terminal.svg"
open(path, "w").write(svg)
print(f"wrote {path} ({len(svg)} bytes, {H}px tall)")
