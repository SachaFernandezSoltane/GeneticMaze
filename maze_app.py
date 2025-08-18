import pygame
from maze_generator import MazeGenerator

from population import Population


class MazeApp:
    CELL_SIZE = 40

    def __init__(self, rows, cols):
        self.maze_status = 'RUNNING'
        self.running = True
        self.rows = rows
        self.cols = cols
        self.maze_generator = MazeGenerator(rows, cols)
        self.grid = self.maze_generator.generator_maze()
        self.index_generation = 0

        pygame.init()
        self.screen = pygame.display.set_mode((cols * self.CELL_SIZE, rows * self.CELL_SIZE))
        pygame.display.set_caption("Maze Generator")

        self.colors = {
            0: (255, 255, 255),  # chemin
            1: (0, 0, 0),        # mur
            "S": (0, 255, 0),    # départ
            "E": (255, 0, 0)     # arrivée
        }
        self.population = Population(5,(1,1),(self.rows + self.cols)*2,self.cols, self.rows)
        self.people_update = pygame.USEREVENT
        pygame.time.set_timer(self.people_update, 60)

    def draw(self):
        # Dessine le labyrinthe
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                color = self.colors[cell]
                pygame.draw.rect(self.screen, color,
                                 (c * self.CELL_SIZE, r * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Dessine tous les individus
        for p in self.population.individuals:
            p.draw(self.screen, self.CELL_SIZE)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.people_update:
                all_done = True
                for p in self.population.individuals:
                    p.step(self.grid)
                    if p.has_reached_end:
                        print('The race is finished')
                        self.maze_status = 'FINISHED'

                    if p.has_moves_left:
                        all_done = False

                if all_done:
                    print(f"Fin de la génération : {self.index_generation}")
                    self.index_generation = self.index_generation + 1
                    self.population.select_best(2)
                    self.population.generate_next_generation()


    def run(self):
        while self.running:
            if self.maze_status == 'RUNNING':
                self.handle_events()
                self.draw()

            pygame.display.flip()
        pygame.quit()
