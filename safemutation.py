import random
from circuitsolution import CircuitSolution
from config import *
from copy import deepcopy
from jmetal.operator.mutation import Mutation
from util import *

class CircuitMutation(Mutation):
    def __init__(self, mutation_probability: float = 0.1, TRUTH_TABLE = None):
        super(CircuitMutation, self).__init__(mutation_probability)
        self.mutation_probability = mutation_probability
        self.truth_table = TRUTH_TABLE

    def execute(self, solution):
        # Create proper copy
        new_solution = CircuitSolution()
        new_solution.variables = [deepcopy(solution.variables[0])]
        new_solution.objectives = [None]
        new_solution.constraints = []
        new_solution.attributes = {}

        # Adaptive mutation rate (lower for better solutions)
        fitness_val = solution.objectives[0] if solution.objectives[0] is not None else 0.0
        # Higher fitness = lower mutation rate
        adaptive_rate = self.mutation_probability * (1.0 - fitness_val * 0.5)

        if random.random() < adaptive_rate:
            circuit = new_solution.variables[0]

            # Choose mutation type based on circuit characteristics
            mutation_types = []
            if len(circuit) < MAX_GENES:
                mutation_types.append(['add'])
            if len(circuit) > MIN_GENES:
                mutation_types.append('remove')
            if len(circuit) > 0:
                mutation_types.extend(['change', 'change', 'swap', 'split'])  # Make change more likely
            if self.is_circuit_correct(circuit):
                mutation_types.extend(['optimize'])

            if not mutation_types:
                return new_solution

            mutation_type = random.choice(mutation_types)

            if mutation_type == 'add':
                # Insert at random position
                pos = random.randint(0, len(circuit))
                circuit.insert(pos, random_gate())
            elif mutation_type == 'remove':
                # Remove random gate
                idx = random.randint(0, len(circuit) - 1)
                del circuit[idx]
            elif mutation_type == 'change':
                # Change random gate with another
                idx = random.randint(0, len(circuit) - 1)
                circuit[idx] = random_gate()
            elif mutation_type == 'swap':
                # Swap two random gates
                if len(circuit) > 1:
                    i, j = random.sample(range(len(circuit)), 2)
                    circuit[i], circuit[j] = circuit[j], circuit[i]
            elif mutation_type == 'split':
                # Consider only a subset of the circuit
                if len(circuit) > 2:
                    start = random.randint(0, len(circuit) - 2)
                    end = random.randint(start + 1, len(circuit) - 1)
                    circuit = circuit[start:end]
            elif mutation_type == 'optimize':
                # Perform post-optimization
                circuit = self.post_optimize(circuit)

        return new_solution

    def get_name(self) -> str:
        return "SafeMutation"

    def perm_order(self, p):
        idp = [0,1,2,3]
        cur = p[:]
        for k in range(1, 25): 
            if cur == idp:
                return k
            cur = self.perm_compose(cur, p)
        return 24

    def perm_compose(self, p, q):
        return [q[p[i]] for i in range(4)]

    def gate_perm(self, gtype):
        key = gtype[3:] if gtype.startswith("C") else gtype[1:]
        return QSG_TABLE[key]

    def gates_same_wire(self, g1, g2):
        return (g1[0] == g2[0]) and (g1[1] == g2[1])

    def simplify_local(self,circ):
        if not circ:
            return circ
        out = []
        for g in circ:
            g = normalize_gate(g)
            # drop exact duplicates
            if out and g == out[-1]:
                continue
            # inverse cancellation on same wires (Z-like)
            if out and self.gates_same_wire(g, out[-1]) and g[2][0] == out[-1][2][0]:
                p1 = self.gate_perm(out[-1][2])
                p2 = self.gate_perm(g[2])
                comp = self.perm_compose(p1, p2)
                if comp == [0,1,2,3]:
                    out.pop()
                    continue
            out.append(g)

        # power reduction: k repeats modulo permutation order
        reduced = []
        i = 0
        while i < len(out):
            j = i + 1
            while j < len(out) and out[j] == out[i]:
                j += 1
            run_len = j - i
            if run_len > 1:
                ordk = self.perm_order(self.gate_perm(out[i][2]))
                keep = run_len % ordk
                reduced.extend([out[i]] * keep)
            else:
                reduced.append(out[i])
            i = j
        return reduced

    def greedy_prune(self,circ):
        circ = circ[:]
        changed = True
        while changed:
            changed = False
            i = 0
            while i < len(circ):
                trial = circ[:i] + circ[i+1:]
                if self.is_circuit_correct(trial):
                    circ = trial
                    changed = True
                else:
                    i += 1
            circ = self.simplify_local(circ)
        return circ

    def post_optimize(self,circ):
        c1 = self.simplify_local(circ)
        if self.is_circuit_correct(c1):
            c2 = self.greedy_prune(c1)
            return c2
        return circ
    
    def is_circuit_correct(self, circuit):
        return fitness(circuit, self.truth_table) >= 1.0