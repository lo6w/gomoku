import pygame
import time
import math
from language import languages
from pygame.locals import *
from AI_library import nb_AI_1


class game:
    pygame.display.init()
    pygame.font.init()
    run = True
    screen = pygame.display.set_mode((1280, 720), RESIZABLE | HWACCEL)
    clock = pygame.time.Clock()
    board = []
    for i in range(16):
        board.append([0] * 16)
    mouse_up = [False, False, False]
    mouse_down = [False, False, False]
    fonts = {}
    debug = False
    winner = 0
    win_line = []
    interface = 0
    times = 0
    anti_aliasing = True
    saved = False
    lan = 0
    save_screen = False

    def __init__(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
            self.screen.fill((255, 255, 255))
            if self.interface == 0:
                self.menu()
            elif self.interface == 1:
                self.single_playing()
            elif self.interface == 2:
                self.single_playing_best()
            elif self.interface == 4:
                self.other_menu()
            else:
                self.single_playing_better()
            pygame.display.flip()
            self.clock.tick(60)
            for k in range(3):
                if self.mouse_down[k] and not pygame.mouse.get_pressed()[k]:
                    self.mouse_up[k] = True
                else:
                    self.mouse_up[k] = False
            self.mouse_down = pygame.mouse.get_pressed()
        pygame.quit()

    def write(self, text, pos, color=(0, 0, 0), size=16):
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text), self.anti_aliasing, color)
        self.screen.blit(font, pos)

    def button(self, rect, text=''):
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        size = rect[3] - 6
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text), self.anti_aliasing, (0, 0, 0))
        pos = (rect[0] + rect[2] / 2 - font.get_width() / 2, rect[1] + rect[3] / 2 - font.get_height() / 2)
        self.screen.blit(font, pos)
        if Rect(rect[0], rect[1], rect[2], rect[3]).collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, (127, 127, 127), rect, 3)
            if self.mouse_up[0]:
                return True
            else:
                return False
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
            return False

    def read(self, x, y):
        if x >= 16 or x < 0 or y >= 16 or y < 0:
            return None
        else:
            return self.board[y][x]

    def menu(self):
        global AI
        self.screen.fill((0, 127, 255))
        self.write(languages[self.lan][0], (self.screen.get_width() / 2 - 96, self.screen.get_height() / 8), size=64)
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        font = self.fonts[32].render('NB-AI 1.0!', self.anti_aliasing, (255, 255, 0))
        font = pygame.transform.rotate(font, 20)
        font = pygame.transform.smoothscale(font, (int((math.sin(time.time() * 8) * 0.2 + 1) * font.get_width()),
                                                   int((math.sin(time.time() * 8) * 0.2 + 1) * font.get_height())))
        self.screen.blit(font, (self.screen.get_width() / 2 + 96 - font.get_width() / 2,
                                self.screen.get_height() / 8 + 64 - font.get_height() / 2))
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 100, 400, 38),
                       languages[self.lan][1]):
            self.saved = False
            self.board = []
            self.times = 0
            for i in range(16):
                self.board.append([0] * 16)
            self.winner = 0
            self.win_line = []
            AI = nb_AI_1()
            self.interface = 1
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 50, 400, 38),
                       languages[self.lan][2]):
            self.interface = 4
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2, 400, 38), '语言 language'):
            if self.lan == 0:
                self.lan = 1
            else:
                self.lan = 0

    def other_menu(self):
        global AI
        self.screen.fill((0, 127, 255))
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 100, 400, 38),
                       languages[self.lan][9]):
            self.interface = 0
        if self.button((self.screen.get_width() / 2 - 450, self.screen.get_height() / 2, 400, 38),
                       languages[self.lan][4]):
            self.saved = False
            self.board = []
            self.times = 0
            for i in range(16):
                self.board.append([0] * 16)
            self.winner = 0
            self.win_line = []
            AI = nb_AI_1()
            self.interface = 2
        if self.button((self.screen.get_width() / 2 + 50, self.screen.get_height() / 2, 400, 38),
                       languages[self.lan][3]):
            self.saved = False
            self.board = []
            self.times = 0
            for i in range(16):
                self.board.append([0] * 16)
            self.winner = 0
            self.win_line = []
            AI = nb_AI_1()
            self.interface = 3

    def judgment(self):
        if self.times <= 256:
            for x in range(16):
                for y in range(16):
                    for x_add in range(3):
                        x_add = x_add - 1
                        for y_add in range(3):
                            y_add = y_add - 1
                            if not (x_add == 0 and y_add == 0) and self.winner == 0:
                                line = [0, 0, 0, 0, 0]
                                for long in range(5):
                                    c = self.read(x + long * x_add, y + long * y_add)
                                    if c is not None:
                                        if c != 0:
                                            line[long] = c
                                        else:
                                            break
                                    else:
                                        break
                                if line == [1, 1, 1, 1, 1]:
                                    self.winner = 1
                                elif line == [2, 2, 2, 2, 2]:
                                    self.winner = 2
                                if self.winner != 0:
                                    self.win_line = [(x, y), (x + 4 * x_add, y + 4 * y_add)]
        else:
            self.winner = 3

    def single_playing(self):
        global AI
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32,
                            32, 32)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (0, 255, 0), rect, 3)
                    if self.mouse_up[0] and self.winner == 0 and self.board[y][x] == 0:
                        self.board[y][x] = 1
                        self.times = self.times + 1
                        self.judgment()
                        if self.winner == 0:
                            AI.get(self.board)
                            self.times = self.times + 1
                            self.judgment()
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32, 32,
                            32)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                if (AI.player_point[y][x] != 0 or AI.self_point[y][x] != 0) and self.board[y][x] == 0 and self.debug:
                    self.write(str(AI.player_point[y][x]) + ',' + str(AI.self_point[y][x]), (rect[0], rect[1]))
                if self.board[y][x] == 1:
                    pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 4, rect[1] + 4), (rect[0] + 28, rect[1] + 28),
                                     5)
                    pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 28, rect[1] + 4), (rect[0] + 4, rect[1] + 28),
                                     5)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(self.screen, (0, 0, 255), (rect[0] + 16, rect[1] + 16), 14, 3)

        if self.winner != 0:
            if self.winner != 3:
                pygame.draw.line(self.screen, (0, 255, 0),
                                 (self.screen.get_width() / 2 + (self.win_line[0][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[0][1] - 8) * 32 + 16),
                                 (self.screen.get_width() / 2 + (self.win_line[1][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[1][1] - 8) * 32 + 16), 5)
            else:
                self.write(languages[self.lan][5], (self.screen.get_width() / 2 - 64, 0), (0, 0, 0), 64)
            if self.winner == 1:
                self.write(languages[self.lan][7], (self.screen.get_width() / 2 - 128, 0), (0, 0, 0), 64)
            if self.winner == 2:
                self.write(languages[self.lan][6], (self.screen.get_width() / 2 - 128, 0), (0, 0, 0), 64)
        if self.button((0, 0, 140, 38), languages[self.lan][8]) or pygame.key.get_pressed()[K_r]:
            self.board = []
            self.times = 0
            for i in range(16):
                self.board.append([0] * 16)
            self.winner = 0
            self.win_line = []
            AI = nb_AI_1()
            self.saved = False
        if self.button((0, 40, 140, 38), languages[self.lan][9]):
            self.interface = 0
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        font = self.fonts[32].render(languages[self.lan][10] + ':' + str(self.times), self.anti_aliasing, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 0))
        if (not self.saved) and self.winner != 0:
            if self.save_screen:
                t = time.localtime()
                s = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '\'' + str(
                    t.tm_min) + '\'' + str(t.tm_sec)
                if self.winner == 1:
                    w = '赢'
                else:
                    w = '输'
                pygame.image.save(self.screen, r'photos/normal/' + str(s) + str(w) + '.png')
            self.saved = True

    def single_playing_better(self):
        global AI
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32,
                            32, 32)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (0, 255, 0), rect, 3)
                    if self.mouse_up[0] and self.winner == 0 and self.board[y][x] == 0:
                        self.board[y][x] = 1
                        self.times = self.times + 1
                        self.judgment()
                        if self.winner == 0:
                            AI.get(self.board)
                            self.times = self.times + 1
                            self.judgment()
                            if self.winner == 0:
                                AI.get(self.board)
                                self.times = self.times + 1
                                self.judgment()
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32, 32,
                            32)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                if (AI.player_point[y][x] != 0 or AI.self_point[y][x] != 0) and self.board[y][x] == 0 and self.debug:
                    self.write(str(AI.player_point[y][x]) + ',' + str(AI.self_point[y][x]), (rect[0], rect[1]))
                if self.board[y][x] == 1:
                    pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 4, rect[1] + 4), (rect[0] + 28, rect[1] + 28),
                                     5)
                    pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 28, rect[1] + 4), (rect[0] + 4, rect[1] + 28),
                                     5)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(self.screen, (0, 0, 255), (rect[0] + 16, rect[1] + 16), 14, 3)

        if self.winner != 0:
            if self.winner != 3:
                pygame.draw.line(self.screen, (0, 255, 0),
                                 (self.screen.get_width() / 2 + (self.win_line[0][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[0][1] - 8) * 32 + 16),
                                 (self.screen.get_width() / 2 + (self.win_line[1][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[1][1] - 8) * 32 + 16), 5)
            else:
                self.write(languages[self.lan][5], (self.screen.get_width() / 2 - 64, 0), (0, 0, 0), 64)
            if self.winner == 1:
                self.write(languages[self.lan][7], (self.screen.get_width() / 2 - 128, 0), (0, 0, 0), 64)
            if self.winner == 2:
                self.write(languages[self.lan][6], (self.screen.get_width() / 2 - 128, 0), (0, 0, 0), 64)
        if self.button((0, 0, 140, 38), languages[self.lan][8]) or pygame.key.get_pressed()[K_r]:
            self.board = []
            self.times = 0
            self.saved = False
            for i in range(16):
                self.board.append([0] * 16)
            self.winner = 0
            self.win_line = []
            AI = nb_AI_1()
        if self.button((0, 40, 140, 38), languages[self.lan][9]):
            self.interface = 0
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        font = self.fonts[32].render(languages[self.lan][10] + ':' + str(self.times), self.anti_aliasing, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 0))
        if (not self.saved) and self.winner != 0:
            if self.save_screen:
                t = time.localtime()
                s = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '\'' + str(
                    t.tm_min) + '\'' + str(t.tm_sec)
                if self.winner == 1:
                    w = '赢'
                else:
                    w = '输'
                pygame.image.save(self.screen, r'photos/better/' + str(s) + str(w) + '.png')
            self.saved = True

    def single_playing_best(self):
        global AI
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32,
                            32, 32)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (0, 255, 0), rect, 3)
                    if self.mouse_up[0] and self.winner == 0 and self.board[y][x] == 0:
                        self.board[y][x] = 1
                        self.times = self.times + 1
                        self.judgment()
                        for ix in range(16):
                            for iy in range(16):
                                if self.board[iy][ix] == 0:
                                    self.board[iy][ix] = 2
                        self.judgment()
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32,
                            32, 32)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                if (AI.player_point[y][x] != 0 or AI.self_point[y][x] != 0) and self.board[y][x] == 0 and self.debug:
                    self.write(str(AI.player_point[y][x]) + ',' + str(AI.self_point[y][x]), (rect[0], rect[1]))
                if self.board[y][x] == 1:
                    pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 4, rect[1] + 4),
                                     (rect[0] + 28, rect[1] + 28), 5)
                    pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 28, rect[1] + 4),
                                     (rect[0] + 4, rect[1] + 28), 5)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(self.screen, (0, 0, 255), (rect[0] + 16, rect[1] + 16), 14, 3)

        if self.winner != 0:
            if self.winner != 3:
                pygame.draw.line(self.screen, (0, 255, 0),
                                 (self.screen.get_width() / 2 + (self.win_line[0][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[0][1] - 8) * 32 + 16),
                                 (self.screen.get_width() / 2 + (self.win_line[1][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[1][1] - 8) * 32 + 16), 5)
            else:
                self.write(languages[self.lan][5], (self.screen.get_width() / 2 - 64, 0), (0, 0, 0), 64)
            if self.winner == 1:
                self.write(languages[self.lan][7], (self.screen.get_width() / 2 - 128, 0), (0, 0, 0), 64)
            if self.winner == 2:
                self.write(languages[self.lan][6], (self.screen.get_width() / 2 - 128, 0), (0, 0, 0), 64)
        if self.button((0, 0, 140, 38), languages[self.lan][8]) or pygame.key.get_pressed()[K_r]:
            self.board = []
            self.times = 0
            for i in range(16):
                self.board.append([0] * 16)
            self.winner = 0
            self.win_line = []
            AI = nb_AI_1()
            self.saved = False
        if self.button((0, 40, 140, 38), languages[self.lan][9]):
            self.interface = 0
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        font = self.fonts[32].render(languages[self.lan][10] + ':' + str(self.times), self.anti_aliasing, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 0))
        if (not self.saved) and self.winner != 0:
            if self.save_screen:
                t = time.localtime()
                s = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '\'' + str(
                    t.tm_min) + '\'' + str(t.tm_sec)
                if self.winner == 1:
                    w = '赢'
                else:
                    w = '输'
                pygame.image.save(self.screen, r'photos/best/' + str(s) + str(w) + '.png')
            self.saved = True


if __name__ == '__main__':
    AI = nb_AI_1()
    g = game()
