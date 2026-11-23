# news-image-23-nov

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/xlondze21/news-image-23-nov/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/xlondze21/news-image-23-nov/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A 1024x1024 newspaper-style infographic summing up 23 November 2026's world news in one image — "23 November 2026 — The World in One Day".

## Run it

```sh
python3 render.py              # draw entry.png
python3 main.py                # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Requires Pillow (`pip install Pillow`). No network. Deterministic:
running the generator twice produces byte-identical PNGs.

## The image

- **Hero:** COP31 collapses in Antalya — no deal, the first COP to fail
  since 2009, after the EU and about 130 countries rejected a pact that
  never mentioned fossil fuels.
- **Four stories:** the AI sell-off (ticker: US and Asian closes of
  Friday 20 November, labelled as such — the Monday US session had not
  closed yet); the Russian strike on Dymer, Ukraine; the Russian corvette
  Merkury sunk at Benghazi; the Democrats' 258-seat House win.
- **Strip:** the Shenzhen peace declaration, El Chapo Isidro captured,
  two tankers ablaze near the Strait of Hormuz.
- **Ticker:** US and Asian markets, final closes of Friday 20 November 2026
  (labelled as such — the Monday session did not exist yet at build time,
  and Tokyo was shut Monday for a holiday).

## License

MIT — see LICENSE.

---

<sub>Entered on [make.fun](https://make.fun/?ref=3f98mdh8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
