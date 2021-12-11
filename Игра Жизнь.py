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
        self.cell_size = 20

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


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.board = [[0] * width for _ in range(height)]

    def next_move(self):
        tmp_board = copy.deepcopy(self.board)
        for i in range(self.height):
            for j in range(self.width):
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if j + dx < 0 or j + dx >= self.width or i + dy < 0 or i + dy >= self.height:
                            continue
                        s += self.board[i + dy][j + dx]
                s -= self.board[i][j]
                if s == 3:
                    tmp_board[i][j] = 1
                elif s < 2 or s > 3:
                    tmp_board[i][j] = 0
        self.board = copy.deepcopy(tmp_board)

    def on_click(self, cell_cords):
        if cell_cords is not None:
            self.board[cell_cords[1]][cell_cords[0]] = (self.board[cell_cords[1]][cell_cords[0]] + 1) % 2



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
                    pygame.draw.rect(screen, 'green', (start[0] + j, start[1] + i,
                                                       self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, pygame.Color('white'), (start[0] + j, start[1] + i,
                                                                 self.cell_size, self.cell_size), 1)
                self.cell_cords[-1].append((start[0] + j, start[1] + i))
                count2 += 1
            count2 = 0


board = Life(23, 23)
running = True
play = 0
fps = 10
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 2:
                board.get_click(event.pos)
            elif event.button == 5:
                fps -= 2
                fps = 1 if fps < 1 else fps
            elif event.button == 4:
                fps += 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = (play + 1) % 2
                if play:
                    fps = 10
    if play:
        board.next_move()
    else:
        fps = 60
    clock.tick(fps)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
