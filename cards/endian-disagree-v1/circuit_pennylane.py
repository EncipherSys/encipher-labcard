import pennylane as qml


def circuit():
    qml.Hadamard(0)
    return qml.probs(wires=[0, 1])
