from random import randrange

class MazeGenerator:
    """
    A class to generate a random maze using a randomized version of Prim's algorithm.

    The maze is represented as a 2D grid where:
      - 1 represents a wall
      - 0 represents an open path
      - "S" is the start point
      - "E" is the end point
    """

    def __init__(self, height, width):
        """
        Initialize the maze generator with given height and width.

        Args:
            height (int): Number of rows in the maze
            width (int): Number of columns in the maze
        """
        self.height = height
        self.width = width

    def generator_maze(self):
        """
        Generate the maze using a randomized frontier-based algorithm.

        Returns:
            (list[list[int | str]]): 2D list representing the generated maze
        """
        # Create a grid filled with walls (1)
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Choose a random starting cell (odd coordinates)
        current_row = randrange(1, self.height, 2)
        current_col = randrange(1, self.width, 2)
        grid[current_row][current_col] = 0
        frontier = [(current_row, current_col)]

        # Maze generation loop
        while frontier:
            list_neighbors = self.find_neighbors(current_row, current_col, grid)

            if list_neighbors:
                selected_neighbor = list_neighbors[randrange(len(list_neighbors))]

                # Open the wall between current cell and selected neighbor
                row_to_open = (selected_neighbor[0] + current_row) // 2
                col_to_open = (selected_neighbor[1] + current_col) // 2

                grid[row_to_open][col_to_open] = 0
                grid[selected_neighbor[0]][selected_neighbor[1]] = 0

                frontier.append(selected_neighbor)
                current_row, current_col = frontier[randrange(len(frontier))]
            else:
                frontier.remove((current_row, current_col))
                if frontier:
                    current_row, current_col = frontier[randrange(len(frontier))]

        # Define start (S) and end (E) points
        grid[1][1] = "S"
        grid[self.height - 2][self.width - 2] = "E"

        return grid

    def find_neighbors(self, current_row, current_col, grid):
        """
        Find valid neighbors two cells away from the current position.

        Args:
            current_row (int): Current row position
            current_col (int): Current column position
            grid (list[list[int | str]]): The maze grid

        Returns:
            (list[tuple[int, int]]): List of valid neighbor coordinates
        """
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        neighbors = []

        for dr, dc in directions:
            nr, nc = current_row + dr, current_col + dc
            if 0 <= nr < self.height and 0 <= nc < self.width and grid[nr][nc] != 0:
                neighbors.append((nr, nc))

        return neighbors
