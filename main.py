import time

import pygame, random
from pygame.locals import *

pygame.init()
screen_size = (1000, 700)
screen = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)
myfont = pygame.font.SysFont('Simsun', 20)
tittle = pygame.font.SysFont('Simsun', 50)
pygame.display.set_caption('五子棋')
jm = 0
clock = pygame.time.Clock()
looks = 1
perspective = [0, 0]
press = pygame.key.get_pressed()
player = 1
block = []
player1 = [0, 0]
player2 = [0, 0]
chessbord_size = 10
key_up = list(pygame.key.get_pressed())
kp_enter = 0
wins = False
win_line = [[0, 0], [0, 0]]
winner = 0
map_size = 1
moving = 0
player1_pos = [0, 0]
player2_pos = [0, 0]
mn = 1
first_player = 1
debug = False  # 测试模式
no_win = False


def font_change(font):
    global myfont, tittle
    if font == 0:
        myfont = pygame.font.SysFont('Simsun', 20)
        tittle = pygame.font.SysFont('Simsun', 50)
    else:
        myfont = pygame.font.SysFont('SimHei', 20)
        tittle = pygame.font.SysFont('SimHei', 50)


try:
    s = open(r'./setting.txt', 'r+', encoding='utf-8')
except FileNotFoundError:
    s = open(r'./setting.txt', 'w+', encoding='utf-8')
st = s.read()
if st == '':
    s.write('0\n0')
    language = 0
    f = 0
else:
    try:
        language = int(st[-1])
        f = int(st[0])
    except ValueError:
        s = open(r'./setting.txt', 'w+', encoding='utf-8')
        s.write('0\n0')
        f = 0
        language = 0
font_change(f)
times = 0
p1_t = 0
p2_t = 0
p1_ts = 0
p2_ts = 0
p1_tt = 0
p2_tt = 0
p_t = 0
pt = 0
if __name__ == '__main__':
    run = True
else:
    run = False


class mouse_set:
    x = 0
    y = 0
    xy = (0, 0)
    press = [0, 0, 0]
    up = [0, 0, 0]


class ai:
    player_point = []
    ai_point = []
    all_point = []

    def set(self, size):
        self.player_point = []
        self.ai_point = []
        self.all_point = []
        f1 = []
        for ss in range(size * 2):
            f1.append(0)
        f2 = []
        for ss in range(size * 2):
            f2.append(f1.copy())
        for i in range(len(f2)):
            self.ai_point.append(f2[i].copy())
            self.all_point.append(f2[i].copy())
            self.player_point.append(f2[i].copy())

    def point_player(self):
        global block
        size = len(block) // 2
        for y1 in range(len(block)):
            for x1 in range(len(block[y1])):
                all_points = 0
                if block[y1][x1] == 0:
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 + i1 + 1, y1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    r = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 + i1 + 1, y1 - 1 - i1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    rd = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1, y1 - 1 - i1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    d = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 - i1 - 1, y1 - i1 - 1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    ld = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 - i1 - 1, y1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    l = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 - i1 - 1, y1 + i1 + 1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    lu = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1, y1 + 1 + i1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    u = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 + i1 + 1, y1 + 1 + i1, size) != 1 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    ru = p
                    ss = [u, d, lu, rd, l, r, ld, ru]
                    all_points = max(ss)
                else:
                    all_points = 0
                self.player_point[y1][x1] = all_points

    def point_ai(self):
        global block
        size = len(block) // 2
        for y1 in range(len(block)):
            for x1 in range(len(block[y1])):
                all_point1 = 0
                if block[y1][x1] == 0:
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 + i1 + 1, y1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    r = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 + i1 + 1, y1 - 1 - i1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    rd = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1, y1 - 1 - i1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    d = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 - i1 - 1, y1 - i1 - 1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    ld = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 - i1 - 1, y1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    l = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 - i1 - 1, y1 + i1 + 1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    lu = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1, y1 + 1 + i1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    u = p
                    g = True
                    p = 0
                    for i1 in range(5):
                        if read_block(x1 + i1 + 1, y1 + 1 + i1, size) != 2 and g:
                            if read_block(x1 + i1 + 1, y1 + 1 + i1, size) == 0 and i1 != 0:
                                p = i1 + 1
                            else:
                                p = i1
                            g = False
                    ru = p
                    ss = [u, d, lu, rd, l, r, ld, ru]
                    all_point1 = max(ss)
                else:
                    all_point1 = 0
                self.ai_point[y1][x1] = all_point1

    def decision(self):
        global block
        max_point = [0]
        max_pos = [[0, 0]]
        for y1 in range(len(block)):
            for x1 in range(len(block[y1])):
                p = self.player_point[y1][x1]
                if p > max_point[0]:
                    max_point = [p]
                    max_pos = [[x1, y1]]
                elif p == max_point[0]:
                    max_point.append(p)
                    max_pos.append([x1, y1])
        if len(max_point) == 1:
            p_max = max_pos[0]
            p_p = max_point[0]
        else:
            r = random.randint(0, len(max_point) - 1)
            p_max = max_pos[r]
            p_p = max_point[0]
        max_point = [0]
        max_pos = [[0, 0]]
        for y1 in range(len(block)):
            for x1 in range(len(block[y1])):
                p = self.ai_point[y1][x1]
                if p > max_point[0]:
                    max_point = [p]
                    max_pos = [[x1, y1]]
                elif p == max_point[0]:
                    max_point.append(p)
                    max_pos.append([x1, y1])
        if len(max_point) == 1:
            a_max = max_pos[0]
            a_p = max_point[0]
        else:
            r = random.randint(0, len(max_point) - 1)
            a_max = max_pos[r]
            a_p = max_point[0]
        if a_p > p_p:
            block[a_max[1]][a_max[0]] = 2
        else:
            block[p_max[1]][p_max[0]] = 2


