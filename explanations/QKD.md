# Quantum Key Distribution (QKD) Simulation Explanation

## Introduction to QKD

Quantum Key Distribution (QKD) is a method of securely sharing a secret key between two parties, typically called Alice and Bob. The security of QKD relies on the principles of quantum mechanics, specifically the fact that measuring a quantum state can change it. This makes it possible to detect if someone has tried to intercept the communication.

## BB84 Protocol

BB84 is a specific QKD protocol developed by Charles Bennett and Gilles Brassard in 1984. Here's how it works in simple terms:

1. Alice sends a series of qubits (quantum bits) to Bob.
2. Each qubit represents a binary bit (0 or 1) and is prepared in one of two bases (let's call them + and x).
3. Bob measures each qubit in either the + or x basis, randomly choosing for each qubit.
4. Alice and Bob then publicly compare which bases they used for each qubit, but not the actual bit values.
5. They keep only the bits where they happened to use the same basis, discarding the rest.
6. The remaining bits become their shared secret key.

## Code Explanation

Let's break down the key components of our QKD simulation:

### 1. Importing necessary libraries

```python
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from numpy.random import randint
import numpy as np
```

These imports provide tools for quantum circuit simulation (Qiskit), random number generation, and array manipulation.

### 2. Preparing BB84 qubits

```python
def prepare_bb84_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)  # Flip the qubit if the bit is 1
    if basis == 1:
        qc.h(0)  # Apply Hadamard gate if basis is 1
    return qc
```

This function creates a single qubit for the BB84 protocol:
- If the bit is 1, it applies an X gate (NOT gate) to flip the qubit from |0⟩ to |1⟩.
- If the basis is 1 (representing the x basis), it applies a Hadamard (H) gate, which puts the qubit in a superposition state.

### 3. Alice's role

```python
def alice_sends(n_bits):
    bits = randint(2, size=n_bits)  # Random bits (0 or 1)
    bases = randint(2, size=n_bits)  # Random bases (0: +, 1: x)
    qubits = []
    for i in range(n_bits):
        qc = prepare_bb84_qubit(bits[i], bases[i])
        qubits.append(qc)
    return bits, bases, qubits
```

Alice generates random bits and bases, then prepares qubits accordingly using the `prepare_bb84_qubit` function.

### 4. Eve's Interception

```python
def eve_intercepts(qubits, n_bits):
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
```

Eve intercepts each qubit, measures it in a randomly chosen basis, and then resends a new qubit based on her measurement. This process inevitably introduces errors due to the quantum nature of the information.

### 5. Bob's role

```python
def bob_receives(qubits, n_bits):
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
```

Bob generates his own random bases, then measures each qubit:
- If his basis is 1 (x basis), he applies a Hadamard gate before measurement.
- He then measures the qubit and records the result.

### 6. QKD Simulation with Eve

```python
def qkd_simulation_with_eve(n_bits):
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
```

This function simulates the entire QKD process with Eve's interception:
1. Alice prepares and sends qubits.
2. Eve intercepts, measures, and resends the qubits.
3. Bob measures the received qubits.
4. Alice and Bob compare bases and keep only the bits where their bases matched.
5. They compare a sample of their key to detect Eve's presence.

## Example Output

```
Alice's bits:    [0 1 1 0 0 0 0 1 0 0]
Alice's bases:   [1 1 1 1 0 1 0 0 0 1]
Eve's bases:     [0 0 1 1 0 1 0 1 0 0]
Bob's bits:      [0 0 1 0 0 0 0 1 0 0]
Bob's bases:     [0 1 0 1 0 1 1 1 1 1]
Shared Key:      [1, 0, 0, 0, 0]
Alice's sample:  [0, 0, 0, 1, 0]
Bob's sample:    [0, 0, 0]
*** Eve was detected! ***
```

## Implications and Security Principles

1. **Shared Key Generation**: Alice and Bob can generate a shared secret key without ever transmitting the key directly.

2. **Eavesdropper Detection**: The presence of Eve (an eavesdropper) can be detected due to the errors she introduces when measuring and resending qubits.

3. **Quantum No-Cloning Theorem**: Eve cannot perfectly copy unknown quantum states, which is a fundamental principle (no-cloning theorem) that underpins QKD security.

4. **Basis Reconciliation**: Alice and Bob only keep bits where they used the same basis, which forms the foundation of their shared key.

5. **Error Detection**: By comparing a sample of their key, Alice and Bob can detect if eavesdropping has occurred.

6. **Security Assurance**: In a real-world scenario, if eavesdropping is detected, Alice and Bob would discard the compromised key and restart the process.

## Quantum Principles 

In the BB84 Quantum Key Distribution (QKD) protocol with eavesdropping, several fundamental quantum principles are at play. These principles ensure the security of the key exchange and allow Alice and Bob to detect any eavesdropping attempts by Eve. Here are the main quantum principles involved:

### 1. **Superposition**
Superposition is the ability of quantum particles (like qubits) to exist in multiple states simultaneously until they are measured. In the context of BB84:
- When Alice prepares a qubit in superposition (using the Hadamard basis), the qubit is in a combination of the states |0⟩ and |1⟩.
- The qubit's exact state remains indeterminate until Bob (or an eavesdropper) measures it, causing it to "collapse" into either |0⟩ or |1⟩.

This principle is crucial in the protocol because Eve's measurement of the qubit collapses its state and potentially introduces errors if she uses the wrong basis.

### 2. **Quantum Measurement and the Collapse of the Wavefunction**
According to quantum mechanics, the act of measuring a quantum state forces it to "collapse" from a superposition into one definite state. Before measurement, a qubit can be in a superposition (both |0⟩ and |1⟩), but once it is measured, it collapses to either |0⟩ or |1⟩. In BB84:
- Alice sends qubits in one of two possible bases (Standard or Hadamard).
- If Bob (or Eve) measures the qubit using the same basis as Alice used to prepare it, he will get the correct result. But if Bob or Eve uses a different basis, the measurement may yield the wrong result, disturbing the qubit.

This collapse is key to the security of QKD: if Eve measures a qubit using the wrong basis, it changes the state of the qubit, and this disturbance can be detected when Alice and Bob compare their bases.

### 3. **Quantum No-Cloning Theorem**
The quantum no-cloning theorem states that it is impossible to create an exact copy of an arbitrary unknown quantum state. This principle is essential for the security of QKD because:
- If Eve intercepts the qubit and attempts to copy it, she cannot do so without altering the state of the qubit.
- As a result, Eve cannot perfectly measure the qubit and resend it to Bob without introducing detectable errors.

This means that any attempt by Eve to eavesdrop will either disturb the qubit or force her to make an incorrect measurement, which can then be detected by Alice and Bob.

### 4. **Heisenberg's Uncertainty Principle**
The Heisenberg Uncertainty Principle implies that certain pairs of properties, such as a particle's position and momentum, cannot both be known to arbitrary precision. In the context of QKD, this principle translates to the fact that a qubit cannot be measured in both the standard (computational) and Hadamard bases with certainty:
- If Alice prepares a qubit in the Hadamard basis and Bob (or Eve) measures it in the standard basis, the outcome is probabilistic.
- This uncertainty is a key aspect of QKD, as it ensures that if Eve measures the qubit in the wrong basis, she will disturb the state, which can be detected when Alice and Bob compare a subset of their measurements.

### 5. **Entanglement (Optional in BB84, but Related to QKD)**
Although the BB84 protocol does not use entanglement explicitly, entanglement is a crucial concept in more advanced QKD protocols like E91 (based on the work of Ekert). In entanglement-based QKD, two qubits are entangled such that the measurement of one qubit instantaneously affects the other, no matter how far apart they are. If Eve tries to intercept an entangled qubit, she will disturb the entanglement, alerting Alice and Bob to the eavesdropping attempt.

In BB84, however, the core principles are based on superposition, the collapse of the wavefunction, the no-cloning theorem, and the uncertainty principle.

---

### Summary of Quantum Principles at Play:
1. **Superposition**: Qubits can exist in multiple states until measured.
2. **Quantum Measurement (Wavefunction Collapse)**: Measurement forces a qubit into one of its definite states, potentially introducing errors if measured with the wrong basis.
3. **No-Cloning Theorem**: Qubits cannot be perfectly copied, preventing Eve from making undetectable measurements.
4. **Heisenberg's Uncertainty Principle**: The measurement in one basis disturbs the ability to know the state in another basis, creating detectable errors when Eve measures the qubit.

These principles ensure that any eavesdropping attempt by Eve will be detectable by Alice and Bob, as it disturbs the quantum states in ways that classical communication cannot hide. This makes quantum key distribution highly secure.

## Conclusion

This simulation demonstrates the core principles of Quantum Key Distribution and the BB84 protocol. It showcases how quantum mechanics principles can be leveraged to create a secure communication channel and detect any interference. While this is a simplified version, it captures the essence of how QKD provides a method for two parties to share a secret key securely, even in the presence of an eavesdropper.

In practice, QKD systems would include additional steps such as error correction and privacy amplification to further enhance security. Nevertheless, this simulation provides a solid foundation for understanding the fundamental concepts of quantum cryptography.

