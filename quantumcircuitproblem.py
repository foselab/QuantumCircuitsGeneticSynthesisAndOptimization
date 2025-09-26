from jmetal.core.problem import Problem
import random
from util import fitness, random_gate
from config import *
from circuitsolution import CircuitSolution

# The problem class
class QuantumCircuitProblem(Problem):
    def __init__(self,truth_table):
        super(QuantumCircuitProblem, self).__init__()
        self.number_of_variables = 1
        self.number_of_objectives = 1
        self.number_of_constraints = 0
        self.lower_bound = [MIN_GENES]
        self.upper_bound = [MAX_GENES]
        self.obj_directions = [self.MAXIMIZE]
        self.obj_labels = ['Fitness']
        self.truth_table = truth_table

    def evaluate(self, solution):
        circuit = solution.variables[0]
        fit = fitness(circuit, self.truth_table)
        solution.objectives[0] = fit 

    def create_solution(self):
         # More diverse initial circuit lengths
        num_genes = random.choices([1,2,3,4,5,6,7,8], 
                                 weights=[10,15,20,20,15,10,5,5])[0]
        circuit = [random_gate() for _ in range(num_genes)]
        solution = CircuitSolution(circuit)
        return solution
    
    def name(self):
        return "QuantumCircuitProblem"
    
    def number_of_constraints(self):
        return 0
    
    def number_of_objectives(self):
        return 1
    
    def number_of_variables(self):
        return 1