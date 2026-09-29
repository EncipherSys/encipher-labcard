#!/usr/bin/env python3
"""CPU oracles for public cards. Standard library only."""
from __future__ import annotations

import math


def ket0(n: int):
    state = [0j] * (1 << n)
    state[0] = 1 + 0j
    return state


def apply_h(state, n, q):
    out = state[:]
    for i in range(1 << n):
        if (i >> q) & 1:
            continue
        j = i | (1 << q)
        a, b = state[i], state[j]
        out[i] = (a + b) / math.sqrt(2)
        out[j] = (a - b) / math.sqrt(2)
    return out


def apply_cx(state, n, ctrl, tgt):
    out = state[:]
    for i in range(1 << n):
        if ((i >> ctrl) & 1) and not ((i >> tgt) & 1):
            j = i | (1 << tgt)
            out[i], out[j] = state[j], state[i]
    return out


def apply_ry(state, n, q, theta):
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    out = state[:]
    for i in range(1 << n):
        if (i >> q) & 1:
            continue
        j = i | (1 << q)
        a, b = state[i], state[j]
        out[i] = c * a - s * b
        out[j] = s * a + c * b
    return out


def probs(state, n):
    out = {}
    for i, amp in enumerate(state):
        bits = "".join(str((i >> q) & 1) for q in range(n - 1, -1, -1))
        p = abs(amp) ** 2
        if p > 1e-15:
            out[bits] = p
    return out


def tv(p, q):
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def check(name, got, expected, bound=1e-12) -> bool:
    dist = tv(got, expected)
    ok = dist <= bound
    print(f"{name}: {'AGREE' if ok else 'DISAGREE_ULP'} tv={dist:.3e} got={got}")
    return ok


def main() -> int:
    ok = True
    bell = apply_cx(apply_h(ket0(2), 2, 0), 2, 0, 1)
    ok &= check("bell-v1", probs(bell, 2), {"00": 0.5, "11": 0.5})
    ghz = apply_cx(apply_cx(apply_cx(apply_h(ket0(4), 4, 0), 4, 0, 1), 4, 1, 2), 4, 2, 3)
    ok &= check("ghz-n4-v1", probs(ghz, 4), {"0000": 0.5, "1111": 0.5})
    ry = apply_ry(ket0(1), 1, 0, math.pi)
    ok &= check("rotation-ulp-v1", probs(ry, 1), {"1": 1.0})
    print("endian-disagree-v1: DISAGREE_STRUCTURAL")
    print("aer-gpu-will-not-run-v1: WILL_NOT_RUN published_constraint")
    if not ok:
        raise SystemExit("oracle mismatch")
    print("oracle ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
