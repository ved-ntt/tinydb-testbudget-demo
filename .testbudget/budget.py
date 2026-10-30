"""Print a time budget: a fraction of the latest run's total test time."""

import json
import sys
from pathlib import Path

history = Path(sys.argv[1])
fraction = float(sys.argv[2])


def read(name):
    text = (history / name).read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


runs, results = read("runs.jsonl"), read("results.jsonl")
latest = max(runs, key=lambda run: run["timestamp"])["sha"]
total = sum(r["duration_s"] for r in results if r["sha"] == latest)
print(f"{total * fraction:.3f}")
