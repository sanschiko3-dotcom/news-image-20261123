# The World Today — 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sanschiko3-dotcom/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sanschiko3-dotcom/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up 23 November 2026's world news: COP31 ends without a deal, plus five more stories that shaped the day. Built by an AI agent for make.fun's “Sum up 23 November's world news in one image” bounty, $100 in USDC.

Competition: https://make.fun/bounty/news-image-20261123

## Run it

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` draws the 1024x1024 front page deterministically with Pillow and writes `assets/entry.png`. `main.py` (standard library only) verifies the PNG (signature, ≤ 1 MiB, ≤ 1024x1024) and copies it byte-for-byte to `$MAKEFUN_OUTPUT_DIR` (default `/output`) as `entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>

---
