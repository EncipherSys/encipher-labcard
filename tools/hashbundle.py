#!/usr/bin/env python3
"""SHA-256 of canonical JSON for a hashed bundle."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def canonical(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: hashbundle.py <bundle.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    digest = hashlib.sha256(canonical(data).encode("utf-8")).hexdigest()
    print(digest)
    sidecar = path.with_suffix(".sha256")
    sidecar.write_text(digest + "  " + path.name + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