AI = ai()
mouse = mouse_set()


def write(massage, pos, color=(255, 255, 255)):
    screen.blit(myfont.render(str(massage), True, color), pos)


def anniu(rect, zi='', rect_color=(120, 120, 120), text_color=(255, 255, 255)):  # 按钮
    global mouse
    pygame.draw.rect(screen, rect_color, rect)
    fo = myfont.render(zi, True, text_color)
    screen.blit(fo, (int(rect[0] + (rect[2] / 2) - (fo.get_width() / 2)), int(rect[1] + 10)))
    if rect[0] < mouse.xy[0] < (rect[0] + rect[2]) and rect[1] < mouse.xy[1] < (rect[1] + rect[3]):
        pygame.draw.rect(screen, (255, 255, 255), rect, 4)
        if mouse.up[0]:
            return True
        else:
            return False
    else:
        pygame.draw.rect(screen, (0, 0, 0), rect, 4)
        return False


def choose(start_pos, lists, number, font_color=(255, 255, 255)):
    global mouse
    rt = number
    for i1 in range(len(lists)):
        if start_pos[0] <= mouse.x <= start_pos[0] + 20 and start_pos[1] + i1 * 20 <= mouse.y <= start_pos[1] + 20 + i1 * 20:
            pygame.draw.circle(screen, (230, 230, 230), (start_pos[0] + 10, start_pos[1] + 10 + i1 * 20), 9)
            if mouse.up[0] and number != i1:
                rt = i1
        else:
            pygame.draw.circle(screen, (255, 255, 255), (start_pos[0] + 10, start_pos[1] + 10 + i1 * 20), 9)
        if number == i1:
            pygame.draw.circle(screen, (0, 0, 0), (start_pos[0] + 10, start_pos[1] + 10 + i1 * 20), 6)
        write(lists[i1], (start_pos[0] + 20, start_pos[1] + i1 * 20), font_color)
    return rt


def read_block(x, y, size):
    try:
        if 0 <= int(x) <= size * 2 - 1 and 0 <= int(y) <= size * 2 - 1:
            return block[int(y)][int(x)]
        else:
            return -1
    except IndexError:
        return -1


def win(size):
    global block, wins, winner
    for x1 in range(size * 2):
        for y1 in range(size * 2):
            s = read_block(x1, y1, size)
            if s != 0:
                if not wins:
                    l = 0
                    for i in range(5):
                        if read_block(x1 - i, y1, size) == s:
                            l = l + 1
                    if l >= 5:
                        wins = True
                        win_line[1] = [x1 - 4, y1]
                        win_line[0] = [x1, y1]
                        winner = s
                if not wins:
                    lu = 0
                    for i in range(5):
                        if read_block(x1 - i, y1 + i, size) == s:
                            lu = lu + 1
                    if lu >= 5:
                        wins = True
                        win_line[1] = [x1 - 4, y1 + 4]
                        winner = s
                        win_line[0] = [x1, y1]
                if not wins:
                    u = 0
                    for i in range(5):
                        if read_block(x1, y1 + i, size) == s:
                            u = u + 1
                    if u >= 5:
                        wins = True
                        win_line[1] = [x1, y1 + 4]
                        win_line[0] = [x1, y1]
                        winner = s
                if not wins:
                    ru = 0
                    for i in range(5):
                        if read_block(x1 + i, y1 + i, size) == s:
                            ru = ru + 1
                    if ru >= 5:
                        wins = True
                        win_line[1] = [x1 + 4, y1 + 4]
                        win_line[0] = [x1, y1]
                        winner = s
                if not wins:
                    r = 0
                    for i in range(5):
                        if read_block(x1 + i, y1, size) == s:
                            r = r + 1
                    if r >= 5:
                        wins = True
                        win_line[1] = [x1 + 4, y1]
                        win_line[0] = [x1, y1]
                        winner = s
                if not wins:
                    rd = 0
                    for i in range(5):
                        if read_block(x1 + i, y1 - i, size) == s:
                            rd = rd + 1
                    if rd >= 5:
                        wins = True
                        win_line[1] = [x1 + 4, y1 - 4]
                        win_line[0] = [x1, y1]
                        winner = s
                if not wins:
                    d = 0
                    for i in range(5):
                        if read_block(x1 - i, y1, size) == s:
                            d = d + 1
                    if d >= 5:
                        wins = True
                        win_line[1] = [x1, y1 - 4]
                        winner = s
                        win_line[0] = [x1, y1]
                if not wins:
                    ld = 0
                    for i in range(5):
                        if read_block(x1 - i, y1, size) == s:
                            ld = ld + 1
                    if ld >= 5:
                        wins = True
                        winner = s
                        win_line[1] = [x1 - 4, y1 - 4]
                        win_line[0] = [x1, y1]


