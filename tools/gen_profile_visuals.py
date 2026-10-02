#!/usr/bin/env python3
"""Generate README illustrations with no dependencies.

Run `python3 tools/gen_profile_visuals.py` from any working directory.
The election plays once, with a readable final frame when CSS animations
are unavailable or the reader requests reduced motion.
"""

from html import escape
from pathlib import Path


OUT = Path(__file__).resolve().parents[1] / "assets"
PALETTES = {
    "light": {
        "ink": "#1f2328", "muted": "#59636e", "line": "#d1d9e0",
        "surface": "#f6f8fa", "blue": "#0969da", "blue_bg": "#ddf4ff",
        "green": "#116b45", "green_bg": "#dafbe1",
        "red": "#b42335", "red_bg": "#fff0f1",
    },
    "dark": {
        "ink": "#f0f6fc", "muted": "#a6b0bb", "line": "#3d444d",
        "surface": "#151b23", "blue": "#79c0ff", "blue_bg": "#122c46",
        "green": "#7ee2a8", "green_bg": "#122f24",
        "red": "#ff9ba8", "red_bg": "#361c26",
    },
}


def text(x, y, label, color, size=16, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{escape(label)}</text>'
    )


def svg(width, height, title, description, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" '
        'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="desc">{escape(description)}</desc>\n'
        + "\n".join(body) + "\n</svg>\n"
    )


def server(cx, y, name, role, color, bg, width, offline=False, leader=False):
    x = cx - width / 2
    body = [
        f'<rect x="{x}" y="{y}" width="{width}" height="72" rx="6" '
        f'fill="{bg}" stroke="{color}" stroke-width="1.5"'
        + (' stroke-dasharray="4 4"' if offline else '') + '/>',
        text(cx, y + 29, name, color, 22, 600, "middle"),
        text(cx, y + 53, role, color, 15, 400, "middle"),
    ]
    if leader:
        body.append(
            f'<path d="M{cx - 13} {y - 9} h26" stroke="{color}" '
            'stroke-width="4" stroke-linecap="round"/>'
        )
    if offline:
        body.append(
            f'<path d="M{cx - 4} {y - 13} l8 8 m0 -8 l-8 8" '
            f'stroke="{color}" stroke-width="2"/>'
        )
    return "\n".join(body)


def election(p, compact, animated=True):
    width, height = (360, 228) if compact else (720, 224)
    centers = [62, 180, 298] if compact else [130, 360, 590]
    node_width = 96 if compact else 144
    y = 83
    body = [
        """<style>
          .phase { opacity: 0; }
          .recovered { opacity: 1; }
          @media (prefers-reduced-motion: no-preference) {
            .running { animation: phase-running 4.8s step-end 1 both; }
            .failed { animation: phase-failed 4.8s step-end 1 both; }
            .recovered { animation: phase-recovered 4.8s step-end 1 both; }
          }
          @keyframes phase-running { 0% { opacity: 1; } 33.333%, 100% { opacity: 0; } }
          @keyframes phase-failed { 0% { opacity: 0; } 33.333% { opacity: 1; } 66.667%, 100% { opacity: 0; } }
          @keyframes phase-recovered { 0% { opacity: 0; } 66.667%, 100% { opacity: 1; } }
        </style>""",
        text(8, 20, "RAFT / THREE-SERVER EXAMPLE", p["muted"], 12, 600),
    ]
    phases = [
        ("running", "A leads the cluster.", ["Leader", "Follower", "Follower"], 0),
        ("failed", "A stops responding.", ["Offline", "Follower", "Follower"], None),
        ("recovered", "B wins a majority with C.", ["Offline", "Leader", "Follower"], 1),
    ]
    for phase_index, (name, caption, roles, leader) in enumerate(phases):
        if not animated and name != "recovered":
            continue
        body.extend([f'<g class="phase {name}">', text(8, 51, caption, p["ink"], 22, 600)])
        for left, right in zip(centers, centers[1:]):
            active = phase_index == 0 or (phase_index == 2 and left == centers[1])
            color = p["blue"] if phase_index == 0 else p["green"]
            body.append(
                f'<path d="M{left + node_width / 2 + 4} {y + 36} '
                f'H{right - node_width / 2 - 4}" fill="none" '
                f'stroke="{color if active else p["line"]}" stroke-width="2"'
                + (' stroke-dasharray="3 4"' if not active else '') + '/>'
            )
        for i, (cx, role) in enumerate(zip(centers, roles)):
            offline = role == "Offline"
            key = "red" if offline else ("blue" if phase_index == 0 else "green")
            color = p[key] if offline or i == leader else p["muted"]
            bg = p[key + "_bg"] if offline or i == leader else p["surface"]
            body.append(server(cx, y, chr(65 + i), role, color, bg, node_width, offline, i == leader))
        for i, (cx, label) in enumerate(zip(centers, ["Running", "Leader fails", "New leader"])):
            active = i == phase_index
            color = p[["blue", "red", "green"][i]] if active else p["muted"]
            body.append(text(cx, 191, f"0{i + 1}", color, 12, 600, "middle"))
            body.append(text(cx, 212, label, color, 15, 600 if active else 400, "middle"))
        body.append('</g>')
    if not animated:
        body[0] = '<style>.recovered { opacity: 1; }</style>'
    return svg(width, height, "A Raft cluster elects a new leader", "Illustration, not a live cluster. A leads; A fails; B and C form a majority and elect B. The animated version plays once and holds the recovered state.", body)


def latency(p, compact):
    width, height = (360, 212) if compact else (720, 196)
    right = 188 if compact else 380
    body = [
        text(8, 20, "STORAGE / RESIZE BENCHMARK", p["muted"], 12, 600),
        text(8, 51, "Worst single insert", p["ink"], 22, 600),
        text(8, 76, "4 million keys. Lower is better.", p["muted"], 15),
        f'<path d="M{width / 2} 94 V162" stroke="{p["line"]}"/>',
        text(8, 126, "0.429", p["green"], 36, 600),
        text(112, 126, "ms", p["muted"], 17),
        text(right, 126, "241", p["ink"], 36, 600),
        text(right + 71, 126, "ms", p["muted"], 17),
        text(8, 155, "Incremental HMap", p["ink"], 15),
        text(right, 155, "std::unordered_map", p["ink"], 15),
        text(8, 192 if compact else 189, "Apple M2 / -O2 / in-process", p["muted"], 14),
    ]
    return svg(width, height, "Worst insert latency at four million keys", "Incremental HMap: 0.429 milliseconds. std::unordered_map: 241 milliseconds. Apple M2, -O2, in-process microbenchmark. Custom entries and hashes prepared before timing; std::unordered_map not pre-reserved. Source: https://github.com/DahalAb1/Redis/tree/main/bench", body)


def main():
    OUT.mkdir(exist_ok=True)
    for theme, palette in PALETTES.items():
        for compact in (False, True):
            suffix = f'{"compact-" if compact else ""}{theme}'
            for name, render in (("raft-election", election), ("resize-latency", latency)):
                path = OUT / f"{name}-{suffix}.svg"
                path.write_text(render(palette, compact), encoding="utf-8")
                print(path.relative_to(OUT.parent))
            path = OUT / f"raft-election-static-{suffix}.svg"
            path.write_text(election(palette, compact, animated=False), encoding="utf-8")
            print(path.relative_to(OUT.parent))


if __name__ == "__main__":
    main()
