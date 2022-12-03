import random
import game_framework
import server
from pico2d import *
import game_world

class hamburger:
    image = None
    eat_sound = None

    def __init__(self):
        print('햄버거 배치')
        if hamburger.image == None:
            hamburger.image = load_image('Hamburger.png')

        if hamburger.eat_sound is None:
            hamburger.eat_sound = load_wav('nyang.mp3')
            hamburger.eat_sound.set_volume(32)

        self.x, self.y, self.fall_speed = random.randint(400, 1100), random.randint(50, 600), 0

    def __getstate__(self):
        state = {'x': self.x, 'y': self.y}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)


    def get_bb(self):  # 박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom
        hamburger.image.clip_draw(0, 0, 100, 100, sx, sy)


    def update(self):
        pass


    def handle_collision(self, other, group):
        if group == 'hamburger:Skul': #햄버거 입장에서 해골이 부딪히면
            hamburger.eat_sound.play()
            game_world.remove_object(self)
        if group == 'hamburger:Skul2': #햄버거 입장에서 해골2이 부딪히면
            hamburger.eat_sound.play()
            game_world.remove_object(self)
        if group == 'hamburger:Skul3':
            hamburger.eat_sound.play()
            game_world.remove_object(self)
        if group == 'hamburger:Skul4':
            hamburger.eat_sound.play()
            game_world.remove_object(self)