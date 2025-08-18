from random import choice

import pygame


class People:
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6"]
    colors_name = ["orange", "vert", "bleu", "jaune", "violet"]

    def __init__(self, start_pos, max_moves, number, cols, rows, defined_moves=None):
        self.start_pos = start_pos
        self.position = start_pos  # Position actuelle
        self.moves = []  # Liste des mouvements appliqués
        self.max_moves = max_moves  # Nombre maximal de mouvements
        self.has_moves_left = True  # Booléen pour savoir s'il reste des mouvements
        self.has_reached_end = False # Booléen pour savoir si quelqu'un est sortie du labyrinthe
        self.number = number # Identifiant pour le nb people, utile pour attribuer une couleur
        if defined_moves is None:
            self.random_moves()
        else:
            self.moves = list(defined_moves)

        self.color = People.colors[number]
        self.color_name = People.colors_name[number]
        self.cols = cols
        self.rows = rows
        self.goal_pos = (self.cols - 2, self.rows - 2)
        self.fitness_score = None # Fitness score, plus on est proche de la sortie plus il est bas
        self.moves_left = max_moves

    def random_moves(self):
        """Initialise une liste aléatoire de mouvements."""
        directions = ['up', 'down', 'left', 'right']
        self.moves = [choice(directions) for _ in range(self.max_moves)]

    def step(self, maze):
        if self.moves_left > 0:
            move = self.moves.pop(0)
            self.apply_move(move, maze)
            self.moves_left -= 1
            self.moves.append(move)
        else:
            self.has_moves_left = False

    def apply_move(self, move, maze):
        """Applique un mouvement à la position actuelle si le chemin n'est pas bloqué par un mur (dans ce cas pénalité)"""
        x, y = self.position

        if move == 'up' and y > 0 and maze[y - 1][x] != 1:
            self.position = (x, y - 1)
        elif move == 'down' and y < len(maze) - 1 and maze[y + 1][x] != 1:
            self.position = (x, y + 1)
        elif move == 'left' and x > 0 and maze[y][x - 1] != 1:
            self.position = (x - 1, y)
        elif move == 'right' and x < len(maze[0]) - 1 and maze[y][x + 1] != 1:
            self.position = (x + 1, y)
        else:
            if self.fitness_score is not None:
                self.fitness_score += 2
            else:
                self.fitness_score = 2
        self.has_reach_goal(maze)

    def draw(self, screen, cell_size):
        px, py = self.position
        pygame.draw.circle(screen, self.color,
                           (px * cell_size + cell_size // 2,
                            py * cell_size + cell_size // 2),
                           cell_size // 3)

    def fitness(self):
        x1, y1 = self.position
        x2, y2 = self.goal_pos
        self.fitness_score += abs(x1 - x2) + abs(y1 - y2)

    def has_reach_goal(self, maze):
        x, y = self.position
        if maze[y][x] == "E":
            self.has_reached_end = True

