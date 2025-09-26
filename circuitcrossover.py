import random
from jmetal.operator.crossover import Crossover
from circuitsolution import CircuitSolution
from config import *

class CircuitCrossover(Crossover):
    def __init__(self, probability: float = 0.7):
        super(CircuitCrossover, self).__init__(probability)

    def execute(self, parents):
        if len(parents) != 2:
            return parents

        parent1, parent2 = parents[0], parents[1]
        circuit1 = parent1.variables[0]
        circuit2 = parent2.variables[0]

        if random.random() > self.probability:
            return [parent1.copy(), parent2.copy()]

        # Single-point crossover
        if len(circuit1) > 1 and len(circuit2) > 1:
            cut1 = random.randint(1, len(circuit1))
            cut2 = random.randint(1, len(circuit2))

            child1_circuit = circuit1[:cut1] + circuit2[cut2:]
            child2_circuit = circuit2[:cut2] + circuit1[cut1:]

            # Ensure length constraints
            if len(child1_circuit) > MAX_GENES:
                child1_circuit = child1_circuit[:MAX_GENES]
            if len(child2_circuit) > MAX_GENES:
                child2_circuit = child2_circuit[:MAX_GENES]

            child1 = CircuitSolution(child1_circuit)
            child2 = CircuitSolution(child2_circuit)

            return [child1, child2]

        return [parent1.copy(), parent2.copy()]

    def get_number_of_parents(self):
        return 2

    def get_number_of_children(self):
        return 2

    def get_name(self):
        return "CircuitCrossover"