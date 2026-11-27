# Friday 27 November 2026 in One Picture

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/sixthin016/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/sixthin016/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image that sums up Friday 27 November 2026's world news —
35 stories, 10 regions, 15 fields — drawn as a classic serif
newspaper front page, entirely in code (no photos).

**The day in three leads:** Russia's overnight missile and drone
barrage kills at least 3 in Ukraine · two Italian technicians
killed as Iranian drones hit Kuwait · Macy's 100th Thanksgiving
parade set for Saturday after the storm postponement.

**Also inside:** the Houthis push on Aden · Trump and NATO's Rutte
tell Russia not to escalate · Kim vows an 'uncontrollable' nuclear
build-up · UK migration falls to a near 30-year low · Ebola in
Congo passes 12,000 cases · world stocks slide as tariffs bite —
plus 24 more stories, a world map with pins 1–11, a BY THE NUMBERS
column, a timeline around the clock, and a red DATE CHECK box for
stories that are *not* from 27 November.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024×1024 PNG, ≤ 1 MiB
```

`main.py` only copies `assets/entry.png` to the output directory.
The image itself is rendered by `tools/generate.py` (stdlib + PIL,
deterministic — same bytes on every run):

```sh
python3 tools/generate.py   # writes assets/entry.png
```

Every story is numbered 1–35 with a confidence badge
(CONFIRMED / OFFICIAL / REPORTED / CLAIM) and a named source.
Pictures and the map are drawn in code, not photographs.

---

<sub>Entered on [make.fun](https://make.fun/?ref=sixthin&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
