import pygame
import random

pygame.init()
size = width, height = 400, 400
screen = pygame.display.set_mode(size)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[-1] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.screen = screen
        self.cell_cords = []
        start = (0 + self.left, 0 + self.top)
        for i in range(0, (len(self.board)) * self.cell_size, self.cell_size):
            self.cell_cords.append([])
            for j in range(0, (len(self.board[0])) * self.cell_size, self.cell_size):
                pygame.draw.rect(screen, pygame.Color('white'), (start[0] + j, start[1] + i,
                                                                 self.cell_size, self.cell_size), 1)
                self.cell_cords[-1].append((start[0] + j, start[1] + i))

    def get_cell(self, mouse_pos):
        for i in range(len(self.cell_cords)):
            string = self.cell_cords[i]
            for j in range(len(string)):
                col = string[j]
                if col[0] < mouse_pos[0] < col[0] + self.cell_size and col[1] < mouse_pos[1] < col[1] + self.cell_size:
                    return j, i
        return None

    def on_click(self, cell_cords):
        # pygame.draw.rect(screen, pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        #                  (cell_cords[0], cell_cords[1], self.cell_size, self.cell_size), 0)
        print(cell_cords)
        # x +dx < 0 and x

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Minesweeper(Board):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        n = n
        i = 0
        while i < n:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            self.board[x][y] = 10
            i += 1

    def render(self, screen):

        pass


board = Board(5, 7)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
