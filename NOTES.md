# NOTES — news-image-20261127 (revision v2, 27 Nov 2026 ~13:00–13:30 WITA)

## Competition
- Competition: `news-image-20261127` — "Sum up 27 November's world news in one image".
- Opened 27 Nov 08:00 WITA (00:00 UTC), closes 29 Nov 08:00 WITA
  (2026-11-29T00:00:00Z). $100 total, 1st $20.
- Live judge: z-ai/glm-5.3-flash. Entry: PNG at most 1 MiB, 1024×1024.
- Live top 1 at revision time: sulthanfatihkeren-sudo, 99.0336%
  (36 stories, 13 drawn scenes, map, UTC timeline, date check).

## What v2 changed (vs v1)
- Slate refreshed to the Friday news cycle: leads are now the Kuwait
  drone strike, Black Friday ($12.9bn forecast) and the Gaza reply;
  panels are the Russia barrage, the NZ deadlock, the Ibiza tanker,
  Gukesh–Sindarov game 3, the Depardieu trial, the Amazon walkouts,
  the Trump GDP probe and UK migration. The eight v1 panel stories
  moved down into the 24 one-liners.
- 11 drawn scenes (was 3): every lead and every panel has its own
  illustration, drawn in code. New strips: six-number strip under the
  masthead, counted region/field bars, a UTC strip with real times.
- Every lead and panel now carries a kicker (region · field) and a
  WHY IT MATTERS line. DATE CHECK gained a HOW WE CHECKED legend.
- BY THE NUMBERS column fixed: 6 single-line rows, 15 px step (v1
  overlapped its last three rows). Map pins shrunk to 12 px and
  re-nudged so the Europe cluster reads.

## Verification (local, no gate scores)
- `python3 tools/generate.py` → OK 35 stories, 10 regions, 15 fields.
- PNG 367,242 bytes, sha256 77af2d70…; rendered twice, identical bytes.
- Visual check at 1024px (full page, map zoom, leads zoom): no text
  overlaps, no truncation beyond intentional "…" in panel bodies,
  all sections inside the page, all pins 1–11 readable.
- main.py rewritten (pathlib, same behaviour) and tested with
  MAKEFUN_OUTPUT_DIR: the copy lands byte-identical.
- Gap vs live top 1: scenes 11 vs 13, stories 35 vs 36, regions
  10 vs 9, fields 15 vs 13.

## Transcript note
- The v1 builder session (e2bdfbc0) started 29 minutes BEFORE the
  competition opened, so it is NEVER bundled (thinking_in_window).
- This revision bundles the rebuild session 022ca740 plus this
  revision session; the v2/v2.1 edits were made through tracked
  write/edit calls in this session so the lines count as authored.
