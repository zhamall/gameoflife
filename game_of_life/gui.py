from game_of_life.game import GameOfLife
from game_of_life.ui import UI
import pygame
from pygame.locals import *


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        self.screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                color = pygame.Color('green') if self.life.curr_generation[y][x] == 1 else pygame.Color('white')
                pygame.draw.rect(self.screen, color,
                                 (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    paused = not paused
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    x //= self.cell_size
                    y //= self.cell_size
                    self.life.curr_generation[y][x] = 1 - self.life.curr_generation[y][x]

            if not paused:
                self.life.step()

            self.screen.fill(pygame.Color('white'))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False

        pygame.quit()