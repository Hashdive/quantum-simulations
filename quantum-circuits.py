from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt  # Import this to show the plot

# Superposition Circuit
def superposition_example():
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate to put qubit 0 in superposition
    qc.measure(0, 0)  # Measure the qubit

    # Use the Aer simulator
    simulator = Aer.get_backend('qasm_simulator')
    
    # Transpile the circuit for the backend
    transpiled_qc = transpile(qc, simulator)
    
    # Execute the transpiled circuit
    job = simulator.run(transpiled_qc, shots=1024)
    
    # Get the result and access counts
    result = job.result()
    counts = result.get_counts(transpiled_qc)
    print("Superposition Measurement result:", counts)
    plot_histogram(counts).show()

# Entanglement Circuit
def entanglement_example():
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Apply Hadamard gate to qubit 0
    qc.cx(0, 1)  # Entangle qubit 0 with qubit 1 using CNOT
    qc.measure([0, 1], [0, 1])  # Measure both qubits

    # Use the Aer simulator
    simulator = Aer.get_backend('qasm_simulator')

    # Transpile the circuit for the backend
    transpiled_qc = transpile(qc, simulator)

    # Execute the transpiled circuit
    job = simulator.run(transpiled_qc, shots=1024)

    # Get the result and access counts
    result = job.result()
    counts = result.get_counts(transpiled_qc)
    print("Entanglement Measurement result:", counts)
    plot_histogram(counts).show()

# Run both examples
superposition_example()
entanglement_example()

# Ensure the plot is displayed
plt.show()
