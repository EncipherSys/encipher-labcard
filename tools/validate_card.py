#!/usr/bin/env python3
"""Validate public lab cards with the standard library only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"
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


def validate(card: dict, path: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "id",
        "title",
        "license",
        "qubit_count",
        "endian",
        "expected",
        "cpu_oracle",
        "pins",
        "cause_tags",
    ]
    for key in required:
        if key not in card:
            errors.append(f"{path}: missing {key}")
    if card.get("id") != path.parent.name:
        errors.append(f"{path}: id {card.get('id')!r} does not match directory")
    if card.get("license") != "Apache-2.0":
        errors.append(f"{path}: license must be Apache-2.0")
    if card.get("endian") not in {"qiskit-little", "msb-left"}:
        errors.append(f"{path}: unknown endian")
    status = card.get("cpu_oracle", {}).get("status")
    if status not in STATUSES:
        errors.append(f"{path}: unknown cpu_oracle.status {status!r}")
    expected = card.get("expected", {})
    probs = expected.get("probabilities", {})
    if abs(sum(probs.values()) - 1.0) > 1e-9:
        errors.append(f"{path}: probabilities must sum to 1")
    for filename in ("circuit.qasm", "circuit_qiskit.py", "circuit_pennylane.py"):
        if not (path.parent / filename).is_file():
            errors.append(f"{path.parent}: missing {filename}")
    return errors


def main() -> int:
    errors: list[str] = []
    cards = sorted(CARDS.glob("*/card.yaml"))
    if not cards:
        print("no cards found", file=sys.stderr)
        return 1
    for path in cards:
        try:
            card = load_card(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: {exc}")
            continue
        errors.extend(validate(card, path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"ok {len(cards)} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
