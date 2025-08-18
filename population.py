from random import randint, choice
from people import People


class Population:
    def __init__(self, size, start_pos, max_moves, cols, rows):
        self.size = size
        self.individuals = [People(start_pos, max_moves, i, cols, rows) for i in range(size)]
        self.best_individuals = []
        self.start_pos = start_pos
        self.max_moves = max_moves
        self.cols = cols
        self.rows = rows

    def evaluate(self):
        for ind in self.individuals:
            ind.fitness()

    def select_best(self, n=2):
        self.evaluate()
        self.best_individuals = sorted(self.individuals, key=lambda x: x.fitness_score)[:n]

    def crossover(self, parent1, parent2):
        """Retourne un enfant en croisant deux parents."""
        cut = randint(0, len(parent1.moves) - 1)
        new_moves = parent1.moves[:cut] + parent2.moves[cut:]
        return new_moves

    def mutate(self, moves, mutation_rate=0.2):
        """Applique une mutation aléatoire sur une liste de mouvements."""
        directions = ['up', 'down', 'left', 'right']
        mutated_moves = []
        for move in moves:
            if randint(1, 100) <= mutation_rate * 100:  # probabilité de mutation
                mutated_moves.append(choice(directions))
            else:
                mutated_moves.append(move)
        return mutated_moves

    def generate_next_generation(self):
        if len(self.best_individuals) < 2:
            return  # il faut au moins 2 parents

        parent1, parent2 = self.best_individuals
        new_generation = []

        # Enfant 1 : clone du parent1 (muté)
        moves1 = self.mutate(parent1.moves.copy())
        new_generation.append(People(self.start_pos, self.max_moves, 0,
                                     self.cols, self.rows, defined_moves=moves1))

        # Enfant 2 : clone du parent2 (muté)
        moves2 = self.mutate(parent2.moves.copy())
        new_generation.append(People(self.start_pos, self.max_moves, 1,
                                     self.cols, self.rows, defined_moves=moves2))

        # Enfant 3 : crossover A->B (muté)
        moves3 = self.mutate(self.crossover(parent1, parent2))
        new_generation.append(People(self.start_pos, self.max_moves, 2,
                                     self.cols, self.rows, defined_moves=moves3))

        # Enfant 4 : crossover B->A (muté)
        moves4 = self.mutate(self.crossover(parent2, parent1))
        new_generation.append(People(self.start_pos, self.max_moves, 3,
                                     self.cols, self.rows, defined_moves=moves4))

        # Enfant 5 : mélange aléatoire (muté)
        mixed_moves = [choice([m1, m2]) for m1, m2 in zip(parent1.moves, parent2.moves)]
        moves5 = self.mutate(mixed_moves)
        new_generation.append(People(self.start_pos, self.max_moves, 4,
                                     self.cols, self.rows, defined_moves=moves5))

        self.individuals = new_generation
