from math import pi
from qiskit import QuantumCircuit


def circuit():
    qc = QuantumCircuit(1, 1)
    qc.ry(pi, 0)
    qc.measure(0, 0)
    return qc
