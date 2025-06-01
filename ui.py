import random
from typing import Union, Tuple, Literal

from pygame.locals import *
import time
import pygame

from AI_library import nb_AI_1, nb_AI_2
from niuben import Sound, Nbs, Particle
from setting import *


class input_rect:
    """输入框"""
    inputting = False
    text = ''
    font_color = (0, 0, 0)
    background_color = (0, 0, 0)
    rect = [0, 0, 0, 0]
    number = False
    last_backspace = 0
    font_size = 20

    def __init__(self, rect: Tuple[Union[int, float], Union[int, float], Union[int, float], Union[int, float]], x_center=0.5, y_center=0.5,
                 font_size=32, font_color=(0, 0, 0), input_number=False, background_color=(255, 255, 255)) -> None:
        self.screen = pygame.display.get_surface()
        self.x_center = x_center
        self.y_center = y_center
        self.font_color = font_color
        self.font = pygame.font.Font('unifont-15.0.01.ttf', font_size)
        self.background_color = background_color
        self.rect_ = rect
        self.rect_update()
        self.number = input_number
        self.font_size = font_size
        self.last_backspace = 0

    def rect_update(self):
        self.rect = [int(self.screen.get_width() * self.x_center + self.rect_[0]),
                     int(self.screen.get_height() * self.y_center + self.rect_[1]),
                     self.rect_[2], self.rect_[3]]

    def input_draw(self, key_up: list, key_press, mouse_up, mouse_xy, inputting_text: list) -> None:
        self.rect_update()
        pygame.draw.rect(self.screen, self.background_color, self.rect)
        font = self.font.render(str(self.text), False, self.font_color)
        if font.get_width() < self.rect[2]:
            self.screen.blit(font, (self.rect[0], self.rect[1] + self.rect[3] / 2 - font.get_height() / 2))
            if time.time() % 1 >= 0.5 and self.inputting:
                pygame.draw.line(self.screen, self.font_color,
                                 (self.rect[0] + font.get_width() + 6, self.rect[1] + self.rect[3] / 2 - font.get_height() / 2),
                                 (self.rect[0] + font.get_width() + 6, self.rect[1] + self.rect[3] / 2 + font.get_height() / 2), 3)
        else:
            self.screen.blit(font, (self.rect[0], self.rect[1] + self.rect[3] / 2 - font.get_height() / 2),
                             (font.get_width() - self.rect[2], 0, self.rect[2], self.rect[3]))
            if time.time() % 1 >= 0.5 and self.inputting:
                pygame.draw.line(self.screen, self.font_color,
                                 (self.rect[0] + self.rect[2] - 4, self.rect[1] + self.rect[3] / 2 - font.get_height() / 2),
                                 (self.rect[0] + self.rect[2] - 4, self.rect[1] + self.rect[3] / 2 + font.get_height() / 2), 3)
        if Rect(self.rect).collidepoint(mouse_xy):
            pygame.draw.rect(self.screen, (127, 127, 127), self.rect, 3)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 3)
        if mouse_up[0]:
            if Rect(self.rect).collidepoint(mouse_xy):
                self.inputting = True
            else:
                self.inputting = False

        if self.inputting:
            if K_BACKSPACE in key_up:
                if time.time() - self.last_backspace < 1:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
            if key_press[K_BACKSPACE]:
                if self.last_backspace == 0:
                    self.last_backspace = time.time()
            else:
                self.last_backspace = 0
            if time.time() - self.last_backspace > 1 and self.last_backspace != 0:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
                    self.last_backspace = time.time() - 0.95
            if len(inputting_text) != 0:
                for text in inputting_text:
                    if self.number:
                        if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                            self.text = self.text + str(text)
                    else:
                        self.text = self.text + str(text)

    def get_text(self) -> Union[int, str]:
        if len(self.text) > 0:
            if self.number:
                return int(self.text)
            else:
                return str(self.text)
        else:
            return ''


