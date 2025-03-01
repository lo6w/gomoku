class setting:
    language = '简体中文'
    play_music = False
    play_sound = True
    music_volume = 0.1
    sound_volume = 0.4
    nb = True
    name = ''
    style = 0

    def reset(self, language='简体中文', play_music=False, play_sound=True, music_volume=0.1, sound_volume=0.4, nb=True, name='', style=0):
        self.language = language
        self.play_music = play_music
        self.play_sound = play_sound
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        self.nb = nb
        self.name = name
        self.style = style
