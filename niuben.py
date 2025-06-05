import os
import random
import pygame

pygame.mixer.init()


class Image:
    def __init__(self) -> None:
        if pygame.display.get_active():
            self.totems_undying = []
            self.totems_restart = []
            self.normal = pygame.transform.scale(pygame.image.load(r'image/normal.png'), (128, 128)).convert_alpha()
            self.happy = pygame.transform.scale(pygame.image.load(r'image/happy.png'), (128, 128)).convert_alpha()
            self.angry = pygame.transform.scale(pygame.image.load(r'image/angry.png'), (128, 128)).convert_alpha()
            self.undying_totem = pygame.image.load(r'image/totem of undying.png').convert_alpha()
            self.undying_totem_ = pygame.image.load(r'image/totem_of_undying.png').convert_alpha()
            self.restart_totem = pygame.image.load(r'image/totem of restart.png').convert_alpha()
            self.restart_totem_ = pygame.image.load(r'image/totem_of_restart.png').convert_alpha()
            self.button1 = pygame.image.load(r'image/button1.png').convert_alpha()
            self.button2 = pygame.image.load(r'image/button2.png').convert_alpha()
            self.button3 = pygame.image.load(r'image/button3.png').convert_alpha()
            self.button4 = pygame.image.load(r'image/button4.png').convert_alpha()
        else:
            self.totems_undying = []
            self.totems_restart = []
            self.normal = pygame.transform.scale(pygame.image.load(r'image/normal.png'), (128, 128))
            self.happy = pygame.transform.scale(pygame.image.load(r'image/happy.png'), (128, 128))
            self.angry = pygame.transform.scale(pygame.image.load(r'image/angry.png'), (128, 128))
            self.undying_totem = pygame.image.load(r'image/totem of undying.png')
            self.undying_totem_ = pygame.image.load(r'image/totem_of_undying.png')
            self.restart_totem = pygame.image.load(r'image/totem of restart.png')
            self.restart_totem_ = pygame.image.load(r'image/totem_of_restart.png')
            self.button1 = pygame.image.load(r'image/button1.png')
            self.button2 = pygame.image.load(r'image/button2.png')
            self.button3 = pygame.image.load(r'image/button3.png')
            self.button4 = pygame.image.load(r'image/button4.png')

    def reset(self) -> None:
        self.normal = pygame.transform.scale(pygame.image.load(r'image/normal.png'), (128, 128)).convert_alpha()
        self.happy = pygame.transform.scale(pygame.image.load(r'image/happy.png'), (128, 128)).convert_alpha()
        self.angry = pygame.transform.scale(pygame.image.load(r'image/angry.png'), (128, 128)).convert_alpha()
        self.undying_totem = pygame.image.load(r'image/totem of undying.png').convert_alpha()
        self.undying_totem_ = pygame.image.load(r'image/totem_of_undying.png').convert_alpha()
        self.restart_totem = pygame.image.load(r'image/totem of restart.png').convert_alpha()
        self.restart_totem_ = pygame.image.load(r'image/totem_of_restart.png').convert_alpha()
        self.button1 = pygame.image.load(r'image/button1.png').convert_alpha()
        self.button2 = pygame.image.load(r'image/button2.png').convert_alpha()
        self.button3 = pygame.image.load(r'image/button3.png').convert_alpha()
        self.button4 = pygame.image.load(r'image/button4.png').convert_alpha()


class Sounds:

    def __init__(self, file):
        self.sound = pygame.mixer.Sound(file)

    def play(self, sound_play=True):
        self.sound.stop()
        if sound_play:
            self.sound.play(maxtime=int(self.sound.get_length() * 1000))

    def set_volume(self, volume=0.5):
        self.sound.set_volume(volume)


class Sound:
    sounds = {'ngm1': Sounds(r'sound/ngm1.mp3'), 'ngm2': Sounds(r'sound/ngm2.mp3'), 'lblh1': Sounds(r'sound/lblh1.mp3'),
              'lblh2': Sounds(r'sound/lblh2.mp3'), 'xun1': Sounds(r'sound/xun1.mp3'), 'xun2': Sounds(r'sound/xun2.mp3'),
              'undying': Sounds(r'sound/totem of undying.mp3')}
    volume = 0.5
    playing = True

    def __init__(self, volume=0.5):
        self.volume = volume

    def play(self, name: str):
        if self.playing:
            self.sounds[name].set_volume(self.volume)
            self.sounds[name].play()

    def update(self):
        if self.playing:
            for i in self.sounds:
                self.sounds[i].set_volume(self.volume)


class Music:
    play = False
    musics = os.listdir(r'music')
    music_name = []
    for i in musics:
        if os.path.splitext(i)[1] in ('.mp3', '.ogg'):
            music_name.append(os.path.splitext(i)[0])
    if 'Moog City 2' in music_name:
        music_name.remove('Moog City 2')
    music_name.append('Moog City 2')
    if 'Moog City 2.mp3' in musics:
        musics.remove('Moog City 2.mp3')
    for i in range(len(musics)):
        musics[i] = r'music/' + musics[i]

    def __init__(self, volume=0.3) -> None:
        self.volume = volume
        self.playing = -2

    def update(self) -> None:
        if self.play:
            pygame.mixer.music.set_volume(self.volume)
            if not pygame.mixer.music.get_busy():
                self.playing = random.randint(0, len(self.musics) - 1)
                try:
                    pygame.mixer.music.load(self.musics[self.playing])
                    pygame.mixer.music.play()
                except pygame.error:
                    print('缺失文件:' + str(self.musics[self.playing]))
        else:
            pygame.mixer.music.stop()

    def get_lost(self) -> None:
        if self.play:
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.stop()
            self.playing = -1
            try:
                pygame.mixer.music.load(r'music/Moog City 2.mp3')
                pygame.mixer.music.play()
            except pygame.error:
                print('缺失文件:' + 'music/Moog City 2.mp3')
                self.playing = -2

    def get_name(self) -> str:
        if self.play != -2:
            return str(self.music_name[self.playing])
        else:
            return ''


class Particle:
    x = 0
    y = 0
    x_offset = 0
    y_offset = 0
    color = (0, 0, 0)

    def __init__(self, x_offset, y_offset, color):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.color = color

    def update(self, dt: int):
        self.x = int(self.x + self.x_offset * dt)
        self.y = int(self.y + self.y_offset * dt)
        self.y_offset = self.y_offset + 0.3 * dt


class Nbs:
    undying_totem = 0
    restart_totem = 0
    angry_time = 0
    happy_time = 0

    def clear(self):
        self.undying_totem = 0
        self.restart_totem = 0

    def init(self, u=5, r=2):
        self.undying_totem = u
        self.restart_totem = r


sounds = Sound()
musics = Music()
