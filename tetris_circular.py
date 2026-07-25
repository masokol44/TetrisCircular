# tetris_circular.py — круговой тетрис на Python

import os
import time
import random
import sys

try:
    import keyboard
except ImportError:
    print("Установите keyboard: pip install keyboard")
    sys.exit(1)

WIDTH = 10
HEIGHT = 20
BLOCK = '█'
EMPTY = ' '
SHAPES = [
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[0,1,0],[1,1,1]],
    [[0,1,1],[1,1,0]],
    [[1,1,0],[0,1,1]],
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]]
]
COLORS = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[97m']
RESET = '\033[0m'

class Tetris:
    def __init__(self):
        self.field = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.level = 1
        self.speed = 0.5
        self.game_over = False
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.next_piece = None
        self.spawn_piece()

    def spawn_piece(self):
        if self.next_piece is None:
            self.next_piece = random.choice(SHAPES)
        self.current_piece = self.next_piece
        self.next_piece = random.choice(SHAPES)
        self.current_x = WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        if not self.is_valid(self.current_piece, self.current_x, self.current_y):
            self.game_over = True

    def is_valid(self, piece, x, y):
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    field_x = (x + col) % WIDTH  # цилиндрический эффект
                    field_y = y + row
                    if field_y >= HEIGHT or field_y < 0:
                        return False
                    if field_y >= 0 and self.field[field_y][field_x] != EMPTY:
                        return False
        return True

    def lock_piece(self):
        for row in range(len(self.current_piece)):
            for col in range(len(self.current_piece[row])):
                if self.current_piece[row][col]:
                    field_x = (self.current_x + col) % WIDTH
                    field_y = self.current_y + row
                    if field_y >= 0:
                        self.field[field_y][field_x] = BLOCK
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        lines = 0
        y = HEIGHT - 1
        while y >= 0:
            if all(self.field[y][x] != EMPTY for x in range(WIDTH)):
                for yy in range(y, 0, -1):
                    self.field[yy] = self.field[yy-1][:]
                self.field[0] = [EMPTY for _ in range(WIDTH)]
                lines += 1
            else:
                y -= 1
        if lines:
            self.score += lines * 100
            self.level = 1 + self.score // 500
            self.speed = max(0.1, 0.5 - (self.level-1) * 0.05)

    def move(self, dx, dy):
        if self.is_valid(self.current_piece, self.current_x + dx, self.current_y + dy):
            self.current_x += dx
            self.current_y += dy
            return True
        elif dy == 1:  # при падении вниз
            self.lock_piece()
        return False

    def rotate(self):
        piece = [list(row) for row in zip(*self.current_piece[::-1])]
        if self.is_valid(piece, self.current_x, self.current_y):
            self.current_piece = piece

    def hard_drop(self):
        while self.is_valid(self.current_piece, self.current_x, self.current_y + 1):
            self.current_y += 1
        self.lock_piece()

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("🌀 TetrisCircular  |  Счёт: {}  |  Уровень: {}".format(self.score, self.level))
        print("Следующая:")
        for row in self.next_piece:
            print('  ' + ' '.join(BLOCK if cell else EMPTY for cell in row))
        print('+' + '-' * (WIDTH*2+1) + '+')
        for y in range(HEIGHT):
            line = '|'
            for x in range(WIDTH):
                if (self.current_piece is not None and
                    self.current_y <= y < self.current_y + len(self.current_piece) and
                    self.current_x <= x < self.current_x + len(self.current_piece[0])):
                    row = y - self.current_y
                    col = x - self.current_x
                    if self.current_piece[row][col]:
                        line += BLOCK + ' '
                        continue
                line += self.field[y][x] + ' '
            print(line + '|')
        print('+' + '-' * (WIDTH*2+1) + '+')
        print("Управление: ← → движение, ↑ вращение, ↓ ускорение, Пробел - сброс, Q - выход")

    def run(self):
        last_fall = time.time()
        while not self.game_over:
            self.draw()
            # Обработка ввода
            if keyboard.is_pressed('left'): self.move(-1, 0)
            if keyboard.is_pressed('right'): self.move(1, 0)
            if keyboard.is_pressed('down'): self.move(0, 1)
            if keyboard.is_pressed('up'): self.rotate()
            if keyboard.is_pressed('space'): self.hard_drop()
            if keyboard.is_pressed('q'): break
            # Падение
            if time.time() - last_fall > self.speed:
                if not self.move(0, 1):
                    self.lock_piece()
                last_fall = time.time()
            time.sleep(0.02)
        self.draw()
        print("ИГРА ОКОНЧЕНА! Ваш счёт:", self.score)

if __name__ == "__main__":
    game = Tetris()
    game.run()
