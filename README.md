# The World in One Image — Monday, 23 November 2026

A one-page newspaper front page summing up the world news of Monday
23 November 2026, built for the make.fun competition
`news-image-20261123`.

## Stories on the page

- **Lead:** Tanker clash off Hormuz as the US blockade meets Iran's
  Kharg fleet.
- COP31 collapse leaves climate talks in crisis after record overtime.
- Rescuers dig for 14 in Kyiv rubble as Zelenskyy pleads for Patriots.
- Burning Sparta II drifts toward NATO waters.
- South Korea minister quits over AI cheating chaos in the university exam.
- Search resumes Monday for missing in the Indonesia candy-factory fire.
- Nepal PM Shah meets Modi in Delhi for a first face-to-face summit.
- Markets reopen Monday after the AI rout erased Nasdaq's 2026 gains.
- Ferrari boss calls the Hamilton-Leclerc clash 'unacceptable' after Vegas.
- Settler arson in the West Bank condemned as 'Jewish terrorism'.
- Saudi coalition intercepts a Houthi missile over the western region.
- India pile up a record 720/9 in the Wellington Test.
- Thousands march in Lisbon as living costs fuel anger.
- Plus 12 briefs and a 6-item ticker — 31 stories in all.

## How it works

- `stories.json` holds the day's stories (headline, summary, region,
  artwork motif, map coordinates).
- `generate.py` draws the 1024x1024 front page with Pillow: masthead,
  world map with 13 numbered pins, lead column, 12 illustrated cards,
  briefs panel and ticker. Every illustration is drawn from shapes in
  code; nothing is downloaded.
- `main.py` renders `entry.png` to `MAKEFUN_OUTPUT_DIR` (or `/output`).

The output is deterministic: the same `stories.json` always produces
byte-identical `entry.png`.

## Run it

```
python3 generate.py          # writes ./entry.png (needs Pillow)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/DavidQlla06/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/DavidQlla06/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