class Basic:
    board = []
    for i in range(16):
        board.append([0] * 16)
    win_line = [(0, 0), (0, 0)]
    winner = 0
    mouse_up = [False, False, False]
    game_over = False
    fonts = {}
    lan = 0
    exit = False
    player1_previous_step = [0, 0]
    player1_steps = 0
    player2_previous_step = [0, 0]
    player2_steps = 0
    AI1 = nb_AI_1()
    AI2 = nb_AI_1()
    NB1 = Nbs()
    NB2 = Nbs()

    def __init__(self, settings: setting, languages, images, difficulty=0):
        self.images = images
        self.languages = languages
        self.screen = pygame.display.get_surface()
        self.settings = settings
        self.exit = False
        if difficulty == 0:
            self.AI1 = nb_AI_1()
            self.AI2 = nb_AI_1()
        else:
            self.AI1 = nb_AI_2()
            self.AI2 = nb_AI_2()

    def read(self, x, y) -> Union[int, None]:
        """读取棋盘"""
        if x >= 16 or x < 0 or y >= 16 or y < 0:
            return None
        else:
            return self.board[y][x]

    def text(self, name: str) -> str:
        if self.lan in self.languages:
            if name in self.languages[self.lan]:
                return self.languages[self.lan][name]
            else:
                return ''
        else:
            return ''

    def judgment(self) -> None:
        if (self.player2_steps + self.player1_steps) <= 256:
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

    def write(self, text, pos, color=(0, 0, 0), size=16, center=False) -> None:
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text), False, color)
        font: pygame.Surface
        if center:
            self.screen.blit(font, (pos[0] - font.get_width() // 2, pos[1] - font.get_height() // 2))
        else:
            self.screen.blit(font, pos)

    def button(self, rect, text='') -> bool:
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        size = rect[3] - 6
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text), False, (0, 0, 0))
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

    def init(self, step1=0, step2=0, difficulty=0) -> None:
        """重置棋盘"""
        self.board = []
        self.player1_steps = step1
        self.player2_steps = step2
        self.NB1.clear()
        self.NB2.clear()
        for i in range(16):
            self.board.append([0] * 16)
        self.winner = 0
        self.win_line = []
        self.game_over = False
        self.exit = False
        self.NB1.init()
        self.NB2.init()
        if difficulty == 0:
            self.AI1 = nb_AI_1()
            self.AI2 = nb_AI_1()
        else:
            self.AI1 = nb_AI_2()
            self.AI2 = nb_AI_2()

    def get_steps(self, player: Literal[0, 1, 2] = 0) -> int:
        if player == 0:
            return int(self.player1_steps + self.player2_steps)
        elif player == 1:
            return int(self.player1_steps)
        else:
            return int(self.player2_steps)

    def step(self, player: Literal[1, 2]) -> None:
        """棋子计数增加"""
        if player == 1:
            self.player1_steps = self.player1_steps + 1
        else:
            self.player2_steps = self.player2_steps + 1

    def down(self, x: int, y: int):
        """下棋子"""
        pass

    def player1_won(self, sounds: Sound):
        """玩家1赢行为"""
        pass

    def player2_won(self, sounds: Sound):
        """玩家2赢行为"""
        pass

    def none_won(self, sounds: Sound):
        """无人胜利行为"""
        pass

    def do(self, sounds: Sound):
        """每一步的行为"""
        pass

    def draw_nb(self):
        """绘制牛犇"""
        if self.winner == 2:
            self.screen.blit(self.images.happy, (0, self.screen.get_height() - 128))
        elif self.winner == 1 or time.time() - self.NB2.angry_time < 0:
            self.screen.blit(self.images.angry, (0, self.screen.get_height() - 128))
        else:
            self.screen.blit(self.images.normal, (0, self.screen.get_height() - 128))

    def draw_totem(self):
        """绘制图腾"""
        pass

    def say1(self, sounds: Sound):
        """嘲讽"""
        if self.settings.nb:
            if random.randint(0, 1) == 1:
                sounds.play('xun1')
            else:
                sounds.play('xun2')

    def say2(self, sounds: Sound):
        """生气"""
        if self.settings.nb:
            if random.randint(0, 1) == 1:
                sounds.play('ngm1')
            else:
                sounds.play('ngm2')

    def say3(self, sounds: Sound):
        """骄傲"""
        if self.settings.nb:
            if random.randint(0, 1) == 1:
                sounds.play('lblh1')
            else:
                sounds.play('lblh2')

    def show_steps(self):
        """展示步数"""
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        font = self.fonts[32].render(self.text('player_steps') + ':' + str(self.get_steps(1)), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 0))
        font = self.fonts[32].render(self.text('AI_steps') + ':' + str(self.get_steps(2)), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 32))

    def lose(self):
        if self.winner == 1:
            self.write(self.text('player_won'), (self.screen.get_width() / 2, 64), size=64, center=True)
        if self.winner == 2:
            self.write(self.text('ai_won'), (self.screen.get_width() / 2, 64), size=64, center=True)

    def restart_button(self):
        if self.button((0, 0, 140, 38), self.text('restart')) or pygame.key.get_pressed()[K_r]:
            self.init()
            self.NB1.init()
            self.NB2.init()

    def draw(self, mouse_up, sounds: Sound, language: int):
        self.lan = language
        self.mouse_up = mouse_up.copy()
        if self.settings.style == 1:
            self.screen.fill((185, 122, 87))
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32,
                            32, 32)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (0, 255, 0), rect, 3)
                    if self.mouse_up[0] and self.winner == 0 and self.board[y][x] == 0:
                        self.player1_previous_step = [x, y]
                        self.say3(sounds)
                        self.down(x, y)
        self.do(sounds)

        b = 0
        for x in range(16):
            for y in range(16):
                if self.board[y][x] == 0:
                    b = b + 1
        if b == 0 and self.winner == 0:
            self.winner = 3
        if self.winner == 2 and (not self.game_over):
            self.game_over = True
            self.player2_won(sounds)
            self.say1(sounds)
        elif self.winner == 1 and (not self.game_over):
            self.game_over = True
            self.player1_won(sounds)
            self.say2(sounds)
        if self.winner == 3 and (not self.game_over):
            self.game_over = True
            self.none_won(sounds)
            self.say1(sounds)
        if self.settings.style == 1:
            for x in range(16):
                pygame.draw.line(self.screen, (0, 0, 0), (self.screen.get_width() // 2 - 32 * 8 + 16 + x * 32, self.screen.get_height() // 2 - 32 * 8 + 16),
                                 (self.screen.get_width() // 2 - 32 * 8 + 16 + x * 32, self.screen.get_height() // 2 + 32 * 8 - 16))
            for y in range(16):
                pygame.draw.line(self.screen, (0, 0, 0), (self.screen.get_width() // 2 - 32 * 8 + 16, self.screen.get_height() // 2 - 32 * 8 + 16 + y * 32),
                                 (self.screen.get_width() // 2 + 32 * 8 - 16, self.screen.get_height() // 2 - 32 * 8 + 16 + y * 32))
        for x in range(16):
            for y in range(16):
                rect = Rect(self.screen.get_width() / 2 + (x - 8) * 32, self.screen.get_height() / 2 + (y - 8) * 32, 32,
                            32)
                if self.settings.style == 0:
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                    if self.board[y][x] == 1:
                        pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 4, rect[1] + 4), (rect[0] + 28, rect[1] + 28), 5)
                        pygame.draw.line(self.screen, (255, 0, 0), (rect[0] + 28, rect[1] + 4), (rect[0] + 4, rect[1] + 28), 5)
                    elif self.board[y][x] == 2:
                        pygame.draw.circle(self.screen, (0, 0, 255), (rect[0] + 16, rect[1] + 16), 14, 3)
                else:
                    if self.board[y][x] == 1:
                        pygame.draw.circle(self.screen, (0, 0, 0), (rect[0] + 16, rect[1] + 16), 14)
                    elif self.board[y][x] == 2:
                        pygame.draw.circle(self.screen, (255, 255, 255), (rect[0] + 16, rect[1] + 16), 14)

        if self.winner != 0:
            if self.winner != 3:
                pygame.draw.line(self.screen, (0, 255, 0),
                                 (self.screen.get_width() / 2 + (self.win_line[0][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[0][1] - 8) * 32 + 16),
                                 (self.screen.get_width() / 2 + (self.win_line[1][0] - 8) * 32 + 16,
                                  self.screen.get_height() / 2 + (self.win_line[1][1] - 8) * 32 + 16), 5)
            else:
                self.write(self.text('none won'), (self.screen.get_width() / 2 - 64, 0), (0, 0, 0), 64)
            self.lose()
        self.restart_button()
        if self.button((0, 40, 140, 38), self.text('exit')):
            self.exit = True
        self.show_steps()
        if self.settings.nb:
            self.draw_nb()
        self.draw_totem()


class Single_play(Basic):
    def __init__(self, settings: setting, languages, images, difficulty=0):
        super().__init__(settings, languages, images, difficulty)

    def down(self, x: int, y: int):
        self.board[y][x] = 1
        self.step(1)
        self.judgment()
        self.NB2.angry_time = time.time() + 1
        if self.winner == 0:
            self.AI2.get(self.board)
            self.step(2)
            self.judgment()


class Better_play(Basic):
    def __init__(self, settings: setting, languages, images, difficulty=0):
        super().__init__(settings, languages, images, difficulty)

    def down(self, x: int, y: int):
        self.board[y][x] = 1
        self.step(1)
        self.judgment()
        self.NB2.angry_time = time.time() + 1
        if self.winner == 0:
            self.AI2.get(self.board)
            self.step(2)
            self.judgment()
            if self.winner == 0:
                self.AI2.get(self.board)
                self.step(2)
                self.judgment()


class Best_play(Basic):
    def __init__(self, settings: setting, languages, images, difficulty=0):
        super().__init__(settings, languages, images, difficulty)

    def down(self, x: int, y: int):
        self.board[y][x] = 1
        self.step(1)
        self.judgment()
        for ix in range(16):
            for iy in range(16):
                if self.board[iy][ix] == 0:
                    self.board[iy][ix] = 2
                    self.step(2)
        self.judgment()


class Tortoise_play(Basic):
    totem_types = 0
    particles = []
    totem_time = 0

    def __init__(self, settings: setting, languages, images, difficulty=0):
        super().__init__(settings, languages, images, difficulty)
        self.AI2 = nb_AI_1(fight=0)
        self.NB2.init()

    def judgment(self) -> None:
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

    def init(self, step1=0, step2=0, difficulty=0) -> None:
        self.board = []
        self.player1_steps = step1
        self.player2_steps = step2
        if step1 == 0 and step2 == 0:
            self.NB1.init()
            self.NB2.init()
            self.totem_time = 0
            self.particles = []
        for i in range(16):
            self.board.append([0] * 16)
        self.winner = 0
        self.win_line = []
        self.game_over = False
        self.exit = False
        if difficulty == 0:
            self.AI1 = nb_AI_1()
            self.AI2 = nb_AI_1()
        else:
            self.AI1 = nb_AI_2()
            self.AI2 = nb_AI_2()

    def down(self, x: int, y: int):
        self.board[y][x] = 1
        self.step(1)
        self.judgment()
        self.NB2.angry_time = time.time() + 1
        if self.winner == 0:
            self.AI2.get(self.board)
            self.step(2)
            self.judgment()

    def draw_nb(self):
        if self.winner == 2:
            self.screen.blit(self.images.happy, (0, self.screen.get_height() - 128))
        elif self.winner == 1 or time.time() - self.NB2.angry_time < 0:
            self.screen.blit(self.images.angry, (0, self.screen.get_height() - 128))
        else:
            self.screen.blit(self.images.normal, (0, self.screen.get_height() - 128))
        self.screen.blit(self.images.undying_totem_, (128, self.screen.get_height() - 32))
        self.write('×' + str(self.NB2.undying_totem), (160, self.screen.get_height() - 32), size=32)
        self.screen.blit(self.images.restart_totem_, (128, self.screen.get_height() - 64))
        self.write('×' + str(self.NB2.restart_totem), (160, self.screen.get_height() - 64), size=32)

    def player1_won(self, sounds):
        if self.NB2.restart_totem > 0 or self.NB2.undying_totem > 0:
            if self.NB2.restart_totem == 0:
                u = 2
            elif self.NB2.undying_totem == 0:
                u = 1
            else:
                u = random.randint(1, 2)
            if u == 1:
                self.NB2.restart_totem = self.NB2.restart_totem - 1
                self.init(self.player1_steps, self.player2_steps)
                self.totem_types = 1
            else:
                self.NB2.undying_totem = self.NB2.undying_totem - 1
                self.board[self.player1_previous_step[1]][self.player1_previous_step[0]] = 2
                self.AI2.get(self.board, True)
                self.player2_previous_step = (self.AI2.x, self.AI2.y)
                self.step(2)
                self.judgment()
                self.totem_types = 0
            self.NB2.angry_time = time.time() + 2
            self.totem_time = 180
            self.winner = 0
            self.game_over = False
            sounds.play('undying')
            for i in range(random.randint(15, 45)):
                self.particles.append(Particle(random.randint(-10, 10), random.randint(-5, 5), (random.randint(0, 255), 255, 0)))

    def draw_totem(self):
        for p in self.particles:
            pygame.draw.circle(self.screen, p.color, (self.screen.get_width() // 2 + p.x, self.screen.get_height() // 2 + p.y), 8)
        ds = 0
        for i in range(len(self.particles)):
            if self.particles[i - ds].y > self.screen.get_height() // 2:
                self.particles.pop(i - ds)
                ds = ds + 1

        if self.totem_time > 0:
            for p in self.particles:
                p: Particle
                p.update(1)
            if self.totem_types == 0:
                if len(self.images.totems_undying) == 180:
                    t = self.images.totems_undying[self.totem_time - 1]
                else:
                    t = pygame.Surface((100, 100))
            else:
                if len(self.images.totems_restart) == 180:
                    t = self.images.totems_restart[self.totem_time - 1]
                else:
                    t = pygame.Surface((100, 100))
            t = pygame.transform.scale2x(t)
            xt = self.totem_time
            self.screen.blit(t,
                             (self.screen.get_width() // 2 - t.get_width() // 2 + 0.3 * xt * (xt - 400) / 90 + 0.3 * 200 * 200 / 90,
                              self.screen.get_height() // 2 - t.get_height() // 2))
            if self.totem_time < 0:
                self.totem_time = 0
                self.particles = []
        else:
            self.particles = []
        if self.totem_time > 0:
            self.totem_time = self.totem_time - 1
        elif self.totem_time < 0:
            self.totem_time = 0

    def none_won(self, sounds: Sound):
        self.init(self.player1_steps, self.player2_steps)
        self.totem_types = 1
        self.totem_time = 180
        self.game_over = False


class Tortoise_watch(Basic):
    totem_types = 0
    particles = []
    totem_time = 0
    ts = 0

    def __init__(self, settings: setting, languages, images, difficulty=0):
        super().__init__(settings, languages, images, difficulty)
        self.difficulty = difficulty
        if difficulty == 0:
            self.AI1 = nb_AI_1(fight=0)
            self.AI2 = nb_AI_1(fight=0)
            self.NB2.init()
            self.NB1.init()
        else:
            self.AI1 = nb_AI_2()
            self.AI2 = nb_AI_2()

    def judgment(self) -> None:
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

    def lose(self):
        if self.winner == 1:
            self.write(self.text('ai1_won'), (self.screen.get_width() / 2, 64), size=64, center=True)
        if self.winner == 2:
            self.write(self.text('ai2_won'), (self.screen.get_width() / 2, 64), size=64, center=True)

    def init(self, step1=0, step2=0, difficulty=0) -> None:
        self.ts = time.time()
        self.board = []
        for i in range(16):
            self.board.append([0] * 16)
        self.player1_steps = step1
        self.player2_steps = step2
        self.difficulty = difficulty
        if step1 == 0 and step2 == 0:
            if self.difficulty == 0:
                self.NB1.init()
                self.NB2.init()
            self.totem_time = 0
            self.particles = []
        self.winner = 0
        self.win_line = []
        self.game_over = False
        self.exit = False
        if self.difficulty == 0:
            self.AI1 = nb_AI_1()
            self.AI2 = nb_AI_1()
        else:
            self.AI1 = nb_AI_2()
            self.AI2 = nb_AI_2()
            self.board[random.randint(0, 15)][random.randint(0, 15)] = 2

    def do(self, sounds: Sound):
        if not self.game_over:
            self.AI1.get(self.board, 1)
            self.player1_previous_step = (self.AI1.x, self.AI1.y)
            self.step(1)
            self.judgment()
            if self.winner == 0:
                self.AI2.get(self.board)
                self.player2_previous_step = (self.AI2.x, self.AI2.y)
                self.step(2)
                self.judgment()

    def draw_nb(self):
        if self.winner == 2:
            self.screen.blit(self.images.happy, (0, self.screen.get_height() - 128))
        elif self.winner == 1 or time.time() - self.NB2.angry_time < 0:
            self.screen.blit(self.images.angry, (0, self.screen.get_height() - 128))
        else:
            self.screen.blit(self.images.normal, (0, self.screen.get_height() - 128))
        self.screen.blit(self.images.undying_totem_, (128, self.screen.get_height() - 32))
        self.write('×' + str(self.NB2.undying_totem), (160, self.screen.get_height() - 32), size=32)
        self.screen.blit(self.images.restart_totem_, (128, self.screen.get_height() - 64))
        self.write('×' + str(self.NB2.restart_totem), (160, self.screen.get_height() - 64), size=32)
        if self.winner == 1:
            self.screen.blit(self.images.happy, (self.screen.get_width() - 128, self.screen.get_height() - 128))
        elif self.winner == 2 or time.time() - self.NB1.angry_time < 0:
            self.screen.blit(self.images.angry, (self.screen.get_width() - 128, self.screen.get_height() - 128))
        else:
            self.screen.blit(self.images.normal, (self.screen.get_width() - 128, self.screen.get_height() - 128))
        self.screen.blit(self.images.undying_totem_, (self.screen.get_width() - 128 - 64, self.screen.get_height() - 32))
        self.write('×' + str(self.NB1.undying_totem), (self.screen.get_width() - 128 - 32, self.screen.get_height() - 32), size=32)
        self.screen.blit(self.images.restart_totem_, (self.screen.get_width() - 128 - 64, self.screen.get_height() - 64))
        self.write('×' + str(self.NB1.restart_totem), (self.screen.get_width() - 128 - 32, self.screen.get_height() - 64), size=32)

    def show_steps(self):
        """展示步数"""
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        font = self.fonts[32].render(self.text('AI1_steps') + ':' + str(self.get_steps(1)), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 0))
        font = self.fonts[32].render(self.text('AI2_steps') + ':' + str(self.get_steps(2)), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 32))

    def player1_won(self, sounds):
        if self.NB2.restart_totem > 0 or self.NB2.undying_totem > 0:
            if self.NB2.restart_totem == 0:
                u = 2
            elif self.NB2.undying_totem == 0:
                u = 1
            else:
                u = random.randint(1, 2)
            if u == 1:
                self.NB2.restart_totem = self.NB2.restart_totem - 1
                self.init(self.player1_steps, self.player2_steps, difficulty=self.difficulty)
                self.totem_types = 1
            else:
                self.NB2.undying_totem = self.NB2.undying_totem - 1
                self.board[self.player1_previous_step[1]][self.player1_previous_step[0]] = 2
                self.judgment()
                self.totem_types = 0
            self.NB2.angry_time = time.time() + 2
            self.totem_time = 180
            self.winner = 0
            self.game_over = False
            sounds.play('undying')
            for i in range(random.randint(15, 45)):
                self.particles.append(Particle(random.randint(-10, 10), random.randint(-5, 5), (random.randint(0, 255), 255, 0)))

    def player2_won(self, sounds):
        if self.NB1.restart_totem > 0 or self.NB1.undying_totem > 0:
            if self.NB1.restart_totem == 0:
                u = 2
            elif self.NB1.undying_totem == 0:
                u = 1
            else:
                u = random.randint(1, 2)
            if u == 1:
                self.NB1.restart_totem = self.NB1.restart_totem - 1
                self.init(self.player1_steps, self.player2_steps, difficulty=self.difficulty)
                self.totem_types = 1
            else:
                self.NB1.undying_totem = self.NB1.undying_totem - 1
                self.board[self.player2_previous_step[1]][self.player2_previous_step[0]] = 1
                self.judgment()
                self.totem_types = 0
            self.NB1.angry_time = time.time() + 2
            self.totem_time = 180
            self.winner = 0
            self.game_over = False
            sounds.play('undying')
            for i in range(random.randint(15, 45)):
                self.particles.append(Particle(random.randint(-10, 10), random.randint(-5, 5), (random.randint(0, 255), 255, 0)))

    def restart_button(self):
        if self.button((0, 0, 140, 38), self.text('restart')) or pygame.key.get_pressed()[K_r]:
            self.init(difficulty=self.difficulty)
            self.NB1.init()
            self.NB2.init()

    def draw_totem(self):
        for p in self.particles:
            pygame.draw.circle(self.screen, p.color, (self.screen.get_width() // 2 + p.x, self.screen.get_height() // 2 + p.y), 8)
        ds = 0
        for i in range(len(self.particles)):
            if self.particles[i - ds].y > self.screen.get_height() // 2:
                self.particles.pop(i - ds)
                ds = ds + 1
        dt = int((time.time() - self.ts) * 30)
        if dt <= 0:
            dt = 1
        if self.totem_time > 0:
            for p in self.particles:
                p: Particle
                p.update(dt)
            if self.totem_types == 0:
                if len(self.images.totems_undying) == 180:
                    t = self.images.totems_undying[self.totem_time - 1]
                else:
                    t = pygame.Surface((100, 100))
            else:
                if len(self.images.totems_restart) == 180:
                    t = self.images.totems_restart[self.totem_time - 1]
                else:
                    t = pygame.Surface((100, 100))
            t = pygame.transform.scale2x(t)
            xt = self.totem_time
            self.screen.blit(t,
                             (self.screen.get_width() // 2 - t.get_width() // 2 + 0.3 * xt * (xt - 400) / 90 + 0.3 * 200 * 200 / 90,
                              self.screen.get_height() // 2 - t.get_height() // 2))
            if self.totem_time < 0:
                self.totem_time = 0
                self.particles = []
        else:
            self.particles = []
        if self.totem_time > 0:
            self.totem_time = self.totem_time - dt
        elif self.totem_time < 0:
            self.totem_time = 0
        self.ts = time.time()

    def none_won(self, sounds: Sound):
        self.init(self.player1_steps, self.player2_steps, difficulty=self.difficulty)
        self.totem_types = 1
        self.totem_time = 180
        self.game_over = False


class Multi_play(Basic):
    def __init__(self, settings: setting, languages, images, difficulty=0):
        super().__init__(settings, languages, images, difficulty)
        self.did = False
        self.go = 0
        self.player1_name = ''
        self.player2_name = ''
        self.first = ''
        self.ip = ''
        self.port = ''
        self.wait = 0
        self.main = False
        self.restart = False
        self.history = []
        self.say = 0

    def down(self, x: int, y: int):
        if not self.did and self.wait == 0:
            if self.main and self.go == 1:
                self.board[y][x] = 1
                self.player1_previous_step = (x, y)
                self.did = True
            elif (not self.main) and self.go == 2:
                self.board[y][x] = 2
                self.player1_previous_step = (x, y)
                self.did = True

    def restart_button(self):
        if self.winner != 0:
            if self.button((0, 0, 140, 38), self.text('restart')) or pygame.key.get_pressed()[K_r]:
                self.restart = True
            else:
                self.restart = False

    def say1(self, sounds: Sound):
        pass

    def say2(self, sounds: Sound):
        pass

    def say3(self, sounds: Sound):
        pass

    def draw_nb(self):
        for i in range((self.screen.get_height() - 200) // 16):
            if i + 1 <= len(self.history):
                if time.time() - self.history[-i - 1][0] <= 10:
                    self.write(self.history[-i - 1][1], (0, self.screen.get_height() - 66 - i * 16))

    def lose(self):
        if self.winner == 1:
            self.write(self.text('player1_won'), (self.screen.get_width() / 2, 64), size=64, center=True)
        elif self.winner == 2:
            self.write(self.text('player2_won'), (self.screen.get_width() / 2, 64), size=64, center=True)
        else:
            self.write(self.text('none_won'), (self.screen.get_width() / 2, 64), size=64, center=True)

    def do(self, sounds: Sound):
        if self.wait == -1:
            self.write(self.text('wait'), (self.screen.get_width() // 2, 50), size=32, center=True)
        elif self.wait == 1:
            self.write(self.text('wait1'), (self.screen.get_width() // 2, 50), size=32, center=True)
        elif self.wait == 2:
            self.write(self.text('wait2'), (self.screen.get_width() // 2, 50), size=32, center=True)
        if self.button((0, self.screen.get_height() - 40, 100, 40), self.text('say') + '1'):
            self.say = 1
            if random.randint(0, 1) == 1:
                sounds.play('xun1')
            else:
                sounds.play('xun2')
        if self.button((100, self.screen.get_height() - 40, 100, 40), self.text('say') + '2'):
            self.say = 2
            if random.randint(0, 1) == 1:
                sounds.play('ngm1')
            else:
                sounds.play('ngm2')
        if self.button((200, self.screen.get_height() - 40, 100, 40), self.text('say') + '3'):
            self.say = 3
            if random.randint(0, 1) == 1:
                sounds.play('lblh1')
            else:
                sounds.play('lblh2')

    def show_steps(self):
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        font = self.fonts[32].render(self.text('player1_steps') + ':' + str(self.get_steps(1)), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 0))
        font = self.fonts[32].render(self.text('player2_steps') + ':' + str(self.get_steps(2)), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 32))
        font = self.fonts[32].render(self.text('player1') + ':' + str(self.player1_name), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 64))
        font = self.fonts[32].render(self.text('player2') + ':' + str(self.player2_name), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 96))
        font = self.fonts[32].render(self.text('first') + ':' + str(self.first), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 128))
        font = self.fonts[32].render(self.text('ip') + ':' + str(self.ip), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 160))
        font = self.fonts[32].render(self.text('port') + ':' + str(self.port), False, (0, 0, 0))
        self.screen.blit(font, (self.screen.get_width() - font.get_width(), 192))
