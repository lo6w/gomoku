import math
import os
import pickle
import socket
import threading
import webbrowser

import pygame.display
from server import server
from niuben import sounds, musics, Image
from ui import *

images = Image()


def xy(x, y, z=0, xt=0, yt=80, ts=1):
    return (int(((math.cos(math.radians(xt)) * x) - (math.sin(math.radians(xt)) * y)) * ts),
            int(((math.cos(math.radians(yt)) * (
                    (math.sin(math.radians(xt)) * x) + (math.cos(math.radians(xt)) * y))) + (
                         math.sin(math.radians(yt)) * z)) * ts))


class Game:

    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((1280, 720), RESIZABLE | HWACCEL | DOUBLEBUF)
        loads = threading.Thread(target=self.loading, daemon=True)
        loads.start()
        pygame.font.init()
        self.run = True
        self.clock = pygame.time.Clock()
        self.i = 0
        self.mouse_up = [False, False, False]
        self.mouse_down = [False, False, False]
        self.fonts = {}
        self.interface = 0
        self.anti_aliasing = True
        self.lan = 0
        self.settings = setting()
        self.tittle = ''
        self.name = ''
        self.name_input = input_rect((-200, 0, 400, 50), y_center=0.01)
        self.ip_input = input_rect((-200, -100, 400, 50))
        self.port_input = input_rect((-200, 100, 400, 50), input_number=True)
        self.description_input = input_rect((-200, -100, 400, 50))
        self.key_up = []
        self.key_press = []
        self.input_text = []
        self.servers_list = []
        self.servers = server(sounds)
        self.send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.totems_undying = []
        self.totems_restart = []
        self.languages = {}
        self.choice = 0
        self.difficulty=False
        self.error_text = ''
        tittles = ['NB-gomoku 2.0 特供版!', '牛犇AI 1.0!', '&&&&&&&&', '牛犇AI2.0是个谎言!', '你被骗了', '牛犇就是NB', '&点我没有惊喜&']
        self.line = 0
        try:
            settings = open('setting.ini', 'rb+')
            self.settings = pickle.load(settings)
        except FileNotFoundError:
            settings = open('setting.ini', 'wb+')
            self.settings.reset()
            # noinspection PyTypeChecker
            pickle.dump(self.settings, settings)
        try:
            servers_list = open('servers.ini', 'rb+')
            self.servers_list = pickle.load(servers_list)
        except FileNotFoundError:
            servers_list = open('servers.ini', 'wb+')
            self.servers_list = []
            # noinspection PyTypeChecker
            pickle.dump(self.servers_list, servers_list)
        self.settings: setting
        self.servers_list: list
        settings.close()
        self.language_names = []
        for lt in os.listdir(r'languages/'):
            if os.path.isfile(r'languages/' + str(lt)):
                if os.path.splitext(lt)[1] == '.txt':
                    name = os.path.splitext(lt)[0]
                    self.languages[name] = {}
                    self.language_names.append(name)
                    try:
                        ls = open(r'languages/' + str(lt), 'r+', encoding='utf-8').read().split('\n')
                        for li in ls:
                            if len(li.split('=')) == 2:
                                n, t = li.split('=')
                                self.languages[name][n] = str(t)
                    except FileNotFoundError:
                        print(str(lt) + '不是有效文件')

        musics.volume = self.settings.music_volume
        musics.play = self.settings.play_music
        sounds.volume = self.settings.sound_volume
        sounds.playing = self.settings.play_sound
        self.name = self.settings.name
        self.name_input.text = self.settings.name
        self.lan = self.settings.language
        self.tittle = tittles[random.randint(0, len(tittles) - 1)]
        if self.settings.nb:
            pygame.display.set_icon(pygame.image.load(r'nb.png'))
        else:
            pygame.display.set_icon(pygame.image.load(r'gomoku.png'))
        pygame.display.set_caption('NB gomoku')
        while self.run:
            self.input_text = []
            self.event = []
            for event in pygame.event.get():
                self.event.append(event)
                if event.type == QUIT:
                    self.run = False
                if event.type == KEYUP:
                    if event.key == K_m:
                        musics.get_lost()
                    self.key_up.append(event.key)
                if event.type == TEXTINPUT:
                    self.input_text.append(event.text)
            self.key_press = pygame.key.get_pressed()
            self.screen.fill((255, 255, 255))
            if self.interface == 0:
                self.write('loading...', (self.screen.get_width() // 2, self.screen.get_height() // 2), center=True)
                j = (len(images.totems_undying) + len(images.totems_restart)) / 360
                if j == 1:
                    self.interface = 1
                    self.single = Single_play(self.settings, self.languages, images)
                    self.better = Better_play(self.settings, self.languages, images)
                    self.best = Best_play(self.settings, self.languages, images)
                    self.tortoise = Tortoise_play(self.settings, self.languages, images)
                    self.tortoise_watch = Tortoise_watch(self.settings, self.languages, images)
                    self.multi_play = Multi_play(self.settings, self.languages, images)

                self.write(str(round(j * 100, 2)) + '%',
                           (self.screen.get_width() // 2, self.screen.get_height() // 2 + 20), center=True)
            elif self.interface == 1:
                self.menu()
            elif self.interface == 2:
                self.choice_menu()
            elif self.interface == 3:
                self.single.draw(self.mouse_up, sounds, self.lan)
                if self.single.exit:
                    self.interface = 2
                    self.single.init()
            elif self.interface == 4:
                self.better.draw(self.mouse_up, sounds, self.lan)
                if self.better.exit:
                    self.interface = 2
                    self.better.init()
            elif self.interface == 5:
                self.best.draw(self.mouse_up, sounds, self.lan)
                if self.best.exit:
                    self.interface = 2
                    self.best.init()
            elif self.interface == 6:
                self.tortoise.draw(self.mouse_up, sounds, self.lan)
                if self.tortoise.exit:
                    self.interface = 2
                    self.tortoise.init()
            elif self.interface == 7:
                self.tortoise_watch.draw(self.mouse_up, sounds, self.lan)
                if self.tortoise_watch.exit:
                    self.interface = 2
                    self.tortoise_watch.init()
            elif self.interface == 8:
                self.setting()
            elif self.interface == 9:
                self.about()
            elif self.interface == 10:
                self.server_list()
            elif self.interface == 11:
                self.create_connection()
            elif self.interface == 12:
                self.set_language()
            elif self.interface == 13:
                self.create_room()
            elif self.interface == 14:
                self.error()
            elif self.interface == 15:
                self.multi_play.go = self.servers.go
                self.servers.main = self.multi_play.main
                self.multi_play.player1_steps = self.servers.steps1
                self.multi_play.player2_steps = self.servers.steps2
                self.multi_play.player1_name = self.servers.player1
                self.multi_play.player2_name = self.servers.player2
                self.multi_play.board = self.servers.board
                self.multi_play.first = self.servers.first
                self.multi_play.draw(self.mouse_up, sounds, self.lan)
                self.multi_play.winner = self.servers.winner
                self.multi_play.win_line = self.servers.win_line
                self.multi_play.history = self.servers.history
                if self.multi_play.main != -1:
                    if self.multi_play.main:
                        if self.servers.go == 2:
                            self.multi_play.wait = 2
                        else:
                            self.multi_play.wait = 0
                    else:
                        if self.servers.go == 1:
                            self.multi_play.wait = 1
                        else:
                            self.multi_play.wait = 0
                if self.multi_play.did:
                    self.multi_play.did = False
                    self.servers.down = self.multi_play.player1_previous_step
                    self.servers.sends(self.multi_play.player1_previous_step[0], self.multi_play.player1_previous_step[1], self.multi_play)
                if self.multi_play.exit:
                    self.interface = 10
                    self.multi_play.init()
                    if not self.multi_play.main:
                        self.servers.send_exit_message()
                if self.multi_play.say != 0:
                    if self.servers.player2_address != ():
                        self.servers.send.sendto(pickle.dumps({'type': 'say', 'say': self.multi_play.say}), self.servers.player2_address)
                    self.multi_play.say = 0
                if self.multi_play.main and self.multi_play.wait == -1:
                    if self.servers.go != 0:
                        self.multi_play.wait = 0
                if self.multi_play.restart:
                    if self.multi_play.main:
                        self.servers.board_init()
                        self.servers.go = random.randint(1, 2)
                        if self.servers.player2_address != ():
                            self.servers.send.sendto(pickle.dumps({'type': 'rs_y', 'go': self.servers.go}), self.servers.player2_address)
                    else:
                        self.servers.send_restart_message()
                if self.servers.restart:
                    self.servers.restart = False
                    self.multi_play.init()
                    self.multi_play.first = self.servers.first
                    self.multi_play.board = self.servers.board
                    self.multi_play.go = self.servers.go
            if musics.play and self.interface in (1, 2, 8):
                self.write(musics.get_name(), (0, self.screen.get_height() - 32), size=32)
            pygame.display.flip()
            if self.interface != -1:
                musics.update()
            sounds.update()
            self.clock.tick(60)
            for k in range(3):
                if self.mouse_down[k] and not pygame.mouse.get_pressed()[k]:
                    self.mouse_up[k] = True
                else:
                    self.mouse_up[k] = False
            self.mouse_down = pygame.mouse.get_pressed()
        pygame.quit()
        self.settings.reset(language=self.lan, play_music=musics.play, play_sound=sounds.playing,
                            music_volume=musics.volume,
                            sound_volume=sounds.volume, nb=self.settings.nb, name=self.name,style=self.settings.style)
        settings = open("setting.ini", "wb")
        # noinspection PyTypeChecker
        pickle.dump(self.settings, settings)
        settings.close()
        servers = open("servers.ini", "wb")
        # noinspection PyTypeChecker
        pickle.dump(self.servers_list, servers)
        servers.close()

    def menu(self):
        """主菜单"""
        self.screen.fill((0, 127, 255))
        self.write('GOMOKU', (self.screen.get_width() / 2 - 96, self.screen.get_height() / 8), size=64)
        if not (32 in self.fonts):
            self.fonts[32] = pygame.font.Font('unifont-15.0.01.ttf', 32)
        m = self.tittle
        if '&' in m:
            for i in range(len(m)):
                if m[i] == '&':
                    m = m[:i] + chr(random.randint(256, 1024)) + m[i + 1:]
        font = self.fonts[32].render(m, self.anti_aliasing, (255, 255, 0))
        font = pygame.transform.rotate(font, 20)
        font = pygame.transform.smoothscale(font, (int((math.sin(time.time() * 8) * 0.1 + 1) * font.get_width()),
                                                   int((math.sin(time.time() * 8) * 0.1 + 1) * font.get_height())))
        self.screen.blit(font, (self.screen.get_width() / 2 + 96 - font.get_width() / 2,
                                self.screen.get_height() / 8 + 64 - font.get_height() / 2))
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 150, 400, 38),
                       self.text('single')):
            self.interface = 2
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 100, 400, 38),
                       self.text('multi')):
            self.servers = server(sounds)
            self.interface = 10
            self.refresh_server_list()
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 50, 400, 38),
                       self.text('about')):
            self.interface = 9
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2, 400, 38),
                       self.text('setting')):
            self.interface = 8
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 + 50, 400, 38),
                       self.text('exit')):
            self.run = False
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 + 100, 400, 38),
                       '语言 language'):
            self.interface = 12

    def choice_menu(self):
        """其它模式界面"""
        self.screen.fill((0, 127, 255))
        self.write(self.text('description'), (self.screen.get_width() / 2 + 200, self.screen.get_height() / 2 - 200), size=32,
                   center=True)
        if self.choice == 0:
            t = self.text('single_d')
        elif self.choice == 1:
            t = self.text('better_d')
        elif self.choice == 2:
            t = self.text('best_d')
        elif self.choice == 3:
            t = self.text('tortoise_d')
        else:
            t = self.text('watch_tortoise_d')
        self.write(t, (self.screen.get_width() / 2 + 200, self.screen.get_height() / 2 - 100), size=32, center=True)
        self.write(self.text('difficulty'),(self.screen.get_width() // 2-50, self.screen.get_height() // 2),size=32)
        self.difficulty =self.switch(self.text('hard'), 32, (self.screen.get_width() // 2 + 30, self.screen.get_height() // 2), self.difficulty)
        self.difficulty = not self.switch(self.text('easy'), 32, (self.screen.get_width() // 2 + 150, self.screen.get_height() // 2), not self.difficulty)
        if self.button((self.screen.get_width() / 2 - 200, self.screen.get_height() - 38, 400, 38),
                       self.text('exit')):
            self.interface = 1
        if self.button((self.screen.get_width() / 2 - 450, self.screen.get_height() / 2 - 145, 300, 50),
                       self.text('single'), texture=True, choice=self.choice == 0):
            self.choice = 0
        if self.button((self.screen.get_width() / 2 - 450, self.screen.get_height() / 2 - 85, 300, 50),
                       self.text('better'), texture=True, choice=self.choice == 1):
            self.choice = 1
        if self.button((self.screen.get_width() / 2 - 450, self.screen.get_height() / 2 - 25, 300, 50),
                       self.text('best'), texture=True, choice=self.choice == 2):
            self.choice = 2
        if self.button((self.screen.get_width() / 2 - 450, self.screen.get_height() / 2 + 35, 300, 50),
                       self.text('tortoise'), texture=True, choice=self.choice == 3):
            self.choice = 3
        if self.button((self.screen.get_width() / 2 - 450, self.screen.get_height() / 2 + 95, 300, 50),
                       self.text('watch_tortoise'), texture=True, choice=self.choice == 4):
            self.choice = 4
        if self.button((self.screen.get_width() / 2 + 150, self.screen.get_height() / 2 + 100, 300, 50),
                       self.text('start')):
            if self.difficulty:
                d = 1
            else:
                d = 0
            if self.choice == 0:
                self.single.init(difficulty=d)
                self.interface = 3
            elif self.choice == 1:
                self.better.init(difficulty=d)
                self.interface = 4
            elif self.choice == 2:
                self.best.init(difficulty=d)
                self.interface = 5
            elif self.choice == 3:
                self.tortoise.init(difficulty=d)
                self.interface = 6
            else:
                self.tortoise_watch.init(difficulty=d)
                self.interface = 7

    def setting(self):
        """设置页面"""
        self.screen.fill((0, 127, 255))
        self.settings: setting
        if self.button((0, 0, 120, 38), self.text('exit')):
            self.interface = 1
        musics.play = self.switch(self.text('musics'), 32,
                                  (self.screen.get_width() // 2 - 200, self.screen.get_height() // 2 - 200),
                                  musics.play)
        sounds.playing = self.switch(self.text('sounds'), 32,
                                     (self.screen.get_width() // 2 + 200, self.screen.get_height() // 2 - 200),
                                     sounds.playing)
        if self.settings.style == 0:
            if self.button((self.screen.get_width() // 2 - 300, self.screen.get_height() // 2, 600, 40),
                           self.text('style') + ':' + self.text('x')):
                self.settings.style = 1
        else:
            if self.button((self.screen.get_width() // 2 - 300, self.screen.get_height() // 2, 600, 40),
                           self.text('style') + ':' + self.text('o')):
                self.settings.style = 0
        musics.volume = self.slider(self.text('musics_volume'), 32,
                                    (self.screen.get_width() // 2 - 400, self.screen.get_height() // 2 - 150, 400, 40),
                                    musics.volume)
        sounds.volume = self.slider(self.text('sounds_volume'), 32,
                                    (self.screen.get_width() // 2 + 100, self.screen.get_height() // 2 - 150, 400, 40),
                                    sounds.volume)
        self.settings.nb = self.switch(self.text('nb'), 32,
                                       (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 100),
                                       self.settings.nb)

    def set_language(self):
        """语言页面"""
        self.screen.fill((0, 127, 255))
        if self.button((self.screen.get_width() // 2 - 160, self.screen.get_height() - 40, 150, 38), self.text('exit')):
            self.interface = 1
        if self.button((self.screen.get_width() // 2 + 10, self.screen.get_height() - 40, 150, 38), self.text('rf')):
            self.language_names = []
            for lt in os.listdir(r'languages/'):
                if os.path.isfile(r'languages/' + str(lt)):
                    if os.path.splitext(lt)[1] == '.txt':
                        name = os.path.splitext(lt)[0]
                        self.languages[name] = {}
                        self.language_names.append(name)
                        try:
                            ls = open(r'languages/' + str(lt), 'r+', encoding='utf-8').read().split('\n')
                            for li in ls:
                                if len(li.split('=')) == 2:
                                    n, t = li.split('=')
                                    self.languages[name][n] = str(t)
                        except FileNotFoundError:
                            print(str(lt) + '不是有效文件')
        for i in range((self.screen.get_height() - 150) // 40):
            ls = i + self.line
            if ls <= len(self.language_names) - 1:
                if self.button((self.screen.get_width() // 2 - 250, 20 + i * 45, 500, 40), self.language_names[ls]):
                    self.lan = str(self.language_names[ls])
        if (self.screen.get_height() - 150) // 40 + self.line > len(self.language_names):
            self.line = len(self.language_names) - (self.screen.get_height() - 150) // 40
        if (self.screen.get_height() - 150) // 40 < len(self.language_names):
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (self.screen.get_width() // 2 + 300, 20, 10, (self.screen.get_height() - 150) // 40 * 45))
            r = (self.screen.get_height() - 150) // 40 * 45 * ((self.screen.get_height() - 150) // 40 / len(self.language_names))
            pygame.draw.rect(self.screen, (200, 200, 200), (
                self.screen.get_width() // 2 + 300, 20 + self.line / (len(self.language_names) - (self.screen.get_height() - 150) // 40) * (
                        (self.screen.get_height() - 150) // 40 * 45 - r), 10, r))
            if self.button((self.screen.get_width() // 2 + 300, self.screen.get_height() // 2 - 50, 40, 40), '↑'):
                if self.line - 1 >= 0:
                    self.line = self.line - 1
                else:
                    self.line = 0
            if self.button((self.screen.get_width() // 2 + 300, self.screen.get_height() // 2 + 10, 40, 40), '↓'):
                if (self.screen.get_height() - 150) // 40 + self.line - 1 <= len(self.language_names):
                    self.line = self.line + 1
                else:
                    if (self.screen.get_height() - 150) // 40 < len(self.language_names):
                        self.line = len(self.language_names) - (self.screen.get_height() - 150) // 40
        else:
            self.line = 0
        for e in self.event:
            if e.type == MOUSEWHEEL:
                if e.y < 0:
                    if (self.screen.get_height() - 150) // 40 + self.line - e.y <= len(self.language_names):
                        self.line = self.line - e.y
                    else:
                        if (self.screen.get_height() - 150) // 40 < len(self.language_names):
                            self.line = len(self.language_names) - (self.screen.get_height() - 150) // 40
                elif e.y > 0:
                    if self.line - e.y >= 0:
                        self.line = self.line - e.y
                    else:
                        self.line = 0
        self.write(self.text('translate'), (self.screen.get_width() // 2, self.screen.get_height() - 56), size=32, center=True)

    def text(self, name: str) -> str:
        if self.lan in self.languages:
            if name in self.languages[self.lan]:
                return self.languages[self.lan][name]
            else:
                return ''
        else:
            return ''

    def write(self, text, pos: Tuple[Union[int, float], Union[int, float]], color=(0, 0, 0), size=16, center=False) -> None:
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text), self.anti_aliasing, color)
        font: pygame.Surface
        if center:
            self.screen.blit(font, (pos[0] - font.get_width() // 2, pos[1] - font.get_height() // 2))
        else:
            self.screen.blit(font, pos)

    def button(self, rect: Tuple[Union[int, float], Union[int, float], Union[int, float], Union[int, float]], text='', size=32,
               texture=False, choice=False) -> bool:
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        size = size
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text), self.anti_aliasing, (0, 0, 0))
        pos = (rect[0] + rect[2] / 2 - font.get_width() / 2, rect[1] + rect[3] / 2 - font.get_height() / 2)
        if Rect(rect[0], rect[1], rect[2], rect[3]).collidepoint(pygame.mouse.get_pos()):
            if not texture:
                pygame.draw.rect(self.screen, (127, 127, 127), rect, 3)
                self.screen.blit(font, pos)
            if self.mouse_up[0]:
                if texture:
                    if choice:
                        self.screen.blit(images.button4, (rect[0], rect[1]))
                        self.screen.blit(font, pos)
                    else:
                        self.screen.blit(images.button3, (rect[0], rect[1]))
                        self.screen.blit(font, pos)
                return True
            else:
                if texture:
                    if choice:
                        self.screen.blit(images.button4, (rect[0], rect[1]))
                        self.screen.blit(font, pos)
                    else:
                        self.screen.blit(images.button1, (rect[0], rect[1]))
                        self.screen.blit(font, pos)
                return False
        else:
            if not texture:
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
                self.screen.blit(font, pos)
            else:
                if choice:
                    self.screen.blit(images.button4, (rect[0], rect[1]))
                    self.screen.blit(font, pos)
                else:
                    self.screen.blit(images.button1, (rect[0], rect[1]))
                    self.screen.blit(font, pos)
            return False

    def loading(self) -> None:
        global images
        images = Image()
        self.i = 0
        for i in range(180):
            images.totems_undying.append(pygame.image.load(r'image/totem/undying' + str(i) + '.png').convert_alpha())

        for i in range(180):
            images.totems_restart.append(pygame.image.load(r'image/totem/restart' + str(i) + '.png').convert_alpha())

    def totem(self, times: int, types: Literal[0, 1]) -> pygame.Surface:
        """图腾特效"""
        self.i = 0
        b = pygame.Surface((80, 80 + 20)).convert_alpha()
        b.fill((0, 0, 0, 0))
        if types == 0:
            h = pygame.surfarray.pixels3d(images.undying_totem)
        else:
            h = pygame.surfarray.pixels3d(images.restart_totem)
        xt = int(times)
        for x in range(80):
            for y in range(80):
                pos = xy(x - 40, 0, y - 40, int(10 * xt * (xt - 180) / 90))
                s = 2
                color = (int(h[x * s, y * s, 0]), int(h[x * s, y * s, 1]), int(h[x * s, y * s, 2]))
                if color != (0, 0, 0):
                    pygame.draw.rect(b, color, (pos[0] + 40, pos[1] + 40, 1, 1))
        size = int(-3 / 81 * times * (times - 180) + 40) // 2
        b = pygame.transform.scale(pygame.transform.rotate(b, 5), (size, size))
        return b

    def switch(self, text, size:int, pos:tuple, opening:bool) -> bool:
        """开关"""
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text), self.anti_aliasing, (0, 0, 0))
        self.screen.blit(font, pos)
        pygame.draw.circle(self.screen, (255, 255, 255), (pos[0] + font.get_width() + size // 2, pos[1] + size // 2),
                           size / 2)
        if opening:
            pygame.draw.circle(self.screen, (0, 0, 0), (pos[0] + font.get_width() + size // 2, pos[1] + size // 2),
                               size / 2 * 0.8)
        r = Rect(pos[0] + font.get_width(), pos[1], size, size)
        if r.collidepoint(pygame.mouse.get_pos()) and self.mouse_up[0]:
            if opening:
                return False
            else:
                return True
        else:
            return opening

    def slider(self, text, size, rect, value) -> float:
        """滑块"""
        if value > 1 or value < 0:
            value = 0
        rect = pygame.Rect(rect)
        pygame.draw.rect(self.screen, (127, 127, 127), rect)
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, (255, 255, 255), (rect[0] + value * (rect[2] - 4), rect[1], 4, rect[3]))
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), (rect[0] + value * (rect[2] - 4), rect[1], 4, rect[3]))
        if not (size in self.fonts):
            self.fonts[size] = pygame.font.Font('unifont-15.0.01.ttf', size)
        font = self.fonts[size].render(str(text) + ' ' + str(int(value * 100)) + '%', self.anti_aliasing, (0, 0, 0))
        self.screen.blit(font, (
            rect[0] + rect[2] // 2 - font.get_width() // 2, rect[1] + rect[3] // 2 - font.get_height() // 2))
        if rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_down[0]:
            value = round((pygame.mouse.get_pos()[0] - rect[0]) / rect[2], 2)
            return value
        else:
            return value

    def refresh_server_list(self):
        """刷新服务器列表"""
        for ls in range(len(self.servers_list)):
            for i in range(3):
                r = self.servers.get_information((self.servers_list[ls][2], int(self.servers_list[ls][3])))
                if r == {}:
                    self.servers_list[ls] = [self.text('server'), '', self.servers_list[ls][2], self.servers_list[ls][3], 0]
                    break
                else:
                    if r['type'] == 'test':
                        continue
                    elif r['type'] == 'info':
                        self.servers_list[ls] = [self.text('server'), str(r['description']), self.servers_list[ls][2],
                                                 self.servers_list[ls][3], 1]
                        break
                    elif r['type'] == 'full':
                        self.servers_list[ls] = [self.text('server'), str(r['description']), self.servers_list[ls][2],
                                                 self.servers_list[ls][3], 2]
                        break
                    else:
                        self.servers_list[ls] = [self.text('server'), '', self.servers_list[ls][2], self.servers_list[ls][3], 0]
                        break

    def server_list(self) -> None:
        """服务器列表"""
        self.screen.fill((0, 127, 255))
        if self.button((self.screen.get_width() // 2 - 300, self.screen.get_height() - 80, 300, 40), self.text('exit')):
            self.interface = 1
        self.write(self.text('s_l'), (self.screen.get_width() // 2, 96), size=32, center=True)
        self.write(self.text('p_n'),
                   (self.screen.get_width() // 2 - 400, self.screen.get_height() * 0.01 + 9), size=32)
        self.name = self.name_input.get_text()
        self.name_input.input_draw(self.key_up, self.key_press, self.mouse_up, pygame.mouse.get_pos(), self.input_text)
        if self.button((self.screen.get_width() // 2, self.screen.get_height() - 40, 300, 40),
                       self.text('rf')):
            self.refresh_server_list()
        if self.button((self.screen.get_width() // 2, self.screen.get_height() - 80, 300, 40),
                       self.text('new_room')):
            self.interface = 13
            self.port_input.text = '6532'
            self.description_input.text = '这是一个棋局'
        if self.button((self.screen.get_width() // 2 - 300, self.screen.get_height() - 40, 300, 40),
                       self.text('c_c')):
            self.interface = 11
            self.port_input.text = '6532'
            self.ip_input.text = '192.168.0.100'
        t = 0
        for sl in self.servers_list:
            ps = (self.screen.get_width() // 2 - 200, self.screen.get_height() * 0.3 + t * 50)
            if self.button((ps[0], ps[1], 400, 40)):
                for i in range(3):
                    r = self.servers.get_information((sl[2], int(sl[3])))
                    if r == {}:
                        self.error_text = self.text('not_connected') + '0:' + str(r)
                        self.interface = 14
                    elif r['type'] == 'info':
                        if self.servers.join((sl[2], int(sl[3])), self.name_input.get_text()):
                            self.servers.player2_address = (sl[2], int(sl[3]))
                            self.servers.board_init()
                            self.multi_play.player1_name = self.servers.player1
                            self.multi_play.player2_name = self.servers.player2
                            self.multi_play.first = self.servers.first
                            self.multi_play.board = self.servers.board
                            self.multi_play.go = self.servers.go
                            self.multi_play.ip = sl[2]
                            self.multi_play.port = int(sl[3])
                            self.interface = 15
                            break
                        else:
                            self.error_text = self.text('not_connected') + '3:' + str(r['type'])
                            self.interface = 14
                    elif r['type'] == 'full':
                        self.error_text = self.text('not_connected') + '2:' + str(r)
                        self.interface = 14
                    elif r['type'] == 'test':
                        continue
                    else:
                        self.error_text = self.text('not_connected') + '1:' + str(r)
                        self.interface = 14

            self.write(sl[0], (ps[0] + 10, ps[1] + 5))
            self.write(sl[1], (ps[0] + 100, ps[1] + 5))
            if self.button((ps[0] + 420, ps[1], 80, 40), self.text('delete')):
                self.servers_list.pop(t)
                t = t - 1
            if sl[4] == 1:
                self.write(self.text('connected'), (ps[0] + 350, ps[1] + 5))
            elif sl[4] == 2:
                self.write(self.text('full'), (ps[0] + 350, ps[1] + 5))
            else:
                self.write(self.text('not_connected'), (ps[0] + 350, ps[1] + 5))
            t = t + 1

    def create_room(self) -> None:
        """创建房间"""
        self.screen.fill((0, 127, 255))
        if self.button((0, 0, 200, 38), self.text('exit')):
            self.interface = 10
        self.write(self.text('description'), (self.screen.get_width() // 2, self.screen.get_height() // 2 - 150),
                   size=32,
                   center=True)
        self.write(self.text('port'), (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50),
                   size=32, center=True)
        self.description_input.input_draw(self.key_up, self.key_press, self.mouse_up, pygame.mouse.get_pos(), self.input_text)
        self.port_input.input_draw(self.key_up, self.key_press, self.mouse_up, pygame.mouse.get_pos(), self.input_text)
        if self.button((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 300, 200, 38),
                       self.text('ct')):
            if len(self.name_input.get_text()) > 0 and self.port_input.get_text() != '':
                self.servers = server(sounds)
                try:
                    self.servers.player1 = self.name_input.get_text()
                    self.servers.describe = self.description_input.get_text()
                    self.servers.start_server(self.port_input.get_text())
                    self.multi_play.main = True
                    self.multi_play.wait = -1
                    self.servers.board_init()
                    self.multi_play.board = self.servers.board
                    self.multi_play.ip = self.servers.ip
                    self.multi_play.port = self.servers.port
                    self.interface = 15
                except OSError as ose:
                    self.error_text = self.text('invalid_port') + ':' + str(ose)
                    self.interface = 14
            else:
                if self.name_input.get_text() == '':
                    self.error_text = self.text('invalid_name')
                else:
                    self.error_text = self.text('invalid_port')
                self.interface = 14

    def error(self) -> None:
        self.screen.fill((0, 127, 255))
        self.write(self.error_text, (self.screen.get_width() // 2, self.screen.get_height() // 2), size=32, center=True)
        if self.button((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 100, 200, 40), self.text('exit')):
            self.interface = 10

    def create_connection(self) -> None:
        """创建连接"""
        self.screen.fill((0, 127, 255))
        if self.button((0, 0, 200, 38), self.text('exit')):
            self.interface = 10
        self.write(self.text('ip'), (self.screen.get_width() // 2, self.screen.get_height() // 2 - 150),
                   size=32,
                   center=True)
        self.write(self.text('port'), (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50),
                   size=32, center=True)
        self.ip_input.input_draw(self.key_up, self.key_press, self.mouse_up, pygame.mouse.get_pos(), self.input_text)
        self.port_input.input_draw(self.key_up, self.key_press, self.mouse_up, pygame.mouse.get_pos(), self.input_text)
        if self.button((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 300, 200, 38),
                       self.text('ct')):
            r = self.servers.get_information((self.ip_input.get_text(), self.port_input.get_text()))
            if r == {}:
                self.servers_list.append([self.text('server'), '', self.ip_input.get_text(), self.port_input.get_text(), 0])
            else:
                if r['type'] == 'info':
                    self.servers_list.append(
                        [self.text('server'), str(r['description']), self.ip_input.get_text(), self.port_input.get_text(), 1])
                else:
                    self.servers_list.append(
                        [self.text('server'), str(r['description']), self.ip_input.get_text(), self.port_input.get_text(), 0])
            self.interface = 10

    def about(self):
        """关于"""
        self.screen.fill((0, 127, 255))
        if self.button((0, 0, 200, 38), self.text('exit')):
            self.interface = 1
        if self.button((0, self.screen.get_height() - 38, 200, 38), self.text('link')):
            webbrowser.open('https://space.bilibili.com/1779252995')
        self.write(self.text('copyleft'), (self.screen.get_width() // 2, self.screen.get_height() // 2),
                   size=int(math.sin(time.time() * 2) * 20 + 40), center=True)
        self.write(self.text('thank1'), (self.screen.get_width() // 2, 128), size=32, center=True)
        self.write(self.text('thank2'), (self.screen.get_width() // 2, 160), size=32, center=True)


if __name__ == '__main__':
    g = Game()
