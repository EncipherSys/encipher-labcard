# Encipher Systems Lab Cards

Public circuit cards and schemas Encipher Systems uses when a lab needs a hashed known-answer bundle. CPU-only default. This is not a quantum SDK, not a backend, and not a QPU service.

Encipher inventories the cryptography and the lab stack you already run, and writes the sequence and the refuse list. Encipher does not run your job and does not claim speedup.

## What this repository is

- Machine-readable cards for a named software pin
- A hashed-bundle schema
- A status vocabulary: `RUNS`, `CPU_ONLY`, `REFUSE`, `AGREE`, `DISAGREE_ULP`, `DISAGREE_STRUCTURAL`, `WILL_NOT_RUN`, `EMULATION`
- A CPU oracle so CI stays green on a laptop

## What this repository is not

- A fourth circuit SDK
- A CUDA-Q, Qiskit, PennyLane, or Braket backend
- A QPU service
- A claim that an AMD GPU runs CUDA-Q
- A certification of any library
- An Encipher measurement of a named lab pin

Status on these cards is a published vendor constraint or a CPU-oracle result. This repository contains no Encipher measurement of CUDA-Q on ROCm.

See [docs/WHAT-WE-DO-NOT-BUILD.md](docs/WHAT-WE-DO-NOT-BUILD.md).

## Cards

| ID | Point of the card | CPU oracle |
| --- | --- | --- |
| `bell-v1` | Bell pair. Expected `00` / `11` at 1/2. Qiskit little-endian. | `AGREE` |
| `ghz-n4-v1` | Four-qubit GHZ. Expected `0000` / `1111` at 1/2. | `AGREE` |
| `rotation-ulp-v1` | `RY(π)` on one qubit. Ideal `P(1)=1`. Used to tag `DISAGREE_ULP` when one path is fp32 and another is fp64. | `AGREE` on CPU fp64 |
| `endian-disagree-v1` | Hadamard on q0 with expected bits written MSB-left. Fixture for `DISAGREE_STRUCTURAL`. | tags `ENDIAN_CONTRACT` |
| `aer-gpu-will-not-run-v1` | Records `WILL_NOT_RUN` for `qiskit-aer-gpu` off x86_64 Linux, and `REFUSE` for `cudaq.set_target("amd")`. | no execution |

## Tools

```bash
python3 tools/validate_card.py
python3 tools/run_oracle.py
python3 tools/hashbundle.py examples/sample-bundle/bundle.json
```

No GPU is required. Qiskit is optional.

## License

Apache-2.0 on code and schemas. Circuit text in this repository is original Encipher Systems work.
