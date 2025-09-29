# Genetic Algorithm for Synthesizing a Quantum Circuit given its truth table

import random
from copy import deepcopy
from quantumcircuitproblem import QuantumCircuitProblem
from jmetal.operator.selection import BinaryTournamentSelection
from safemutation import CircuitMutation
from circuitcrossover import CircuitCrossover
from config import *
from jmetal.util.observer import PrintObjectivesObserver
from jmetal.util.termination_criterion import TerminationCriterion
from util import *
from geneticalgorithm import ElitistGeneticAlgorithm

TRUTH_TABLE = generate_subcomparator_truth_table()
CIRCUIT_NAME = "SubComparator"
OUTPUT_FILE_NAME = "output" + CIRCUIT_NAME + ".txt"
BEST_CIRCUIT = "best_circuit_" + CIRCUIT_NAME + ".txt"
N_REPETITIONS = 20

class TerminationByFitness(TerminationCriterion):
    def __init__(self, target_fitness: float, max_evaluation: int):
        super(TerminationByFitness, self).__init__()
        self.target_fitness = target_fitness
        self.best_fitness = float('-inf')
        self.max_evaluations = max_evaluation
        self.evaluations = 0

    @property
    def is_met(self):
        current_best = max(algorithm.result().objectives)
        if current_best > self.best_fitness:
            self.best_fitness = current_best
        #return self.best_fitness == self.target_fitness or 
        return self.evaluations >= self.max_evaluations
    
    def update(self, *args, **kwargs):
        self.evaluations = kwargs["EVALUATIONS"]

# Main function
if __name__ == "__main__":

    best_finess = 0

    # Open the file to log results
    with open(OUTPUT_FILE_NAME, "w") as f:
        f.write("Run,Best Fitness,Circuit Length\n")

        for n in range(N_REPETITIONS):
            print(f"\n--- RUN {n+1}/{N_REPETITIONS} ---\n")

            problem = QuantumCircuitProblem(TRUTH_TABLE)

            algorithm = ElitistGeneticAlgorithm(
                problem=problem,
                population_size=POP_SIZE,
                offspring_population_size=POP_SIZE,
                mutation=CircuitMutation(MUTATION_RATE, TRUTH_TABLE),
                crossover=CircuitCrossover(CROSSOVER_RATE),
                termination_criterion=TerminationByFitness(1.0,POP_SIZE*GENERATIONS),
                elite_size=10,
                selection=BinaryTournamentSelection()
            )

            algorithm.observable.register(observer=PrintObjectivesObserver(POP_SIZE))

            algorithm.run()
            result = algorithm.result()

            best_circuit = result.variables[0]

            # Print final circuit
            print("Circuit Length:", len(best_circuit))
            print("Circuit Gates:")
            for i, g in enumerate(best_circuit):
                print(f"{i+1}: Control={g[0]}, Target={g[1]}, Gate={g[2]}")

            # Validate against truth table
            print("Truth Table Check for the given circuit:")
            success = True
            for inp, expected in TRUTH_TABLE.items():
                output = simulate_circuit(best_circuit, inp)
                check_result = "✔️" if output[2] == expected[2] else "❌"
                if check_result == "❌":
                    success = False
                print(f"a={inp[0]} b={inp[1]} → f={output[2]} (expected {expected[2]}) {check_result}")

            if success:
                print("\nSUCCESS: Circuit correctly detects the given function")
            else:
                print("\n!!WARNING!!: Circuit has issues detecting the given function")

            # Log results
            f.write(f"{n+1},{result.objectives[0]},{len(best_circuit)}\n")
            f.flush()

            # Save best circuit to file
            if (result.objectives[0] > best_finess and result.objectives[0] >= 1):
                best_finess = result.objectives[0]
                with open(BEST_CIRCUIT, "w") as f2:
                    f2.write(f"# Best circuit found (Fitness: {result.objectives[0]}, Length: {len(best_circuit)})\n")
                    for i, g in enumerate(best_circuit):
                        f2.write(f"{i+1}: Control={g[0]}, Target={g[1]}, Gate={g[2]}\n")