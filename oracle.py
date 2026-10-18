#!/usr/bin/env python3
# Bitrate Math oracle - mirrors engine.js.
import json, math

def _whole(x, lo, hi, msg):
    if not isinstance(x, int) or x < lo or x > hi:
        raise ValueError(msg)
    return x

def _kbps(x): return _whole(x, 1, 1000000, "bitrate must be a whole number of kbps from 1 to 1000000")
def _min(x): return _whole(x, 1, 100000, "minutes must be a whole number from 1 to 100000")
def _gb(x): return _whole(x, 1, 100000, "capacity must be a whole number of GB from 1 to 100000")

def _hund(x, msg):
    if not math.isfinite(x) or x <= 0 or x > 1000000:
        raise ValueError(msg)
    return math.floor(x * 100 + 0.5)

def _fixed2(h):
    whole, frac = divmod(h, 100)
    return f"{whole}.{frac:02d}"

def _fmt(h):
    whole, frac = divmod(h, 100)
    if frac == 0:
        return str(whole)
    f = f"{frac:02d}"
    if f[1] == "0":
        f = f[0]
    return f"{whole}.{f}"

def _plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")

def size_truth(kbps, minutes):
    k = _kbps(kbps)
    m = _min(minutes)
    x = k * m
    mb = (3 * x + 2) // 4
    gb = (3 * x + 2000) // 4000
    return f"{k} kbps for {_plural(m, 'minute')}: {_fixed2(mb)} MB, {_fixed2(gb)} GB."

def fit_truth(cap, kbps):
    c = _gb(cap)
    k = _kbps(kbps)
    mins = c * 400000 // (k * 3)
    h, r = divmod(mins, 60)
    return (f"Capacity {c} GB at {k} kbps holds {_plural(mins, 'minute')}, which is "
            f"{_plural(h, 'hour')} {_plural(r, 'minute')}.")

def rate_truth(size, minutes):
    s = _hund(size, "size must be between 0 and 1000000 MB, over 0")
    m = _min(minutes)
    t = (80 * s + 3 * m) // (6 * m)
    whole, frac = divmod(t, 10)
    text = str(whole) if frac == 0 else f"{whole}.{frac}"
    return f"{_fmt(s)} MB over {_plural(m, 'minute')} averages {text} kbps."

FNS = {"sizeTruth": size_truth, "fitTruth": fit_truth, "rateTruth": rate_truth}

CASES = [
    ("sizeTruth", [128, 60]), ("sizeTruth", [8000, 90]), ("sizeTruth", [1, 1]), ("sizeTruth", [5000, 1]),
    ("sizeTruth", [320, 3]), ("sizeTruth", [1000000, 100000]), ("sizeTruth", [0, 60]), ("sizeTruth", [128, 0]),
    ("sizeTruth", [128.5, 60]), ("sizeTruth", [1000001, 60]), ("sizeTruth", [128, 100001]),
    ("fitTruth", [500, 8000]), ("fitTruth", [1, 1000000]), ("fitTruth", [1000, 128]), ("fitTruth", [64, 192]),
    ("fitTruth", [1, 8000]), ("fitTruth", [0, 8000]), ("fitTruth", [500, 0]), ("fitTruth", [100001, 8000]),
    ("fitTruth", [100000, 1]),
    ("rateTruth", [450, 60]), ("rateTruth", [4700, 120]), ("rateTruth", [3.5, 4]), ("rateTruth", [0.01, 1]),
    ("rateTruth", [1000, 1]), ("rateTruth", [0, 60]), ("rateTruth", [450, 0]), ("rateTruth", [1000001, 60]),
    ("rateTruth", [450, 1.5]), ("rateTruth", [100, 7]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
