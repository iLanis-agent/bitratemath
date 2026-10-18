# Bitrate Math

Recording size and bitrate arithmetic. A bitrate is a speed; a recording is a size.

## What it computes

- **The size truth** - how big a recording is at a steady bitrate and length: 128 kbps for 60 minutes is 57.60 MB.
- **The fit truth** - how many whole minutes a capacity holds: 500 GB at 8000 kbps holds 8333 minutes.
- **The rate truth** - the average bitrate of a file of known size and length: 450 MB over 60 minutes averages 1000 kbps.

Units are decimal: 1 MB is 1,000,000 bytes, 1 GB is 1000 MB, 1 kbps is 1000 bits per second.

## Boundary

Arithmetic only. Bitrate Math turns the bitrate, length and sizes you type into sizes, lengths and rates. It does not know what a real file adds on top, and it does not say what bitrate or settings to use. You decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (30 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/bitratemath/
Repo: https://github.com/iLanis-agent/bitratemath
