# Friday 27 November 2026 in One Picture

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/sixthin016/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/sixthin016/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image that sums up Friday 27 November 2026's world news —
35 stories, 10 regions, 16 fields — drawn as a classic serif
newspaper front page, entirely in code (no photos).

**The day in three leads:** a drone strike in Kuwait kills two
Italian technicians · Black Friday opens with $12.9bn in US online
sales forecast · Hamas weighs its reply after 10 die in Gaza.

**Also inside:** Russia's overnight barrage kills at least 3 ·
New Zealand's final count ends in deadlock, one seat short of a
majority · a tanker capsizes off Ibiza with 7,000 tonnes of diesel
aboard · Gukesh–Sindarov game 3 ends drawn · Depardieu to stand
trial for rape · Amazon workers strike in 20 countries · Trump
seeks a probe into 'fake' GDP · UK migration falls to a near
30-year low · a Thanksgiving storm leaves 800,000 in the dark ·
Musk gifts every US child SpaceX shares — plus 22 more stories, a
six-number strip, counted region and field bars, a UTC strip, a
world map with pins 1–13, a BY THE NUMBERS column, and a red DATE
CHECK box with a how-we-checked legend for stories that are *not*
from 27 November.

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
Every lead and every panel carries its own drawn scene and a
WHY IT MATTERS line. Pictures and the map are drawn in code,
not photographs. v2.3: 13 drawn scenes (3 leads + 10 panels);
see DISSECTION-v2.3.md for the top-1 dissection, the idea rounds
and the full verification (VM = Simular Box byte-identical).

---

<sub>Entered on [make.fun](https://make.fun/?ref=sixthin&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
