from qiskit import QuantumCircuit


def circuit():
    qc = QuantumCircuit(1, 1)
    qc.measure(0, 0)
    return qc
