import pennylane as qml


def circuit():
    return qml.probs(wires=[0])
