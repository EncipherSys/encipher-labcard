import pennylane as qml


def circuit():
    qml.Hadamard(0)
    qml.CNOT(wires=[0, 1])
    return qml.probs(wires=[0, 1])