def press_show(key, key_name, rect, not_show_color=(255, 255, 255), show_color=(0, 0, 0)):
    if press[key]:
        pygame.draw.rect(screen, show_color, rect)
        write(key_name, (rect[0] + rect[2] / 2 - 10, rect[1] + rect[3] / 2 - 10), (127, 127, 127))
        pygame.draw.rect(screen, (0, 0, 0), rect, 3)
    else:
        pygame.draw.rect(screen, not_show_color, rect)
        write(key_name, (rect[0] + rect[2] / 2 - 10, rect[1] + rect[3] / 2 - 10), (127, 127, 127))
        pygame.draw.rect(screen, (0, 0, 0), rect, 3)


def long(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def play(size=10):
    global player, player1, player2, perspective, block, wins, jm, winner, moving, player1_pos, player2_pos, mn, first_player, times, no_win, p1_t, p2_t, p1_ts, p2_ts, p1_tt, p2_tt
    if looks == 1:
        screen.fill((255, 255, 255))
    else:
        screen.fill((220, 140, 50))
    for x1 in range(size * 2 + 1):
        pygame.draw.line(screen, (0, 0, 0), (screen_size[0] / 2 - size * 32 + x1 * 32 + perspective[0], screen_size[1] / 2 - size * 32 + perspective[1]),
                         (screen_size[0] / 2 - size * 32 + x1 * 32 + perspective[0], screen_size[1] / 2 + size * 32 + perspective[1]))
    for y1 in range(size * 2 + 1):
        pygame.draw.line(screen, (0, 0, 0), (screen_size[0] / 2 - size * 32 + perspective[0], screen_size[1] / 2 - size * 32 + y1 * 32 + perspective[1]),
                         (screen_size[0] / 2 + size * 32 + perspective[0], screen_size[1] / 2 - size * 32 + y1 * 32 + perspective[1]))
    pygame.draw.circle(screen, (0, 0, 0), (perspective[0] + screen_size[0] / 2, perspective[1] + screen_size[1] / 2), 3)
    for iy in range(size * 2):
        for ix in range(size * 2):
            if block[iy][ix] == 1:
                if looks == 1:
                    pygame.draw.circle(screen, (20, 20, 255), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16), 15, 3)
                else:
                    pygame.draw.circle(screen, (20, 20, 255), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16), 15)
            elif block[iy][ix] == 2:
                if looks == 1:
                    pygame.draw.line(screen, (255, 20, 20), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 4, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 4),
                                     (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 28, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 28), 5)
                    pygame.draw.line(screen, (255, 20, 20), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 28, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 4),
                                     (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 4, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 28), 5)
                else:
                    pygame.draw.circle(screen, (255, 20, 20), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16), 15)
    if not wins and not no_win:
        if times >= (size * 2) ** 2:
            no_win = True
        if player == 1:
            pygame.draw.rect(screen, (255, 20, 20),
                             (screen_size[0] / 2 - player2_pos[0] // 32 * 32 + perspective[0] - 32, screen_size[1] / 2 - player2_pos[1] // 32 * 32 + perspective[1] - 32, 32, 32), 5)
            if read_block(-perspective[0] // 32 + size, -perspective[1] // 32 + size, size) == 0:
                pygame.draw.rect(screen, (20, 20, 255), (perspective[0] % 32 + screen_size[0] / 2 - 32, perspective[1] % 32 + screen_size[1] / 2 - 32, 32, 32), 5)
        else:
            pygame.draw.rect(screen, (20, 20, 255),
                             (screen_size[0] / 2 - player1_pos[0] // 32 * 32 + perspective[0] - 32, screen_size[1] / 2 - player1_pos[1] // 32 * 32 + perspective[1] - 32, 32, 32), 5)
            if read_block(-perspective[0] // 32 + size, -perspective[1] // 32 + size, size) == 0:
                pygame.draw.rect(screen, (255, 20, 20), (perspective[0] % 32 + screen_size[0] / 2 - 32, perspective[1] % 32 + screen_size[1] / 2 - 32, 32, 32), 5)
        pygame.draw.circle(screen, (128, 128, 128), (screen_size[0] / 2, screen_size[1] / 2), 5)
    write([-perspective[0] // 32 + size, perspective[1] // 32 + size], (0, 40), (0, 0, 0))
    press_show(K_a, 'A', (0, screen_size[1] - 40, 40, 40))
    press_show(K_s, 'S', (40, screen_size[1] - 40, 40, 40))
    press_show(K_d, 'D', (80, screen_size[1] - 40, 40, 40))
    press_show(K_w, 'w', (40, screen_size[1] - 80, 40, 40))
    press_show(K_f, 'F', (120, screen_size[1] - 40, 40, 40))
    press_show(K_KP_ENTER, 'Enter', (screen_size[0] - 80, screen_size[1] - 40, 80, 40))
    press_show(K_RIGHT, '→', (screen_size[0] - 120, screen_size[1] - 40, 40, 40))
    press_show(K_DOWN, '↓', (screen_size[0] - 160, screen_size[1] - 40, 40, 40))
    press_show(K_LEFT, '←', (screen_size[0] - 200, screen_size[1] - 40, 40, 40))
    press_show(K_UP, '↑', (screen_size[0] - 160, screen_size[1] - 80, 40, 40))
    if language == 0:
        write('先手:玩家' + str(first_player), (0, 20), (0, 0, 0))
        write('玩家1用时：' + str(int(p1_t)) + '秒', (0, 60), (0, 0, 0))
        write('玩家2用时：' + str(int(p2_t)) + '秒', (0, 80), (0, 0, 0))
        if anniu((screen_size[0] - 100, 0, 100, 40), '退出'):
            jm = 0
        if anniu((screen_size[0] - 100, 40, 100, 40), '重来') or key_up[K_r]:
            p1_t = 0
            p2_t = 0
            p1_ts = time.time()
            p2_ts = time.time()
            p1_tt = 0
            p2_tt = 0
            times = 0
            perspective = [0, 0]
            player1 = [chessbord_size, chessbord_size]
            player2 = [chessbord_size, chessbord_size]
            player1_pos = [0, 0]
            player2_pos = [0, 0]
            winner = 0
            player = first_player
            wins = False
            s1 = []
            for x in range(map_size * 10 + 10):
                s1.append(0)
            block = []
            for y in range(map_size * 10 + 10):
                block.append(s1.copy())
    else:
        write('First Hand: Player' + str(first_player), (0, 20), (0, 0, 0))
        write('Player 1 time:' + str(int(p1_t)) + 'sec', (0, 60), (0, 0, 0))
        write('Player 2 time:' + str(int(p2_t)) + 'sec', (0, 80), (0, 0, 0))
        if anniu((screen_size[0] - 100, 0, 100, 40), 'exit'):
            jm = 0
        if anniu((screen_size[0] - 100, 40, 100, 40), 'start over') or key_up[K_r]:
            p1_t = 0
            p2_t = 0
            p1_ts = time.time()
            p2_ts = time.time()
            p1_tt = 0
            p2_tt = 0
            times = 0
            perspective = [0, 0]
            player1 = [chessbord_size, chessbord_size]
            player2 = [chessbord_size, chessbord_size]
            player1_pos = [0, 0]
            player2_pos = [0, 0]
            winner = 0
            player = first_player
            wins = False
            s1 = []
            for x in range(map_size * 10 + 10):
                s1.append(0)
            block = []
            for y in range(map_size * 10 + 10):
                block.append(s1.copy())
    if not wins and not no_win:
        if language == 0:
            write('现在是玩家' + str(player) + '下棋', (screen_size[0] / 2 - 80, 0), (0, 0, 0))
        else:
            write('Now Player' + str(player) + ' play Chess', (screen_size[0] / 2 - 80, 0), (0, 0, 0))
        if not moving:
            if player == 1:
                p1_t = p1_tt + time.time() - p1_ts
                player1 = [-perspective[0] // 32 + size, perspective[1] // 32 + size]
                player1_pos = perspective
                if key_up[K_f] and read_block(-perspective[0] // 32 + size, -perspective[1] // 32 + size, size) == 0:
                    block[-player1[1] - 1][player1[0]] = 1
                    times = times + 1
                    player = 2
                    perspective = player2_pos
                    win(size)
                    p2_ts = time.time()
                    p1_tt = p1_t
            else:
                p2_t = p2_tt + time.time() - p2_ts
                player2 = [-perspective[0] // 32 + size, perspective[1] // 32 + size]
                player2_pos = perspective
                if kp_enter and read_block(-perspective[0] // 32 + size, -perspective[1] // 32 + size, size) == 0:
                    block[-player2[1] - 1][player2[0]] = 2
                    times = times + 1
                    player = 1
                    perspective = player1_pos
                    win(size)
                    p1_ts = time.time()
                    p2_tt = p2_t
            if player == 1:
                if press[K_w]:
                    perspective[1] = perspective[1] + 2
                if press[K_s]:
                    perspective[1] = perspective[1] - 2
                if press[K_a]:
                    perspective[0] = perspective[0] + 2
                if press[K_d]:
                    perspective[0] = perspective[0] - 2
            else:
                if press[K_UP]:
                    perspective[1] = perspective[1] + 2
                if press[K_DOWN]:
                    perspective[1] = perspective[1] - 2
                if press[K_LEFT]:
                    perspective[0] = perspective[0] + 2
                if press[K_RIGHT]:
                    perspective[0] = perspective[0] - 2
    else:
        if wins:
            perspective = [-(win_line[0][0] - size) * 32 + 16, -(win_line[0][1] - size) * 32 + 16]
            pygame.draw.line(screen, (20, 255, 20),
                             (screen_size[0] / 2 - size * 32 + win_line[0][0] * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + win_line[0][1] * 32 + perspective[1] + 16),
                             (screen_size[0] / 2 - size * 32 + win_line[1][0] * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + win_line[1][1] * 32 + perspective[1] + 16), 10)
            if language == 0:
                screen.blit(tittle.render('玩家' + str(winner) + '赢了', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            else:
                screen.blit(tittle.render('Player' + str(winner) + 'won', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
        else:
            if language == 0:
                screen.blit(tittle.render('平局', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            else:
                screen.blit(tittle.render('Draw', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))


def one_play(size=10):
    global perspective, player, AI, jm, wins, block, no_win, times, p_t, pt
    if looks == 1:
        screen.fill((255, 255, 255))
    else:
        screen.fill((220, 140, 50))
    for x1 in range(size * 2 + 1):
        pygame.draw.line(screen, (0, 0, 0), (screen_size[0] / 2 - size * 32 + x1 * 32 + perspective[0], screen_size[1] / 2 - size * 32 + perspective[1]),
                         (screen_size[0] / 2 - size * 32 + x1 * 32 + perspective[0], screen_size[1] / 2 + size * 32 + perspective[1]))
    for y1 in range(size * 2 + 1):
        pygame.draw.line(screen, (0, 0, 0), (screen_size[0] / 2 - size * 32 + perspective[0], screen_size[1] / 2 - size * 32 + y1 * 32 + perspective[1]),
                         (screen_size[0] / 2 + size * 32 + perspective[0], screen_size[1] / 2 - size * 32 + y1 * 32 + perspective[1]))
    pygame.draw.circle(screen, (0, 0, 0), (perspective[0] + screen_size[0] / 2, perspective[1] + screen_size[1] / 2), 3)
    for iy in range(size * 2):
        for ix in range(size * 2):
            if max(AI.ai_point[iy][ix], AI.player_point[iy][ix]) != 0 and debug:
                write(str(max(AI.ai_point[iy][ix], AI.player_point[iy][ix])),
                      (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16), (0, 0, 0))
            if block[iy][ix] == 1:
                if looks == 1:
                    pygame.draw.circle(screen, (20, 20, 255), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16), 15, 3)
                else:
                    if first_player == 1:
                        pygame.draw.circle(screen, (0, 0, 0), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16), 15)
                    else:
                        pygame.draw.circle(screen, (255, 255, 255), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16),
                                           15)
            elif block[iy][ix] == 2:
                if looks == 1:
                    pygame.draw.line(screen, (255, 20, 20), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 4, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 4),
                                     (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 28, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 28), 5)
                    pygame.draw.line(screen, (255, 20, 20), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 28, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 4),
                                     (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 4, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 28), 5)
                else:
                    if first_player == 2:
                        pygame.draw.circle(screen, (0, 0, 0), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16), 15)
                    else:
                        pygame.draw.circle(screen, (255, 255, 255), (screen_size[0] / 2 - size * 32 + ix * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + iy * 32 + perspective[1] + 16),
                                           15)
    point_to = (int((mouse.x - perspective[0] - screen_size[0] / 2) // 32 + size), int(-(mouse.y - perspective[1] - screen_size[1] / 2) // 32 + size))
    if not wins and not no_win:
        if 0 <= point_to[0] < size * 2 and 0 <= point_to[1] < size * 2:
            pygame.draw.rect(screen, (0, 0, 0), (
                (mouse.x - screen_size[0] / 2) // 32 * 32 + (perspective[0] % 32) + screen_size[0] / 2, (mouse.y - screen_size[1] / 2 - 1) // 32 * 32 + perspective[1] % 32 + screen_size[1] / 2, 32,
                32), 3)
            if mouse.up[0] and block[-point_to[1] - 1][point_to[0]] == 0:
                block[-point_to[1] - 1][point_to[0]] = 1
                times = times + 1
                win(size)
                if times >= (size * 2) ** 2:
                    no_win = True
                else:
                    if not wins and not no_win:
                        AI.point_player()
                        AI.point_ai()
                        AI.decision()
                        AI.point_player()
                        AI.point_ai()
                        win(size)
                        times = times + 1
                        if times >= (size * 2) ** 2:
                            no_win = True
        if press[K_w]:
            perspective[1] = perspective[1] + 2
        if press[K_s]:
            perspective[1] = perspective[1] - 2
        if press[K_a]:
            perspective[0] = perspective[0] + 2
        if press[K_d]:
            perspective[0] = perspective[0] - 2
    else:
        if wins:
            perspective = [-(win_line[0][0] - size) * 32 + 16, -(win_line[0][1] - size) * 32 + 16]
            pygame.draw.line(screen, (20, 255, 20),
                             (screen_size[0] / 2 - size * 32 + win_line[0][0] * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + win_line[0][1] * 32 + perspective[1] + 16),
                             (screen_size[0] / 2 - size * 32 + win_line[1][0] * 32 + perspective[0] + 16, screen_size[1] / 2 - size * 32 + win_line[1][1] * 32 + perspective[1] + 16), 10)
            if winner == 1:
                if language == 0:
                    screen.blit(tittle.render('玩家赢了', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
                else:
                    screen.blit(tittle.render('player won', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            else:
                if language == 0:
                    screen.blit(tittle.render('AI赢了', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
                else:
                    screen.blit(tittle.render('AI won', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
        else:
            if language == 0:
                screen.blit(tittle.render('平局', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            else:
                screen.blit(tittle.render('Draw', True, (0, 0, 0)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))

    write(point_to, (0, 20), (0, 0, 0))
    if not wins and not no_win:
        if language == 0:
            write('用时：' + str(int(time.time() - p_t)) + '秒', (0, 40), (0, 0, 0))
        else:
            write('Elapsed time:' + str(int(time.time() - p_t)) + 'sec', (0, 40), (0, 0, 0))
    else:
        if pt == 0:
            pt = time.time() - p_t
        if language == 0:
            write('用时：' + str(int(pt)) + '秒', (0, 40), (0, 0, 0))
        else:
            write('Elapsed time:' + str(int(pt)) + 'sec', (0, 40), (0, 0, 0))
    if language == 0:
        if anniu((screen_size[0] - 100, 0, 100, 40), '退出'):
            jm = 0
        if anniu((screen_size[0] - 100, 40, 100, 40), '重来') or key_up[K_r]:
            AI.set(int(map_size * 5 + 5))
            p_t = time.time()
            pt = 0
            perspective = [0, 0]
            player = first_player
            wins = False
            s1 = []
            for x in range(map_size * 10 + 10):
                s1.append(0)
            block = []
            for y in range(map_size * 10 + 10):
                block.append(s1.copy())
    else:
        if anniu((screen_size[0] - 100, 0, 100, 40), 'exit'):
            jm = 0
        if anniu((screen_size[0] - 100, 40, 100, 40), 'start over') or key_up[K_r]:
            AI.set(int(map_size * 5 + 5))
            p_t = time.time()
            pt = 0
            perspective = [0, 0]
            player = first_player
            wins = False
            s1 = []
            for x in range(map_size * 10 + 10):
                s1.append(0)
            block = []
            for y in range(map_size * 10 + 10):
                block.append(s1.copy())


while run:
    if screen_size != (screen.get_width(), screen.get_height()):
        screen_size = (screen.get_width(), screen.get_height())
    for i in range(len(key_up)):
        if press[i] == pygame.key.get_pressed()[i] + 1:
            key_up[i] = 1
        else:
            key_up[i] = 0
    if press[K_KP_ENTER] and not pygame.key.get_pressed()[K_KP_ENTER]:
        kp_enter = 1
    else:
        kp_enter = 0
    press = pygame.key.get_pressed()
    mouse.xy = pygame.mouse.get_pos()
    mouse.x = mouse.xy[0]
    mouse.y = mouse.xy[1]
    for i in range(3):
        if mouse.press[i] == 1 and pygame.mouse.get_pressed()[i] == 0:
            mouse.up[i] = 1
        else:
            mouse.up[i] = 0
    mouse.press = pygame.mouse.get_pressed()

    screen.fill((0, 0, 0))
    if jm == 0:
        screen.fill((100, 100, 255))
        if language == 0:
            screen.blit(tittle.render('五子棋', True, (255, 255, 255)), (screen_size[0] / 2 - 75, screen_size[1] / 4 - 25))
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 - 20, 200, 40), '双人游戏'):
                jm = 1
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 - 80, 200, 40), '单人游戏'):
                jm = 3
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 40, 200, 40), '说明'):
                jm = 4
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 160, 200, 40), '退出'):
                run = False

        else:
            screen.blit(tittle.render('Gomoku', True, (255, 255, 255)), (screen_size[0] / 2 - 75, screen_size[1] / 4 - 25))
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 - 20, 200, 40), 'two-player game'):
                jm = 1
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 - 80, 200, 40), 'single-player'):
                jm = 3
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 40, 200, 40), 'Description'):
                jm = 4
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 160, 200, 40), 'Exit'):
                run = False
        if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 100, 200, 40), '设置 settings'):
            jm = 7
    if jm == 1:
        screen.fill((100, 100, 255))
        if language == 0:
            screen.blit(tittle.render('选择模式', True, (255, 255, 255)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            looks = choose((screen_size[0] / 2 - 50, screen_size[1] / 4,), ['黑白子样式', '圆叉样式'], looks)
            write('棋盘大小', (screen_size[0] / 2 - 50, screen_size[1] / 3 - 20), (255, 255, 255))
            map_size = choose((screen_size[0] / 2 - 50, screen_size[1] / 3), [5, 10, 15, 20, 25, 30, 35, 40, 45, 50], map_size)
            write('先手', (screen_size[0] / 2 - 50, screen_size[1] / 1.5))
            first_player = choose((screen_size[0] / 2 - 50, screen_size[1] / 1.5 + 20), ['玩家1', '玩家2'], first_player - 1) + 1
            if anniu((screen_size[0] * 0.75, screen_size[1] / 1.5 - 20, 200, 40), '开始'):
                p1_t = 0
                p2_t = 0
                p1_ts = time.time()
                p2_ts = time.time()
                p1_tt = 0
                p2_tt = 0
                perspective = [0, 0]
                times = 0
                player1 = [chessbord_size, chessbord_size]
                player2 = [chessbord_size, chessbord_size]
                player1_pos = [0, 0]
                player2_pos = [0, 0]
                winner = 0
                player = first_player
                wins = False
                s1 = []
                for x in range(map_size * 10 + 10):
                    s1.append(0)
                block = []
                for y in range(map_size * 10 + 10):
                    block.append(s1.copy())
                jm = 2
            if anniu((screen_size[0] / 4 - 100, screen_size[1] / 1.5 - 20, 200, 40), '返回'):
                jm = 0
        else:
            screen.blit(tittle.render('Select Mode', True, (255, 255, 255)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            looks = choose((screen_size[0] / 2 - 50, screen_size[1] / 4,), ['black and white substyle', 'round fork style'], looks)
            write('board size', (screen_size[0] / 2 - 50, screen_size[1] / 3 - 20), (255, 255, 255))
            map_size = choose((screen_size[0] / 2 - 50, screen_size[1] / 3), [5, 10, 15, 20, 25, 30, 35, 40, 45, 50], map_size)
            write('firsthand', (screen_size[0] / 2 - 50, screen_size[1] / 1.5))
            first_player = choose((screen_size[0] / 2 - 50, screen_size[1] / 1.5 + 20), ['player1', 'player2'], first_player - 1) + 1
            if anniu((screen_size[0] * 0.75, screen_size[1] / 1.5 - 20, 200, 40), 'start'):
                p1_t = 0
                p2_t = 0
                p1_ts = time.time()
                p2_ts = time.time()
                p1_tt = 0
                p2_tt = 0
                perspective = [0, 0]
                times = 0
                player1 = [chessbord_size, chessbord_size]
                player2 = [chessbord_size, chessbord_size]
                player1_pos = [0, 0]
                player2_pos = [0, 0]
                winner = 0
                player = first_player
                wins = False
                s1 = []
                for x in range(map_size * 10 + 10):
                    s1.append(0)
                block = []
                for y in range(map_size * 10 + 10):
                    block.append(s1.copy())
                jm = 2
            if anniu((screen_size[0] / 4 - 100, screen_size[1] / 1.5 - 20, 200, 40), 'return'):
                jm = 0
    if jm == 2:
        play(int(map_size * 5 + 5))
    if jm == 3:
        screen.fill((100, 100, 255))
        if language == 0:
            screen.blit(tittle.render('选择模式', True, (255, 255, 255)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            looks = choose((screen_size[0] / 2 - 50, screen_size[1] / 4,), ['黑白子样式', '圆叉样式'], looks)
            write('棋盘大小(不宜过大，否则会很卡)', (screen_size[0] / 2 - 145, screen_size[1] / 3), (255, 255, 255))
            map_size = choose((screen_size[0] / 2 - 50, screen_size[1] / 2 - 80), [5, 10, 15, 20], map_size)
            write('先手', (screen_size[0] / 2 - 50, screen_size[1] / 2))
            first_player = choose((screen_size[0] / 2 - 50, screen_size[1] / 2 + 30), ['玩家', 'AI'], first_player - 1) + 1
            if anniu((screen_size[0] / 4 - 100, screen_size[1] / 1.5 - 20, 200, 40), '返回'):
                jm = 0
            if anniu((screen_size[0] * 0.75, screen_size[1] / 1.5 - 20, 200, 40), '开始'):
                AI.set(int(map_size * 5 + 5))
                p_t = time.time()
                pt = 0
                perspective = [0, 0]
                times = 0
                no_win = False
                player = first_player
                wins = False
                s1 = []
                for x in range(map_size * 10 + 10):
                    s1.append(0)
                block = []
                for y in range(map_size * 10 + 10):
                    block.append(s1.copy())
                if first_player == 2:
                    block[map_size * 5 + 5][map_size * 5 + 5] = 2
                jm = 6
        else:
            screen.blit(tittle.render('Select Mode', True, (255, 255, 255)), (screen_size[0] / 2 - 100, screen_size[1] / 5 - 25))
            looks = choose((screen_size[0] / 2 - 50, screen_size[1] / 4,), ['black and white substyle', 'round fork style'], looks)
            write('Checkerboard size (not too large, otherwise it will be stuck)', (screen_size[0] / 2 - 145, screen_size[1] / 3), (255, 255, 255))
            map_size = choose((screen_size[0] / 2 - 50, screen_size[1] / 2 - 80), [5, 10, 15, 20], map_size)
            write('first-hand', (screen_size[0] / 2 - 50, screen_size[1] / 2))
            first_player = choose((screen_size[0] / 2 - 50, screen_size[1] / 2 + 30), ['player', 'AI'], first_player - 1) + 1
            if anniu((screen_size[0] / 4 - 100, screen_size[1] / 1.5 - 20, 200, 40), 'return'):
                jm = 0
            if anniu((screen_size[0] * 0.75, screen_size[1] / 1.5 - 20, 200, 40), 'start'):
                AI.set(int(map_size * 5 + 5))
                p_t = time.time()
                pt = 0
                perspective = [0, 0]
                times = 0
                no_win = False
                player = first_player
                wins = False
                s1 = []
                for x in range(map_size * 10 + 10):
                    s1.append(0)
                block = []
                for y in range(map_size * 10 + 10):
                    block.append(s1.copy())
                if first_player == 2:
                    block[map_size * 5 + 5][map_size * 5 + 5] = 2
                jm = 6
    if jm == 4:
        screen.fill((100, 100, 255))
        if language == 0:
            screen.blit(tittle.render('说明', True, (255, 255, 255)), (screen_size[0] / 2 - 50, 50))
            write('单人游戏：与AI对决，鼠标下棋子', (screen_size[0] / 2 - 100, screen_size[1] / 2 - 100))
            write('双人模式：玩家1使用ADWS移动视角，按f下棋', (screen_size[0] / 2 - 100, screen_size[1] / 2 - 50))
            write('玩家2使用箭头移动视角，按下回车下棋', (screen_size[0] / 2, screen_size[1] / 2))
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 150, 200, 40), '返回'):
                jm = 0
        else:
            screen.blit(tittle.render('description', True, (255, 255, 255)), (screen_size[0] / 2 - 50, 50))
            write('Single Player: Versus AI, Mouse Playing Pieces', (screen_size[0] / 2 - 100, screen_size[1] / 2 - 100))
            write('Two-player mode: player 1 uses ADWS to move the perspective and press F to play chess', (screen_size[0] / 2 - 100, screen_size[1] / 2 - 50))
            write('Player 2 uses the arrows to move the perspective, press Enter to play chess', (screen_size[0] / 2, screen_size[1] / 2))
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 150, 200, 40), 'return'):
                jm = 0

    if jm == 5:
        one_play(int(map_size * 5 + 5))
    if jm == 6:
        screen.fill((100, 100, 255))
        if mouse.up[0] == 0:
            jm = 5
    if jm == 7:
        screen.fill((100, 100, 255))
        if language == 0:
            screen.blit(tittle.render('设置', True, (255, 255, 255)), (screen_size[0] / 2 - 50, 50))
            if f == 0:
                if anniu((screen_size[0] / 2 - 450, screen_size[1] / 2 + 100, 350, 40), '切换字体为微软雅黑'):
                    f = 1
                    font_change(f)
            else:
                if anniu((screen_size[0] / 2 - 450, screen_size[1] / 2 + 100, 350, 40), '切换字体为宋体'):
                    f = 0
                    font_change(f)
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 150, 200, 40), '返回'):
                jm = 0
        else:
            screen.blit(tittle.render('Settings', True, (255, 255, 255)), (screen_size[0] / 2 - 100, 50))
            if f == 0:
                if anniu((screen_size[0] / 2 - 450, screen_size[1] / 2 + 100, 350, 40), 'Switch font to Microsoft Yahei'):
                    f = 1
                    font_change(f)
            else:
                if anniu((screen_size[0] / 2 - 450, screen_size[1] / 2 + 100, 350, 40), 'switch font to Arial'):
                    f = 0
                    font_change(f)
            if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 150, 200, 40), 'return'):
                jm = 0
        if anniu((screen_size[0] / 2 + 100, screen_size[1] / 2 + 100, 200, 40), '简体中文'):
            language = 0
        if anniu((screen_size[0] / 2 + 100, screen_size[1] / 2 + 40, 200, 40), 'English'):
            language = 1
    write('fps:' + str(int(clock.get_fps())), (0, 0), (0, 0, 0))
    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type is QUIT:
            run = False
pygame.quit()
s = open(r'./setting.txt', 'w+', encoding='utf-8')
s.write(str(f) + '\n' + str(language))
s.close()
