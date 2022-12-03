import random
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







# class TileBackground:
#
#     def __init__(self):
#         # fill here
#         pass
#
#     def update(self):
#         pass
#
#     def draw(self):
#         # fill here
#         pass



# class InfiniteBackground:
#
#     def __init__(self):
#         self.image = load_image('futsal_court.png')
#         self.canvas_width = get_canvas_width()
#         self.canvas_height = get_canvas_height()
#         self.w = self.image.w
#         self.h = self.image.h
#
#
#
#     def draw(self):
#         self.image.clip_draw_to_origin(self.q3l, self.q3b, self.q3w, self.q3h, 0, 0)                        # quadrant 3
#         self.image.clip_draw_to_origin(self.q2l, self.q2b, self.q2w, self.q2h, 0, 0)                 # quadrant 2
#         self.image.clip_draw_to_origin(self.q4l, self.q4b, self.q4w, self.q4h, 0, 0)                 # quadrant 4
#         self.image.clip_draw_to_origin(self.q1l, self.q1b, self.q1w, self.q1h, 0, 0)          # quadrant 1
#
#     def update(self):
#
#         # quadrant 3
#         self.q3l = (int(server.saybar.x) - self.canvas_width // 2) % self.w
#         self.q3b = (int(server.saybar.y) - self.canvas_height // 2) % self.h
#         self.q3w = clamp(0, self.w - self.q3l, self.w)
#         self.q3h = clamp(0, self.h - self.q3b, self.h)
#
#         # quadrant 2
#         self.q2l = 0
#         self.q2b = 0
#         self.q2w = 0
#         self.q2h = 0
#
#         # quadrand 4
#         self.q4l = 0
#         self.q4b = 0
#         self.q4w = 0
#         self.q4h = 0
#
#         # quadrand 1
#         self.q1l = 0
#         self.q1b = 0
#         self.q1w = 0
#         self.q1h = 0






