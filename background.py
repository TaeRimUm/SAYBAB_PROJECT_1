
import server
from pico2d import *


class FixedBackground:

    def __init__(self):
        self.image = load_image('SAYBAB_background.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

        self.bgm = load_music('ground_music.mp3') #load_music는 mp3하고 ogg를 읽을 수 있음.
        self.bgm.set_volume(32) # 중요 : ground가 플레이 함. #
        self.bgm.repeat_play() #반복적으로 플레이

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom,
                                       self.canvas_width, self.canvas_height,
                                       0, 0)

    def update(self):
        self.window_left = clamp(0,
                                 int(server.saybar.x) - self.canvas_width // 2,
                                 self.w - self.canvas_width - 1)

        self.window_bottom = clamp(0,
                                   int(server.saybar.y) - self.canvas_height // 2,
                                   self.h - self.canvas_height - 1)
    def handle_event(self, event):
        pass
