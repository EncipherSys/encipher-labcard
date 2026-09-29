#!/usr/bin/env python3
"""Validate public lab cards. Stdlib only. Cards are JSON written as card.yaml."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"
REQUIRED = ("id", "title", "provenance", "status", "qubits")
PROVENANCE = {"cpu_oracle", "published_constraint"}
STATUSES = {
    "RUNS",
    "CPU_ONLY",
    "REFUSE",
    "AGREE",
    "DISAGREE_ULP",
    "DISAGREE_STRUCTURAL",
    "WILL_NOT_RUN",
    "EMULATION",
}


def load_card(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path) -> list[str]:
    errors = []
    try:
        card = load_card(path)
    except json.JSONDecodeError as exc:
        return [f"{path}: not JSON ({exc})"]
    for key in REQUIRED:
        if key not in card:
            errors.append(f"{path}: missing {key}")
    if card.get("id") != path.parent.name:
        errors.append(f"{path}: id {card.get('id')!r} != directory {path.parent.name!r}")
    if card.get("provenance") not in PROVENANCE:
        errors.append(f"{path}: bad provenance {card.get('provenance')!r}")
    if card.get("status") not in STATUSES:
        errors.append(f"{path}: bad status {card.get('status')!r}")
    if not isinstance(card.get("qubits"), int) or card["qubits"] < 0:
        errors.append(f"{path}: qubits must be a non-negative int")
    return errors


def main() -> int:
    paths = sorted(CARDS.glob("*/card.yaml"))
    if not paths:
        print("no cards found", file=sys.stderr)
        return 1
    errors: list[str] = []
    for path in paths:
        item_errors = validate(path)
        if item_errors:
            print(f"fail {path.parent.name}")
            errors.extend(item_errors)
        else:
            print(f"ok {path.parent.name}")
    if errors:
        for item in errors:
            print(item, file=sys.stderr)
        return 1
    print(f"validated {len(paths)} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
