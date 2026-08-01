<!-- ──────────────────────── hero ──────────────────────── -->
<img src="assets/terminal.svg?v=2" width="880" alt="Terminal session: Abhinesh Dahal, CS and Applied Math student at Texas State; focused on distributed systems and software engineering; projects include raft-kv in Go and a Redis-style server in C++, both built from the syscalls up; seeking a Summer 2027 software engineering internship">

<!-- ──────────────────────── about ─────────────────────── -->

I build distributed systems from the socket up — consensus, storage, replication.

The next decade needs two things: intelligence, and infrastructure big enough to
hold it. A model nobody can reach is just a research result. I want to build the
layer that gets it to everyone.

<!-- ─────────────────────── projects ───────────────────── -->

### Projects

**[raft-kv](https://github.com/DahalAb1/raft-kv)** · Go — Raft implemented from
[the paper](https://raft.github.io/raft.pdf): leader election, log replication,
crash persistence, and snapshots, with a linearizable key/value store on top.
~1,700 lines, every layer validated with 100-run test gauntlets. The hardest bugs
failed at **14%, 9%, and 2.5%** rather than deterministically, so they had to be
found by measurement instead of by reading.
[**Watch a cluster elect a leader →**](https://dahalab1.github.io/raft-demo/)

**[Redis](https://github.com/DahalAb1/Redis)** · C++ — a Redis-style server built up
from `socket(2)`: non-blocking I/O, a `poll()` event loop, and a hashtable that
migrates a bounded number of nodes per operation instead of stalling to rehash.
Pipelined over loopback it holds **1M GET ops/sec** on a single thread, and its
worst insert during a resize stays **under 1ms**, where `std::unordered_map`
freezes for **~240ms** at four million keys.

<!-- ─────────────────────── before ─────────────────────── -->

**Before systems:** a data-science internship at the Texas Department of Family and
Protective Services, running survival analysis on foster-care placement data across
254 counties and presenting the findings to 40+ stakeholders.

<!-- ─────────────────────── expandables ────────────────── -->

<details>
<summary><code>cat how-i-got-here.md</code></summary>

<br>

I spent two years building from tutorials, which made me feel fast and left me
empty: I was decorating the top floors of a building whose foundation I had never
seen. A C++ course fixed that — pointers, memory, the machine underneath. I went
down the stack and stayed there, which is why every project here starts at the
bottom instead of at a library.

</details>

<details>
<summary><code>cat ~/.profile</code></summary>

<br>

Away from the keyboard I play soccer and go mountain biking. The avatar is Senku,
from *Dr. Stone*. Favorite book: *The Count of Monte Cristo*.


</details>

<!-- ─────────────────────── sign-off ───────────────────── -->

```
~ % grep lesson notes/raft.md
stay with a problem long enough and the shape of it appears
```

<!-- ────────────────────────  contact ─────────────────── -->

[LinkedIn](https://linkedin.com/in/abhinesh-dahal) ·
[dahalabhinesh1@gmail.com](mailto:dahalabhinesh1@gmail.com)

<!-- ─────────────────────── status bar ─────────────────── -->

<img src="assets/statusbar.svg" width="880" alt="Abhinesh Dahal · Go, C++, Python · open to Summer 2027">
