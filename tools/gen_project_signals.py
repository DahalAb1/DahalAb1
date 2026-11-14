#!/usr/bin/env python3
"""Play all diagrams once, pause, then repeat them in project order."""
from pathlib import Path
import re

OUT = Path(__file__).resolve().parents[1] / 'assets'
# Every SVG uses this schedule relative to its load time. GitHub embeds the
# files independently, so network/lazy-loading can offset their start clocks.
DURATIONS = {'consensus': 4.8, 'resize': 4.6, 'sanscue': 4.8, 'network': 2.7}
OPENING_PAUSE = 1
INTRO_END = max(DURATIONS.values())
LOOP_START = INTRO_END + OPENING_PAUSE
LOOP_SECONDS = sum(DURATIONS.values())
TITLES = {
    'consensus': ('Raft leader failover', "In this four-server illustration, A goes offline. After an election timeout, B requests votes from C and D. With its own vote and both replies, B becomes leader with a three-of-four majority. A stays offline."),
    'resize': ('A request through the Redis-style server', 'GET city travels from a client through the event loop to an in-memory table. The matching value, Austin, returns to the client.'),
    'sanscue': ('SansCue audience feedback loop', 'Speaker context informs an AI check-in draft. A moderator reviews and publishes it. Audience clarity feedback returns to the speaker.'),
    'network': ('Neural-network forward pass', 'Two inputs pass through two hidden neurons to one output.'),
}


