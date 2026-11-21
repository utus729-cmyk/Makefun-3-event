[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/utus729-cmyk/Makefun-3-event/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/utus729-cmyk/Makefun-3-event/reward.svg)](https://make.fun/bounty/news-image-20261121)
[make.fun bounty: Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121)

# The World in One Day — 21 November 2026

A program that draws a one-image summary of the world news of
**Saturday, November 21, 2026** as a newspaper front page.

Built for the make.fun bounty "Sum up 21 November's world news in one
image" ($100, 50 winners, AI judging) — the third daily edition in a row
from the same author, after the 19 November entry (repo
`utus729-cmyk/Makefun-event`) and the 20 November entry (repo
`utus729-cmyk/Makefun-2-event`).

## Run it

```sh
python3 main.py
```

- Python 3, standard library only. No network access.
- Writes `/output/entry.png` (falls back to `./entry.png`).
- Output: 1024 × 1024 PNG.
- **Deterministic:** every run produces byte-identical output
  (SHA-256 verified across consecutive runs before submitting).

## What's on the page

1. Russia's biggest barrage in weeks — 400+ drones and 110 missiles hit
   Ukraine; two missiles and a suspected drone came down in Poland, and
   PM Tusk called it a deliberate provocation.
2. AI rout sends Wall Street into correction — S&P 500 −3.7% to 6,910.39
   (7th straight loss), Nasdaq −5.3%, after Anthropic's flat second day.
3. Cancer pill daraxonrasib erases pancreatic tumours in a trial —
   cancer undetectable on scans in 1 in 12 patients.
4. UK and EU sign the biggest post-Brexit deals — food exports, carbon
   markets and youth mobility, signed in Brussels.
5. COP31 in Antalya runs into overtime — nearly 200 nations deadlocked
   over fossil fuels.
6. Iran says it downed a US MQ-9 over the Strait of Hormuz, as Trump
   weighs new strikes under pressure from Israel.

Plus a markets ticker with Friday's real closes and an "also today"
strip (Gen Z protests in 25 European countries, GTA 6's $4.9B day-one
record, Myanmar rejecting the ICJ ruling, Lewis Pugh's Hormuz swim).

## How it works

Everything is drawn in code — an embedded 5×7 bitmap font, canvas
primitives, and a hand-rolled PNG encoder (zlib + struct). No image
assets, no external files, no randomness, no clock: the same input
always yields the same bytes.
