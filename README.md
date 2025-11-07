# Genetic Synthesis of Compact Quaternary Reversible Comparators for Quantum Computing

This repository contains the implementation of a genetic algorithm designed to synthesize quantum circuits that perform quaternary reversible comparisons, as described in the paper ``Genetic Synthesis of Compact Quaternary Reversible Comparators for Quantum Computing''. 
The algorithm focuses on optimizing the circuit size while ensuring accurate functionality.

By starting from the truth table of the desired comparator, the genetic algorithm iteratively evolves a population of candidate quantum circuits. The fitness of each circuit is evaluated based on its ability to correctly implement the comparison operation and its overall size. The algorithm employs selection, crossover, and mutation operations to explore the search space and converge towards optimal or near-optimal solutions.

In our work, we tested the algorithm on various quaternary reversible comparator functions, demonstrating its effectiveness in producing compact quantum circuits that meet the required specifications. More specifically, this repository contains the results for the synthesis of:

- Lower-than comparator
- Greater-than comparator
- Equal-to comparator
- Full comparator
- Subcompator (to be used in the generalization of the 1-qudt full comparator to n-qudit full comparator)

## Requirements
- Python 3.7 or highr
- jMetalPy library
- NumPy

## Usage

After having cloned the repository, you can run the genetic algorithm using the following command:

```bash
python main.py
```

In the `main.py` file, you can adjust parameters such as the number of runs (`N_REPETITIONS`), the name of the circuit to be synthesized (`CIRCUIT_NAME`), and provide the function returning the truth table for the desired comparator (`TRUTH_TABLE`).

The execution will generate two output files:
- `output<CIRCUIT_NAME>.csv`: Contains the best fitness, circuit length, and execution time for each run.
- `best_circuit_<CIRCUIT_NAME>.txt`: Contains the details of the best circuit found among the runs.

### Further configurations

Further configuration parameters can be adjusted directly in the `config.py` file:
- `NUM_QULINES`, the number of qudits in the circuit
- `QUBASE`, the base of the qudits (4 for quaternary circuits)
- `MAX_GENES`, the maximum number of gates in a circuit
- `MIN_GENES`, the minimum number of gates in a circuit
- `POP_SIZE`, the population size
- `GENERATIONS`, the number of generations
- `MUTATION_RATE`, the mutation rate
- `CROSSOVER_RATE`, the crossover rate
- `STAGNATION_LIMIT`, the number of generations without improvement before introducing diversity

### Available truth tables

The file `util.py` contains the truth tables for the available comparator functions. You can modify or add new truth tables as needed. Currently, the following truth tables are implemented:
- `generate_lower_truth_table()`, for the lower-than comparator
- `generate_greater_truth_table()`, for the greater-than comparator
- `generate_equal_truth_table()`, for the equal-to comparator
- `generate_ququart_truth_table()`, for the full comparator
- `generate_subcomparator_truth_table()`, for the subcomparator