# Shor's Algorithm Implementation

This project implements Shor's algorithm for integer factorization using quantum computing simulation. It's designed to factor the number 15 using Qiskit, a quantum computing framework.

## Overview

Shor's algorithm is a quantum algorithm for integer factorization, significant for its ability to break RSA encryption. This implementation demonstrates the algorithm's core concepts using a quantum circuit to factor the number 15.

## Prerequisites

To run this code, you need:

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone [your-repository-url]
   cd [your-project-directory]
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

4. Install the required packages:
   ```bash
   pip install qiskit numpy matplotlib
   ```

## Usage

1. Ensure your virtual environment is activated.

2. Run the script using Python:
   ```bash
   python shor_algorithm.py
   ```

The script will attempt to factor 15 using Shor's algorithm. It will output:
- The randomly chosen 'a' value
- The measured quantum state
- The corresponding phase
- The calculated order 'r'
- The guessed factors

The algorithm will continue running until it finds a non-trivial factor.

## Code Structure

- `c_amod15(a, power)`: Creates a controlled-U gate for modular exponentiation.
- `qft_dagger(n)`: Implements the inverse Quantum Fourier Transform.
- `qpe_amod15(a)`: Performs the Quantum Phase Estimation for a given 'a'.
- `shors_algorithm()`: The main function implementing Shor's algorithm.

## How It Works

1. The algorithm randomly selects a number 'a' coprime to 15.
2. It uses Quantum Phase Estimation to find the period of the function f(x) = a^x mod 15.
3. From this period, it calculates potential factors of 15.
4. It repeats this process until a non-trivial factor is found.

## Limitations

This implementation is designed specifically for factoring 15 and uses a local quantum simulator. For factoring larger numbers or using real quantum hardware, significant modifications would be required.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or extensions to the algorithm.

## License

[Specify your chosen license here]

## Acknowledgements

This implementation is based on Qiskit's tutorials and documentation on Shor's algorithm.

## Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment:

```bash
deactivate
```

This will return you to your global Python environment.