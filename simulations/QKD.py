from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from numpy.random import randint
import numpy as np

# Function to prepare qubits for the BB84 protocol
def prepare_bb84_qubit(bit, basis):
    """Prepare a BB84 qubit given a classical bit and a basis (0: standard, 1: Hadamard)."""
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)  # Flip the qubit if the bit is 1
    if basis == 1:
        qc.h(0)  # Apply Hadamard gate if basis is 1
    return qc

# Function for Alice to send bits using random bases
def alice_sends(n_bits):
    """Alice prepares and sends n_bits qubits using random bits and bases."""
    bits = randint(2, size=n_bits)  # Random bits (0 or 1)
    bases = randint(2, size=n_bits)  # Random bases (0: standard, 1: Hadamard)
    qubits = []
    for i in range(n_bits):
        qc = prepare_bb84_qubit(bits[i], bases[i])
        qubits.append(qc)
    return bits, bases, qubits

# Function for Eve to intercept and measure the qubits
def eve_intercepts(qubits, n_bits):
    """Eve intercepts and measures the qubits using random bases."""
    eve_bases = randint(2, size=n_bits)  # Eve uses random bases (0: standard, 1: Hadamard)
    simulator = Aer.get_backend('qasm_simulator')

    for i in range(n_bits):
        qc = qubits[i]
        if eve_bases[i] == 1:
            qc.h(0)  # Apply Hadamard gate if Eve measures in Hadamard basis
        qc.measure(0, 0)

        # Transpile and run the circuit
        transpiled_qc = transpile(qc, simulator)
        job = simulator.run(transpiled_qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        eve_bit = int(max(counts, key=counts.get))  # Eve's measured bit
        
        # After measurement, Eve resends the qubit based on her measurement
        qubits[i] = prepare_bb84_qubit(eve_bit, eve_bases[i])

    return eve_bases

# Function for Bob to measure the received qubits using random bases
def bob_receives(qubits, n_bits):
    """Bob measures the received qubits using random bases."""
    bases = randint(2, size=n_bits)  # Random bases (0: standard, 1: Hadamard)
    measured_bits = []
    simulator = Aer.get_backend('qasm_simulator')

    for i in range(n_bits):
        qc = qubits[i]
        if bases[i] == 1:
            qc.h(0)  # Apply Hadamard if measuring in Hadamard basis
        qc.measure(0, 0)

        # Transpile and run the circuit
        transpiled_qc = transpile(qc, simulator)
        job = simulator.run(transpiled_qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        measured_bit = int(max(counts, key=counts.get))  # Extract the most common result
        measured_bits.append(measured_bit)

    return np.array(measured_bits), bases

# Function to simulate the QKD protocol with Eve's interception
def qkd_simulation_with_eve(n_bits):
    """Simulates a QKD protocol between Alice and Bob with Eve's interception."""
    # Step 1: Alice sends random bits using random bases
    alice_bits, alice_bases, qubits = alice_sends(n_bits)
    print(f"Alice's bits:    {alice_bits}")
    print(f"Alice's bases:   {alice_bases}")
    
    # Step 2: Eve intercepts and measures the qubits
    eve_bases = eve_intercepts(qubits, n_bits)
    print(f"Eve's bases:     {eve_bases}")
    
    # Step 3: Bob receives qubits and measures them in random bases
    bob_bits, bob_bases = bob_receives(qubits, n_bits)
    print(f"Bob's bits:      {bob_bits}")
    print(f"Bob's bases:     {bob_bases}")
    
    # Step 4: Alice and Bob compare their bases publicly to discard mismatches
    key = []
    for i in range(n_bits):
        if alice_bases[i] == bob_bases[i]:
            key.append(int(alice_bits[i]))  # Keep the bit where the bases match
    
    print(f"Shared Key:      {key}")
    
    # Step 5: Detect eavesdropping by comparing a portion of the key
    sample_size = min(len(key), 5)  # Compare 5 bits (or fewer if the key is small)
    if sample_size > 0:
        sample_indices = np.random.choice(range(len(key)), sample_size, replace=False)
        alice_sample = [key[i] for i in sample_indices]
        bob_sample = [int(bob_bits[i]) for i in sample_indices if alice_bases[i] == bob_bases[i]]
        
        print(f"Alice's sample:  {alice_sample}")
        print(f"Bob's sample:    {bob_sample}")
        
        if alice_sample != bob_sample:
            print("*** Eve was detected! ***")
        else:
            print("*** No eavesdropping detected. ***")
    
    return key

# Run the QKD simulation with Eve for a set number of bits
qkd_simulation_with_eve(10)
