import random
from typing import List, Optional, Tuple
import pathlib

Grid = List[List[int]]
Cell = Tuple[int, int]
Cells = List[int]

class GameOfLife:
    def __init__(self, size: Tuple[int, int], randomize: bool = True, max_generations: Optional[int] = None) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for y in range(self.rows):
                for x in range(self.cols):
                    grid[y][x] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                ny, nx = cell[0] + dy, cell[1] + dx
                if 0 <= ny < self.rows and 0 <= nx < self.cols:
                    neighbours.append(self.curr_generation[ny][nx])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()
        for y in range(self.rows):
            for x in range(self.cols):
                cell = (y, x)
                live_neighbours = sum(self.get_neighbours(cell))

                if self.curr_generation[y][x] == 1:
                    new_grid[y][x] = 1 if live_neighbours in [2, 3] else 0
                else:
                    new_grid[y][x] = 1 if live_neighbours == 3 else 0

        return new_grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        with open(filename, 'r') as file:
            grid = [[int(char) for char in line.strip()] for line in file.readlines()]
        size = (len(grid), len(grid[0]))
        game = GameOfLife(size, randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, 'w') as file:
            for row in self.curr_generation:
                file.write(''.join(map(str, row)) + '\n')
