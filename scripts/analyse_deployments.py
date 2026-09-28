#!/usr/bin/env python3
from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_deployments.csv"

def parse(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def load():
    with DATA.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def metrics(rows):
    successes = [r for r in rows if r["result"] == "success"]
    durations = [
        (parse(r["desktop_time"]) - parse(r["start_time"])).total_seconds() / 60
        for r in successes
    ]
    return {
        "total": len(rows),
        "successes": len(successes),
        "success_rate": round(len(successes) / len(rows) * 100, 1),
        "average_success_minutes": round(sum(durations) / len(durations), 1),
        "failures_by_stage": {
            stage: sum(1 for r in rows if r["failure_stage"] == stage)
            for stage in sorted({r["failure_stage"] for r in rows if r["failure_stage"]})
        },
    }

if __name__ == "__main__":
    for key, value in metrics(load()).items():
        print(f"{key}: {value}")
