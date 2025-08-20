from random import choice
import pygame


class People:
    """
    Represents an individual in the genetic maze solver.

    Attributes:
        start_pos (tuple[int, int]): Starting coordinates (x, y) in the maze.
        position (tuple[int, int]): Current position in the maze.
        moves (list[str]): List of movements ('up', 'down', 'left', 'right').
        max_moves (int): Maximum number of moves allowed.
        current_move (int): Index of the current move being executed.
        has_moves_left (bool): True if the individual still has moves left.
        has_reached_end (bool): True if the individual has reached the goal.
        number (int): Unique index of the individual (used for color).
        color (tuple[int, int, int]): RGB color of the individual.
        color_name (str): Name of the color.
        goal_pos (tuple[int, int]): Maze exit coordinates.
        fitness_score (int): Fitness score of the individual.
        best_path (list[tuple[int, int]]): Optimal path through the maze.
    """

    COLORS = [
        "#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6",
        "#1ABC9C", "#E67E22", "#E74C3C", "#8E44AD", "#34495E",
    ]

    COLORS_NAME = [
        "orange", "green", "blue", "yellow", "purple",
        "turquoise", "carrot", "red", "dark_mauve", "dark_blue_gray",
    ]

    def __init__(self, start_pos, number, cols, rows, best_path, defined_moves=None):
        """
        Initialize a People instance.

        Args:
            start_pos (tuple[int, int]): Starting coordinates (x, y).
            number (int): Unique index of the individual.
            cols (int): Number of columns in the maze.
            rows (int): Number of rows in the maze.
            best_path (list[tuple[int, int]]): Optimal path for guidance.
            defined_moves (list[str], optional): Predefined sequence of moves.
        """
        self.start_pos = start_pos
        self.position = start_pos
        self.moves = []
        self.max_moves = (rows + cols) * 2
        self.current_move = 0
        self.has_moves_left = True
        self.has_reached_end = False
        self.number = number
        self.color = People.COLORS[number]
        self.color_name = People.COLORS_NAME[number]
        self.goal_pos = (cols - 2, rows - 2)
        self.fitness_score = None
        self.best_path = best_path

        if defined_moves is None:
            self.random_moves()
        else:
            self.moves = list(defined_moves)

    def random_moves(self):
        """Initialize a list of random moves ('up', 'down', 'left', 'right')."""
        directions = ['up', 'down', 'left', 'right']
        self.moves = [choice(directions) for _ in range(self.max_moves)]

    def step(self, maze):
        """
        Execute one move of the individual.

        Args:
            maze (list[list[int]]): Maze grid for collision detection.
        """
        if self.current_move < self.max_moves:
            move = self.moves[self.current_move]
            self.apply_move(move, maze)
            self.current_move += 1
        else:
            self.has_moves_left = False

    def apply_move(self, move, maze):
        """
        Apply a single movement if the path is free; penalize if blocked.

        Args:
            move (str): Direction to move ('up', 'down', 'left', 'right').
            maze (list[list[int]]): Maze grid for collision detection.
        """
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
        """
        Draw the individual on the Pygame screen as a colored circle.

        Args:
            screen (pygame.Surface): Pygame surface to draw on.
            cell_size (int): Size of a maze cell in pixels.
        """
        px, py = self.position
        pygame.draw.circle(
            screen,
            self.color,
            (px * cell_size + cell_size // 2, py * cell_size + cell_size // 2),
            cell_size // 3
        )

    def fitness(self):
        """
        Compute the fitness score.

        Penalizes being off the optimal path and distance from goal.
        """
        self.fitness_score = 0
        if self.position not in self.best_path:
            self.fitness_score += 15

        x1, y1 = self.position
        x2, y2 = self.goal_pos
        self.fitness_score += abs(x1 - x2) + abs(y1 - y2)

    def has_reach_goal(self, maze):
        """
        Check if the individual has reached the maze exit.

        Args:
            maze (list[list[int]]): Maze grid.
        """
        x, y = self.position
        if maze[y][x] == "E":
            self.has_reached_end = True