def schedule_timeline(css, kind):
    """Give each effect an opening pass and a slot in the shared repeat cycle."""
    keyframes = {}
    pattern = r'@keyframes\s+([\w-]+)\s*\{((?:[^{}]|\{[^{}]*\})*)\}'
    for match in re.finditer(pattern, css):
        frames = {}
        for frame in re.finditer(r'([\d.,%\s]+)\{([^{}]*)\}', match[2]):
            for percent in frame[1].split(','):
                frames[float(percent.strip().rstrip('%'))] = frame[2].strip()
        keyframes[match[1]] = frames
    css = re.sub(pattern, '', css)
    duration = DURATIONS[kind]
    slot = sum(value for name, value in list(DURATIONS.items())[:list(DURATIONS).index(kind)])
    # Internal stages are part of the timeline, not per-element CSS delays.
    offsets = {'grant-vote-late': .12, 'travel-output': .9}
    aliases = {'grant-vote-late': 'grant-vote', 'travel-output': 'travel'}
    generated = []

    def scheduled_frames(source, source_seconds, start, span, end):
        final = source[100]
        frames = {0: final, span: final}
        if start > 0:
            frames[start - .00001] = final
        for percent, declarations in sorted(source.items()):
            time = min(start + source_seconds * percent / 100, end)
            frames[time] = declarations
        frames[end] = final
        return ''.join(f'{time / span * 100:.8f}%{{{body}}}'
                       for time, body in sorted(frames.items()))

    def animation(match):
        name, seconds, easing = match[1], float(match[2]), match[3]
        source = keyframes[aliases.get(name, name)]
        offset = offsets.get(name, 0)
        opening = scheduled_frames(source, seconds, offset, duration, duration)
        repeat = scheduled_frames(source, seconds, slot + offset, LOOP_SECONDS, slot + duration)
        generated.extend([f'@keyframes {name}-intro{{{opening}}}',
                          f'@keyframes {name}-sequence{{{repeat}}}'])
        return (f'animation:{name}-intro {duration:g}s {easing} 0s 1, '
                f'{name}-sequence {LOOP_SECONDS:g}s {easing} {LOOP_START:g}s infinite;')

    css = re.sub(r'animation:([\w-]+) ([\d.]+)s (ease-in-out|linear) 1;', animation, css)
    return css + ''.join(generated)


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
        return f'<circle class="packet{" output" if delay else ""}" cx="{x}" cy="{y}" r="3" fill="{accent}" style="--dx:{dx}px;--dy:{dy}px"/>'
    parts = []
    height = 76
    extra_motion = ''
    if kind == 'consensus':
        height = 156
        parts += [f'''<g font-size="10" letter-spacing="1">{label(200, 16, 'FOUR SERVERS · MAJORITY = 3')}</g>
        <path d="M92 74 H144" stroke="{border}" stroke-width="1.5" stroke-dasharray="3 4"/>
        <g fill="none" stroke="{border}" stroke-width="1.5">
          <path d="M234 65 L300 39 M300 49 L234 75"/>
          <path d="M234 81 L300 101 M300 111 L234 91"/>
        </g>
        <g class="old-server" opacity=".45">
          <rect x="16" y="54" width="76" height="42" rx="7" fill="{bg}" stroke="{border}"/>
          <text x="54" y="71" text-anchor="middle" fill="{ink}" font-size="14" font-weight="600">A</text>
          <g class="initial-role" opacity="0">{label(54, 88, 'leader')}</g>
          <g class="offline-role">{label(54, 88, 'offline')}</g>
        </g>
        <rect x="144" y="54" width="90" height="42" rx="7" fill="{bg}" stroke="{border}"/>
        <rect class="new-leader" x="144" y="54" width="90" height="42" rx="7" fill="{soft}" stroke="{accent}" stroke-width="1.5"/>
        <text x="189" y="71" text-anchor="middle" fill="{accent}" font-size="14" font-weight="600">B</text>
        <g class="follower-role" opacity="0">{label(189, 88, 'follower')}</g>
        <g class="candidate-role" opacity="0">{label(189, 88, 'candidate')}</g>
        <g class="leader-role">{label(189, 88, 'leader')}</g>
        <rect x="300" y="25" width="84" height="42" rx="7" fill="{bg}" stroke="{border}"/>
        <text x="342" y="42" text-anchor="middle" fill="{ink}" font-size="14" font-weight="600">C</text>
        {label(342, 59, 'follower')}
        <rect x="300" y="87" width="84" height="42" rx="7" fill="{bg}" stroke="{border}"/>
        <text x="342" y="104" text-anchor="middle" fill="{ink}" font-size="14" font-weight="600">D</text>
        {label(342, 121, 'follower')}
        <g class="stage-start" opacity="0">{label(200, 146, 'A leads the cluster')}</g>
        <g class="stage-timeout" opacity="0">{label(200, 146, 'A goes offline · election timeout')}</g>
        <g class="stage-vote" opacity="0">{label(200, 146, 'B votes for itself and asks C + D')}</g>
        <g class="stage-done">{label(200, 146, 'B + C + D · 3 of 4 votes · B elected')}</g>
        <circle class="packet vote-request" cx="234" cy="65" r="3" fill="{accent}" style="--dx:66px;--dy:-26px"/>
        <circle class="packet vote-request" cx="234" cy="81" r="3" fill="{accent}" style="--dx:66px;--dy:20px"/>
        <circle class="packet vote-reply" cx="300" cy="49" r="3" fill="{accent}" style="--dx:-66px;--dy:26px"/>
        <circle class="packet vote-reply vote-reply-late" cx="300" cy="111" r="3" fill="{accent}" style="--dx:-66px;--dy:-20px"/>
        ''']
        if animated:
            # The default SVG is the final state, including without CSS animation.
            # Opacity intervals keep the text changes discrete and non-overlapping.
            intervals = {
                'initial-role': (0, 20), 'offline-role': (20, 100),
                'follower-role': (0, 38), 'candidate-role': (38, 84),
                'leader-role': (84, 100), 'new-leader': (84, 100),
                'stage-start': (0, 20), 'stage-timeout': (20, 38),
                'stage-vote': (38, 84), 'stage-done': (84, 100),
            }
            for name, (start, end) in intervals.items():
                keys = ('0%{opacity:1;}' if start == 0 else
                        f'0%,{start-.01}%{{opacity:0;}}{start}%{{opacity:1;}}')
                keys += ('100%{opacity:1;}' if end == 100 else
                         f'{end-.01}%{{opacity:1;}}{end}%,100%{{opacity:0;}}')
                extra_motion += f'.{name}{{animation:{name} 4.8s linear 1;}}@keyframes {name}{{{keys}}}'
            extra_motion += '''
            .old-server { animation:disconnect 4.8s linear 1; }
            .vote-request { animation:ask-vote 4.8s ease-in-out 1; }
            .vote-reply { animation:grant-vote 4.8s ease-in-out 1; }
            .vote-reply-late { animation:grant-vote-late 4.8s ease-in-out 1; }
            @keyframes disconnect {
              0%,19.99% { opacity:1; } 20%,100% { opacity:.45; }
            }
            @keyframes ask-vote {
              0%,40% { opacity:0; transform:translateX(0); }
              44% { opacity:1; transform:translateX(0); }
              57% { opacity:1; transform:translate(var(--dx),var(--dy)); }
              60%,100% { opacity:0; transform:translate(var(--dx),var(--dy)); }
            }
            @keyframes grant-vote {
              0%,61% { opacity:0; transform:translateX(0); }
              64% { opacity:1; transform:translateX(0); }
              77% { opacity:1; transform:translate(var(--dx),var(--dy)); }
              80%,100% { opacity:0; transform:translate(var(--dx),var(--dy)); }
            }
            @media(prefers-reduced-motion:reduce) {
              .old-server,.vote-request,.vote-reply,.vote-reply-late,
              .initial-role,.offline-role,.follower-role,.candidate-role,.leader-role,
              .new-leader,.stage-start,.stage-timeout,.stage-vote,.stage-done { animation:none; }
            }
            '''
    elif kind == 'resize':
        height = 112
        parts += [f'''<g font-size="10" letter-spacing="1">
          {label(60, 18, 'CLIENT')}{label(194, 18, 'EVENT LOOP')}{label(332, 18, 'IN MEMORY')}
        </g>
        <path d="M104 50 H279 M332 79 V91 H60 V73" fill="none" stroke="{border}" stroke-width="1.5"/>
        <path d="M272 47 L279 50 L272 53 M57 80 L60 73 L63 80" fill="none" stroke="{accent}" stroke-width="1.5"/>
        <rect x="16" y="31" width="88" height="42" rx="7" fill="{bg}" stroke="{border}"/>
        <text x="60" y="55" text-anchor="middle" fill="{accent}" font-family="ui-monospace,Menlo,monospace" font-size="12">GET city</text>
        <circle cx="194" cy="50" r="17" fill="{bg}" stroke="{border}" stroke-width="2"/>
        <g class="io-ring" style="transform-origin:194px 50px">
          <path d="M194 33 A17 17 0 0 1 211 50" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>
        </g>
        <text x="194" y="54" text-anchor="middle" fill="{ink}" font-size="10">I/O</text>
        <rect x="279" y="31" width="106" height="48" rx="6" fill="{bg}" stroke="{border}"/>
        <rect class="lookup-row" x="282" y="34" width="100" height="21" rx="3" fill="{accent}" opacity=".12"/>
        <g font-family="ui-monospace,Menlo,monospace" font-size="11">
          <text x="290" y="48" fill="{ink}">city</text><text x="329" y="48" fill="{accent}">Austin</text>
          <text x="290" y="70" fill="{ink}">id</text><text x="329" y="70" fill="{ink}">42</text>
        </g>
        <text x="194" y="106" text-anchor="middle" fill="{accent}" font-family="ui-monospace,Menlo,monospace" font-size="12">"Austin"</text>
        <circle class="packet request" cx="104" cy="50" r="3" fill="{accent}"/>
        <circle class="packet response" cx="332" cy="91" r="3" fill="{accent}"/>
        ''']
        # One complete request/lookup/response sequence per loop.
        extra_motion = '''
        .request { animation:request 4.6s ease-in-out 1; }
        .response { animation:response 4.6s ease-in-out 1; }
        .io-ring { animation:poll 4.6s ease-in-out 1; }
        .lookup-row { animation:lookup 4.6s ease-in-out 1; }
        @keyframes request {
          0%,5% { opacity:0; transform:translateX(0); }
          10% { opacity:1; transform:translateX(0); }
          26% { opacity:1; transform:translateX(90px); }
          43% { opacity:1; transform:translateX(175px); }
          46%,100% { opacity:0; transform:translateX(175px); }
        }
        @keyframes response {
          0%,54% { opacity:0; transform:translate(0,0); }
          58% { opacity:1; transform:translate(0,0); }
          87% { opacity:1; transform:translate(-272px,0); }
          94% { opacity:1; transform:translate(-272px,-18px); }
          97%,100% { opacity:0; transform:translate(-272px,-18px); }
        }
        @keyframes poll {
          0%,15% { transform:rotate(0); }
          46%,100% { transform:rotate(360deg); }
        }
        @keyframes lookup {
          0%,40%,70%,100% { opacity:.12; }
          48%,58% { opacity:.4; }
        }
        @media(prefers-reduced-motion:reduce) {
          .request,.response,.io-ring,.lookup-row { animation:none; }
        }
        ''' if animated else ''
    elif kind == 'sanscue':
        height = 112
        parts += [f'''<g font-size="10" letter-spacing="1">
          {label(56, 18, 'SPEAKER')}{label(197, 18, 'MODERATOR')}{label(332, 18, 'AUDIENCE')}
        </g>
        <path d="M96 52 H141 M253 52 H289 M332 76 V91 H56 V75" fill="none" stroke="{border}" stroke-width="1.5"/>
        <path d="M134 49 L141 52 L134 55 M282 49 L289 52 L282 55 M53 82 L56 75 L59 82" fill="none" stroke="{accent}" stroke-width="1.5"/>
        <rect x="16" y="31" width="80" height="44" rx="7" fill="{bg}" stroke="{border}"/>
        <g class="speech-wave" stroke="{accent}" stroke-width="2" stroke-linecap="round">
          <path d="M34 49 V57 M43 42 V64 M52 47 V59 M61 39 V67 M70 46 V60 M79 50 V56"/>
        </g>
        <rect x="141" y="31" width="112" height="44" rx="7" fill="{bg}" stroke="{border}"/>
        <text x="197" y="47" text-anchor="middle" fill="{ink}" font-size="12">AI check-in draft</text>
        <rect class="review-gate" x="145" y="53" width="104" height="18" rx="4" fill="{accent}" opacity=".12"/>
        <text x="197" y="66" text-anchor="middle" fill="{accent}" font-size="10">review &amp; publish</text>
        <rect x="289" y="31" width="87" height="45" rx="7" fill="{bg}" stroke="{border}"/>
        <g class="audience-reply" fill="{soft}" stroke="{accent}" stroke-width="1.5" style="--soft:{soft};--accent:{accent}">
          <circle cx="309" cy="44" r="4"/><circle cx="332" cy="44" r="4"/><circle cx="355" cy="44" r="4"/>
          <path d="M302 65 V59 A7 7 0 0 1 316 59 V65 M325 65 V59 A7 7 0 0 1 339 59 V65 M348 65 V59 A7 7 0 0 1 362 59 V65"/>
        </g>
        <text x="197" y="106" text-anchor="middle" fill="{accent}" font-size="12">clarity feedback</text>
        <circle class="packet context" cx="96" cy="52" r="3" fill="{accent}"/>
        <circle class="packet check-in" cx="253" cy="52" r="3" fill="{accent}"/>
        <circle class="packet feedback" cx="332" cy="91" r="3" fill="{accent}"/>
        ''']
        extra_motion = '''
        .context { animation:context 4.8s ease-in-out 1; }
        .check-in { animation:publish 4.8s ease-in-out 1; }
        .feedback { animation:feedback 4.8s ease-in-out 1; }
        .review-gate { animation:review 4.8s ease-in-out 1; }
        .speech-wave { animation:speech 4.8s ease-in-out 1; }
        .audience-reply { animation:reply 4.8s ease-in-out 1; }
        @keyframes context {
          0%,5% { opacity:0; transform:translateX(0); }
          8% { opacity:1; transform:translateX(0); }
          22% { opacity:1; transform:translateX(45px); }
          25%,100% { opacity:0; transform:translateX(45px); }
        }
        @keyframes review {
          0%,22%,46%,100% { opacity:.12; }
          29%,39% { opacity:.4; }
        }
        @keyframes publish {
          0%,43% { opacity:0; transform:translateX(0); }
          46% { opacity:1; transform:translateX(0); }
          60% { opacity:1; transform:translateX(36px); }
          63%,100% { opacity:0; transform:translateX(36px); }
        }
        @keyframes feedback {
          0%,69% { opacity:0; transform:translate(0,0); }
          72% { opacity:1; transform:translate(0,0); }
          92% { opacity:1; transform:translate(-276px,0); }
          96% { opacity:1; transform:translate(-276px,-16px); }
          99%,100% { opacity:0; transform:translate(-276px,-16px); }
        }
        @keyframes speech {
          0%,12%,100% { opacity:1; }
          6% { opacity:.35; }
        }
        @keyframes reply {
          0%,60%,75%,100% { fill:var(--soft); }
          66% { fill:var(--accent); }
        }
        @media(prefers-reduced-motion:reduce) {
          .context,.check-in,.feedback,.review-gate,.speech-wave,.audience-reply { animation:none; }
        }
        ''' if animated else ''
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
    .packet { opacity:0; animation:travel 1.8s ease-in-out 1; }
    @keyframes travel {
      0%,12% { opacity:0; transform:translate(0,0); }
      22% { opacity:1; }
      72% { opacity:1; transform:translate(var(--dx),var(--dy)); }
      84%,100% { opacity:0; transform:translate(var(--dx),var(--dy)); }
    }
    @media(prefers-reduced-motion:reduce) { .packet { animation:none; } }
    ''' if animated else '.packet { opacity:0; }'
    if animated:
        if kind == 'network':
            motion += '.output { animation:travel-output 1.8s ease-in-out 1; }'
            motion += '@media(prefers-reduced-motion:reduce) { .output { animation:none; } }'
            motion = schedule_timeline(motion, kind)
        else:
            # Other diagrams define their own packet motions.
            motion = '.packet { opacity:0; }'
            extra_motion = schedule_timeline(extra_motion, kind)
    title, desc = TITLES[kind]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="{height}" viewBox="0 0 400 {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title><desc id="desc">{desc} Schematic illustration.</desc>
  <style>{motion}{extra_motion}</style>
  <rect width="400" height="{height}" rx="8" fill="{bg}"/>
  <g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="13">{''.join(parts)}</g>
</svg>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for kind in TITLES:
        for dark in (False, True):
            for animated in (True, False):
                name = f"{kind}-{'static-' if not animated else ''}{'dark' if dark else 'light'}.svg"
                (OUT / name).write_text("\n".join(line.rstrip() for line in render(kind, dark, animated).splitlines()) + "\n")
    print('Generated 16 project diagrams (light, dark, animated, reduced motion).')
