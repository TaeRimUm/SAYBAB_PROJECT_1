import random
import game_framework
import server
from pico2d import *
import game_world

class hamburger:
    image = None
    def do(self):
        self.x = clamp(0, self.x, 1600)

    def __init__(self):
        print('햄버거 배치')
        if hamburger.image == None:
            hamburger.image = load_image('Hamburger.png')

        self.x, self.y, self.fall_speed = random.randint(400, 1100), random.randint(50, 140), 0


    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        hamburger.image.clip_draw(0, 0, 100, 100, sx, sy)

    def update(self):
        pass

    def get_bb(self):  # 박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
        return self.x - 20, self.y - 30, self.x + 20, self.y + 20

    def handle_collision(self, other, group):
        if group == 'hamburger:Skul': #햄버거 입장에서 해골이 부딪히면
            game_world.remove_object(self)