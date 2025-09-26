import random
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from quantumcircuitproblem import QuantumCircuitProblem
from util import *
from config import *

class ElitistGeneticAlgorithm(GeneticAlgorithm):
    def __init__(self, problem, population_size, offspring_population_size, 
                 mutation, crossover, termination_criterion, selection, elite_size=5):
        super().__init__(problem, population_size, offspring_population_size,
                        mutation, crossover, selection, termination_criterion)
        self.elite_size = elite_size
        self.best_fitness_history = []
        self.generation_count = 0
        self.stagnation_count = 0
        self.best_seen = 0.0

    def replacement(self, population, offspring_population):
        self.generation_count += 1

        # Combine populations
        all_solutions = population + offspring_population

        # Sort by fitness (descending for maximization)
        all_solutions.sort(key=lambda x: x.objectives[0] if x.objectives[0] is not None else float('-inf'), 
                          reverse=True)

        # Check for stagnation
        current_best = all_solutions[0].objectives[0] if all_solutions[0].objectives[0] is not None else 0.0
        if current_best <= self.best_seen + 1e-6:
            self.stagnation_count += 1
        else:
            self.best_seen = current_best
            self.stagnation_count = 0
            print(f"NEW BEST FITNESS: {current_best:.6f} at generation {self.generation_count}")

            # Apply local search to new best solutions
            if current_best > 0.8:  # Only for high-fitness solutions
                print("Applying local search to best solution...")
                improved = self.local_search(all_solutions[0])
                if improved.objectives[0] > current_best:
                    all_solutions[0] = improved
                    print(f"Local search improvement: {improved.objectives[0]:.6f}")

        # Diversity injection if stagnated
        if self.stagnation_count > STAGNATION_LIMIT and current_best > 0.8:
            print(f"AGGRESSIVE DIVERSITY INJECTION at generation {self.generation_count}")
            elite_solutions = all_solutions[:self.elite_size]

            # Replace 50% with diverse solutions when close to optimum
            diverse_solutions = []
            for _ in range(int(self.population_size * 0.8)):
                new_solution = self.problem.create_solution()
                self.problem.evaluate(new_solution)
                diverse_solutions.append(new_solution)

            remaining_needed = self.population_size - len(elite_solutions) - len(diverse_solutions)
            remaining_solutions = all_solutions[self.elite_size:self.elite_size + remaining_needed]

            new_population = elite_solutions + diverse_solutions + remaining_solutions
            self.stagnation_count = 0
        elif self.stagnation_count > STAGNATION_LIMIT:
            print(f"DIVERSITY INJECTION at generation {self.generation_count}")
            # Keep elite but replace 30% with new random solutions
            elite_solutions = all_solutions[:self.elite_size]
            diverse_solutions = []

            for _ in range(int(self.population_size * 0.3)):
                new_solution = self.problem.create_solution()
                self.problem.evaluate(new_solution)
                diverse_solutions.append(new_solution)

            remaining_needed = self.population_size - len(elite_solutions) - len(diverse_solutions)
            remaining_solutions = all_solutions[self.elite_size:self.elite_size + remaining_needed]

            new_population = elite_solutions + diverse_solutions + remaining_solutions
            self.stagnation_count = 0
        else:
            # Standard elitist selection
            new_population = all_solutions[:self.population_size]

        # Track fitness
        self.best_fitness_history.append(current_best)

        # Progress reporting
        if self.generation_count % 50 == 0:
            avg_fitness = sum(sol.objectives[0] for sol in new_population[:10] if sol.objectives[0] is not None) / 10
            diversity = self.calculate_diversity(new_population[:20])
            print(f"Gen {self.generation_count:3d}: Best={current_best:.4f}, Avg={avg_fitness:.4f}, Diversity={diversity:.3f}")

        return new_population
    
    def local_search(self, solution):
        """Hill climbing local search on a solution"""
        best_solution = solution.copy()
        current_fitness = solution.objectives[0] if solution.objectives[0] is not None else 0.0

        # Try multiple local modifications
        for attempt in range(20):  # 20 local search attempts
            # Create a neighbor by small modification
            neighbor = best_solution.copy()
            circuit = neighbor.variables[0]

            if len(circuit) == 0:
                continue

            # Choose modification type
            mod_type = random.choice(['change', 'add', 'remove', 'swap'])

            if mod_type == 'change' and len(circuit) > 0:
                idx = random.randint(0, len(circuit) - 1)
                circuit[idx] = random_gate()
            elif mod_type == 'add' and len(circuit) < MAX_GENES:
                pos = random.randint(0, len(circuit))
                circuit.insert(pos, random_gate())
            elif mod_type == 'remove' and len(circuit) > MIN_GENES:
                idx = random.randint(0, len(circuit) - 1)
                del circuit[idx]
            elif mod_type == 'swap' and len(circuit) > 1:
                i, j = random.sample(range(len(circuit)), 2)
                circuit[i], circuit[j] = circuit[j], circuit[i]

            # Evaluate neighbor
            self.problem.evaluate(neighbor)

            if neighbor.objectives[0] > current_fitness:
                best_solution = neighbor.copy()
                current_fitness = neighbor.objectives[0]

        return best_solution

    def calculate_diversity(self, solutions):
        """Calculate diversity based on circuit length variation"""
        if not solutions:
            return 0.0
        lengths = [len(sol.variables[0]) for sol in solutions if sol.variables]
        if len(set(lengths)) <= 1:
            return 0.0
        return len(set(lengths)) / len(lengths)