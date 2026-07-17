### Abhinesh Dahal

I build systems from first principles: complex infrastructure is a
composition of simple concepts, and I take things apart until that
composition is visible.

**Building now:** consensus from the ground up.

| | |
|---|---|
| [raft-kv](https://github.com/DahalAb1/raft-kv) | Raft and a linearizable key/value store in Go. ~1,700 lines, validated with 100-run test gauntlets. The README is the full build story, bug by bug. |
| [raft-demo](https://github.com/DahalAb1/raft-demo) | The same code running live: election, failover, crash recovery. `go run .`, or [watch it animated](https://dahalab1.github.io/raft-demo/). |
| [Redis](https://github.com/DahalAb1/Redis) | A Redis-shaped server in C++, from scratch: event loop, protocol, hashtable. Written up chapter by chapter. |

My favorite bug so far, as its latency histogram:

```text
20-25ms  ██████████████████ 239
25-30ms  ▌ 6
30-35ms  █████████████████████████████ 377
35-40ms  ▌ 4
40-45ms  ██████████████████ 234
```

Spikes exactly 10ms apart with near-empty bins between: a fixed-period
clock was quantizing every operation. Two greps later, two 10ms sleeps
in the hot path. The shape of a distribution is a diagnostic; the full
story is in [raft-kv](https://github.com/DahalAb1/raft-kv).

[LinkedIn](https://linkedin.com/in/abhinesh-dahal) · dahalabhinesh1@gmail.com
