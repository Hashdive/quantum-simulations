import numpy as np
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from math import gcd
from fractions import Fraction
from numpy.random import randint

# Function to create the controlled-U gate for a given power of a mod 15
def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2,4,7,8,11,13]:
        raise ValueError("'a' must be 2,4,7,8,11 or 13")
    U = QuantumCircuit(4)
    for _iteration in range(power):
        if a in [2,13]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [7,8]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [4, 11]:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    c_U = U.control()
    return c_U

# Function to create the inverse quantum Fourier transform (QFT†)
def qft_dagger(n):
    """n-qubit QFT†"""
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

# Function to run Shor's period-finding algorithm for a given 'a'
def qpe_amod15(a):
    """Performs quantum phase estimation on the operation a*r mod 15."""
    N_COUNT = 8
    qc = QuantumCircuit(4 + N_COUNT, N_COUNT)
    for q in range(N_COUNT):
        qc.h(q)  # Initialize counting qubits in state |+>
    qc.x(N_COUNT)  # Auxiliary register in state |1>
    for q in range(N_COUNT):  # Do controlled-U operations
        qc.append(c_amod15(a, 2**q), [q] + [i + N_COUNT for i in range(4)])
    qc.append(qft_dagger(N_COUNT), range(N_COUNT))  # Inverse QFT
    qc.measure(range(N_COUNT), range(N_COUNT))
    # Simulate Results
    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(transpile(qc, aer_sim), shots=1, memory=True)
    readings = job.result().get_memory()
    print("Register Reading: " + readings[0])
    phase = int(readings[0], 2) / (2**N_COUNT)
    print(f"Corresponding Phase: {phase}")
    return phase

# Function to factor N = 15 using Shor's algorithm
def shors_algorithm():
    N = 15  # We are factoring 15
    FACTOR_FOUND = False
    
    while not FACTOR_FOUND:
        a = randint(2, N)  # Random 'a' between 2 and N-1
        print(f"Random a chosen: {a}")

        # Ensure 'a' and N are coprime
        if gcd(a, N) != 1:
            print(f"'a' and {N} are not coprime, trivial factor found: {gcd(a, N)}")
            continue  # Retry with a different 'a'

        # Run quantum phase estimation
        phase = qpe_amod15(a)
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        print(f"Order r: {r}")
        
        if r % 2 != 0:
            print(f"Odd order {r}, retrying...")
            continue  # Retry if the order is odd
        
        # Guesses for factors
        guesses = [gcd(a**(r//2) - 1, N), gcd(a**(r//2) + 1, N)]
        print(f"Guessed Factors: {guesses[0]} and {guesses[1]}")
        
        for guess in guesses:
            if guess not in [1, N] and N % guess == 0:
                print(f"*** Non-trivial factor found: {guess} ***")
                FACTOR_FOUND = True
                break

# Run Shor's algorithm to factor 15
shors_algorithm()
