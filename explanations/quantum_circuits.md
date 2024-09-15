# Demonstrating Superposition and Entanglement with Qiskit

This code demonstrates two fundamental concepts in quantum computing: superposition and entanglement. We'll use Qiskit, a quantum computing framework, to create quantum circuits that illustrate these concepts.

## Setup and Imports

```python
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
```

These imports provide the necessary tools for creating quantum circuits, simulating them, and visualizing the results.

## Superposition Example

Superposition is a quantum state where a qubit can exist in multiple states simultaneously.

```python
def superposition_example():
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate to put qubit 0 in superposition
    qc.measure(0, 0)  # Measure the qubit

    simulator = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulator)
    job = simulator.run(transpiled_qc, shots=1024)
    result = job.result()
    counts = result.get_counts(transpiled_qc)
    print("Superposition Measurement result:", counts)
    plot_histogram(counts).show()
```

### Explanation:

1. We create a quantum circuit with one qubit and one classical bit.
2. We apply a Hadamard gate (h) to the qubit, putting it in a superposition of |0⟩ and |1⟩ states.
3. We measure the qubit, which collapses the superposition.
4. We simulate this circuit 1024 times using Qiskit's QASM simulator.
5. The results are printed and visualized in a histogram.

Expected output: You should see approximately equal counts for '0' and '1' (around 512 each), demonstrating the 50/50 probability of measuring either state in superposition.

## Entanglement Example

Entanglement is a quantum phenomenon where two or more qubits are correlated in such a way that the quantum state of each qubit cannot be described independently.

```python
def entanglement_example():
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Apply Hadamard gate to qubit 0
    qc.cx(0, 1)  # Entangle qubit 0 with qubit 1 using CNOT
    qc.measure([0, 1], [0, 1])  # Measure both qubits

    simulator = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulator)
    job = simulator.run(transpiled_qc, shots=1024)
    result = job.result()
    counts = result.get_counts(transpiled_qc)
    print("Entanglement Measurement result:", counts)
    plot_histogram(counts).show()
```

### Explanation:

1. We create a quantum circuit with two qubits and two classical bits.
2. We apply a Hadamard gate to the first qubit, putting it in superposition.
3. We apply a CNOT (Controlled-NOT) gate with the first qubit as control and the second as target. This entangles the two qubits.
4. We measure both qubits.
5. We simulate this circuit 1024 times using Qiskit's QASM simulator.
6. The results are printed and visualized in a histogram.

Expected output: You should see approximately equal counts for '00' and '11' (around 512 each), demonstrating that the qubits are entangled. When you measure one qubit, you instantly know the state of the other.

## Running the Examples

```python
superposition_example()
entanglement_example()
plt.show()
```

These lines run both examples and ensure that the plots are displayed.

## Key Concepts

1. **Superposition**: A quantum state where a qubit can exist in multiple states simultaneously. The Hadamard gate is commonly used to create superposition.

2. **Entanglement**: A quantum phenomenon where two or more qubits are correlated such that the quantum state of each qubit cannot be described independently. The CNOT gate is often used to create entanglement.

3. **Measurement**: The act of observing a quantum system, which causes the collapse of superposition or entanglement into definite classical states.

4. **Quantum Simulation**: Using classical computers to simulate quantum systems. While useful for learning and small-scale experiments, it becomes infeasible for large numbers of qubits due to the exponential growth in computational resources required.

## Conclusion

This code provides a practical demonstration of two fundamental quantum computing concepts: superposition and entanglement. By using Qiskit to create and simulate quantum circuits, we can observe these quantum behaviors in action. Understanding these concepts is crucial for grasping the power and potential of quantum computing.

The histograms produced by this code visually represent the probabilistic nature of quantum measurements and the unique correlations that arise in entangled systems. These examples serve as a foundation for exploring more complex quantum algorithms and phenomena.