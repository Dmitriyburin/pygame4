import pygame
import copy

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 40

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
        print(cell_cords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.selected_cell = None

    def has_path(self, x1, y1, x2, y2):
        d = {(x1, y1): 0}
        v = [(x1, y1)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if self.board[y + dy][x + dx] == 0:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append(
                                (x + dx, y + dy))
        dist = d.get((x2, y2), -1)
        return dist >= 0

    def on_click(self, cell):
        if cell is not None:
            x = cell[0]
            y = cell[1]
            if self.selected_cell is None:
                if self.board[y][x] == 1:
                    self.selected_cell = x, y
                else:
                    self.board[y][x] = 1
            else:
                if self.selected_cell == (x, y):
                    self.selected_cell = None
                    return
                x2 = self.selected_cell[0]
                y2 = self.selected_cell[1]
                if self.has_path(x2, y2, x, y):
                    self.board[y][x] = 1
                    self.board[y2][x2] = 0
                    self.selected_cell = None

    def render(self, screen):

        self.screen = screen
        self.cell_cords = []
        start = (0 + self.left, 0 + self.top)
        count1, count2 = -1, 0
        for i in range(0, (len(self.board)) * self.cell_size, self.cell_size):
            self.cell_cords.append([])
            count1 += 1
            for j in range(0, (len(self.board[0])) * self.cell_size, self.cell_size):
                if self.board[count1][count2] == 1:
                    color = pygame.Color('blue')
                    if self.selected_cell == (count2, count1):
                        color = pygame.Color('red')
                    pygame.draw.ellipse(screen, color, (start[0] + j + 3,
                                                        start[1] + i + 3,
                                                        self.cell_size - 6,
                                                        self.cell_size - 6), 0)
                pygame.draw.rect(screen, pygame.Color('white'), (start[0] + j, start[1] + i,
                                                                 self.cell_size, self.cell_size), 1)
                self.cell_cords[-1].append((start[0] + j, start[1] + i))
                count2 += 1
            count2 = 0


board = Lines(10, 10)
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
