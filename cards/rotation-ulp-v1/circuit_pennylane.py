import pennylane as qml
from pennylane import numpy as np


def circuit():
    qml.RY(np.pi, wires=0)
    return qml.probs(wires=[0])
