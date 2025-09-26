from jmetal.core.solution import Solution
from copy import deepcopy

class CircuitSolution(Solution):
    def __init__(self, variables=None):
        super(CircuitSolution, self).__init__(1,1)
        self.variables = [variables] if variables is not None else []
        self.objectives = [None]
        self.constraints = []
        self.attributes = {}

    def copy(self):
        new_solution = CircuitSolution()
        new_solution.variables = [deepcopy(self.variables[0])]
        new_solution.objectives = [self.objectives[0] if self.objectives[0] is not None else None]
        new_solution.constraints = self.constraints.copy()
        new_solution.attributes = self.attributes.copy()
        return new_solution

    def __str__(self):
        return f"Circuit: {self.variables}, Fitness: {self.objectives[0]}"