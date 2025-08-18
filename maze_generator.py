from random import randrange

class MazeGenerator:
    def __init__(self, height, width):
        self.height = height
        self.width = width


    def generator_maze(self):
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # point de départ aléatoire sur une cellule "impair"
        current_row = randrange(1, self.height, 2)
        current_col = randrange(1, self.width, 2)
        grid[current_row][current_col] = 0
        frontier = [(current_row, current_col)]

        while len(frontier) > 0:
            list_neighbors = self.find_neighbors(current_row, current_col, grid)

            if len(list_neighbors) > 0:
                # choisir un voisin aléatoire
                index_selected_neighbors = randrange(len(list_neighbors))
                selected_neighbor = list_neighbors[index_selected_neighbors]

                # ouvrir le mur entre les cellules
                row_to_open = (selected_neighbor[0] + current_row) // 2
                col_to_open = (selected_neighbor[1] + current_col) // 2

                grid[row_to_open][col_to_open] = 0
                grid[selected_neighbor[0]][selected_neighbor[1]] = 0

                # ajouter le voisin à frontier
                frontier.append(selected_neighbor)

                # choisir une cellule aléatoire dans frontier
                current_row, current_col = frontier[randrange(len(frontier))]
            else:
                frontier.remove((current_row, current_col))
                if len(frontier) > 0:
                    current_row, current_col = frontier[randrange(len(frontier))]

        # définir le départ et l'arrivée
        grid[1][1] = "S"  # départ
        grid[self.height - 2][self.width - 2] = "E"  # arrivée

        return grid

    def find_neighbors(self, current_row, current_col, grid):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # haut, bas, gauche, droite
        neighbors = []
        for dr, dc in directions:
            nr, nc = current_row + dr, current_col + dc
            if 0 <= nr < self.height and 0 <= nc < self.width and grid[nr][nc] != 0:
                neighbors.append((nr, nc))
        return neighbors

    def print_maze(self, grid):
        for row in grid:
            line = ""
            for cell in row:
                if cell == 1:
                    line += "#"  # mur
                elif cell == 0:
                    line += " "  # chemin
                else:
                    line += cell  # S ou E
            print(line)


