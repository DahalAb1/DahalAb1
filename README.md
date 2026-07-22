<!-- ──────────────────────── hero ──────────────────────── -->
<img src="assets/terminal.svg" width="880" alt="Terminal session: Abhinesh Dahal, CS and Applied Math student at Texas State; focused on distributed systems and software engineering; seeking a Summer 2027 software engineering internship">

<!-- ──────────────────────── about ─────────────────────── -->

I am a Computer Science and Applied Mathematics student at Texas State
building distributed systems in Go and C++. I work on systems because it
is the hardest thinking I have found. Nothing in it can be hand-waved.
Every decision has to be argued for, because the ones you skip do not
announce themselves: the system lies to you quietly, and you find out
later.

> When I started Raft I did not know where to begin. I kept coming back
> to the same questions, each pass cleared a little more, and eventually
> it was not a mystery. Stay exposed to a problem long enough and it
> opens.

<!-- ─────────────────────── expandables ────────────────── -->

<details>
<summary><code>cat method.md</code></summary>

<br>

I like to understand the mechanics underneath a system before I build
anything on top of it. First I built a Redis-style server in C++ using
raw TCP sockets, a `poll()` event loop, and a hashtable that migrates a
bounded number of nodes per operation instead of stalling to rehash.
Pipelined over loopback it holds around 1M GET ops/sec on a single
thread, and its worst insert during a resize stays under a millisecond
where `std::unordered_map` freezes for ~240ms at four million keys.

I tend to choose these problems because nothing else lights up my head
the same way, and because of where I think the next decade goes. Two
things will matter most: intelligence itself, and getting it to
everyone. Models get the attention, but a model nobody can reach is a
research result — serving one to billions of people is a storage,
replication, and coordination problem. That is infrastructure, and it is
the layer I want to build on.

Before the systems work I did machine learning and data analysis. At the
Texas Department of Family and Protective Services I ran survival
analysis on foster-care placement data across 254 counties and presented
the findings to 40+ stakeholders.

It took me a while to work this way. I spent two years building from
tutorials, which made me feel fast and left me empty — I was decorating
the top floors of a building whose foundation I had never seen. A C++
course fixed that: pointers, memory, the machine underneath. I went down
the stack and stayed there, which is why every project here starts at
the bottom instead of at a library.

</details>

<details>
<summary><code>cat ~/.profile</code></summary>

<br>

Away from the keyboard I play soccer and go mountain biking. The avatar
is Senku, from *Dr. Stone*. Favorite book: *The Count of Monte Cristo*.

</details>

<!-- ────────────────────────  contact ─────────────────── -->

[LinkedIn](https://linkedin.com/in/abhinesh-dahal) ·
[dahalabhinesh1@gmail.com](mailto:dahalabhinesh1@gmail.com)

<!-- ─────────────────────── status bar ─────────────────── -->

<img src="assets/statusbar.svg" width="880" alt="Abhinesh Dahal · Go, C++, Python · open to Summer 2027">
