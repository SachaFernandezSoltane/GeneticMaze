from collections import deque
import pygame

from src.genetic.population import Population
from src.maze.maze_generator import MazeGenerator


class MazeApp:
    """
    MazeApp runs a genetic algorithm simulation to solve a randomly generated maze.

    It handles:
        - Maze generation
        - Rendering the maze and individuals using Pygame
        - Stepping through individuals in the population
        - Evolving the population when all individuals finish
        - BFS pathfinding for the optimal path (used to guide the population)

    Attributes:
        CELL_SIZE (int): Size of each cell in pixels.
        running (bool): Controls the main loop.
        rows (int): Number of rows in the maze.
        cols (int): Number of columns in the maze.
        maze_generator (MazeGenerator): Instance to generate the maze.
        grid (list[list[int]]): 2D list representing the maze grid.
        index_generation (int): Current generation index.
        screen (pygame.Surface): Pygame window.
        colors (dict): Mapping of cell types to colors.
        population (Population): Current population of individuals solving the maze.
        people_update (int): Pygame event ID for population updates.
    """

    CELL_SIZE = 40

    def __init__(self, rows, cols, initial_population_size, refreshing_timer):
        """
        Initialize MazeApp.

        Args:
            rows (int): Number of rows in the maze.
            cols (int): Number of columns in the maze.
            initial_population_size (int): Number of individuals in the population.
            refreshing_timer (int): Pygame timer in milliseconds for each step update.
        """
        pygame.init()
        pygame.display.set_caption("Genetic maze solver")
        self.people_update = pygame.USEREVENT
        pygame.time.set_timer(self.people_update, refreshing_timer)

        self.running = True
        self.rows = rows
        self.cols = cols
        self.maze_generator = MazeGenerator(rows, cols)
        self.grid = self.maze_generator.generator_maze()
        self.index_generation = 0

        self.screen = pygame.display.set_mode((cols * self.CELL_SIZE, rows * self.CELL_SIZE))

        self.colors = {
            0: (255, 255, 255),  # Path is white
            1: (0, 0, 0),        # Wall is black
            "S": (0, 255, 0),    # Start is green
            "E": (255, 0, 0)     # End is red
        }

        path_to_exit = self.bfs(self.grid, (1, 1), (self.rows - 2, self.cols - 2), rows, cols)
        self.population = Population(initial_population_size, (1, 1), self.cols, self.rows, path_to_exit)

    def draw(self):
        """
        Draw the maze and all individuals on the Pygame screen.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                color = self.colors[cell]
                pygame.draw.rect(self.screen, color,
                                 (c * self.CELL_SIZE, r * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        for p in self.population.individuals:
            p.draw(self.screen, self.CELL_SIZE)

    def handle_events(self):
        """
        Handle Pygame events, move individuals, and manage generation updates.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.people_update:
                all_done = True
                for p in self.population.individuals:
                    p.step(self.grid)
                    if p.has_reached_end:
                        print('The race is finished')
                        self.running = False
                    if p.has_moves_left:
                        all_done = False

                if all_done:
                    print(f"Fin de la génération : {self.index_generation}")
                    self.index_generation += 1
                    self.population.generate_next_generation()

    def bfs(self, maze, start, end, rows, cols):
        """
        Find the shortest path from start to end in the maze using BFS.

        Args:
            maze (list[list[int]]): The maze grid.
            start (tuple[int, int]): Starting cell coordinates (row, col).
            end (tuple[int, int]): Target cell coordinates (row, col).
            rows (int): Number of rows in the maze.
            cols (int): Number of columns in the maze.

        Returns:
            list[tuple[int, int]]: Ordered list of coordinates from start to end.
            Returns None if no path exists.
        """
        queue = deque([start])
        visited = {start}
        parent = {}

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                path = []
                cur = end
                while cur != start:
                    path.append(cur)
                    cur = parent[cur]
                path.append(start)
                return path[::-1]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if maze[nx][ny] != 1 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
        return None

    def run(self):
        """
        Start the main Pygame loop to run the simulation.
        """
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
        pygame.quit()
